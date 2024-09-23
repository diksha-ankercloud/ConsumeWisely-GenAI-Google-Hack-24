import os
from dotenv import load_dotenv
import base64
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from vertexai.preview.generative_models import grounding as preview_grounding
import vertexai
from vertexai.generative_models import (
    GenerationResponse,
    GenerativeModel,
    Tool,
    grounding,
)
from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)


# Load environment variables
load_dotenv()

# Initialize Vertex AI
PROJECT_ID = "vision-forge-414908"
REGION = "us-central1"
vertexai.init(project=PROJECT_ID, location=REGION)

# Existing products data
products = [
    # ... (keep the existing product data)
]

# Existing routes
@app.route('/')
def home():
    return "Hello, this is a basic Flask server running on port 4000!"

@app.route('/products', methods=['GET'])
def list_products():
    return jsonify(products)

@app.route('/product/<product_id>', methods=['GET'])
def get_product(product_id):
    for product in products:
        if dict(product).get("id", "") == product_id:
            return product
    return "Not Found"

# New methods and routes

def create_genai_model():
    """Create and return a GenerativeModel instance."""
    return GenerativeModel("gemini-1.5-flash-001")

def get_product_info(product):
    """Retrieve product information using Google Search Retrieval."""
    model_ground = create_genai_model()
    prompt = f"only give me the nutritional(benefits/harms) content regarding the consumptions of {product}. Also if there is any recent news regarding if the {product} has some false claims. Also find if the product is from a small busiess or not"
    tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())
    response = model_ground.generate_content(prompt, tools=[tool])
    return response.candidates[0].content.parts[0].text

def create_chat_model():
    """Create and return a ChatGoogleGenerativeAI instance."""
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-001",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

def create_chat_prompt():
    """Create and return a ChatPromptTemplate instance."""
    return ChatPromptTemplate.from_messages([
        SystemMessage(content='''You are well experienced dietician and nutritionist. You will be given the Age, height, weight and dietary precautions and goals of the person. 
                        You will be given a product and its ingredients select one from each category based on the ingredients and health goals of the person.
                        Category 1: how frequently can i consume it based on my weight goals:
                        1. daily consumption
                        2. weekly consumption
                        3. monthly consumption
                        Category 2: and as per my diet is this food :
                        1. nutritional
                        2. recreations
                        3.  or regular consumption for me

                        Category 3: If the food product follows any of the following:
                        1. Organic
                        2. Sustainable: 
                        3. Supports Small Businesses
                        4. Animal Cruelty-Free: 

                        Category 4: flag alergens if they are related to my allergy otherwise don't flag a warning
                        Category 5: you need to also flag diet type match this with the input of user info and flag if it is suitable for their dietary type or restrictions.
                        Category 6: Alert if there is a higher presence of nutrients desired in low qty (fats, sugar, sodium, calories)
                        Your final answer should only contain tags among one option of each category based on product nutrition analysis.
                        If the answer is None just drop that category output.
                        -Finally if the 4 out of 6 categories are suitable for this user add that as highly recommended product.
                        Your next input will be the info of the person, the name of the product, and screenshot of the ingredients
                        Make sure you are thorough about all the different tags before printing, all the tags category should be printed, and only the tags
                        
            '''
        ),
        HumanMessagePromptTemplate.from_template(
            template='''The person's info is as follows:
                Person info: I am a {gender} who is {age} years old, my weight is {weight}, my height is {height}, I am {diet_type} and I want to {health_goal}. Allergic to {allergen}.
                Product info: {product_info_str}
                'image_url': "data:image/jpeg;base64,{image_data}
                
                "'''
        ),
    ])

def process_image(image_file):
    """Process the uploaded image file and return base64 encoded data."""
    return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_product(user_info, product_info, image_data):
    """Analyze the product based on user info and product details."""
    chat_model = create_chat_model()
    chat_prompt = create_chat_prompt()
    chain = chat_prompt | chat_model

    response = chain.invoke({
        "image_data": image_data,
        "age": user_info["age"],
        "weight": user_info["weight"],
        "gender": user_info["gender"],
        "height": user_info["height"],
        "diet_type": user_info["diet_type"],
        "health_goal": user_info["health_goal"],
        "allergen": user_info["allergen"],
        "product_info_str": product_info
    })

    return response.content

@app.route('/analyze_product', methods=['POST'])
def analyze_product_endpoint():
    user_info = {
        "age": request.form['age'],
        "weight": request.form['weight'],
        "gender": request.form['gender'],
        "height": request.form['height'],
        "diet_type": request.form['diet_type'],
        "health_goal": request.form['health_goal'],
        "allergen": request.form['allergen']
    }
    product_name = request.form['product_name']
    image_file = request.files['product_image']

    product_info = get_product_info(product_name)
    image_data = process_image(image_file)
    result = analyze_product(user_info, product_info, image_data)

    return jsonify({"analysis": result})

def get_detailed_product_info(product):
    model = GenerativeModel("gemini-1.5-flash-001")
    
    # Get ingredients
    ingredients_prompt = f"What are the ingredients or major composition of {product}?"
    tool = Tool.from_google_search_retrieval(preview_grounding.GoogleSearchRetrieval())
    ingredients_response = model.generate_content(ingredients_prompt, tools=[tool])
    ingredients = ingredients_response.text

    # Get additional information
    prompt = f"""Make sure you compulsory do the followings for {product}:
    The product is {product} and the ingredients are {ingredients}, now do the following.
    Category 1: Can you give me a brief of taste on what the {product} is and add that full info in(*** ***).
    Category 2: Also only list the nutritional (benefits/harms) if there are any.
    Category 3 (only mention relevant category): look if the product is suitable for a vegan or keto or jain or all diets and flag only the name of that diet of any or multiple suitable in (*** ***).
    Category 4 (single word answer): If the {product} is organic or supports sustainability or small businesses add that in (*** ***).
    Category 5: Also if there is any recent news regarding {product} flag it in less than 3 words in (*** ***).
    Give me the ingredients of this {product} from the internet (*** ***)"""

    max_attempts = 3
    attempts = 0
    llm_results = []

    while attempts < max_attempts and not llm_results:
        response = model.generate_content(prompt, tools=[tool])
        response_string = str(response.text)
        llm_results = re.findall(r'\(\*\*\*(.*?)\*\*\*\)', response_string)
        attempts += 1

    if not llm_results:
        llm_results = ["No results obtained after multiple attempts"]

    return {
        'ingredients': ingredients,
        'llm_results': llm_results
    }

@app.route('/get_detailed_product_info', methods=['GET'])
def get_detailed_product_info_endpoint():
    product = request.args.get('product')
    if not product:
        return jsonify({"error": "Product parameter is required"}), 400
    
    result = get_detailed_product_info(product)
    return jsonify(result)

@app.route('/get_ingredients', methods=['GET'])
def get_ingredients():
    product = request.args.get('product')
    if not product:
        return jsonify({"error": "Product parameter is required"}), 400
    
    model = GenerativeModel("gemini-1.5-flash-001")
    prompt = f"What are the ingredients or major composition of {product}"
    tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())
    
    response = model.generate_content(prompt, tools=[tool])
    ingredients = response.candidates[0].content.parts[0].text
    
    return jsonify({"product": product, "ingredients": ingredients})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)