#all the necessary imports
from flask import render_template, redirect, request, url_for, flash, Flask, session
from flask import jsonify
import vertexai,requests,re,os
import base64,json
from google.cloud import firestore
from vertexai.generative_models import GenerativeModel, Tool, grounding
from googleapiclient.discovery import build
from flask_cors import CORS
import os
import base64
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    grounding,
)

import re

from dotenv import load_dotenv
load_dotenv()

#keys required to run application
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ="./cred.json"
vertexai.init(project="vision-forge-414908", location="us-central1")
os.environ["cxid"] = "20551f7fc808b4671"
cxid = os.environ['cxid']
os.environ["apikey"] = "AIzaSyA9zpnFCZ51r7rnGz7vxNQbjcj8AzIV4m0"
apikey = os.environ['apikey']
search_url = "https://www.googleapis.com/customsearch/v1"
# genai.configure(api_key = os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

app = Flask(__name__)
CORS(app)

#database funtions 
collection_name="Shopping-Products"
db = firestore.Client.from_service_account_json(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

####################################listing all prodcut fror front page####################################

# This function lists all the products from the db in the ui. it will retrive only the first image url and the product name from the db.
@app.route('/list_products',methods=['POST'])
def list_products():
    products_ref = db.collection('products')
    
    products = []

    # Stream all documents in the products collection
    for doc in products_ref.stream():
        product_data = doc.to_dict()
        matched_products={
            "product":product_data.get('product'),
            "image":product_data.get('images',{}).get('image-1')
        }
        
        matched_products['product'] = doc.id  
        products.append(matched_products)
            
    if products:
        print('All products from DB::')
        return jsonify(products)   #return 1 image url and name for each product
    
#########################################################################################################



#############################lisitng search products with similar names from db##########################

#this one is when the customer seraches for a name and all the products that match the prodcut name appear
@app.route('/list_search_products',methods=['POST'])
def list_search_products():
    product_name=request.form.get('product')
    print('Product name::',product_name)
    search_words = product_name.lower()
    products_ref = db.collection('products')

    products = []

    # Stream all documents in the products collection
    for doc in products_ref.stream():
        if search_words in doc.id.lower():
            print('data-type of dcouments:',type(doc))
            product_data = doc.to_dict()
            matched_products={
                "product":product_data.get('product'),
                "image":product_data.get('images',{}).get('image-1')
            }
            
            matched_products['product'] = doc.id  
            products.append(matched_products)
            
    if products:
        print('All products from DB::')
        return jsonify(products)     #returns 1 image url and product name for each product
    

##########################################################################################################


########check if complete product is there in db otherwise the complete search output from web###########



# This is the first function to check if the product exists in the db  if not it goes to the else block and from the model and vertex-ai, custom search it brings the data for storing it in db.
@app.route('/check_product_and_web_search',methods=['POST'])
def check_product_and_web_search():

    data = request.get_json()
    product_name=data["product"]
    print('Product name',product_name)
    search_words = product_name.lower()
    products_ref = db.collection('products')
    matched_products = []

    # Stream all documents in the products collection
    for doc in products_ref.stream():
        if search_words in doc.id.lower():
            product_data = doc.to_dict()
            product_data['product'] = doc.id  
            matched_products.append(product_data)
            print('Products matched are',matched_products)
            
    if matched_products:
        images_name=product_data.get('images')
        des=product_data.get('description')
        product_information=product_data.get('product_info')
        product_names=product_data.get('product_name')
        ans={
            'description':des,
            'images':images_name,
            'product_name':product_names,
            'product_info':product_information
        }
        print(images_name)
        print('ans',ans)
        # image1=matched_products.get('')
        return jsonify(matched_products[0])   
    
    else:
        print('Product not found in the db so searching the other apis.........')
        final=get_combined_ingre_img(product_name)
        return final
    
# This is the second function that it calls if the product name was not found in the firestore db. it gets the produt name and first pass it to the vertex ai search api then gets the image link and bytes code form the downloadimage function and finally pass it to the chat-bot to categorize the product.
def get_combined_ingre_img(product_name):
    print('Inside',product_name)
    product=product_name
    ingredients = get_ingre_search(product)
    # product_info = get_combined_ingre_img(product, ingredients)
    data=downloadImage(product)
    links=data.get('links')
    
    request_data={
        "product": product,
        "ingredients": ingredients,
        "links":links
    }
    res=get_search_info(request_data)
    return jsonify(res)

def get_ingre_search(product):
    prompt = f"what are the ingredients or major composition of {product}"
    tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())
    model = GenerativeModel("gemini-1.5-flash-001")
    response = model.generate_content(prompt, tools=[tool])
    ingredients = response.candidates[0].content.parts[0].text
    return ingredients

