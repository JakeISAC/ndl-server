from cassandra.cluster import Cluster
from util.endpoints import Endpoints
from datetime import datetime

class DbOperationsSession:
    def __init__(self):
        self._cluster = Cluster()
        self._session = self._cluster.connect()
        self._endpoints = Endpoints()
        self._session.set_keyspace(self._endpoints.KEYSPACE_SESSION)

    def upload_to_db(self, token):
        try:
            query_str = f"INSERT INTO {self._endpoints.SESSION_TABLE} (token, timestamp) VALUES (?, ?)"
            query = self._session.prepare(query_str)
            self._session.execute(query, [token, str(datetime.now())])
            return True
        except Exception as e:
            return False

    def check_token(self, token):
        try:
            result = []
            query = f"SELECT * FROM {self._endpoints.SESSION_TABLE} WHERE token=?"
            prepared_query = self._session.prepare(query)
            for row in self._session.execute(prepared_query, [token]):
                result.append(row.password)
            if result:
                return True
            return False

        except Exception:
            return None

