import json
from domains.user import User
from database.users_db import DbOperationsUsers as db

class UserApi:
    def __init__(self):
        self._authorized_users = db()

    def login(self, json_string: str):
        user_data = User.extract_user(json_string)
        return self._authorized_users.check_user(user_data.username, user_data.password)