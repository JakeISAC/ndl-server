import json
from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str

    @classmethod
    def extract_user(cls, json_data):
        data = json.loads(json_data)
        return User(username=data["username"], password=data["password"])