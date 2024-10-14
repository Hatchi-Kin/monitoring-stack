import os
import random
from dotenv import load_dotenv

import requests
from locust import HttpUser, task, between

# Load environment variables from .env file implicitly
load_dotenv()

class MyLoadTest(HttpUser):
    # Define the wait time between tasks
    wait_time = between(1, 5)
    base_url = os.getenv("BASE_URL")
    username = os.getenv("USERNAME_BENDER")
    password = os.getenv("PASSWORD_BENDER")
    token = None

    def on_start(self):
        # Retrieve a valid token from the API
        response = requests.post(
            f"{self.base_url}/auth/token",
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'username': self.username,
                'password': self.password,
            }
        )
        self.token = response.json().get("access_token")

    @task(2)
    def auth_users(self):
        # Simulate a GET request to the /auth/users endpoint
        self.client.get(f"{self.base_url}/auth/users", headers={"Authorization": f"Bearer {self.token}"})

    @task(2)
    def music_library_song(self):
        # Simulate a GET request to the /music_library/song/{id} endpoint
        song_id = random.randint(1, 16200)
        self.client.get(f"{self.base_url}/music_library/song/{song_id}", headers={"Authorization": f"Bearer {self.token}"})

    @task(5)
    def openl3_embeddings(self):
        # Simulate a POST request to the /openl3/embeddings endpoint
        self.client.post(
            f"{self.base_url}/openl3/embeddings/",
            headers={"Authorization": f"Bearer {self.token}"},
            json={"file_path": "KavinskyAngeleNightcall.mp3"}
        )

    @task(5)
    def openl3_embeddings(self):
        # Simulate a POST request to the /openl3/embeddings endpoint
        self.client.post(
            f"{self.base_url}/openl3/embeddings/?file_path=KavinskyAngeleNightcall.mp3",
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {self.token}'
            },
            data=''  # Empty data payload
        )

    @task(2)
    def minio_metadata(self):
        # Simulate a POST request to the /minio/metadata endpoint
        self.client.post(
            f"{self.base_url}/minio/metadata",
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            },
            json={"file_path": "MegaSet/No Place For Soul/2002 - Full Global Racket/04 A.I.M.mp3"}
        )

    @task(1)
    def monitoring_host(self):
        # Simulate a GET request to the /monitoring/host endpoint
        self.client.get(f"{self.base_url}/monitoring/pi", headers={"Authorization": f"Bearer {self.token}"})

"""
Run simulate traffic:
locust -f locustfile.py --web-host 127.0.0.1 --host https://BASE_URL
"""