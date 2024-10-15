import requests
from locust import HttpUser, task, between, events
from locust.argument_parser import LocustArgumentParser


class MyLoadTest(HttpUser):
    # Define the wait time between tasks
    wait_time = between(1, 3)
    token = None


    def on_start(self):
        # Retrieve a valid token from the API using the provided username and password
        response = requests.post(
            f"{self.environment.host}/auth/token",
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'username': self.environment.parsed_options.username,
                'password': self.environment.parsed_options.password,
            }
        )
        self.token = response.json().get("access_token")

    @task(1)
    def user_me(self):
        self.client.get(f"{self.environment.host}/auth/users/me", headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def count_songs(self):
        self.client.get(f"{self.environment.host}/music_library/count", headers={"Authorization": f"Bearer {self.token}"})

    @task(2) 
    def random_song(self):
        self.client.get(f"{self.environment.host}/music_library/random", headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def artists(self):
        self.client.get(f"{self.environment.host}/music_library/artists", headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def albums(self):
        self.client.post(
            f"{self.environment.host}/music_library/albums",
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            },
            json={"artist_folder": "MegaSet/Johnny Clegg"}
        )

    @task(1)
    def uploaded_songs(self):
        self.client.get(f"{self.environment.host}/uploaded/", headers={"Authorization": f"Bearer {self.token}"})
        
    @task(2)
    def milvus_entity(self):
        self.client.get(f"{self.environment.host}/milvus/entity/666", headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def milvus_similar(self):
        self.client.get(f"{self.environment.host}/milvus/similar/666", headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def milvus_similar_short_entity(self):
        self.client.post(
            f"{self.environment.host}/milvus/similar_short_entity",
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            },
            json={"path": ["MegaSet/System Of A Down/Mezmerize/10-Old School Hollywood.mp3"]}
        )

    task(1)
    def minio_list_objects_in_folder(self):
        self.client.post(
            f"{self.environment.host}/minio/list-objects/",
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            },
            json={"album_folder": "MegaSet/No Place For Soul/2002 - Full Global Racket"}
        )

    @task(1)
    def milvus_plot_genres(self):
        self.client.post(
            f"{self.environment.host}/milvus/plot_genres",
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            },
            json={"file_path": "MegaSet/No Place For Soul/2002 - Full Global Racket/04 A.I.M.mp3"}
        )

    @task(3)
    def openl3_embeddings_and_delete(self):
        # Simulate a POST request to the /openl3/embeddings endpoint
        self.client.post(
            f"{self.environment.host}/openl3/embeddings/?file_path=KavinskyAngeleNightcall.mp3",
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {self.token}'
            },
            data=''  # Empty data payload
        )
        # immediately delete the pkl file to force the /openl3/embeddings/ endpoint to recompute the embeddings
        # we can still see both requests in the Locust UI even if they are executed in sequence in same task
        self.client.post(
            f"{self.environment.host}/minio/delete-temp",
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            },
            json={"file_path": "KavinskyAngeleNightcall.pkl"}
        )

    @task(1)
    def auth_users(self):
        self.client.get(f"{self.environment.host}/auth/users", headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def music_library_song(self):
        self.client.get(f"{self.environment.host}/music_library/song/666", headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def minio_metadata(self):
        self.client.post(
            f"{self.environment.host}/minio/metadata",
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            },
            json={"file_path": "MegaSet/No Place For Soul/2002 - Full Global Racket/04 A.I.M.mp3"}
        )

    @task(1)
    def monitoring_host(self):
        self.client.get(f"{self.environment.host}/monitoring/pi", headers={"Authorization": f"Bearer {self.token}"})


# Add custom command-line arguments for the username and password
@events.init_command_line_parser.add_listener
def _(parser: LocustArgumentParser):
    parser.add_argument("--username", type=str, required=True, help="Username for authentication")
    parser.add_argument("--password", type=str, required=True, help="Password for authentication")


"""
Run simulate traffic locally with the following command:
locust -f locust/locust_file.py --web-host 127.0.0.1 --host http://api.example.com --username YOUR_USERNAME --password YOUR_PASSWORD
"""