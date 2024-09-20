from flask import render_template, redirect, request, url_for, flash, Flask, session
import os
from flask import jsonify
import vertexai
import os
import requests
import re
import google.generativeai as genai
from vertexai.preview.generative_models import GenerativeModel
from PIL import Image
REGION = "us-central1"
vertexai.init(project="vision-forge-414908", location="us-central1")
os.environ['GOOGLE_API_KEY'] ="AIzaSyA-Wq-bd6YjRHDkepVfsZq12mKA2r9zWac"
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
#default route
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['GET', 'POST'])
def get_response():
    print('Hi there you are inside the function')
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
I will provide an image of a product ingrediants confirms where the products is safe to consume for humans including kids,pregnat women,old people,diabets,heart patient,etc...
    Consumption 1: how frequently can i consume:
    1. daily
    2. weekly
    3. monthly
    Category :
    1. nutritional
    2. recreations
    3.  or regular consumption for me

    Allergies: flag alergens if they are related to my allergy otherwise don't flag a warning if there are any claims verify if it is true provide the resorce for this details. if any ingrediants can affect or trigger the allergy then provide a caution information.
                                                            
    Diet Type:  Provide who all can consume based on their diet type like: vegan,vegetarian,pescatarian,keto,paleo,mediterranean,gluten-Free,Whole30,carnivore,flexitarian,etc..

    ### Provide the information in terms of a lable like it contains gluent,excess sugar bad for diabetics,etc.. remove all the filler words the output should be consise and exact not like a paragraph.                                                 
    ### Provide the right details and information if the product is not safe to consume and affects the health and provide alternative organic product which falls in the same budget
    ### Provide what category does this product fall into remember to mention all the product category under the provided category.mention all the categories that the product fall into             
    ### Finally provide the product name at the first line with following syntax Product Name: XXXXX. and recommend similar product  within the same budget.                  
"""
    request_message=prompt
    print(request_message,request_image)
    image = Image.open(request_image)
    generative_multimodal_model = genai.GenerativeModel("gemini-1.5-flash-001")
    response = generative_multimodal_model.generate_content([request_message,image])
    print(response.__dict__)
    ans=response._result.candidates[0].content.parts[0].text
    ans=ans.replace('*','')
    ans=ans.split('\n\n')
    print(ans)
    answer=""
    for i in (ans):
        answer+=i.strip()
    print('Answer:',answer)
    output_json={
        "message": answer
    }
    return jsonify(output_json)

if __name__ == "__main__":
    app.run(host = "0.0.0.0",port=8085, debug=False, use_reloader=False)