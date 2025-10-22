import requests
import os
import json
import re

def retrieve_key():
        key = os.environ.get('SPOONACULAR_KEY')
        return key

#Before append_recipe_id can work with the results there will need to be validation of what was returned
#check_for_entries can validate whether something is returned but if it is nothing then we need to decide what to return the user
#Do we still return results if 2/3 are hits? 1/3? Or do we want 3/3 in order to return results?
#Do we ask the user to provide another country/location etc or do we ask the AI for different recipes?


def check_for_entries(api_data_input):
    """Validation for input that does not return a result"""
    recipe_results = api_data_input['results']
    if recipe_results != []:
        return True
    else:
        return False
       
            

def query_api(key_input, name_input):
    """Retrieves data from API based on user input string
    :param key_input: environment variable, called from retrieve_key()
    :param name_input: input of recipe name that will be queried by the API
    :returns: the full json query for the titleMatch call to API"""
    try:
        url = 'https://api.spoonacular.com/recipes/complexSearch?'
        query = {'titleMatch': name_input, 'apiKey': key_input}

        data = requests.get(url, params=query, timeout=10).json()
        recipe_results = data['results']
        return recipe_results, name_input
    
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
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"Error: An unhandled exception occurred: {e}")
        return None


def parse_api_return(api_data_input, recipe_name_input):
        """Performs a regex search to ensure title is in recipe name then if so searches for middle length
         recipe name and returns that id
        to a list to be used by retrieve_recipes
        :param api_data_input: Full dictionary of JSON data retrieved from API using titleMatch call
        :returns: List of recipe ID to call Get Recipe Information"""


        recipe_parse_information = {}

        for item in api_data_input:
            text = item['title']

            #regex is used to see if desired title appears in the recipe name, if yes ID appended to list
            match_object = re.search(recipe_name_input.lower(), text.lower())

            #if regex finds match, dictionary entry of id and length of name added to dictionary
            if match_object:
                recipe_parse_information[item['id']] = len(text)

        #the id attributed to the shortest recipe name is selected, this is done because re.search only selects
        #recipes that match the exact input string, so the shortest match is closest to the exact search string
        #first instance of match is taken in the event two recipe names are the same length
        shortest_recipe_id = min(recipe_parse_information, key=recipe_parse_information.get)

        return shortest_recipe_id
        
def retrieve_recipe(key_input, id_input):
    """Retrieves the recipes based on list of id and formatted for workable output
    This will need to change to alter output to JSON or objects
    :param key_input: environment variable, called from retrieve_key()
    :param id_input: id returned from parse_api_return"""   
    
    #Clears the txt file for new text
    # file_name = 'recipes_output.txt'
    # open(file_name, 'w').close()

    try:

        url = f'https://api.spoonacular.com/recipes/{id_input}/information?'
        query = {'includeNutrition': 'false', 'addWinePairing': 'false', 'addTastedata': 'false', 
                    'apiKey': key_input}
            
        data = requests.get(url, params=query, timeout=10).json()

        # #writes json data to txt as it is too long to view in terminal
        # with open(file_name, 'a') as file:
        #     json.dump(data, file, indent=4)

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
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"Error: An unhandled exception occurred: {e}")
        return None

def extract_recipe_information(recipe_request_input):
    recipe_information = {}
    
    recipe_name = recipe_request_input['title']
    cooking_time = recipe_request_input['readyInMinutes']
    serving_amount = recipe_request_input['servings']
    recipe_credit = recipe_request_input['creditsText']
    recipe_url = recipe_request_input['sourceUrl'] 

    recipe_stats = {'recipe_name': recipe_name, 'cooking_time_minutes': cooking_time, 'serving_amount': serving_amount,
                    'recipe_credit': recipe_credit, 'url': recipe_url}
    
    #Pulls information from requests section of dictionary
    # eventually trim <ol><li> here!!!!!!!    
    recipe_instructions = recipe_request_input['instructions']

    #adds recipe stats first to dictionary
    recipe_information['recipe_stats'] = recipe_stats

    recipe_information['instructions'] = recipe_instructions
     
    #shortened for ease of reference
    ingredients = recipe_request_input['extendedIngredients']

    for i in range(len(ingredients)):
        recipe_information[i] = [ingredients[i]['name'], ingredients[i]['amount'],
                                 ingredients[i]['unit']]

    return recipe_information
