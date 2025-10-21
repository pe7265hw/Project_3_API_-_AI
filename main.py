from api_logic import query_api as api



def main():
    key = api.retrieve_key()
    empty_recipe_return = 0

    gemini_recipe_input = []
    flask_recipe_output = []

    for item in gemini_recipe_input:
        if api.check_for_entries() ==  True:
            recipe_all, recipe_name = api.query_api(key, 'tortellini')
            chosen_id = api.parse_api_return(recipe_all, recipe_name)
            recipe_information = api.retrieve_recipe(key, chosen_id)
            extracted_recipe_information = api.extract_recipe_information(recipe_information)
            flask_recipe_output.append(extracted_recipe_information)

        else:
            recipe_return_count += 1

    if empty_recipe_return >= 2:
        return
    else:
        return flask_recipe_output





if __name__ == '__main__':
    main()