import os
from dotenv import load_dotenv
import base64
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from vertexai.preview.generative_models import grounding as preview_grounding
import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    grounding,
)
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Load environment variables
load_dotenv()

def initialize_environment():
    """Initialize environment variables and Google Cloud settings."""
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/DELL/Downloads/13-Google-GenAI-Hack-24/GenAI-Google--Hack-24/vision-forge-414908-d792f2fc2ff6.json"
    
    PROJECT_ID = "vision-forge-414908"
    REGION = "us-central1"
    vertexai.init(project=PROJECT_ID, location=REGION)

def create_genai_model():
    """Create and return a GenerativeModel instance."""
    return GenerativeModel("gemini-1.5-flash-001")

def get_product_info(product):
    """Retrieve product information using Google Search Retrieval."""
    model_ground = create_genai_model()
    prompt = f"Give me the ingredients and composition of this {product}. Give me the nutritional (benefits/harms) content regarding the consumption of {product}. Also give information regarding the parent company and its carbon footprint of available of the{product} . Also find if the product is from a small business or not."
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
                        You will be given a product and its ingredients select one from each category based on the ingredients and health goals of the person only add in the result each category name should be in (#category#) and only answer of each category in (** **).
                        (Frequency of cunsumption): how frequently can i consume it based on my weight goals:
                        1. daily consumption
                        2. weekly consumption
                        3. monthly consumption
                        (habit of eating): and as per my diet is this food :
                        1. nutritional
                        2. recreations
                        3.  or regular consumption for me

                        (sustainibility parameters): If the food product follows any of the following:
                        1. Organic
                        2. Sustainable: 
                        3. Supports Small Businesses
                        4. Animal Cruelty-Free: 
                        5. Lower carbon footprint

                        (allergy alert): flag alergens if they are related to my allergy otherwise don't flag a warning
                        (diet type): you need to also flag diet type match this with the input of user info and flag if it is suitable for their dietary type or restrictions(eg vegan/jain/vegetarian/keto) based on user input also flag why not suitable should be a part of the answe in (** **).
                        (nutrient alert): Alert if there is a higher presence of nutrients desired in low qty (fats, sugar, sodium, calories)
                        (carbon footprint info): give info about carbon footprint of the product and also give info about the parent company of the product.
                        Your final answer should only contain tags among one option of each category based on product nutrition analysis.
                        If the answer is None just drop that category output.
                        -Finally if the 4 out of 6 categories are suitable for this user add that as highly recommended product.
                        Your next input will be the info of the person, the name of the product, and screenshot of the ingredients
                        Make sure you are thorough about all the different tags before printing, all the tags category should be printed, and only the tags
                        
            '''),
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
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    user_info = {
        "age": data.get('age'),
        "weight": data.get('weight'),
        "gender": data.get('gender'),
        "height": data.get('height'),
        "diet_type": data.get('diet_type'),
        "health_goal": data.get('health_goal'),
        "allergen": data.get('allergen')
    }
    
    product_name = data.get('product_name')
    image_data_base64 = data.get('image_data')

    if not product_name or not image_data_base64:
        return jsonify({"error": "Missing required parameters: product_name or image_data"}), 400

    product_info = get_product_info(product_name)
    result = analyze_product(user_info, product_info, image_data_base64)

    # Process the result using regex to create the desired JSON format
    processed_result = {}
    pattern = r'#\s*(.*?)\s*#:\s*\*\*(.*?)\*\*'
    matches = re.findall(pattern, result)
    
    for key, value in matches:
        processed_result[key.strip()] = value.strip()

    return jsonify({"analysis": processed_result})




if __name__ == "__main__":
    initialize_environment()
    app.run(host='0.0.0.0', port=5000, debug=True)
