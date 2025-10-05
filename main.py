import requests
import os
from pprint import pprint

def retrieve_key():
    """Retrieves API key"""
    key = os.environ.get('SPOONACULAR_KEY')
    return key

def retrieve_recipe_ids(key_input, name_input):
    """Retrieves all recipe IDs from API based on recipe name provided by AI"""
    url = 'https://api.spoonacular.com/recipes/complexSearch?'
    query = {'titleMatch': name_input, 'apiKey': key_input}

    data = requests.get(url, params=query).json()
    recipe_results = data['results']

    all_recipe_id = []

    for id in recipe_results:
        recipe_id = id['id']
        all_recipe_id.append(recipe_id)
    return all_recipe_id

#determine if what output needs to be
def retrieve_recipes(key_input, id_input):
    """Retrieves the recipes based on list of id and formatted for workable output"""


def main():
    key = retrieve_key()
    food_id_all = retrieve_recipe_ids(key, 'vanilla cake')
    

main()