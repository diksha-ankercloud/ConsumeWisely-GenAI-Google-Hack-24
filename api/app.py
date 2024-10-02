from flask import request, Flask
import os
from flask import jsonify
import vertexai
import requests
import re
import google.generativeai as genai
from PIL import Image
from flask_cors import CORS
os.environ['GOOGLE_API_KEY'] =""
vertexai.init(project="", location="")
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
app = Flask(__name__)

def download_image(image_url, folder_path, image_name=None):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        response = requests.get(image_url)
        response.raise_for_status() 
        if not image_name:
            image_name = image_url.split("/")[-1]
        image_path = os.path.join(folder_path, image_name)
        with open(image_path, 'wb') as image_file:
            image_file.write(response.content)
        return image_path
        print(f"Image downloaded and saved as {image_path}")
    except Exception as e:
        print(f"Failed to download image. Error: {e}")

@app.route('/get_response', methods=['GET', 'POST'])
def get_response():
    print('Hi there you are inside the function',request)
    request_message = request.form.get('message')
    print('Message:', request_message)
    url_pattern = r'(https?://[^\s]+)'
    url_match = re.search(url_pattern, request_message)
    print('URL:',url_match)
    if url_match:
        image_url = url_match.group(0)
        print(f"Found URL: {image_url}")
        request_image=download_image(image_url,folder_path='images')
    else:   
        request_image = request.files.get('image')
        print('Image:', request_image)
    
    prompt="""
I will provide an image of a product ingredients confirms where the products is safe to consume for humans including kids, pregnant women, old people, diabetes, heart patient ,etc...
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

    ### Provide the information in terms of a label like it contains gluten ,excess sugar bad for diabetics.. remove all the filler words the output should be concise and exact not like a paragraph.                                                 
    ### Provide the right details and information if the product is not safe to consume and affects the health.
    ### Highlight and Recommend a product separately on the next line under organic and healthy products with a complete name and brand name of that single product which falls with in the budget. maintain the diet type, also provide the alternative product price as a category note all the above categories it should be mostly nutritional, sustainable, contains no allergy.
    ### Recommend a product which should also fall in the same product type but a healthier and safer choich if its biscuit then recommend biscuit, if its chips then recommend chips ,etc. like a if i upload a cream biscuit the alternative recommended product should also be a cream biscuit but a healthier one.    ### Provide what category does this product fall into remember to mention all the product category under the provided category. mention all the categories that the product fall into. keep the response short and crisp.           
    ### Output Format for both the current product and recommended product details separately Provide only necessary labels, remember the responses will be reflected in the UI with correct punctuation and these headers in first letter should be capital everything in new line:      
    Product Name:
    Brand: 
    Price Range:
    Ingredients: 
    Frequency: 
    All the above Categories:
    <br>
    Recommended Product Name:
    Brand:
    Price Range:
    Ingredients:
    Frequency:
    Categories:
"""
    request_message=prompt
    print(request_message,request_image)
    image = Image.open(request_image)
    generative_multimodal_model = genai.GenerativeModel("gemini-1.5-flash-001")
    response = generative_multimodal_model.generate_content([request_message,image])
    print(response.__dict__)
    ans=response._result.candidates[0].content.parts[0].text
    ans=ans.replace('*','')
    ans=ans.replace('##','')
    ans=ans.split('\n\n')
    # print(ans)

    answer=""
    for i in (ans):
        answer+=i.strip()
    print('Answer:',answer)
    match = re.search(r'Product Name:\s*(.*?):', answer)
    match1 = re.search(r'Alternative Product Name:\s*(.*)', answer)  
    if match1:
        alternate_product = match1.group(1).strip()
        print(f"Product1: {alternate_product}")
    if match:
        alternate_product = match.group(1).strip()
        print(f"Product: {alternate_product}")
    else:
        print("No alternate product found.")
    output_json={
        "message": answer
    }
    return jsonify(output_json)

