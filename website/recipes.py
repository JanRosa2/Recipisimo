import requests
from requests.exceptions import RequestException, HTTPError
import os
from dotenv import load_dotenv

# In secret.env are secret variables, so we will load that file
load_dotenv()
# And get the variables from
API_KEY=os.getenv('API_KEY')


def get_recipes(ingredients, ranking):
    
    """
    This function returns recipes in JSON format through API "spoonacular" 
    depending on users ingrediens.

    """

    # Parameters for request 
    # (reference: https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients)
    parameters = {
        "apiKey" : API_KEY,
        "ingredients" : ingredients,
        "number" : 6,
        "ranking" : ranking,
        "ignorePantry" : True,
    }
    try:
        response = requests.get(url="https://api.spoonacular.com/recipes/findByIngredients", params=parameters)
        # Print out a status code - if successful a response code = 200
        print(f"API request status code: {response.status_code}")
        # Raise HTTP error if bad request by raise_for_status method
        print(f"API request status: {response.raise_for_status()}")
    # If NOT successful a response code = 404 (page doesn't exist) or 500 (internal server error)
    # Those are HTTP errors - requests module "exception" called "HTTPError" will handle those
    except HTTPError as e:
        print(f"HTTPError: {e.response.text}")
        return False
    # When general exception occurs - requests module "exception" called "RequestException" will handle this
    except RequestException as e:
        print(f"RequestException: {e.response.text}")
        return False
    # Return json
    return response.json()


def process_json(data_json):

    """
    This function processes the json data requested through "Spoonacular" API to make it more organized and 
    more relevant for the project.

    """
    # Create an list for storing processed data
    recipes = []
    # If there are data in data_json continue processing
    if (len(data_json) != 0):
        for recipe in data_json:
            used_ingr_list = [used["name"] for used in recipe["usedIngredients"]]
            miss_ingr_list = [missing["name"] for missing in recipe["missedIngredients"]]
            dict = {
                "title": recipe["title"],
                "image": recipe["image"],
                "used": ", ".join(used_ingr_list),
                "missing": ", ".join(miss_ingr_list),    
            }
            recipes.append(dict)
        return recipes
    else:
        return False
