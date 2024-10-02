# GenAI-Google--Hack-24
# ConsumeWisely

## About
ConsumeWisely empowers consumers to make informed choices about packaged food by providing instant, accurate nutritional insights. It decodes labels, analyzes ingredients, and verifies health claims, helping users understand how products fit their goals (e.g., weight loss, allergies).

This AI-powered platform simplifies label reading and empowers healthier choices by analyzing ingredients, verifying claims, and offering personalized insights.

At ConsumeWisely, we leverage Generative AI to automate the collection of data from packaged food products, providing you with instant, reliable insights. From understanding the ingredients to the brand's nutritional claims, our AI-driven product catalog helps you make informed as well as easy non-cluttered decisions about the foods you consume.

## Features

### 1. Quick AI Scan
Provides complete product details including:
- Product category
- Product description
- Brief on taste
- Allergies and cross-contamination allergens
- Sustainability assessment based on global rules (organics, reusable packaging, animal cruelty-free, etc.)
- Harmful or beneficial nutrients
- Diet types (keto/vegan/vegetarian/cholesterol-free/sugar-free, etc.)
- Recent news about the product
- Per serving ingredients and nutrients
- False claims check

### 2. Personalized Consumption Analysis
Based on user's physical attributes and health goals:
- Recommended consumption frequency based on weight goals
- Eating habits analysis
- Consumption and allergy alerts
- Diet suitability check
- Carbon footprint assessment of product and company

### 3. Recipe Recommendations
- Tailored recipes based on user's diet plan and requirements
- Suggestions incorporating current product choices

### 4. Dynamic Product Catalog
- Exhaustive and continuously updated catalog
- End-to-end information on food products across the internet

### 5. Intelligent Chatbot
- Assists with multi-modal inputs
- Enables scanning of physical products

### 6. Multilingual Support
- Allows users to navigate the website in their preferred language

### Steps to setup project

### Prerequisites
- Node.js and npm (for React)
- Python 3.x (for the backend)
- Git (for cloning the repository)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/consumewisely.git
cd consumewisely
```
### Step 2: Install all requirements
```bash
pip install -r requirements.txt
```

### Step 4: Starting backend server
```bash
cd src
cd api_gateway
```

```bash
python app.py
```
### Step 5: Starting frontend server
```bash
cd frontend
```
```bash
npm install
```
```bash
npm start
```
Consume Wisely helps you make the right choice for your product purchase where you can know the exact product that best suits your diet and health.

- The list_products API basically retrives all the products available in the Firestore and display it in the UI.
  
- In the check_product_and_web_search API when the customer searches for a product it first search for the exact product in the Firestore Database so that the number of direct api calls for the Gemini model is reduced. The Firestore DB where a list of already searched products are available only if the product is not found in the Data Base it goes to Google Vertex AI search using grounding Tools for retriving the products ingredients information and then the product name is passed to the custom search api where the custom search api is used to retrive product images from the custom domain like amazon,big basket. finally all these details like product name, ingredients from the vertex ai search is passed to the Gemini Flash 1.5 model where we are categorizing the product based on their allergens,diet suitability,nutritional benefits harms,sustainibility factor.

- The chat_bot API basically expects an image input after getting the image it converts them into bytes 64 and passed into the Gemini Flash 1.5 Model the prompt template is structure to analyze the image and categorize the product on few categories like how often then consume this product is it safe for kids, elders to consume.


- The list_products API basically retrives all the products available in the Firestore and display it in the UI.
  
- In the check_product_and_web_search API when the customer searches for a product it first search for the exact product in the Firestore Database so that the number of direct api calls for the Gemini model is reduced. The Firestore DB where a list of already searched products are available only if the product is not found in the Data Base it goes to Google Vertex AI search using grounding Tools for retriving the products ingredients information and then the product name is passed to the custom search api where the custom search api is used to retrive product images from the custom domain like amazon,big basket. finally all these details like product name, ingredients from the vertex ai search is passed to the Gemini Flash 1.5 model where we are categorizing the product based on their allergens,diet suitability,nutritional benefits harms,sustainibility factor.
