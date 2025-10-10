import requests
import os
import json

def retrieve_key():
    """Retrieves API key"""
    key = os.environ.get('SPOONACULAR_KEY')
    return key

def query_api_ids(key_input, name_input):
    """Retrieves data from API based on user input string
    :param key_input: environment variable, called from retrieve_key()
    :param name_input: input of recipe name that will be queried by the API
    :returns: the full json query for the titleMatch call to API"""
    try:
        url = 'https://api.spoonacular.com/recipes/complexSearch?'
        query = {'titleMatch': name_input, 'apiKey': key_input}

        data = requests.get(url, params=query, timeout=10).json()
        return data
    except requests.exceptions.Timeout:
        print("Error: The API request timed out.")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Check network connection or URL.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        # Catch any other requests-related exceptions not specifically handled
        print(f"Error: An unexpected requests error occurred: {e}")
        return None
    except ValueError:
        # Catches errors if the response content is not valid JSON
        print("Error: API response is not valid JSON.")
        return None
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"Error: An unhandled exception occurred: {e}")
        return None
    
def append_recipe_id(api_data_input):
        """Takes an individual recipe id from API return and appends it to a list to later use to
        query Get Recipe Information
        :param api_data_input: Full dictionary of JSON data retrieved from API using titleMatch call
        :returns: List of recipe ID to call Get Recipe Information"""
        recipe_results = api_data_input['results']

        all_recipe_id = []

        #each id is retrieved from dictionary and appended to list then returned
        for id in recipe_results:
            recipe_id = id['id']
            all_recipe_id.append(recipe_id)
        return all_recipe_id
        
def retrieve_recipes(key_input, id_input):
    """Retrieves the recipes based on list of id and formatted for workable output
    This will need to change to alter output to JSON or objects
    :param key_input: environment variable, called from retrieve_key()
    :param id_input: list of id's returned from append_recipe_id"""   
    #Clears the txt file for new text
    # file_name = 'recipes_output.txt'
    # open(file_name, 'w').close()

    try:
        #each id in list is queried against API and json is appended to txt for output
        for id in id_input:
            url = f'https://api.spoonacular.com/recipes/{id}/information?'
            query = {'includeNutrition': 'false', 'addWinePairing': 'false', 'addTastedata': 'false', 
                    'apiKey': key_input}

            data = requests.get(url, params=query).json()

            parse_recipe_info(data)

            # #writes json data to txt as it is too long to view in terminal
            # with open(file_name, 'a') as file:
            #     json.dump(data, file, indent=4)
    except requests.exceptions.Timeout:
        print("Error: The API request timed out.")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Check network connection or URL.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        # Catch any other requests-related exceptions not specifically handled
        print(f"Error: An unexpected requests error occurred: {e}")
        return None
    except ValueError:
        # Catches errors if the response content is not valid JSON
        print("Error: API response is not valid JSON.")
        return None
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"Error: An unhandled exception occurred: {e}")
        return None
    
def parse_recipe_info(recipe_request_input):
    recipe_name = recipe_request_input['title']
    cooking_time = recipe_request_input['readyInMinutes']
    serving_amount = recipe_request_input['servings']
    recipe_credit = recipe_request_input['creditsText']
    recipe_url = recipe_request_input['sourceUrl'] 

    recipe_info = [recipe_name, cooking_time, serving_amount, recipe_credit, recipe_url]

    for i in range(len(recipe_request_input['extendedIngredients'])):
        recipe_ingredients = {}