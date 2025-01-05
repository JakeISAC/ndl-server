import time
from datetime import datetime, timedelta
from threading import Thread

from cassandra.cluster import Cluster

from logs.logs import Logs
from util.endpoints import Endpoints


class SessionTokenDaemon:
    def __init__(self):
        self._logger = Logs().get_logger()
        self._cluster = Cluster()
        self._session = self._connect()
        self._endpoints = Endpoints()
        self._session.set_keyspace(self._endpoints.KEYSPACE_SESSION)

    def _connect(self):
        try:
            self._logger.info("Connecting to Session database - Daemon")
            return self._cluster.connect()
        except Exception as e:
            self._logger.exception(f"Failed to connect to Session database: {e}")
            raise e

    def _delete_outdated_tokens(self):
        try:
            threshold = datetime.now() - timedelta(days=3)
            threshold_str = threshold.strftime("%Y-%m-%d %H:%M:%S")

            select_query = f"SELECT session_token FROM {self._endpoints.SESSION_TABLE} WHERE timestamp < ? ALLOW FILTERING"
            prepared_select = self._session.prepare(select_query)
            rows_to_delete = self._session.execute(prepared_select, [threshold_str])

            for row in rows_to_delete:
                delete_query = f"DELETE FROM {self._endpoints.SESSION_TABLE} WHERE session_token = ?"
                prepared_delete = self._session.prepare(delete_query)
                self._session.execute(prepared_delete, [row.session_token])

            self._logger.debug("Deleted outdated tokens")
        except Exception as e:
            self._logger.exception(f"Failed to delete outdated tokens: {e}")

    def _run(self):
        while True:
            self._delete_outdated_tokens()
            time.sleep(86400)

    def run(self):
        daemon_thread = Thread(target=self._run)
        daemon_thread.start()
