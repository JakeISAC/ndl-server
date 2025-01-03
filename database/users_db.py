from cassandra.cluster import Cluster

from domains.user import User
from logs.logs import Logs
from util.endpoints import Endpoints


class DbOperationsUsers:
    def __init__(self):
        self._logger = Logs().get_logger()
        self._cluster = Cluster()
        self._session = self._connect()
        self._endpoints = Endpoints()
        self._session.set_keyspace(self._endpoints.KEYSPACE_USERS)

    def _connect(self):
        try:
            self._logger.debug("Connecting to User database")
            return self._cluster.connect()
        except Exception as e:
            self._logger.exception(f"Failed to connect to User database: {e}")
            raise e

    def upload(self, user: User):
        try:
            query_str = f"INSERT INTO {self._endpoints.USERS_TABLE} (username, password) VALUES (?, ?)"
            query = self._session.prepare(query_str)
            self._session.execute(query, [user.username, user.password])
            self._logger.debug(f"Uploaded user {user.username}")
            return True
        except Exception as e:
            self._logger.exception(f"Failed to upload a user: {e}")
            return False

    def delete(self, username):
        try:
            query_str = f"DELETE FROM {self._endpoints.USERS_TABLE} WHERE username=?"
            query = self._session.prepare(query_str)
            self._session.execute(query, [username])
            self._logger.debug(f"Deleted user {username}")
            return True
        except Exception as e:
            self._logger.exception(f"Failed to delete user {username}: {e}")
            return None

    def get_all(self):
        try:
            people = []
            query = f"SELECT * FROM {self._endpoints.USERS_TABLE}"
            prepared_query = self._session.prepare(query)
            for row in self._session.execute(prepared_query):
                people.append(self._row_to_user(row))
            self._logger.debug("Successfully retrieved all users")
            return people
        except Exception as e:
            self._logger.exception(f"Failed to retrieve all users: {e}")
            return None

    def check(self, username, password):
        try:
            result = []
            query = f"SELECT password FROM {self._endpoints.USERS_TABLE} WHERE username=?"
            prepared_query = self._session.prepare(query)
            for row in self._session.execute(prepared_query, [username]):
                result.append(row.password)
            if result:
                # technically to db constraints there should only be one under the given username, but just to be safe
                # collect to array
                for passwd in result:
                    if passwd == password:
                        self._logger.debug(f"User {username} exists in the authorized database")
                        return True
            self._logger.debug(f"User {username} does not exist in the authorized database")
            return False
        except Exception as e:
            self._logger.exception(f"Failed to check user {username}: {e}")
            return None

    def change_password(self, username, new_password):
        try:
            query_str = f"UPDATE {self._endpoints.USERS_TABLE} SET password=? WHERE username=?"
            query = self._session.prepare(query_str)
            self._session.execute(query, [new_password, username])
            self._logger.debug(f"Changed password for user {username}")
            return True
        except Exception as e:
            self._logger.exception(f"Failed to change password for user {username}: {e}")
            return None

    @classmethod
    def _row_to_user(cls, row):
        from domains.user import User
        try:
            return User(username=row.username, password=row.password)
        except Exception as e:
            raise e
