import uuid
from time import sleep

from domains.user import User
from database.users_db import DbOperationsUsers
from database.session_db import DbOperationsSession
from logs.logs import Logs

class UserApi:
    def __init__(self):
        self._user_db = DbOperationsUsers()
        self._session_db = DbOperationsSession()
        self._logger = Logs().get_logger()

    def login(self, user_data: User):
        self._logger.info("Attempting to login")
        try:
            if self._user_db.check_user(user_data.username, user_data.password):
                token = uuid.uuid4().hex
                self._session_db.upload(token)
                return token
            else:
                return None
        except Exception as e:
            self._logger.exception(f"Failed to login a user: {e}")
            return None

    def register(self, json_string: str):
        self._logger.info("Attempting to register")
        try:
            user_data = User.extract_user(json_string)
            return self._user_db.upload(user_data)
        except Exception as e:
            self._logger.exception(f"Failed to register a user: {e}")
            return None