from cassandra.cluster import Cluster

from util.endpoints import Endpoints


class DbOperationsRfid:
    def __init__(self):
        self._cluster = Cluster()
        self._session = self._cluster.connect()
        self._endpoints = Endpoints()
        self._session.set_keyspace(self._endpoints.KEYSPACE_RFID)

    def upload(self, rfid: str):
        try:
            query_str = f"INSERT INTO {self._endpoints.RFID_TABLE} (tag_id) VALUES (?)"
            query = self._session.prepare(query_str)
            self._session.execute(query, [rfid])
            return True
        except Exception:
            return None

    def check(self, rfid):
        try:
            result = []
            query = f"SELECT * FROM {self._endpoints.RFID_TABLE} WHERE tag_id=?"
            prepared_query = self._session.prepare(query)
            for row in self._session.execute(prepared_query, [rfid]):
                result.append(row)
            if result:
                return True
            return False
        except Exception:
            return False

    def remove(self, tag_id):
        try:
            query_str = f"DELETE FROM {self._endpoints.RFID_TABLE} WHERE tag_id=?"
            query = self._session.prepare(query_str)
            self._session.execute(query, [tag_id])
            return True
        except Exception:
            return None