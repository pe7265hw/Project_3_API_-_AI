import logging
from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel
import os

# Open the gemini_system_instructions.txt file and save it as a variable to pass to the gemini response
with open('gemini/gemini_system_instructions.txt', 'r') as file:
    gemini_instructions = file.read()

# Pydantic model for structured recipe output
# This model defines the expected structure of the recipe data returned by the AI.
class Recipe(BaseModel):
    recipes: list[str]


def gemini_recipe_chat(cuisine, cost, nutrition):
    """Gemini interaction function. The function takes in cuisine, cost, and nutrition parameters and then uses those in a formatted
       string prompt which is used for the user input (contents) in the gemini response configuration. The Recipe pydantic model is
       used to ensure the response is correctly structured as a list of strings."""

    #Gemini API key read and passed to client and used in response
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key) 

    # Set up logging configuration
    logging.basicConfig(level=logging.INFO)
    
    formatted_user_input = (f"Give me some {cuisine} recipes that are {nutrition}, make sure the price is {cost}.")
    try:
        recipe_list = []

        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=formatted_user_input,
            config=GenerateContentConfig(
                system_instruction=gemini_instructions,
                response_mime_type="application/json",
                response_schema=Recipe
            )
        )
        recipe_list = response.parsed.recipes
        # print(recipe_list)
    
    except Exception as e:
        print("Sorry, I couldn't understand the response. Please try again.", e)
    except ValueError as ve:
        print("The response format was incorrect:", ve)

    return recipe_list

# Uncomment the lines below to test the gemini_recipe_chat function directly
# recipe_list = gemini_recipe_chat('curry', 'healthy', 'cheap')
# print(recipe_list)


