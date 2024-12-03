import json
import uuid
from datetime import datetime

from domains.user import User
from database.users_db import DbOperationsUsers as db
from database.session_db import DbOperationsSession as session_db

class UserApi:
    def __init__(self):
        self._db_access = db()
        self._session_db = session_db()

    def login(self, json_string: str):
        user_data = User.extract_user(json_string)
        # generate session token
        token = uuid.uuid4().hex
        self._session_db.upload_to_db(token)
        return self._db_access.check_user(user_data.username, user_data.password), token

    def register(self, json_string: str):
        user_data = User.extract_user(json_string)
        return self._db_access.upload_to_db(user_data)