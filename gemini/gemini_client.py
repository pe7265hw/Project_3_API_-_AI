import logging
from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel
import os
import requests
import json

 # Set up logging configuration
logging.basicConfig(level=logging.INFO)

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

    # Create a gemini client object
    client = genai.Client(api_key=api_key) 
    
    formatted_user_input = (f"Give me some {cuisine} recipes that are {nutrition}, make sure the price is {cost}.")
    try:
        # Initialize a blank list to store recipes returned by gemini
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
        # Parse the gemini response to get the contents of the list
        recipe_list = response.parsed.recipes

        # Log the response from gemini
        logging.info(recipe_list)
    
    except ValueError as e:
        logging.error(f'Value error occured: {e}')
    except Exception as e:
        logging.error(f'An exception occured: {e}')
    except requests.exceptions.ConnectionError as e:
        logging.error(f'A connection error occured with the Gemini API: {e}')
    except json.JSONDecodeError as e:
        logging.error(f'A json decoding error occured {e}')

    return recipe_list

# Uncomment the lines below to test the gemini_recipe_chat function directly
# recipe_list = gemini_recipe_chat('curry', 'healthy', 'cheap')
# print(recipe_list)


