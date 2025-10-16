from api_logic import query_api as api



def main():
    key = api.retrieve_key()
    recipe_all, recipe_name = api.query_api(key, 'Blini')
    all_id = api.parse_api_return(recipe_all, recipe_name)
    api.retrieve_recipes(key, all_id)


if __name__ == '__main__':
    main()