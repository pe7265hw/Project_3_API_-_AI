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

# Pydantic model for structured recipe output
# This model defines the expected structure of the recipe data returned by the AI.
class Recipe(BaseModel):
    name: list[str]
    dietary_restrictions: list[str] 

def gemini_recipe_chat():
    """This does not create a actual chat, instead it uses 2 separate send_message calls with different configurations 
    to allow for the response schema to be applied only on the 2nd turn."""
    
    client = genai.Client()
    model = "gemini-2.5-flash"
    # Configuration for the first response (no schema) just text response
    default_config = GenerateContentConfig(
            system_instruction=system_prompt
    )

    # Response schema configuration to be used on the for the second response 
    schema_config = GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type='application/json',
            response_schema=Recipe
        )

    print('Hello! I\'m your recipe assistant. Give me a country or region and I will give you some popular recipes from that area.')

    is_first_interaction = True

    while True:

        if is_first_interaction:
            config = default_config
        else:
            config = schema_config

        if is_first_interaction:
            prompt = input('> ')
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=config
            )
            print(response.text)
            is_first_interaction = False
            continue
        try:
            prompt = input('> ')
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=config
            )
            print(response.parsed)
            
        except Exception as e:
            print("Sorry, I couldn't understand the response. Please try again.")
        
gemini_recipe_chat()