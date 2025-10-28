import logging
from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel
import os

def system_prompt_info():

    system_prompt = """
    You are a friendly and helpful recipe assistant. Your goal is to provide users with recipes that match their desired cuisine and healthiness level as well as their expense choice.
    Follow these steps precisely:
    1.  The user will provide you with a cuisine type (e.g., Italian, Mexican, Indian) and one of three preferences for healthiness (e.g., unhealthy, somewhat healthy, or healthy) and expense (e.g., cheap, moderate, or expensive).
    2.  Based on the cuisine and preferences provided by the user, suggest 3 recipe names that fits those criteria.
    3.  You will return your responce in the exact same format as the response schema provided, with no additional text or explanation.
    Here is the response schema you must follow:
    {
    [
        "Recipe Name 1",
        "Recipe Name 2",
        "Recipe Name 3"
    ]
    }
    """
    return system_prompt

##Lines that are double commented out are for team partner to review removing, I believe we do not need them

# Pydantic model for structured recipe output
# This model defines the expected structure of the recipe data returned by the AI.
class Recipe(BaseModel):
    recipes: list[str]


def gemini_recipe_chat(cuisine, cost, nutrition):
    """This does not create an actual chat, instead it uses 2 separate GenerateContentConfig calls with different configurations 
    to allow for the response schema to be applied only on the 2nd turn."""

    #Gemini API key read and passed to client and used in response
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key) 

    # Set up logging configuration
    logging.basicConfig(level=logging.INFO)

    system_prompt = system_prompt_info()
    
    formatted_user_input = (f"Give me some {cuisine} recipes that are {nutrition}, make sure the price is {cost}.")
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=formatted_user_input,
            config=GenerateContentConfig(
                system_instruction=system_prompt,
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

# gemini_recipe_chat('curry', 'healthy', 'cheap')


