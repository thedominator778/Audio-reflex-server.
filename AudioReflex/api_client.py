import requests

BASE_URL = "http://127.0.0.1:8000"

def register(username, password):
    try:
        response = requests.post(
            f"{BASE_URL}/register/",
            json={"username": username, "password": password}
        )
        return response
    except requests.exceptions.ConnectionError:
        return None

def login(username, password):
    try:
        response = requests.post(
            f"{BASE_URL}/login/",
            data={"username": username, "password": password}
        )
        return response
    except requests.exceptions.ConnectionError:
        return None

def get_leaderboard(token: str):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/leaderboard/", headers=headers)
        return response
    except requests.exceptions.ConnectionError:
        return None

def post_score(score: int, token: str):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{BASE_URL}/scores/",
            json={"score": score},
            headers=headers
        )
        return response
    except requests.exceptions.ConnectionError:
        return None
