from flask import Flask, render_template, request
import gemini_client as g_client
from api_logic import query_api as api

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/get_recipes')
def get_recipes():
    cuisine = request.args.get('recipe')
    cost = request.args.get('diet')
    nutrition = request.args.get('recipe')

    recipe_names = g_client.gemini_recipe_chat(cuisine, cost, nutrition)

    key = api.retrieve_key()


    recipes = []
    
    for item in recipe_names:
        recipe_all, recipe_name = api.query_api(key, item)
        if recipe_all:
            chosen_id = api.parse_api_return(recipe_all, recipe_name)
            if chosen_id:
                recipe_information = api.retrieve_recipe(key, chosen_id)
                extracted_recipe_information = api.extract_recipe_information(recipe_information)
                recipes.append(extracted_recipe_information)

    if recipes:
        return render_template('food.html', recipes=recipes)

    else:
        return render_template('no_results.html',cuisine=cuisine, cost=cost, nutrition=nutrition)
    


    
if __name__ == '__main__':
    app.run()
