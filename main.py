import requests
import os
from pprint import pprint
import json

def retrieve_key():
    """Retrieves API key"""
    key = os.environ.get('SPOONACULAR_KEY')
    return key

def retrieve_recipe_ids(key_input, name_input):
    """Retrieves all recipe IDs from API based on recipe name provided by AI or string for testing"""
    url = 'https://api.spoonacular.com/recipes/complexSearch?'
    query = {'titleMatch': name_input, 'apiKey': key_input}

    data = requests.get(url, params=query).json()
    recipe_results = data['results']

    all_recipe_id = []

    #each id is retrieved from dictionary and appended to list then returned
    for id in recipe_results:
        recipe_id = id['id']
        all_recipe_id.append(recipe_id)
    return all_recipe_id

#final output type will be revised
def retrieve_recipes(key_input, id_input):
    """Retrieves the recipes based on list of id and formatted for workable output"""

    #Clears the txt file for new text
    file_name = 'recipes_output.txt'
    open(file_name, 'w').close()

    #each id in list is queried against API and json is appended to txt for output
    for id in id_input:
        url = f'https://api.spoonacular.com/recipes/{id}/information?'
        query = {'includeNutrition': 'false', 'addWinePairing': 'false', 'addTastedata': 'false', 
                'apiKey': key_input}

        data = requests.get(url, params=query).json()

        #writes json data to txt as it is too long to view in terminal
        with open(file_name, 'a') as file:
            json.dump(data, file, indent=4)

def main():
    key = retrieve_key()
    food_id_all = retrieve_recipe_ids(key, 'vanilla cake')
    retrieve_recipes(key, food_id_all)

main()