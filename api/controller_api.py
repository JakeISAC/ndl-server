from database.rfid_db import DbOperationsRfid


class ControllerApi:
    def __init__(self, logger):
        self._rfid_db = DbOperationsRfid()

    def rfid_check(self, uid):
        try:
            return self._rfid_db.check(uid)
        except Exception:
            return None
