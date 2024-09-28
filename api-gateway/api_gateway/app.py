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
########################### hard coded products from stagnant code #####################################



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
 


########################################################################################################

import re

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

##############################################################################################################



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
                        2. recreations
                        3.  or regular consumption for me

                        (sustainibility parameters): If the food product follows any of the following:
                        1. Organic
                        2. Sustainable: 
                        3. Supports Small Businesses
                        4. Animal Cruelty-Free: 
                        5. Lower carbon footprint

                        (#allergy alert#): flag alergens if they are related to my allergy otherwise don't flag a warning
                        (#diet type#): you need to also flag diet type match this with the input of user info and flag if it is suitable for their dietary type or restrictions(eg vegan/jain/vegetarian/keto) based on user input , answer should be in (** **) mentioning which diet it is suitable or not suitable for.
                        (#nutrient alert#): Alert if there is a higher presence of nutrients desired in low qty (fats, sugar, sodium, calories)
                        (#carbon footprint info#): give info about carbon footprint of the product and also give info about the parent company of the product.
                        Your final answer should only contain tags among one option of each category based on product nutrition analysis.
                        If the answer is None just drop that category output.
                        -Finally if the 4 out of 6 categories are suitable for this user add that as highly recommended product.
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









if __name__ == "__main__":
    app.run(host = "0.0.0.0",port=8088,debug=True)
