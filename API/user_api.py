from domains.user import User
from database.users_db import DbOperationsUsers as db
from logs.logs import Logs

logging = Logs().get_logger()


class UserApi:
    def __init__(self):
        self._authorized_users = db()

    def login(self, json_string: str):
        try:
            user_data = User.extract_user(json_string)
            check = self._authorized_users.check_user(user_data.username, user_data.password)
            if check:
                logging.info(f"User authorized: {user_data.username}")
            else:
                logging.info(f"User not-authorized: {user_data.username}")
            return
        except Exception as e:
            logging.exception(e)