import requests

BASE_URL = "https://mephi.opentoshi.net/api/v1"

def post_request(path, params=None):
    url = BASE_URL + path
    response = requests.post(url, params=params)
    try:
        return response.json()
    except:
        return {"status_code": response.status_code, "text": response.text}

def get_request(path, params=None):
    url = BASE_URL + path
    response = requests.get(url, params=params)
    try:
        return response.json()
    except:
        return {"status_code": response.status_code, "text": response.text}

def register_team():
    result = get_request("/team/register")
    print("\nОтвет сервера:")
    print(result)
    return result

def create_reactor(team_id):
    result = post_request("/reactor/create_reactor", {"team_id": team_id})
    print("\nОтвет сервера:")
    print(result)

def get_data(team_id):
    result = get_request("/reactor/history", {"team_id": team_id})
    print("\nИстория:")
    print(result)

def refill_water(team_id, amount):
    result = post_request()