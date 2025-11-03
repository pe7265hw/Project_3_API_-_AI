from flask import Flask, render_template, request
import gemini.gemini_client as gemini_client
from spoonacular_logic import query_spoonacular as spoonacular

#####################################################################################
# BEFORE RUNNING APP CHANGE OPEN STATEMENT AT TOP OF gemini_client.py
#####################################################################################


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/get_recipes')
def get_recipes():
    over_api_call = 0 # will change in API function calls if user has hit limit
    recipes = [] # final processed recipes returned by Spoonacular

    cuisine = request.args.get('cuisine')
    cost = request.args.get('cost')
    nutrition = request.args.get('nutrition')

    recipe_names = gemini_client.gemini_recipe_chat(cuisine, cost, nutrition)

    if recipe_names != []:

        over_api_call, recipes = spoonacular.retrieve_recipe_information(recipe_names)

    if over_api_call > 0 or recipe_names == []:
        return render_template('unexpected_results.html', recipe_names=recipe_names) #handles no results from Gemini or maxed out API calls

    if len(recipes) == 0:
        return render_template('no_results.html',cuisine=cuisine, cost=cost, nutrition=nutrition) #handles no returns from Spoonacular

    else:
        return render_template('food.html', recipes=recipes) # if all results are successfully returned they are displayed here
    

            


    
if __name__ == '__main__':
    app.run()


    # cuisine = 'chicken'
    # cost = 'cheap'
    # nutrition = 'healthy'

    # cuisine = request.args.get('recipe')
    # cost = request.args.get('diet')
    # nutrition = request.args.get('recipe')