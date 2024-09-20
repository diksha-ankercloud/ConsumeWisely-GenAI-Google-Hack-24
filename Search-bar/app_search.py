# app.py
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel, Tool
from vertexai.preview.generative_models import grounding as preview_grounding
import re
from langchain_community.tools import TavilySearchResults

app = Flask(__name__)

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "path/to/your/credentials.json"
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

PROJECT_ID = "your-project-id"
REGION = "us-central1"

vertexai.init(project=PROJECT_ID, location=REGION)

def get_product_info(product):
    # Tavily search
    tools = TavilySearchResults(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_images=True
    )
    
    PROMPT = f"Give me the ingredients that are present in {product}"
    tavily_reply = tools.invoke({"query": PROMPT})
    first_reply = tavily_reply[0]
    ingredients = first_reply.get('content')
    
    # Vertex AI processing
    model = GenerativeModel("gemini-1.5-pro")
    prompt_2 = f"""The product is {product} and the ingredients are {ingredients}, now do the following.
    Category 1: Can you give me a brief of taste on what the {product} is and add that full info in(*** ***).
    Category 2: Also only list the nutritional (benefits/harms) if there are any.
    Category 3 (only mention relevant category): look if the product is suitable for a vegan or keto or jain or all diets and flag only the name of that diet of any or multiple suitable in (*** ***).
    Category 4 (single word answer): If the {product} is organic or supports sustainability or small businesses add that in (*** ***).
    Category 5: Also if there is any recent news regarding {product} flag it in less than 3 words in (*** ***).
    Give me the ingredients of this {product} from the internet (*** ***)"""
    
    tool = Tool.from_google_search_retrieval(preview_grounding.GoogleSearchRetrieval())
    response = model.generate_content(prompt_2, tools=[tool])
    response_string = str(response)
    
    # Extract information from response
    matches = re.findall(r'\(\*\*\*(.*?)\*\*\*\)', response_string)
    
    # Get image URL (assuming it's in the Tavily response)
    image_url = first_reply.get('image_url', '')
    
    return matches, image_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form['product_name']
        results, image_url = get_product_info(product_name)
        return render_template('results.html', product_name=product_name, results=results, image_url=image_url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)