# GenAI-Google--Hack-24

Consume Wisely helps you make the right choice for your product purchase where you can know the exact product that best suits your diet and health.

- The list_products API basically retrives all the products available in the Firestore and display it in the UI.
  
- In the check_product_and_web_search API when the customer searches for a product it first search for the exact product in the Firestore Database so that the number of direct api calls for the Gemini model is reduced. The Firestore DB where a list of already searched products are available only if the product is not found in the Data Base it goes to Google Vertex AI search using grounding Tools for retriving the products ingredients information and then the product name is passed to the custom search api where the custom search api is used to retrive product images from the custom domain like amazon,big basket. finally all these details like product name, ingredients from the vertex ai search is passed to the Gemini Flash 1.5 model where we are categorizing the product based on their allergens,diet suitability,nutritional benefits harms,sustainibility factor.

- The chat_bot API basically expects an image input after getting the image it converts them into bytes 64 and passed into the Gemini Flash 1.5 Model the prompt template is structure to analyze the image and categorize the product on few categories like how often then consume this product is it safe for kids, elders to consume.
