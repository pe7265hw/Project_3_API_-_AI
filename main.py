import requests
import os


def retrieve_key():
    """Retrieves API key"""
    key = os.environ.get('SPOONACULAR_KEY')
    return key
   
def main():
    retrieve_key()

main()