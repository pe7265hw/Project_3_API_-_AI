import requests
import os


def retrieve_key():
    """Retrieves API key"""
    key = os.environ.get('SPOONACULAR_KEY')
    return key

def retrieve_recipe_ID(key_input, name_input):
    """Retrieves recipe ID from API based on recipe name provided by AI"""
    url = 'https://api.spoonacular.com/recipes/complexSearch?'
    query = {'titleMatch': name_input, 'apiKey': key_input}
   
def main():
    retrieve_key()

main()