from database.rfid_db import DbOperationsRfid
from logs.logs import Logs


class ControllerApi:
    def __init__(self):
        self._rfid_db = DbOperationsRfid()
        self._logger = Logs().get_logger()

    def rfid_check(self, uid):
        self._logger.trace("Attempting to check rfid uid")
        try:
            return self._rfid_db.check(uid)
        except Exception as e:
            self._logger.exception(f"{e}")
            return None
