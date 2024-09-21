# app.py
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel, Tool
from vertexai.preview.generative_models import grounding as preview_grounding
import re

app = Flask(__name__)

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/DELL/Downloads/13-Google-GenAI-Hack-24/GenAI-Google--Hack-24/Built-RAG/search_keys.json"

PROJECT_ID = "vision-forge-414908"
REGION = "us-central1"

vertexai.init(project=PROJECT_ID, location=REGION)

def get_product_info(product):
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form['product_name'].strip()
        if not product_name:
            return render_template('index.html', error="Please enter a product name")
        product_info = get_product_info(product_name)
        print(product_info)
        return render_template('results.html', product_name=product_name, product_info=product_info)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)