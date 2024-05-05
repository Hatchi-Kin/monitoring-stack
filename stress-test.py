import os
import requests
import time
import random
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv() 

LOGIN_ENDPOINT = os.getenv("LOGIN_ENDPOINT")
ERROR_CODES = {400, 401, 403, 404, 500} 

def get_tokens(login_endpoint, accounts):
    """Fetch tokens for each account."""
    tokens = []
    for account in accounts:
        data = {
            "username": account['username'],
            "password": account['password']
        }
        response = requests.post(login_endpoint, data=data)
        if response.status_code == 200:
            tokens.append(response.json().get('access_token'))
        else:
            raise Exception(f"Failed to get token for {account['username']}, status code: {response.status_code}")
    return tokens

def call_api(endpoints, tokens, num_requests):
    """Call API endpoints with random tokens and return error messages."""
    headers = {"Authorization": ""}
    error_messages = set()
    current_endpoint = random.choice(endpoints)
    for _ in tqdm(range(num_requests)):
        headers["Authorization"] = f"Bearer {random.choice(tokens)}"
        response = requests.get(current_endpoint, headers=headers)
        if response.status_code in ERROR_CODES:
            error_messages.add(f"Error: status code {response.status_code} for {current_endpoint}")
        time.sleep(random.randint(2, 4))  # pause 
        remaining_endpoints = [ep for ep in endpoints if ep != current_endpoint]
        current_endpoint = random.choice(remaining_endpoints) if remaining_endpoints else current_endpoint
    return error_messages

accounts = [
    {"username": os.getenv("USERNAME_PROMETHEUS"), "password": os.getenv("PASSWORD_PROMETHEUS")},
    {"username": os.getenv("USERNAME_BENDER"), "password": os.getenv("PASSWORD_BENDER")},
    {"username": os.getenv("USERNAME_BENDER2"), "password": os.getenv("PASSWORD_BENDER2")}
]

endpoints = [
    "https://api.music-sim.fr/auth/users",
    "https://api.music-sim.fr/music_library/count",
    "https://api.music-sim.fr/music_library/random",
    f"https://api.music-sim.fr/music_library/song/{random.randint(1, 16200)}",
    "https://api.music-sim.fr/music_library/artist",
    "https://api.music-sim.fr/music_library/artists",
    "https://api.music-sim.fr/music_library/albums",
    "https://api.music-sim.fr/lyrics/random-lyrics",
    "https://api.music-sim.fr/lyrics/random-lyrics-metadata",
    "https://api.music-sim.fr/auth/gui",
    "https://api.music-sim.fr/minio/random-metadata",
    "https://api.music-sim.fr/monitoring/pi"
]



if __name__ == "__main__":
    try:
        tokens = get_tokens(LOGIN_ENDPOINT, accounts)
        if tokens:
            error_messages = call_api(endpoints, tokens, 500)
            if error_messages:
                for msg in error_messages:
                    print(msg)
            else:
                print("All requests were successful")
    except Exception as e:
        print(f"An error occurred: {e}")
    