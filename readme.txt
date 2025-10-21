***This readme is a work in progress and may be ammended in the future***

Our app will ask the user for a country/region/ethnicity of food they would like recipes from they
will also be asked for any dietary restrictions or considerations that they would like the app to
take into consideration. 

The app will then query AI (TBD) to find 3-5 to recipes and generate a list
of food items that may be relavant specific to that country/region/ethnicity to the users dietary 
consideration. 

The recipe names will be queried in the Spoonacular API first by searching the name using the 
titleMatch parameter then using the returned ID to find the recipe ingredients with the 
Get Ingredients parameter.

Once this is returned the list of dietary ingredients, given by AI will be searched against the recipes 
ingredients and if anything matches Spoonaculars Get Ingredients Substitute will be used to find
replacement ingredients.

(For all examples add own apiKey)
Example of Spoonacular API return with titleMatch:
https://api.spoonacular.com/recipes/complexSearch?titleMatch=bolognese&apiKey=

Example of Spoonacular API return with Get Recipe Information:
https://api.spoonacular.com/recipes/634900/information?includeNutrition=false&apiKey=

