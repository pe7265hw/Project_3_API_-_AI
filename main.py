import requests
import os


def retrieve_key():
    """Retrieves API key"""
    key = os.environ.get('SPOONACULAR_KEY')
    print(key)
    
def main():
    retrieve_key()

main()