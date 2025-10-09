import requests
import os
from pprint import pprint
import json
from api_logic import query_api as api



def main():
    key = retrieve_key()
    food_id_all = retrieve_recipe_ids(key, 'vanilla cake')
    retrieve_recipes(key, food_id_all)

main()