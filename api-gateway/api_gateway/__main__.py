from flask import Flask, jsonify
from flask_cors import CORS 
from googleapiclient.discovery import build
import google.generativeai as genai
from PIL import Image
import requests
import os
import re

app = Flask(__name__)
CORS(app) 

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

def download_images(image_urls, folder_path='sample-images'):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Create the folder if it doesn't exist

    for i, image_url in enumerate(image_urls):
        try:
            image_name = image_url.split("/")[-1].split("?")[0]  # Clean up the image name
            image_path = os.path.join(folder_path, image_name)
            print(f'Downloading image: {image_name}')

            # Get the image content from the URL
            response = requests.get(image_url)
            response.raise_for_status()  # Check if the request was successful
            
            # Write the image to the file
            with open(image_path, 'wb') as image_file:
                image_file.write(response.content)
            
            print(f'Image saved to: {image_path}')
        except requests.exceptions.RequestException as e:
            print(f'Error downloading {image_url}: {e}')
        except Exception as e:
            print(f'Unexpected error: {e}')

products = [
  {
    "id" : "1",
    "name": "Britannia Good Day Cashew Biscuit",
    "description": "Britannia Good Day Cashew Cookies are delicious crunchy cookies blended with a nutty flavour of cashews. 100% vegetarian, cashews cookies satisfy your cravings between meals. Britannia biscuits, cookies, cakes and rusk are a perfect companion for your tea.",
    "price": "43",
    "tags": "Supports small businesses, Animal Cruelty free,vegan,Animal Cruelty-Free",
    "ingredients": "Refined Wheat Flour, Sugar, Edible Vegetable Oil, BUTTER (4.2%), Cashew Bits (4%), Milk solids, Raising agent [E500(ii), E503(ii)], Salt, Emulsifier (E322(i), E471), Artificial flavouring substances (Nuts, Butter, Vanilla)",
    "brands": "famous",
    "category": "snacks",
    "image_front": "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=70,metadata=none,w=1440/app/assets/products/sliding_images/jpeg/c86f28aa-9922-405a-99c1-ed08a5ba00c7.jpg?ts=1722761285",
    "image_back": "https://drive.google.com/file/d/1hLYGpFDUW3VTGjOBNAKFNfXM_nNh0Igc/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1FXtdjOYUdKUm-1JNy6CZUxLJYq4TkbLH/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/1XCVXbAv6OCPuNKGXYcNS751FHR_K1RzN/view?usp=drive_link"
  },
  { "id" : "2",
    "name": "Hide & Seek Chocolate Chip Cookies",
    "description": "Sprinkled with the goodness of chocolate, the Parle Hide & Seek Chocolate Chip Cookie is a perfect blend of crunch and taste. These square cookies leave a chocolatey flavour in the mouth with each bite and have a delightful taste. A chocolate cookie that is sprinkled with the goodness of chocolate chips. Has a crunchy texture in each bite. Square-shaped, so it can be dunked in your tea or coffee with ease.",
    "price": "48",
    "tags": "Supports small businesses, Animal Cruelty free,Non organinc,Animal Cruelty-Free",
    "ingredients": "Wheat Flour, Chocolate [Sugar, Cocoa Solids, Cocoa Butter, Dextrose, Emulsifier (Lecithin of Soya Origin) and Added Flavour (Artificial Flavouring Substances - Vanilla)] min 14.7%, Sugar, Edible Vegetable Oil, Invert Sugar Syrup, Raising Agents [503(ii), Baking Powder], Cocoa Solids 0.6%, Salt, Emulsifier [Di-Acetyl Tartaric Acid Esters of Mono and Di-Glycerides of Edible Vegetable Oils] and Dough Conditioner (223), Contains Added Flavours (Artificial Flavouring Substances - Vanilla)",
    "brands": "famous",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/1azLFgDeycV8kNX9laFT5eWpiZHC75pgY/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/10HUJ-wMKfFBw4aqiH2SxB-mXDTCo4FbN/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1OphgjBI5pWUW4gQWNi9ePbWM0ytQYNGv/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/1UIr7IecX6tukun-pUfOzI9mclsnAJJa9/view?usp=drive_link"
  },
  { "id" : "3",
    "name": "Let's Try Fruit Cake Rusk with Goodness of Wheat",
    "description": "Wheat Goodness",
    "price": "148",
    "tags": "Supports small businesses, Non Organic,Animal Cruelty-Free",
    "ingredients": "Wheat Flour, Milk, Brown Sugar, Edible Vegetable Fat, Fruit Cherry, Milk Powder, Custard Powder, Butter, Eggless Cake Concentrate, Baking powder, Cake Improver, Essence, Baking Soda, iodized Salt.",
    "brands": "Local",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/1-pdsv9QXU7JBLMfi_7JQDC4YGWaCmjBD/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/1LnekpDw9dJyGlb3OXwjwJQ5pG3b0fwQA/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1chEBPIBYgIDpNai0asov45jvGpcvNFik/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/151rKYuSt0MkTnI_hm-DeuKK2iJ6U_DBt/view?usp=drive_link"
  },
  { "id" : "4",
    "name": "Parle Real Elaichi Premium Rusk",
    "description": "Made from the choicest ingredients and baked to perfection, Parle Real Elaichi Rusk is perfect to satisfy those light hunger pangs. This crispy, crunchy all-time snack is the perfect companion to your daily cup of piping hot Chai.",
    "price": "48",
    "tags": "Supports small business,Non organinc,Animal Cruelty-Free,Sustainable",
    "ingredients": "Wheat Flour, Sugar, Edible Vegtable Oil, Suji, Yeast, Milk Solids, Salt, Butter, Wheat Gluten, Emulsifiers, Wheat Fibre, Spices, Antioxidant (300), Improver (1100)",
    "brands": "Famous",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/1_w2jOIqQjr-e5WdYL3GeklJ88snCPGwq/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/1bhSb60yxS_lQcq0BwPpLv42dK4NYtSBw/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/12V8_Kt4Z1alLyRF8BOCd-1LhnS8joavH/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/1DTaJDZ0sO0H2us6SVAOj_k54FZoUAhqp/view?usp=drive_link"
  },
  { "id" : "5",
    "name": "Parle-G Glucose Biscuit",
    "description": "Treat yourself to a pack of yummy Parle-G Biscuits filled with the goodness of milk and wheat. Tasty, healthy and power packed with glucose, these biscuits are a great tea-time accompaniment.",
    "price": "25",
    "tags": "Supports small business,Non organinc,Animal Cruelty-Free,Sustainable",
    "ingredients": "Wheat Flour (67%), Sugar Edible Vegetable Oil, Invert Sugar Syrup [Sugar, Citric Acid], Raising Agents [503 (Ii), Baking Powder], Salt, Milk Solids (0.6%), Emulsifier [Di-Acetyl Tartaric Acid Esters Of Mono and Di-Glycerides Of Edible Vegetable Oils] and Dough Conditioner [223]",
    "brands": "famous",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/1yz9MvDkBkgWuYtA2dddWArM8_IhY3ZqI/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/1a6t2EHl-uAlZlJn6vFKr-ewuoatPVrMK/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1ccQFu32gZQaqHzZ4xfVo7GgcOJsf4CMQ/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/16whkftuZACgOm-wikouasthV9cZaxiNw/view?usp=drive_link"
  },
  { "id" : "6",
    "name": "Patanjali Doodh Biscuit",
    "description": "Take a well-deserved break with wholesome patanjali doodh biscuits. Enhanced with fibre, the 100% atta biscuits are enriched with cow's milk. Simple and delicious, enjoy patanjali doodh biscuits as an energy snack without or with tea and coffee.",
    "price": "40",
    "tags": "Supports small business,Non organinc,Animal Cruelty-Free,Sustainable",
    "ingredients": "Wheat Flour (Atta-58.6%), Edible Vegetable Oil (Palm), Sugar, Liquid Glucose, Milk Solids (1.7%), Lodized Salt, Leavening Agents [INS-500(Ii), INS 503(Ii), Ins-341(I)], Cheese, Dough Conditioner (INS 223), Antioxidant (INS 319), Emulsifier [INS 322(I)], Flavours-natural, Nature Identical, Artificial Flavouring Substances (Milk & Vanilla).",
    "brands": "Famous",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/1wnDV5q2obD1wAnJyXH6s3XSPv2KR-YwS/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/1BpPuuiZSx2TYwUjcSGA4Nrh8m1ptbuID/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1EI037yixesDOsfkR-9RClHtbvwqGjB4L/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/1wGiJyINmXHzH12pTlNLlN9nZpn7x5aH8/view?usp=drive_link"
  },
  { "id" : "7",
    "name": "Cadbury Chocobakes Choc Layered Chocolate Cake",
    "description": "Experience the new exciting Chocobakes chocolate layered cakes \u2013 Your loved Cadbury, now inside a chocolate cake. Make moments with your loved ones sweeter \u2013 with Chocobakes cakes.",
    "price": "80",
    "tags": "Supports small business,Non organinc,Animal Cruelty-Free,Sustainable",
    "ingredients": "ingredients: Cake (45%*) - Refined Wheat Hour (Maida), Sugar, Humectants (420 (ii),\n422, 1520), Palm Olein, Liquid Glucose, Milk Solids, Cocoa Solids, Starch, Emulsifiers (322, 475, 471, 491), Raising Agent (500(ii), 450(i), 341(i)), lodised Salt, Flavours (Natural Flavour, Nature Identical Ravouring Substances), Preservative (202), Stabilizer (415). Chocolayer (29%*) - Sugar, Hydrogenated Vegetable Oils, Lactose-Rich Deproteinized Whey Permeate Powder, Cocoa Sollds, Emulsifiers (442, 476), Ravours (Nature Identical, Artificial (Vanilla and Caramel) Flavouring Substances. Filling (26%*) - Sugar, Fractionated Fat, Liquid Glucose, Humectant (422, 1520), Water, Emulsifiers (322, 475, 471, 491), Cocoa Solids, Flavours (Natural flavour, Nature Identical Flavouring Substances), lodised Salt, Preservative (202). Allergen Information: Contains Milk, Wheat, Sulphites and Soy.",
    "brands": "famous",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/1ItF3ZGibCQUOY9AmAL2xqbAJQVcxqNcJ/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/1L1zICMthkDODA7DmZdnjqLu5VKC7rrP3/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1PRZ2kloMNM4HsA1vY2poCDnDsovZEyln/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/1ItbK2idESL7iHGDCagejCI-f9ZghWxwD/view?usp=drive_link"
  },
  { "id" : "8",
    "name": "Munchy's Munchini Chocolate Wafer Roll",
    "description": "Indulge in the creamy, crunchy, tasty experience in every bite and rediscover the happiness of sharing. Every chocolate lover is in for a treat with these flavoured wafer bites and rolls. Flavoured wafers are a convenient way of snacking up at tea time",
    "price": "119",
    "tags": "Supports small business,Non organinc,Animal Cruelty-Free,Sustainable",
    "ingredients": " Sugar, Refined Wheat Flour\n(Maida), Vegetable Fat (Palm Oil), Cocoa Powder, Fructose, Modified Starch (E1414), Lactose, Milk Powder, Emulsifier- Soybean Lecithin (E322), Glucose Syrup, Salt, Flavourings, Food Colouring (Caramel E150d).",
    "brands": "famous",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/1Qz_r8HsxFiRMgEEYon6VpXBcI0NTCZNw/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/1fDjxyoe3su-wXi2Q_5I9pUN7TNx0waxE/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1XvgbmAPAdARFrNwzhM8ZIPxVQkh1SEC2/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/1d9eHwEMlqOdip45h85Kn1aJw_DF0Njn8/view?usp=drive_link"
  },
  { "id" : "9",
    "name": "English Oven Extra Crunchy Premium Rusk",
    "description": "Make your tea time crispy and rusky with amazingly delicious premium rusk. The taste of it makes you go irresistible. premium rusk biscuits provide best nutrition to your health.",
    "price": "62",
    "tags": "Supports small business,Non organinc,Animal Cruelty-Free,Sustainable",
    "ingredients": "Refined Wheat Flour (Maida) (62%), Sugar, Edible Vegetable Oil (Palm & Palmolein Oil), Semolina (Suji) (3.7%), Yeast, Natural Colour (Ins 150a), Invert Syrup, Milk Solids, Wheat Gluten. Iodised Salt, Spices (0.17%) (Cardamom), Emulsifiers [ins 471, Ins 481(i), Ins 472e], Improvers (Ins 1100(i), Ins 1102, Ins 1104, Ins 514 Antioxidant(Ins 300).",
    "brands": "famous",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/1GpEAibteywp0qRyyz_ZX5BtHrN4jXudE/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/1EWtn2Jbj-zpmEAvA1t7OjL26Y04o5bWB/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1ucpIpLF3-cneIuWuq0XWFoiBVQhcz9M4/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/1rBJekC5TtemRXqgZt05zfKMUyBASLDe5/view?usp=drive_link"
  },
  { "id" : "10",
    "name": "Harvest Gold Bombay Pav",
    "description": "Enhance the taste of your bhaji with Harvest Gold Bombay Pav. Rich in carbohydrates, proteins, calcium, sodium, potassium and energy calories, it is light and baked to perfection.",
    "price": "40",
    "tags": "Supports small business,Non organinc,Animal Cruelty-Free,Sustainable",
    "ingredients": "Wheat Flour (55%), Sugar, Wheat Protein, Yeast, Salt, Edible Vegetable Oil, Soya Flour, Permitted Emulsifier (E481 (i)), Class II Preservative (E282), Acidity Regulator (E260) and Antioxidant (E300)",
    "brands": "local",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/1dG26-kOoHZ-8BlAk67Ao9Otm_qd2WaVe/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/1KWmINXzGsR4pfLwWEqtiWa5IGSmCPz_p/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1Yo6MW0Fe3Xv_6nKmYRgq4J7O8_mku8U1/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/12SkYqLdiShKbCizyXYVhu3ZRNQWm7oSo/view?usp=drive_link"
  },
  { "id" : "11",
    "name": "Lay's West Indies Hot n Sweet Chilli Flavour Potato Chips",
    "description": "Experience an out-of-this-world blend of hot and sweet seasoning! The Lay\u2019s West Indies Hot 'n' Sweet Chilli is an exciting adventure waiting to be unfolded. The journey starts with high quality, farm-grown potatoes cooked to crispy perfection. These are then sprinkled with a dash of sugar and a pinch of Chilli for a delicious Caribbean taste. Lay\u2019s West Indies Hot 'n' Sweet Chilli is just perfect for any occasion. From the quick snack breaks at work, to the impromptu get-togethers, this snack is perfect to binge on.",
    "price": "20",
    "tags": "Supports small business,Non organinc,Animal Cruelty-Free,Sustainable",
    "ingredients": "Potato, edible vegetable oil (palmolein, rice bran oil), *seasoning (sugar, maltodextrin, iodized salt, flavour (natural and nature identical flavour substances), ~spices & condiments, flavour enhancers (627, 631), edible vegetable oil (palm, sunflower, peanut) hydrolysed vegetable protein, anticaking agent (551), cocoa solids, lactose).Contains Nut, Milk, Wheat. May contain Sulphite.*As flavouring agent. ~Contains Onion and Garlic",
    "brands": "famous",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/1L7TRKN0-0yxcNr4TX7zrhpS6300JygWt/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/1hfeTMXtUbBYLYz3t-cR3Nj6nmzqtNv_L/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1pMtBR3ypiFjk-5ZBDxIuLI-TOIX2m6lC/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/1SLP5d5MINDp94c1boNZ8ztEvS6KMrj8o/view?usp=drive_link"
  },
  { "id" : "12",
    "name": "Kurkure Masala Munch Crisps - Pack of 3",
    "description": "Kurkure Masala Munch is made from fresh rice meal, corn meal and is spiced with various condiments. As Indian and delicious as ever, this tangy snack is a perfect munch with an enticing flavour of masala.",
    "price": "54",
    "tags": "Supports small business,Non organinc,Animal Cruelty-Free,Sustainable",
    "ingredients": "Rice Meal, Edible Vegetable Oil, Corn Meal, Gram Meal, Spices & Condiments (Onion Powder, Chilli Powder, Coriander Seed Powder, Amchur Powder, Garlic Powder, Ginger Powder, Black Pepper Powder, Turmeric Powder, Spices Extract, Fenugreek Leaf Powder), Salt, Sugar, Black Salt, Tomato Powder, Citric Acid, Tartaric Acid, Dextrose, Milk Solids",
    "brands": "famous",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/1WqiNI1Z5iUa7mKoN3Knviz2qvSlRNErR/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/1w0a38Ao5Q2bQuw0JdRx3u3tpZbucqEyB/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1Ptd703gNODDPK8eImDWrJh-KPMxK2ggc/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/1UH1cW3tMDLGtNsGDbCpclTYsTnp4OaFi/view?usp=drive_link"
  },
  { "id" : "13",
    "name": "Let's Try Crunchy Soya Sticks",
    "description": "Made with 100% Groundnut oil",
    "price": "95",
    "tags": "Supports small business,Non organinc,Animal Cruelty-Free,Sustainable",
    "ingredients": "Roasted Gram Powder, Soya Powder, Rice Powder, Roasted Urad Dal Powder, Palm Oil, Tapioca Starch, lodised Salt, Nutmeg, Clove, Black Salt, Dry Mango, Coriander, Black Cumin, Peprica, Black Pepper, Ginger, Cardamom, Cinnamon, White Cumin, Tomato Paste, E330 Citric Acid & Permitted Flavours.",
    "brands": "local",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/1Cfj77LzBNmWUNjMCvswEXE2slaFY175d/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/1PX93ZDgZsOcbX796JZT5QoymVZe2psBg/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1VSggxFwOjAfGq01gjgIUu8C-kuBmJEHU/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/1AXXTxoR7KKxqre-n3NGCf9Ed4JOOOthA/view?usp=drive_link"
  },
  { "id" : "14",
    "name": "Uncle Chipps Plain Salted Potato Chips",
    "description": "Every effort is made to maintain accuracy of all information. However, actual product packaging and materials may contain more and/or different information. It is recommended not to solely rely on the information presented.",
    "price": "40",
    "tags": "Supports small business,Non organinc,Animal Cruelty-Free,Sustainable",
    "ingredients": "Potato, Edible Vegetable Oil (Palmolein,), Sunflower Oil), lodised Salt (1.5%).",
    "brands": "local",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/1DoSaW-Qh4Ys9Bm2VH49ajfMQUY9jRquy/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/1mpWB0oAs9X7K2WwgjMvljpS9WylAr4Rw/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1SZ1KgG1GBvNIDnnzqrEUw71pFpKLrUrr/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/1rZkAWxrAmonRb1PUKQLgpJjckEAAQ9kW/view?usp=drive_link"
  },
  { "id" : "15",
    "name": "Crax Corn Rings Tangy Tomato Crisps Puffs",
    "description": "This snack from Crax, is now in amazing tomato tangy flavour. Baked, non-fried and trans-fat free. snacks enriched with the goodness of corn and fibre. Pop in a handful of chips or munch them one by one. The great melt in mouth taste of these delicious and crunchy rings is enjoyed by everyone. Not to forget the exciting toy, for kids it's a bundle of joy.",
    "price": "25",
    "tags": "Supports small business,Non organinc,Animal Cruelty-Free,Sustainable",
    "ingredients": "Corn Grits (58%), Edible Vegetable Oil (Refined Palmolein Oil), *Seasoning [Sugar, lodised Salt, Corn Starch, Tomato Powder (0.98%), Chilli, Acidity Regulator (INS 330), Fennel, Anticaking Agent (INS 551), Spice Extract, Flavour Enhancers (INS 627, INS 631)], Flavour(s) (Natural & Nature Identical Flavouring Substances)",
    "brands": "famous",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/105yse_ItDyLXlmx_YzK3Pg0MUaqDmOrY/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/1k0kYmld84AU-of2ZSM_OdvE5SM3R_U5z/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1V985cUk44fJl6lfu9sRXIJNV2sSEecGW/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/1oEjVG6s87puRvwvscwRRLuKfwJboiUCQ/view?usp=drive_link"
  },
  { "id" : "16",
    "name": "Haldiram's Takatak Chatpata Masala Stick",
    "description": "Every effort is made to maintain accuracy of all information. However, actual product packaging and materials may contain more and/or different information. It is recommended not to solely rely on the information presented.",
    "price": "22",
    "tags": "Supports small business,Non organinc,Animal Cruelty-Free,Sustainable",
    "ingredients": "Rice Meal, Edible Vegetable Oil (PalmoleinOil), Corn Meal, Gram Meal, *Spices and Condiments (Red Chilli Powder (0.8%), Raw Mango Powder, Coriander Powder, Cumin Powder, Garlic Powder, Anise Powder (0.1%), Black Pepper Powder, Nutmeg Powder, Cinnamon Powder, Onion Powder, Spices Extract), Edible Common Salt, Whey Powder, Maltodextrin, Dextrose and Acidity Regulators (INS 330 & INS 296).",
    "brands": "famous",
    "category": "snacks",
    "image_front": "https://drive.google.com/file/d/1IMmhE0ebuEu6sJHnWSN5-NKiVQMgOOxB/view?usp=drive_link",
    "image_back": "https://drive.google.com/file/d/1j41tGYFb9SjOLtg_a7bA25jdXhGGdrdU/view?usp=drive_link",
    "image_nutrition": "https://drive.google.com/file/d/1MUcepb3Yc3azzfxpuA_MtSFmTDMs9VtQ/view?usp=drive_link",
    "image_ingredients": "https://drive.google.com/file/d/1VaZ1buyNyKvyUsOLfBceIMjVzlSWBpYQ/view?usp=drive_link"
  }
]

@app.route('/')
def home():
    return "Hello, this is a basic Flask server running on port 4000!"

# Products route
@app.route('/products', methods=['GET'])
def list_products():
    return jsonify(products)

@app.route('/product/<product_id>', methods=['GET'])
def get_product(product_id):

    for product in products:
        if dict(product).get("id", "") == product_id:
            return product

    return "Not Found"
 
@app.route('/get_response', methods=['GET', 'POST'])
def get_response():
    request_message = request.form.get('message')
    print('Message:', request_message)
    url_pattern = r'(https?://[^\s]+)'
    url_match = re.search(url_pattern, request_message)
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
    return output_json

@app.route('/get_image', methods=['GET', 'POST'])
def get_image():
    service = build("customsearch", "v1",
            developerKey=apikey)
    search_url = "https://www.googleapis.com/customsearch/v1"  
    params = {
        "q": searchTerm,
        "cx": cxid,
        "searchType": "image",
        "num": 2,
        "fileType": "jpg",
        "imgType": "photo",
        "key": apikey,
    }
    response = requests.get(search_url, params=params)
    results = response.json()

    image_urls = [item["link"] for item in results.get("items", [])]
    download_images(image_urls)
    return image_urls

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
