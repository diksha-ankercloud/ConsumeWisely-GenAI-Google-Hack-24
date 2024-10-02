from flask import render_template, redirect, request, url_for, flash, Flask, session
from flask import jsonify
import vertexai,requests,re,os
import base64,json
from google.cloud import firestore
from vertexai.generative_models import GenerativeModel, Tool, grounding
from googleapiclient.discovery import build
from flask_cors import CORS
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =r""
vertexai.init(project="", location="")
cxid = ""
apikey = ""
# genai.configure(api_key = os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
app = Flask(__name__)
CORS(app)
search_url = "https://www.googleapis.com/customsearch/v1"
collection_name="Shopping-Products"
db = firestore.Client.from_service_account_json(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

# This function lists all the products from the db in the ui.
@app.route('/list_products',methods=['POST'])
def list_products():
    products_ref = db.collection('products')
    matched_products = []

    # Stream all documents in the products collection
    for doc in products_ref.stream():
        product_data = doc.to_dict()
        product_data['product'] = doc.id  
        matched_products.append(product_data)
        print('Products matched are',matched_products)
            
    if matched_products:
        print('All products from DB::')
        return jsonify(matched_products)   

# This is the first function to check if the product exists in the db or not if it exists it retrives the product if not it goes to the else block and from the model and vertex-ai, custom search it brings the data for storing it in db.
@app.route('/check_product',methods=['POST'])
def check_product():

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
        return jsonify(matched_products)   
    
    else:
        print('Product not found in the db so searching the other apis.........')
        final=get_search_info(product_name)
        return final
    
# This is the second function that it calls if the product name was not found in the firestore db. it gets the produt name and first pass it to the vertex ai search api then gets the image link and bytes code form the downloadimage function and finally pass it to the chat-bot to categorize the product.
def get_search_info(product_name):
    print('Inside',product_name)
    product=product_name
    ingredients = get_ingre_search(product)
    # product_info = get_search_info(product, ingredients)
    data=downloadImage(product)
    links=data.get('links')
    data1=data.get('image_data')
    request_data={
        "product": product,
        "ingredients": ingredients,
        "image":data1,
        "links":links
    }
    res=chat_bot(request_data)
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
    if image_url:
        first_image_url = image_url[0]
        image_name = first_image_url.split('/')[-1]  
        image_path = os.path.join(folder_path, image_name)
        img_response = requests.get(first_image_url)
        with open(image_path, 'wb') as image_file:
            image_file.write(img_response.content)
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
        
    res={
        'links':image_dict,
       'image_data':image_data
    }
    return res

#This function categorize the product into different categories and finally store it in db.
def chat_bot(request_data):
    print('Hi there you are inside the function',request_data)
    if request_data.get('product'):
        product=request_data.get('product')
        request_message = request_data.get('ingredients')
        
    if request_data.get('image'):
        links=request_data.get('links')
        request_image = request_data.get('image')
    # This gemini flash modle expects the image bytes and the ingredients of the product for categorizing the product.
    prompt="""

    I will provide you a product name, ingrediants and the images of the product analyze everything carefully and segrigate the product in the following categories,
    Consumption : how frequently can i consume:
    1. daily
    2. weekly
    3. monthly
    Category :
    1. nutritional
    2. recreations
    3.  or regular consumption.

    Allergies: flag allergens if they are related to my allergy otherwise don't flag a warning if there are any claims verify if it is true provide the resource for this details. if any ingredients can affect or trigger the allergy then provide a caution information.
                                                            
    Diet Type:  Provide who all can consume based on their diet type like: vegan, keto, gluten-Free.
    The description should be about the product a brief explanatio what this product is.
    If the product contains any organic sustainable such as Organic farming and eating organic food are sustainable because they help to protect the environment and promote healthier use of natural resource provide that too.
    ### Provide the information in terms of a label like it contains gluten ,excess sugar bad for diabetics.. remove all the filler words the output should be concise and exact not like a paragraph.                                                 
    ### Provide the right details and information if the product is not safe to consume and affects the health.
        OUTPUT FORMAT:
        {
        "Description": "",
        "product": "",
        "product_info": {
            "allergens": "",
            "diet_suitability": "",
            "ingredients": "",
            "nutritional_benefits_harms": "",
            "organic_sustainable": "",
            "recent_news": "",
            "taste": ""
        }
    }
        </output>
    ###Note if the product does not fall into any of the mentioned categories then provide that category name as key and value as none.
"""
    prompt=request_message+' '+prompt
    generative_multimodal_model = GenerativeModel("gemini-1.5-flash-001")
    response = generative_multimodal_model.generate_content([prompt,request_image])
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
        data_base=store_data_in_firestore(json_data, links)
        print('Data Stored or already exists:::',data_base)
    output_json={
        "message": json_data,
        "links":links
    }
    return output_json

# this function will finally store the data from the chat-bot function.
def store_data_in_firestore(llm_response, links):
    print('Inside the DB;;;;',llm_response)
    print('Type of the data',type(llm_response))
    # First get all the data for storing like links,product,ingredients etc..
    link1 = links.get('image-1', None)
    link2 = links.get('image-2', None)
    link3 = links.get('image-3', None)
    link4 = links.get('image-4', None)
    product_name = llm_response.get("product")
    description = llm_response.get("Description")
    product_info = llm_response.get("product_info", {})
    allergens = product_info.get("allergens")
    diet_suitability = product_info.get("diet_suitability",None)
    ingredients = product_info.get("ingredients",None)
    nutritional_benefits_harms = product_info.get("nutritional_benefits_harms",None)
    organic_sustainable = product_info.get("organic_sustainable",None)
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
        "organic_sustainable": organic_sustainable,
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
