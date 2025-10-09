from api_logic import query_api as api



def main():
    key = api.retrieve_key()
    recipe_all = api.query_api_ids(key, 'vanilla cake')
    all_id = api.append_recipe_id(recipe_all)
    api.retrieve_recipes(key, all_id)

main()