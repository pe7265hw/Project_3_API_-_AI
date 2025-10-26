import logging
from google import genai
from google.genai.types import GenerateContentConfig, Content, Part
from pydantic import BaseModel

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

"""If you do not have the gemini API key set up in your enviroment variables, uncomment lines 10 & 11 below and set it directly."""
# import os
# os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"

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
cuisine = "Italian"
diet = "healthy"
expense = "expensive"

# Pydantic model for structured recipe output
# This model defines the expected structure of the recipe data returned by the AI.
class Recipe(BaseModel):
    recipes: list[str]

def gemini_recipe_chat(cuisine, diet, expense):
    """This does not create an actual chat, instead it uses 2 separate GenerateContentConfig calls with different configurations 
    to allow for the response schema to be applied only on the 2nd turn."""

    print('Hello! I\'m your recipe assistant. Tell me what type of foods you like and I will suggest recipes that fit your health and expense choices.')
    formatted_user_input = f"Give me some {cuisine} recipes that are {diet}, make sure the price is {expense}."
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
        print(recipe_list)
    
    except Exception as e:
        print("Sorry, I couldn't understand the response. Please try again.", e)
    except ValueError as ve:
        print("The response format was incorrect:", ve)

    return recipe_list

gemini_recipe_chat(cuisine, diet, expense)


