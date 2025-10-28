import requests
import os
from thefuzz import fuzz
from thefuzz import process

def retrieve_spoonacular_key():
        key = os.environ.get('SPOONACULAR_KEY')
        return key


def check_for_entries(spoonacular_data_input):
    """Validation for input that does not return a result
    :param spoonacular_data_input: an indidular return from spoonacular based on a recipe given by gemini"""
    recipe_results = spoonacular_data_input['results']
    if recipe_results != []:
        return True
    else:
        return False
       
            

def query_spoonacular_search(spoonacular_api_key_input, gemini_provided_recipe_name_input):
    """Retrieves data from API based on user input string
    :param key_input: environment variable, called from retrieve_key()
    :param name_input: input of recipe name that will be queried by the API
    :returns: the full json query for the titleMatch call to API"""
    try:

        url = 'https://api.spoonacular.com/recipes/complexSearch?'
        query = {'titleMatch': gemini_provided_recipe_name_input, 'apiKey': spoonacular_api_key_input}

        data = requests.get(url, params=query, timeout=10).json()
        recipe_results = data['results']
        return recipe_results
    
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


def pick_id_from_spoonacular_search(all_spoonacular_search_information, gemini_provided_recipe_name_input):
        """Uses TheFuzz to compare the user input string against the recipe titles returned by Spoonacular
        the highest percentage return is returned as the ID to be used to retrieve the full recipe information. If the
        highest match is lower than 40, nothing will be returned, may need to be raised if matches are not same as title
        :param api_data_input: Full dictionary of JSON data retrieved from API using titleMatch call
        :returns: List of recipe ID to call Get Recipe Information"""

        spoonacular_search_id_user_recipe_similarity_score = {}

        for result in all_spoonacular_search_information:
           #extracts the recipe name and ID from returned json
           spoonacular_recipe_name = result['title']
           recipe_id = result['id']
           
           #assigns a score based on similarity between user input and recipe name given by Spoonacular
           similarity_score = fuzz.token_set_ratio(gemini_provided_recipe_name_input, spoonacular_recipe_name)

           #the recipe id is used as the key and the score as the value in a dictionary
           spoonacular_search_id_user_recipe_similarity_score[recipe_id] = similarity_score

        #if there are any scores
        if spoonacular_search_id_user_recipe_similarity_score:
            #the ID of the closest match based on the value (score value set by fuzz) is returned
            closest_match_recipe_id = max(spoonacular_search_id_user_recipe_similarity_score, key=spoonacular_search_id_user_recipe_similarity_score.get)
            highest_fuzz_match = max(spoonacular_search_id_user_recipe_similarity_score.values())
            if highest_fuzz_match >= 40 :
                return closest_match_recipe_id
            else:
                return None
        else:
            #no matches NONE is returned so rest of code is skipped in function call
            return None

           
        
def spoonacular_get_recipe_information(spoonacular_key_input, spoonacular_recipe_search_id_input):
    """Retrieves the recipes based on list of id and formatted for workable output
    This will need to change to alter output to JSON or objects
    :param key_input: environment variable, called from retrieve_key()
    :param id_input: id returned from parse_api_return"""   
    
    try:

        url = f'https://api.spoonacular.com/recipes/{spoonacular_recipe_search_id_input}/information?'
        query = {'includeNutrition': 'false', 'addWinePairing': 'false', 'addTastedata': 'false', 
                    'apiKey': spoonacular_key_input}
            
        recipe_data = requests.get(url, params=query, timeout=10).json()

        return recipe_data

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

def extract_recipe_information(recipe_input):
    recipe_information = {}

    merge_dictionary = {}
    
    recipe_name = recipe_input['title']
    cooking_time = recipe_input['readyInMinutes']
    serving_amount = recipe_input['servings']
    recipe_credit = recipe_input['creditsText']
    recipe_url = recipe_input['sourceUrl'] 

    recipe_stats = {'recipe_name': recipe_name, 'cooking_time_minutes': cooking_time, 'serving_amount': serving_amount,
                    'recipe_credit': recipe_credit, 'url': recipe_url}
    
    #Pulls information from requests section of dictionary
    recipe_instructions = recipe_input['instructions']
    recipe_instructions_clean = recipe_instructions.replace('<ol>', "").replace('<li>',"").replace('</ol>', "").replace('</li>',"")

    recipe_image = recipe_input['image']

    #adds recipe stats first to dictionary
    recipe_information['recipe_stats'] = recipe_stats

    recipe_information['instructions'] = recipe_instructions_clean

    #shortened for ease of reference
    ingredients = recipe_input['extendedIngredients']

    for i in range(len(ingredients)):
        merge_dictionary[i]=[ingredients[i]['name'], ingredients[i]['amount'],
                                 ingredients[i]['unit']]
        
    recipe_information['ingredients'] = merge_dictionary

    recipe_information['picture'] = recipe_image

    return recipe_information


"""
Example of recipe_information return
    recipe_information = {
                          {recipe_stats: {'recipe_name': 'Tortellini In Brodo', 'cooking_time_minutes': 45,
                                          'serving_amount': 6, 'recipe_credit': 'Foodista.com – The Cooking 
                                           Encyclopedia Everyone Can Edit', 
                                          'url': 'https://www.foodista.com/recipe/RPG7M62J/tortellini-in-brodo'}},

                           {'instructions': 'Heat the stock to a boil and 
                                            cook the tortellini. Ladle into bowls, squeeze in lemon 
                                            and stir. Grate cheese and zest on top, and add some 
                                            freshly ground salt and pepper. Serve immediately.'}
                           
                           {{'ingredients': 0: ['chicken stock', 2.0, 'cups'],
                                            1: ['lemon juice', 1.0, 'teaspoon'], 
                                            2: ['lemon zest', 1.0, 'teaspoon'], 
                                            3: ['parmigiano-reggiano', 1.0, 'teaspoon'], 
                                            4: ['salt and pepper', 6.0, 'servings'], 
                                            5: ['tortellini', 0.75, 'cup']}}
                                            
                            {{'picture': 'https://img.spoonacular.com/recipes/634900-556x370.jpg' }}"""


def retrieve_recipe_information(gemini_recipe_names_input):
    """Used for function calls in app.py
    :param recipe_names_input: a list of recipes provided by Gemin """
    spoonacular_key = retrieve_spoonacular_key() #Reads the environment variable

    recipes = []
    
    for gemini_recipe in gemini_recipe_names_input: #For each recipe name provided by Gemini AI
        spoonacular_search_hits = query_spoonacular_search(spoonacular_key, gemini_recipe) #Spoonacular titleMatch Recipe Search is done to retrieve recipes that match
        if spoonacular_search_hits: # if any results are found
            chosen_id = pick_id_from_spoonacular_search(spoonacular_search_hits, gemini_recipe) # The ID with the higest match to the users input using The Fuzz dependency is returned
            if chosen_id: #If any suitable matches exist
                recipe_information = spoonacular_get_recipe_information(spoonacular_key, chosen_id) #Spoonacular Get Recipe Information Search by ID is done using selected ID
                extracted_recipe_information = extract_recipe_information(recipe_information) #Returned JSON is parsed to return information that will be displayed to the user
                recipes.append(extracted_recipe_information) #This information is appended to a main dictionary that contains each recipe that will then be passed to Flask Framework

    return recipes