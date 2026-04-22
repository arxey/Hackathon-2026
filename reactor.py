import requests

BASE_URL = "https://mephi.opentoshi.net/api/v1"

def post_request(path, params=None):
    url = BASE_URL + path