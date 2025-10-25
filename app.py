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




    recipes = []
    if 'results' in data_search and data_search['results']:
        for recipe in data_search['results']:
            recipe_info = {
                'title': recipe['title'],
                'images': recipe.get('image', ''),
                'id': recipe['id']
            }
            recipes.append(recipe_info)
    else:
        return f'No recipes found for {cuisine} ({diet}). Try a different search.'

   

    return render_template('food.html', cuisine=cuisine, diet=diet, recipes=recipes)


    
if __name__ == '__main__':
    app.run()