# This function uses the custom search api for image retrival from the internet
def downloadImage(searchTerm):
    searchTerm=searchTerm
    service = build("customsearch", "v1",
            developerKey=apikey)
    params = {
        "q": searchTerm,
        "cx": cxid,
        "searchType": "image",
        "num": 4,
        "fileType": "jpg",
        "imgType": "photo",
        "key": apikey,
    }
    response = requests.get(search_url, params=params)
    print(response)
    results = response.json()
    # This part maps the retrived links with the number of images link it generated in a key value pair.
    image_url = [item["link"] for item in results.get("items", [])]
    image_dict = {f"image-{i+1}": url for i, url in enumerate(image_url)}
    print('Image-urls::',image_url)
    folder_path='static'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image_name='sample-testing-image-1'
    # This part extracts the image urls and retrive only the first image and convert them to base64 bytes.

        
    res={
        'links':image_dict
    }
    return res

#This function categorize the product into different categories and finally store it in db.
def get_search_info(request_data):
    print('Hi there you are inside the function',request_data)
    if request_data.get('product'):
        product=request_data.get('product')
        request_message = request_data.get('ingredients')
        
    
    links=request_data.get('links')
        
    # this is the model prompt for search it takes in ingredients and then it also takes in prodcut name
    prompt= f'''
    Do the following for the given {product} using the info from {request_message}:
    The Description should be about the product a brief explanation about this product like what is this product.
    Allergens: flag allergens if they are related to my allergy otherwise don't flag a warning if there are any.                                                      
    Diet Suitability: mention if it is suitable for vegan, keto, jain  or gluten-free, diabetic diets, high cholestrol patients etc consumers either one or many options.
    Ingredients: with ** format for ach ingredients list all the {request_message} contents of the product with measurements.
    Nutritional Benefits/Harms: mention if the product has any nutritional benefits or harms for the health of the consumer based on {request_message}.
    Sustainibility factor: mention if the {product} is organic or supports sustainability or small businesses or is animal cruelty free.
    Recent-news: mention there is any recent news regarding {product} flag it in one or 2 sentences.
    Taste: Give a brief on the taste and flavor profiles of the product {product}
    If the product contains any organic sustainable such as Organic farming and eating organic food are sustainable because they help to protect the environment and promote healthier use of natural resource provide that too.                                              
    ### Provide the right details and information if the product is not safe to consume and affects the health.
    '''
    #this is the output format from the llm for websearch each of these key values should be displayed in frontend
    output_format = '''
        OUTPUT FORMAT:
        {
        "description": "",
        "product_name": "" ,
        "product_info": {
            "allergens": "",
            "diet_suitability": "",
            "ingredients": "",
            "nutritional_benefits_harms": "",
            "sustainibility_factor": "",
            "recent_news": "",
            "taste": ""
        }
    }
     ###Note: If you are not able to retrieve information for any of the above categores just pass the value as None
    
'''
    prompt = prompt + output_format
    generative_multimodal_model = GenerativeModel("gemini-1.5-flash-001")
    response = generative_multimodal_model.generate_content([prompt])
    ans=response._raw_response.candidates[0].content.parts[0].text
    # After getting the final response from llm we need to removed un wanted parameters to structure the code. since it is an llm response in json format it would give the output in string only so to convert to json remove the '''json at the beggining and ''' at the end
    ans=ans.replace('**','')
    ans=ans.replace('*','')
    if ans.startswith(r'```json'):
        json_string = re.search(r'```json(.*?)```', ans, re.DOTALL)
        if json_string:
            llm_response = json_string.group(1).strip() 
            
            print('Json string---------------------::',llm_response)
    product_name = re.search(r'"product_name":\s*"(.*?)"', llm_response)
    # After retriving the final data store it in the firestore db
    if product_name:
        print('Inside')
        product_name=f"{product_name.group(1)}"
        json_data = json.loads(llm_response)
        print('Done')
        data_base=store_data_in_firestore(json_data, links,product)
        print('Data Stored',data_base)
        json_data['images']=links
        description=json_data.get('description')
        json_data['description']=description
        
        print('Json_data:::',json_data)
        ans=jsonify(json_data)
        print('Json Description::',json_data['description'])
        # print('Final_answer:',ans)
    return ans

