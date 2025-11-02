***This readme is a work in progress and may be ammended in the future***

Our app will ask the user for what type of food, how healthy and the cost of the food they would like.

The app will then query Gemini to find a list of strings containing 3-5 keywords each that will be used to find recipes
on Spoonacular.

Spoonacular will be searched using the query search to return a json response of recipe titles with an ID (containing other information as well).
These titles will be compared against the keywords returned by Gemini using TheFuzz to return the recipe that has the highest percentage match.

These recipes will be further processed to extract relevant information such as the recipe name, servings, cooking time and ingredients to be displayed
for the user. If no matches are found a different page will be displayed telling the user this and directing them to the homepage.

(For all examples add own apiKey)
Example of Spoonacular API return with titleMatch:
https://api.spoonacular.com/recipes/complexSearch?query=bolognese&apiKey=

Example of Spoonacular API return with Get Recipe Information:
https://api.spoonacular.com/recipes/634900/information?includeNutrition=false&apiKey=


***A note on installing the dependency TheFuzz***
If you are having trouble getting your project to recognize TheFuzz as an import statement, make sure your interpreter is using the python.exe in your virtual environment
In this project it would be: venv/Scripts/python.exe