"""yelp.py: returns list of information on resturants given location and term. using yelp api.  """
import os
import json
from dotenv import find_dotenv, load_dotenv
import requests


load_dotenv(find_dotenv())

YELP_API_KEY = os.getenv("YELP_API_KEY")


def get_resturant_info(resturant):
    """returns dictionary of information given a resturant"""
    try:
        resturant_info = {
            "name": resturant["name"],
            "rating": resturant["rating"],
            "price": resturant["price"],
            "url": resturant["url"],
            "phone": resturant["phone"],
            "image_url": resturant["image_url"],
            "address": resturant["location"]["address1"],
            "city": resturant["location"]["city"],
            "state": resturant["location"]["state"],
            "zip_code": resturant["location"]["zip_code"],
            "distance:": resturant["distance"],
            "transactions": resturant["transactions"],
        }
    except KeyError:
        resturant_info = None
    return resturant_info


def resturant_search(term, location):
    """returns list of dictionaries of resturants given location and term."""
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": "Bearer %s" % YELP_API_KEY}
    params = {
        "term": term,
        "location": location,
        "limit": 10,
        "category": "restaurants",
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    try:
        results = data["businesses"]
    except KeyError:  # invalid location
        results = []

    if results:
        resturants = [get_resturant_info(resturant) for resturant in results]
        resturants = [
            resturant for resturant in resturants if resturant is not None
        ]  # filter out None values
    else:
        resturants = []

    resturants_info = json.dumps(resturants)
    return resturants_info
