from api_logic import query_api as api



def main():
    key = api.retrieve_key()
    recipe_all, recipe_name = api.query_api(key, 'tortellini')
    chosen_id = api.parse_api_return(recipe_all, recipe_name)
    recipe_information = api.retrieve_recipe(key, chosen_id)
    api.extract_recipe_information(recipe_information)



if __name__ == '__main__':
    main()