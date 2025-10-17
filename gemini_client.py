from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel

system_prompt = """
You are a friendly and helpful recipe assistant. Your goal is to provide users with recipes that match their desired cuisine and dietary needs.

Follow these steps precisely:
1.  When the user first specifies a country or region, DO NOT provide recipes immediately.
2.  Instead, your first response must ALWAYS be to ask them if they have any food allergies or dietary restrictions.
3.  Once the user responds with their restrictions (or says they have none), then and only then, provide 3 distinct NAMES ONLY of
    recipes that are unique to the specific region or country that the user specified and ENSURE they meet the dietary 
    needs if any were specified in step 2.
"""

# Create a Pydantic model to give the AI response a structured format
# This makes the AI response more predictable and easier to parse
class Recipe(BaseModel):
    name: str
    dietary_restrictions: list[str] 

def gemini_recipe_chat():
    """Creates a chat with Gemini and handles user interaction for recipe suggestions."""
    
    # Initialize the Gemini client and create a chat session with the system prompt
    client = genai.Client()
    chat = client.chats.create(
        model='gemini-2.5-flash',
        config=GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type='application/json',
            response_schema=Recipe
        )
    )

    print('Hello! I\'m your recipe assistant. Give me a country or region and I will give you some popular recipes from that area.')

    is_first_interaction = True

    while True:

        if is_first_interaction:
            prompt = input('> ')
            response = chat.send_message(prompt)
            print(response.text)
            is_first_interaction = False
            # Parse the AI response into the Recipe model
        try:
            prompt = input('> ')
            response = chat.send_message(prompt)
            recipe = response.parsed
            print(recipe)
        except Exception as e:
            print("Sorry, I couldn't understand the response. Please try again.")
        
gemini_recipe_chat()