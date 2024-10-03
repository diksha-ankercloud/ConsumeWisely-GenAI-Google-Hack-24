from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel, Tool
from vertexai.generative_models import grounding
import re
import time

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Set up Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ""
PROJECT_ID = ""
REGION = ""

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=REGION)

# Initialize the generative model
model = GenerativeModel("gemini-1.5-flash-001")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product = request.form['product']
        ingredients = get_ingre_search(product)
        product_info = get_search_info(product, ingredients)
        print(product_info)
        return render_template('result.html', product=product, ingredients=ingredients, product_info=product_info)
    return render_template('index.html')

def get_ingre_search(product):
    prompt = f"what are the ingredients or major composition of {product}"
    tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())
    response = model.generate_content(prompt, tools=[tool])
    ingredients = response.candidates[0].content.parts[0].text
    print(f"Ingredients for {product}: {ingredients}")  # Confirmation output
    return ingredients

def get_search_info(product, ingredients):
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        prompt = f"""The product is {product} and the ingredients are {ingredients}, now do the following:
        Category 1: Can you give me a brief of taste on what the {product} is and add that full info in(*** ***).
        Category 2: Also only list the nutritional (benefits/harms) if there are any.
        Category 3 (only mention relevant category): look if the product is suitable for a vegan or keto or jain or all diets and flag only the name of that diet of any or multiple suitable in (*** ***).
        Category 4 (single word answer): If the {product} is organic or supports sustainability or small businesses add that in (*** ***).
        Category 5: Also if there is any recent news regarding {product} flag it in less than 3 words in (*** ***).
        Give me the ingredients of this {product} from the internet (*** ***)
        If you are not able to fill in these categories based on ingredients so look into the product name and then gfill in the categories u have to fill them mandatorily understanding and print all ctegories. even if some categories u find no info print them as None"""
        
        tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())
        response = model.generate_content(prompt, tools=[tool])
        response_string = str(response.candidates[0].content.parts[0].text)
        
        #matches = re.findall(r'\(\*\*\*(.*?)\*\*\*\)', response_string)
        return response_string
        
       


if __name__ == '__main__':
    app.run(debug=True)