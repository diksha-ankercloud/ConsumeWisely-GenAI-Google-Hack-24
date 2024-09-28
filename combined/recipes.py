from flask import Flask, request, jsonify
import os
import re
from dotenv import load_dotenv
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from vertexai.generative_models import GenerativeModel, Tool, grounding
import vertexai

# Load environment variables
load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\DELL\Downloads\13-Google-GenAI-Hack-24\GenAI-Google--Hack-24\vision-forge-414908-d792f2fc2ff6.json"
PROJECT_ID = "vision-forge-414908"
REGION = "us-central1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=REGION)

# Initialize Flask app
app = Flask(__name__)

# Define route for getting recipes
@app.route('/get_recipes', methods=['POST'])
def get_recipes():
    # Get the input parameters from the request
    data = request.json
    product = data.get('product', 'parle g biscuit')  # Default value if not provided
    restrictions = data.get('restrictions', 'vegan')  # Default value if not provided
    
    # Initialize generative model
    model_ground = GenerativeModel("gemini-1.5-flash-001")
    
    # Generate product information
    PROMPT = f"give me the description, ingredients and flavor profile or taste of this {product}"
    tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())
    response = model_ground.generate_content(PROMPT, tools=[tool])
    food_info = response.candidates[0].content.parts[0].text

    # Chat model for generating recipes
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-001",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    chat_prompt = ChatPromptTemplate.from_messages(
        messages=[
            SystemMessage(
                content='''You are a great chef that can give quick and easy recipes following specific diets, ingredients, and taste. You will be given the product and its description, and you must provide 2 dishes with simple recipes using that product or similar. If there are dietary restrictions, suggest alternatives that retain similar taste.'''
            ),
            HumanMessagePromptTemplate.from_template(
                template=f'''
                The info is the following:
                the product name of the major foods in the recipe: {{product}}. and the major info regarding the product such as description, taste and ingredients {{food_info}}.
                Limit the recipes to these dietary restrictions: {{restrictions}}.
                Provide the following details:
                (#Recipe Name#): (**short, fun catchy name for recipe here**)
                (#Description#): (**description of the recipe in not more than 1 line. This should include keywords like keto, vegan, jain, cholesterol-less, sugar-free, high-protein, etc.**)
                Example output format: follow the following format to give the out put the category shoudld be in (# #) and the content in (*** ***)
                (#Recipe 1 Name#): (** the name of tthe recipe should be here **)
                (#Description#): (** description **)
                (#Recipe 2 Name#): (** the name of tthe recipe should be here**)
                (#Description#): (** description **)
                Make sure to follow the format  donnot add ingredients or any other stuff.print each recipe only once.
                
                '''
            ),
        ]
    )
    
    # Chain the model with the prompt
    chain = chat_prompt | model
    response_from_model = chain.invoke(
        {
            "product": product,
            "food_info": food_info,
            "restrictions": restrictions
        }
    )

    # Extract and format the recipes
    
    
    recipe_2 = response_from_model.content
    print(recipe_2)
    pattern = r'\(#Recipe (\d+) Name#\): \(\*\*(.*?)\*\*\)\s*\n\(#Description#\): \(\*\*(.*?)\*\*\)'
    matches = re.findall(pattern, recipe_2)

    # Prepare the output format
    result = []
    for match in matches:
        recipe_name = match[1].strip()  # Recipe name
        description = match[2].strip()  # Description
        result.append({
            "Recipe Name": recipe_name,
            "Description": description
        })

    # Convert to JSON and return
    return jsonify({"recipes": result})




# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
