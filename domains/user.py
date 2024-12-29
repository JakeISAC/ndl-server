import json
from dataclasses import dataclass

from logs.logs import Logs


@dataclass
class User:
    username: str
    password: str

    def __post_init__(self):
        self._logger = Logs().get_logger()

    def extract_user(self, json_data):
        try:
            data = json.loads(json_data)
            self._logger.debug("User extracted successfully from JSON")
            return User(username=data["username"], password=data["password"])
        except Exception as e:
            self._logger.exception(f"Failed to extract a User from JSON: {e}")
            return None