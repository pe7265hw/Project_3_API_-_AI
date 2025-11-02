from api_logic import query_api as api

import gemini.gemini_client as g_client

def get_recipes():
    cuisine = 'spaghetti'
    cost = 'cheap'
    nutrition = 'healthy'

    recipe_names = g_client.gemini_recipe_chat(cuisine, cost, nutrition)

    recipes = api.retrieve_recipe_information(recipe_names)

    if recipes:
        thing = 0

    get_recipes()

def main():
    get_recipes()

main()
