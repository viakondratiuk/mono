import json


def get_mono_key() -> str:
    with open("keys.json", "r") as file:
        data = json.load(file)
    
    return data["MONO_KEY"]