##############################################################################################################

@app.route('/search_image', methods=['GET'])
def search_image():
    # Get query parameters
    query = request.args.get('query')
    side = request.args.get('side', False)
    total = request.args.get('total', False)
    
    # API URL for Google Custom Search
    url = f"https://www.googleapis.com/customsearch/v1?key={apikey}&cx={cxid}&q={query + ' packaged food OR snacks OR canned OR frozen OR bottled' + ' site:bigbasket.com OR site:blinkit.com OR site:zeptonow.com'}&searchType=image&fileType=jpg,png&imgSize=medium&safe=active&num=10"
    
    if side and total:
        url = f"https://www.googleapis.com/customsearch/v1?key={apikey}&cx={cxid}&q={query + ' ' + side + ' packaged food OR snacks OR canned OR frozen OR bottled' + ' site:bigbasket.com OR site:blinkit.com OR site:zeptonow.com'}&searchType=image&fileType=jpg,png&imgSize=medium&safe=active&num={total}"

    # Make a request to Google Custom Search API
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['items']

# this function will finally store the new data from web search to the db function.
def store_data_in_firestore(llm_response, links,product):

    print('Inside the DB;;;;',llm_response)
    print('Type of the data',type(llm_response))
    # First get all the data for storing like links,product,ingredients etc..
    link1 = links.get('image-1', None)
    link2 = links.get('image-2', None)
    link3 = links.get('image-3', None)
    link4 = links.get('image-4', None)
    product_name = product
    description = llm_response.get("description")
    product_info = llm_response.get("product_info", {})
    allergens = product_info.get("allergens")
    diet_suitability = product_info.get("diet_suitability",None)
    ingredients = product_info.get("ingredients",None)
    nutritional_benefits_harms = product_info.get("nutritional_benefits_harms",None)
    sustainibility_factor = product_info.get("sustainibility_factor",None)
    recent_news = product_info.get("recent_news",None)
    taste = product_info.get("taste",None)
    # create a schema before storing in db
    data_to_store = {
    "product_name": product_name,
    "description": description,
    
    "product_info": {
        "allergens": allergens,
        "diet_suitability": diet_suitability,
        "ingredients": ingredients,
        "nutritional_benefits_harms": nutritional_benefits_harms,
        "sustainibility_factor": sustainibility_factor,
        "recent_news": recent_news,
        "taste": taste
    },
    "images":{
        "image-1":link1,
        "image-2":link2,
        "image-3":link3,
        "image-4":link4
    }
}   # create a collection under which the product names are stored as the document id
    products_ref = db.collection('products')
    query = products_ref.where("product_name", "==", product_name).limit(1)
    results = query.stream()
    existing_product = list(results)

    if not existing_product:
        # If product does not exist store the new product information
        doc_ref = products_ref.document(product_name) # set the product name as doc id.
        doc_ref.set(data_to_store)
        print(f"New product '{product_name}' successfully stored in Firestore.")
    else:
        # If product exists retrieve its information.
        
        for product in existing_product:
            product_data = product.to_dict()
            print(f"Product '{product_name}' already exists in Firestore. Details:")
            print(json.dumps(product_data, indent=4))




