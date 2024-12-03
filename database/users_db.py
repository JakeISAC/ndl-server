from cassandra.cluster import Cluster
from util.endpoints import Endpoints

class DbOperationsUsers:
    def __init__(self):
        self._cluster = Cluster()
        self._session = self._cluster.connect()
        self._endpoints = Endpoints()
        self._session.set_keyspace(self._endpoints.KEYSPACE_USERS)


    def upload_to_db(self, user: object):
        try:
            query_str = f"INSERT INTO {self._endpoints.USERS_TABLE} (username, pssword) VALUES (?, ?) IF NOT EXISTS"
            query = self._session.prepare(query_str)
            self._session.execute(query, [user.username, user.password])
            return True
        except Exception as e:
            return False

    def get_all(self):
        try:
            people = []
            query = f"SELECT * FROM {self._endpoints.USERS_TABLE}"
            prepared_query = self._session.prepare(query)
            for row in self._session.execute(prepared_query):
                people.append(self._row_to_user(row))
            return people
        except Exception as e:
            return None

    def check_user(self, username, password):
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
                        return True
            return False

        except Exception:
            return None

    @classmethod
    def _row_to_user(cls, row):
        from domains.user import User
        try:
            return User(username=row.username, password=row.password)
        except Exception as e:
            raise e
