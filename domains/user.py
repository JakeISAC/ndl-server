import json
from dataclasses import dataclass

from logs.logs import Logs


@dataclass
class User:
    username: str
    password: str

    @staticmethod
    def extract_user(json_data):
        logger = Logs().get_logger()
        logger.trace("Attempting to extract User from JSON")
        try:
            data = json.loads(json_data)
            logger.debug("User extracted successfully from JSON")
            return User(username=data["username"], password=data["password"])
        except Exception as e:
            logger.exception(f"Failed to extract a User from JSON: {e}")
            return None