#####################personalisation code for after single product page loaded######################################
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
        SystemMessage(content='''
                        You are well experienced dietician and nutritionist. You will be given the Age, height, weight and dietary precautions and goals of the person. 
                        You will be given a product and its ingredients select one from each category based on the ingredients and health goals of the person only add in the result each category name should be in (#category#) and only answer of each category in (** **).
                        Output should lool like:
                        RESULTS:
                        (#Frequency of cunsumption#): how frequently can i consume it based on my weight goals:
                        1. daily consumption
                        2. weekly consumption
                        3. monthly consumption
                        (#habit of eating#): and as per my diet is this food :
                        1. nutritional
                        2. recreational
                        3.  or regular consumption for me

                        (#sustainibility parameters#): Imention if the product has the following characteristics:
                        1. Organic
                        2. Sustainable: 
                        3. Supports Small Businesses
                        4. Animal Cruelty-Free: 
                        5. Lower carbon footprint

                        (#allergy alert#): flag alergens if they are related to my allergy otherwise don't flag a warning
                        (#diet type#): you need to also flag diet type match this with the input of user info and flag if it is suitable for their dietary type or restrictions(eg vegan/jain/vegetarian/keto) based on user input , answer should be in (** **) mentioning which diet it is suitable or not suitable for.
                        (#nutrient alert#): Alert if there is a higher presence of nutrients desired in low qty (fats, sugar, sodium, calories take into consideration all micro and macro nutrients)
                        (#carbon footprint info#): give info about carbon footprint of the product and also give info about the parent company of the product.
                        (#recomendation#):Finally if the 4 out of 6 categories are suitable for this user add that as highly recommended product if 3 or 2 out of 6 categories match say mid recommendation otherwise any lessser say none in  (** **)  
                       Your final answer should only contain tags among one option of each category based on product nutrition analysis.
                        If the answer is None just drop that category output.
                        
                        Your next input will be the info of the person, the name of the product, and screenshot of the ingredients
                        Make sure you are thorough about all the different tags before printing, all the tags category should be printed, and only the tags
                        
            '''),
        HumanMessagePromptTemplate.from_template(
            template='''The person's info is as follows:
                Person info: I am a {gender} who is {age} years old, my weight is {weight}, my height is {height}, I am {diet_type} and I want to {health_goal}. Allergic to {allergen}.
                Product info: {product_info_str}
                
                
                "'''
        ),
    ])



def analyze_product(user_info, product_info):
    """Analyze the product based on user info and product details."""
    chat_model = create_chat_model()
    chat_prompt = create_chat_prompt()
    chain = chat_prompt | chat_model

    response = chain.invoke({
        
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
    

    

    product_info = get_product_info(product_name)
    print(product_info)
    result = analyze_product(user_info, product_info)
    print(result)
    # Process the result using regex to create the desired JSON format
    pattern = re.compile(r"\(#(.*?)#\): \*\*(.*?)\*\*")

    # Find all matches
    matches = pattern.findall(result)

    # Create dictionary from matches
    result_dict = {}
    for key, value in matches:
        # Handle multiple occurrences of the same key
        if key in result_dict:
            # Convert value to a list if it's not already
            if not isinstance(result_dict[key], list):
                result_dict[key] = [result_dict[key]]
            result_dict[key].append(value)
        else:
            result_dict[key] = value

    # Return the dictionary as a JSON response using jsonify
    return jsonify(result_dict)

######################################################################################################


############################listing 2 recipes api ######################################################
# Define route for getting recipes this function needs the name of the product as well as the diet type such as vegan/ketojain/high choletrol/low sugar etc
@app.route('/get_recipes', methods=['POST'])
def get_recipes():
    # Get the input parameters from the request
    data = request.json
    product = data.get('product')  # Default value if not provided
    restrictions = data.get('restrictions')  # Default value if not provided
    
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
    return jsonify({"recipes": result})     # outputs recipe name and a brief description
########################################################################################################







if __name__ == "__main__":
    app.run(host = "0.0.0.0",port=8088,debug=True)
