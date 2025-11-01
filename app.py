from flask import Flask, render_template, request
import gemini_client as g_client
from api_logic import query_api as api


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/get_recipes')
def get_recipes():
    cuisine = request.args.get('cuisine')
    cost = request.args.get('cost')
    nutrition = request.args.get('nutrition')

    recipe_names = g_client.gemini_recipe_chat(cuisine, cost, nutrition)

    over_api_call, recipes = api.retrieve_recipe_information(recipe_names)

    if over_api_call > 0:
        return render_template('over_api_call')

    if len(recipes) == 0:
        return render_template('no_results.html',cuisine=cuisine, cost=cost, nutrition=nutrition)

    else:
        return render_template('food.html', recipes=recipes)
    

            


    
if __name__ == '__main__':
    app.run()


    # cuisine = 'chicken'
    # cost = 'cheap'
    # nutrition = 'healthy'

    # cuisine = request.args.get('recipe')
    # cost = request.args.get('diet')
    # nutrition = request.args.get('recipe')