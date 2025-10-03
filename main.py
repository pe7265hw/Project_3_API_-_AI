import requests
import os
from pprint import pprint

def retrieve_key():
    """Retrieves API key"""
    key = os.environ.get('SPOONACULAR_KEY')
    return key

def retrieve_recipe_ID(key_input, name_input):
    """Retrieves recipe ID from API based on recipe name provided by AI"""
    url = 'https://api.spoonacular.com/recipes/complexSearch?'
    query = {'titleMatch': name_input, 'apiKey': key_input}

    data = requests.get(url, params=query).json()
    return data
   
def main():
    key = retrieve_key()
    food_id = retrieve_recipe_ID(key, 'vanilla cake')
    pprint(food_id)

main()