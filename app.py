from flask import Flask, render_template, request
import requests  # NOT the same as requests 
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/get_recipes')
def get_recipes():
    cuisine = request.args.get('cuisine')
    diet = request.args.get('diet')
    recipe = request.args.get('recipe')

    if not cuisine:
        return ' Please enter  a cuisine or region.'

    
    
        
    api_key = os.environ.get('SPOONACULAR_API_KEY')

   

    url = "https://api.spoonacular.com/recipes/complexSearch?"


    params_search = { 'apiKey':  api_key, 'number': 10}
    if cuisine:
        params_search['cuisine'] = cuisine
    if diet:
        params_search['diet'] = diet
    if recipe:
        params_search['query'] = recipe


        
    try:
        # Make the API request
        response = requests.get(url, params=params_search)
        response.raise_for_status()  # raise exception for HTTP errors
        data_search = response.json()
        print("API response:", data_search)
    except Exception as e:
        return f"Error making API request: {e}"


    recipes = []
    if 'results' in data_search and data_search['results']:
        for recipe in data_search['results']:
            recipe_info = {
                'title': recipe['title'],
                
                'id': recipe['id']
            }
            recipes.append(recipe_info)
    else:
        return f'No recipes found for {cuisine} ({diet}). Try a different search.'

   

    return render_template('food.html', cuisine=cuisine, diet=diet, recipes=recipes)


    
if __name__ == '__main__':
    app.run()