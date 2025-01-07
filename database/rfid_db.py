from cassandra.cluster import Cluster

from logs.logs import Logs
from util.endpoints import Endpoints


class DbOperationsRfid:
    def __init__(self):
        self._logger = Logs().get_logger()
        self._cluster = Cluster()
        self._session = self._connect()
        self._endpoints = Endpoints()
        self._session.set_keyspace(self._endpoints.KEYSPACE_RFID)

    def _connect(self):
        try:
            self._logger.info("Connecting to Rfid database")
            return self._cluster.connect()
        except Exception as e:
            self._logger.critical(f"Failed to connect to Rfid database: {e}")
            raise e

    def upload(self, rfid: str):
        try:
            query_str = f"INSERT INTO {self._endpoints.RFID_TABLE} (tag_id) VALUES (?)"
            query = self._session.prepare(query_str)
            self._session.execute(query, [rfid])
            self._logger.debug(f"Uploaded a new RFID uid: {rfid}")
            return True
        except Exception as e:
            self._logger.exception(f"Failed to upload a new RFID: {e}")
            return None

    def check(self, rfid):
        try:
            result = []
            query = f"SELECT * FROM {self._endpoints.RFID_TABLE} WHERE tag_id=?"
            prepared_query = self._session.prepare(query)
            for row in self._session.execute(prepared_query, [rfid]):
                result.append(row)
            if result:
                self._logger.debug(f"RFID {rfid} exists in the authorized database")
                return True
            return False
        except Exception as e:
            self._logger.exception(f"Failed to check the RFID tag: {e}")
            return None

    def remove(self, tag_id):
        try:
            query_str = f"DELETE FROM {self._endpoints.RFID_TABLE} WHERE tag_id=?"
            query = self._session.prepare(query_str)
            self._session.execute(query, [tag_id])
            self._logger.debug(f"Removed a tag with RFID {tag_id}")
            return True
        except Exception as e:
            self._logger.exception(f"Failed to remove RFID tag: {e}")
            return None
