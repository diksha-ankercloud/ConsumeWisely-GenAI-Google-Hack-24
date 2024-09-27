#all the necessary imports
from flask import render_template, redirect, request, url_for, flash, Flask, session
from flask import jsonify
import vertexai,requests,re,os
import base64,json
from google.cloud import firestore
from vertexai.generative_models import GenerativeModel, Tool, grounding
from googleapiclient.discovery import build
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

#keys required to run application
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =r"C:\Users\DELL\Downloads\13-Google-GenAI-Hack-24\GenAI-Google--Hack-24\vision-forge-414908-d792f2fc2ff6.json"
vertexai.init(project="vision-forge-414908", location="us-central1")
os.environ["cxid"] = os.getenv("cxid")
cxid = os.environ['cxid']
os.environ["apikey"] = os.getenv("apikey")
apikey = os.environ['apikey']
search_url = "https://www.googleapis.com/customsearch/v1"
# genai.configure(api_key = os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

app = Flask(__name__)
CORS(app)


#database funtions 
collection_name="Shopping-Products"
db = firestore.Client.from_service_account_json(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

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

# This is the first function to check if the product exists in the db  if not it goes to the else block and from the model and vertex-ai, custom search it brings the data for storing it in db.
@app.route('/check_product_and_web_search',methods=['POST'])
def check_product_and_web_search():

    product_name=request.form.get('product')
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
        
        # image1=matched_products.get('')
        return jsonify(matched_products)   
    
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

# This function uses the custom search api for image retrival
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
    The Description should be about the product a brief explanation what this product is.
    Allergens: flag allergens if they are related to my allergy otherwise don't flag a warning if there are any.                                                      
    Diet Suitability: mention if it is suitable for vegan, keto, jain  or gluten-free, diabetic diets, high cholestrol patients etc consumers either one or many options.
    Ingredients: list all the {request_message} contents of the product with measurements.
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
        "Description": "",
        "product": "" ,
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
    if ans.startswith(r'```json'):
        json_string = re.search(r'```json(.*?)```', ans, re.DOTALL)
        if json_string:
            llm_response = json_string.group(1).strip() 
            
            print('Json string::',llm_response)
    product_name = re.search(r'"product":\s*"(.*?)"', llm_response)
    # After retriving the final data store it in the firestore db
    if product_name:
        product_name=f"{product_name.group(1)}"
        json_data = json.loads(llm_response)
        data_base=store_data_in_firestore(json_data, links,product)
        print('Data Stored or already exists:::',data_base)
    output_json={
        "message": json_data,
        "links":links
    }
    return output_json

# this function will finally store the data from the chat-bot function.
def store_data_in_firestore(llm_response, links,product):

    print('Inside the DB;;;;',llm_response)
    print('Type of the data',type(llm_response))
    # First get all the data for storing like links,product,ingredients etc..
    link1 = links.get('image-1', None)
    link2 = links.get('image-2', None)
    link3 = links.get('image-3', None)
    link4 = links.get('image-4', None)
    product_name = product
    description = llm_response.get("Description")
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

if __name__ == "__main__":
    app.run(host = "0.0.0.0",port=8088,debug=True)
