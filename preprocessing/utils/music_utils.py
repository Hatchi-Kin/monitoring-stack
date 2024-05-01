import music_tag
import pickle
import random
import json
from pathlib import Path


def print_tags(mp3_file_path):
    try:
        f = music_tag.load_file(mp3_file_path)
        for key in f.keys():
            print(f"{key}: {f[key].first}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def print_info(mp3_file_path):
    pkl_path = Path(mp3_file_path).with_suffix(".pkl")
    if not pkl_path.exists():
        print(f"File {pkl_path} does not exist.")
        return
    try:
        with pkl_path.open("rb") as f:
            file_info = pickle.load(f)
        for key, value in file_info.items():
            print(f"{key}: {value}")
    except pickle.UnpicklingError as e:
        print(f"Error unpickling file {pkl_path}: {e}")


def pick_random_mp3(path_to_dataset):
    list_of_files = list(Path(path_to_dataset).rglob("*.mp3"))
    if not list_of_files:
        raise ValueError(f"No mp3 files found in directory: '{path_to_dataset}'")
    random_file = random.choice(list_of_files)
    return random_file


def check_predictions_87(mp3_file_path):
    pkl_path = Path(mp3_file_path).with_suffix(".pkl")
    try:
        with pkl_path.open("rb") as f:
            file_info = pickle.load(f)
            if len(file_info["predictions_87"]) == 87:
                return True
            else:
                return False
    except:
        return False


def check_embeddings_512(mp3_file_path):
    pkl_path = Path(mp3_file_path).with_suffix(".pkl")
    try:
        with pkl_path.open("rb") as f:
            file_info = pickle.load(f)
            if len(file_info["embedding_512"]) == 512:
                return True
            else:
                return False
    except:
        return False


def get_top_5_genres(mp3_file_path, json_path):
    try:
        with open(json_path, "r") as json_file:
            metadata = json.load(json_file)
        classes = metadata.get("classes")
        if classes is None:
            raise KeyError(f"'classes' key not found in file {json_path}")
        pkl_path = Path(mp3_file_path).with_suffix(".pkl")
        with pkl_path.open("rb") as f:
            file_info = pickle.load(f)
        embedding = file_info.get("predictions_87")
        if embedding is None:
            raise KeyError(f"'predictions_87' key not found in file {pkl_path}")
        sorted_indices = embedding.argsort()
        top_5_indices = sorted_indices[-5:][::-1]
        return [classes[i] for i in top_5_indices]
    except FileNotFoundError as e:
        print(str(e))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file {json_path}: {e}")
    except KeyError as e:
        print(str(e))


def read_genres_from_pkl(mp3_file_path):
    try:
        pkl_path = Path(mp3_file_path).with_suffix(".pkl")
        with pkl_path.open("rb") as f:
            file_info = pickle.load(f)
        return file_info.get("top_5_genres")
    except FileNotFoundError as e:
        print(str(e))


def check_file_info(mp3_file_path):
    pkl_path = Path(mp3_file_path).with_suffix(".pkl")
    
    try:
        with pkl_path.open("rb") as f:
            file_info = pickle.load(f)
            if file_info.get("filename") != pkl_path.name.replace(".pkl", ".mp3"):
                return False
            if file_info.get("filepath") != str(pkl_path).replace(".pkl", ".mp3"):
                return False
            if (
                not isinstance(file_info.get("artist"), str)
                or len(file_info.get("artist")) == 0
            ):
                return False
            if file_info.get("predictions_87") is None or len(file_info.get("predictions_87", [])) != 87:
                return False
            if file_info.get("embedding_512") is None or len(file_info.get("embedding_512", [])) != 512:
                return False
            if not isinstance(file_info.get("top_5_genres"), list) or len(file_info.get("top_5_genres")) != 5:
                return False
            
            return True
        
    except FileNotFoundError as e:
        print(f"File {pkl_path} does not exist.")
        return False
    except pickle.UnpicklingError as e:
        print(f"Error unpickling file {pkl_path}: {e}")
        return False
    

