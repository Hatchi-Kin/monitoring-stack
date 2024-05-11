import os
import time
import random
import requests
from dotenv import load_dotenv
from tqdm.contrib.concurrent import thread_map


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


def call_api(get_endpoints, post_endpoints, tokens, num_requests):
    """Call API endpoints with random tokens and return error count and average time."""
    headers = {"Authorization": ""}
    error_count = 0
    time_per_endpoint = {url: [] for url in (get_endpoints + list(post_endpoints.keys()))}

    def make_request(_):
        nonlocal error_count
        current_endpoint = random.choice(list(get_endpoints) + list(post_endpoints.keys()))
        headers["Authorization"] = f"Bearer {random.choice(tokens)}"
        start_time = time.time()
        if current_endpoint in get_endpoints:
            response = requests.get(current_endpoint, headers=headers)
        else:
            data = post_endpoints[current_endpoint]
            response = requests.post(current_endpoint, headers=headers, json=data)
        end_time = time.time()
        time_per_endpoint[current_endpoint].append(end_time - start_time)
        if response.status_code in ERROR_CODES:
            error_count += 1
        time.sleep(0.25)

    thread_map(make_request, range(num_requests), max_workers=5)

    avg_time_per_endpoint = {url: sum(times)/len(times) for url, times in time_per_endpoint.items()}

    return error_count, avg_time_per_endpoint


accounts = [
    {"username": os.getenv("USERNAME_PROMETHEUS"), "password": os.getenv("PASSWORD_PROMETHEUS")},
    {"username": os.getenv("USERNAME_BENDER"), "password": os.getenv("PASSWORD_BENDER")},
    {"username": os.getenv("USERNAME_BENDER2"), "password": os.getenv("PASSWORD_BENDER2")}
]

get_endpoints = [
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

post_endpoints = {
    "https://api.music-sim.fr/music_library/albums": {"artist_folder": "MegaSet/Katie Melua"},
    "https://api.music-sim.fr/music_library/songs": {"album_folder": "MegaSet/Daft Punk/2013 - Random Access Memories"},
    "https://api.music-sim.fr/music_library/songs/by_artist_and_album": {"artist": "Katie Melua","album": "Pictures"},
    "https://api.music-sim.fr/milvus/similar_short_entity": {"path": ["MegaSet/Yann Tiersen/2001 - Le Fabuleux Destin D'Amelie Poulain/03 - La Valse D'Amelie.mp3"]},
    "https://api.music-sim.fr/minio/list-objects/":{"album_folder": "MegaSet/Daft Punk/2013 - Random Access Memories"},
    "https://api.music-sim.fr/minio/metadata": {"file_path": "MegaSet/No Place For Soul/2002 - Full Global Racket/04 A.I.M.mp3"}
}


if __name__ == "__main__":
    try:
        tokens = get_tokens(LOGIN_ENDPOINT, accounts)
        if tokens:
            error_count, avg_time_per_endpoint = call_api(get_endpoints, post_endpoints, tokens, 750)
            print(f"Number of errors: {error_count}")
            print("Average time per endpoint:")
            for url, avg_time in avg_time_per_endpoint.items():
                print(f"{url}: {round(avg_time, 2)} seconds")
    except Exception as e:
        print(f"An error occurred: {e}")
    