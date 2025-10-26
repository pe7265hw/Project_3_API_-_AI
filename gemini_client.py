from google import genai
from google.genai.types import GenerateContentConfig, Content, Part
from pydantic import BaseModel

def system_prompt_output():

    system_prompt = """
    You are a friendly and helpful recipe assistant. Your goal is to provide users with recipes that match their desired cuisine and dietary needs.

    Follow these steps precisely:
    1.  When the user first specifies a country or region, DO NOT provide recipes immediately.
    2.  Instead, your first response must ALWAYS be to ask them if they have any food allergies or dietary restrictions.
    3.  Once the user responds with their restrictions (or says they have none), then and only then, provide 3 distinct names of
        recipes that are unique to the specific region or country that the user specified and ENSURE they meet the dietary 
        needs if any were specified in step 2.
    4.  Format your final response as a JSON object with the following structure:
        {
            "name": [list of 3 recipe names],
            "dietary_restrictions": [list of dietary restrictions or an empty list if none]
        }

    """

    return system_prompt

# Pydantic model for structured recipe output
# This model defines the expected structure of the recipe data returned by the AI.
class Recipe(BaseModel):
    name: list[str]
    dietary_restrictions: list[str] 

def gemini_recipe_chat():
    """This does not create an actual chat, instead it uses 2 separate GenerateContentConfig calls with different configurations 
    to allow for the response schema to be applied only on the 2nd turn."""

    system_prompt = system_prompt_output()
    
    client = genai.Client()
    model = "gemini-2.5-flash"
    # Configuration for the first response (no schema) just text response
    default_config = GenerateContentConfig(
            system_instruction=system_prompt
    )

    # Response schema configuration to be used on the for the second response 
    schema_config = GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type='application/json',
            response_schema=Recipe
        )

    # Initial greeting
    print('Hello! I\'m your recipe assistant. Give me a country or region and I will give you some popular recipes from that area.')

    """Tracker to determine if it's the first interaction with Gemini or not.
    This is how we switch between the 2 configurations defined above."""
    is_first_interaction = True

    # Initialize conversation history, This a list of Gemini Content objects
    history = []

    # Main interaction loop
    while True:

        # Select configuration based on interaction turn
        if is_first_interaction:
            config = default_config
        else:
            config = schema_config

        # First interaction, returns raw text response
        if is_first_interaction:
            prompt = input('> ')

            # Store the user message content and append to history
            user_message = Content(role='user', parts=[Part(text=prompt)]) 
            history.append(user_message)

            # Generate a response from Gemini
            response = client.models.generate_content(
                model=model,
                contents=history,
                config=config
            )

            # Store Gemini's reply content 
            gemini_reply = response.candidates[0].content 
            history.append(gemini_reply)
        
        if is_first_interaction:
            # Print the raw text response for the first interaction
            print(response.text)

            # Switch to second interaction
            is_first_interaction = False  
            
        else:
        # Second interaction, returns structured response
            try:
                prompt = input('> ')
                user_message = Content(role='user', parts=[Part(text=prompt)])
                history.append(user_message)
                response = client.models.generate_content(
                    model=model,
                    contents=history,
                    config=config
                )
                print(response.parsed)
                break  # Exit after the second interaction
            except Exception as e:
                print("Sorry, I couldn't understand the response. Please try again.")
    
    return response.parsed

        
gemini_recipe_chat()
