import uuid

from database.session_db import DbOperationsSession
from database.users_db import DbOperationsUsers
from domains.user import User
from logs.logs import Logs


class UserApi:
    def __init__(self):
        self._user_db = DbOperationsUsers()
        self._session_db = DbOperationsSession()
        self._logger = Logs().get_logger()

    def login(self, user_data: User):
        self._logger.debug("Attempting to login")
        try:
            if self._user_db.check(user_data.username, user_data.password):
                token = uuid.uuid4().hex
                self._session_db.upload(token)
                return token
            else:
                return None
        except Exception as e:
            self._logger.exception(f"Failed to login a user: {e}")
            return None

    def register(self, user_data: User):
        self._logger.debug("Attempting to register")
        try:
            return self._user_db.upload(user_data)
        except Exception as e:
            self._logger.exception(f"Failed to register a user: {e}")
            return None

    def change_password(self, username, old_password, new_password):
        self._logger.debug("Attempting to change password")
        try:
            if self._user_db.check(username, old_password):
                return self._user_db.change_password(username, new_password)
            else:
                raise Exception("Old password is incorrect")
        except Exception as e:
            self._logger.exception(f"Failed to change password: {e}")
            return None
