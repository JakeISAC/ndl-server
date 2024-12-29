from cassandra.cluster import Cluster
from util.endpoints import Endpoints
from datetime import datetime
from logs.logs import Logs

class DbOperationsSession:
    def __init__(self):
        self._cluster = Cluster()
        self._logger = Logs().get_logger()
        self._session = self._cluster.connect()
        self._endpoints = Endpoints()
        self._session.set_keyspace(self._endpoints.KEYSPACE_SESSION)

    def upload(self, token):
        try:
            query_str = f"INSERT INTO {self._endpoints.SESSION_TABLE} (session_token, timestamp) VALUES (?, ?)"
            query = self._session.prepare(query_str)
            self._session.execute(query, [token, str(datetime.now())])
            self._logger.debug("Uploaded a session token")
            return True
        except Exception as e:
            self._logger.exception(f"Failed to upload session token: {e}")
            return False

    def check_token(self, token) -> bool:
        try:
            result = []
            query = f"SELECT * FROM {self._endpoints.SESSION_TABLE} WHERE session_token=?"
            prepared_query = self._session.prepare(query)
            for row in self._session.execute(prepared_query, [token]):
                result.append(row)
            if result:
                self._logger.debug(f"Checked a session token: {token}")
                return True
            return False
        except Exception as e:
            self._logger.exception(f"Failed to check a session token: {e}")
            return False