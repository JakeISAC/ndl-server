import uuid

from domains.user import User
from database.users_db import DbOperationsUsers
from database.session_db import DbOperationsSession

class UserApi:
    def __init__(self):
        self._user_db = DbOperationsUsers()
        self._session_db = DbOperationsSession()

    def login(self, json_string: str):
        try:
            user_data = User.extract_user(json_string)
            # generate session token
            if self._user_db.check_user(user_data.username, user_data.password):
                token = uuid.uuid4().hex
                self._session_db.upload(token)
                return token
            else:
                return None
        except Exception:
            return None

    def register(self, json_string: str):
        try:
            user_data = User.extract_user(json_string)
            return self._user_db.upload(user_data)
        except Exception:
            return None