from loguru import logger


class Logs:
    def __init__(self):
        self._logger = logger
        self._logger.add("log_files/face_recon.log", filter=self._face_recon)
        self._logger.add("log_files/general_server.log")
        self._logger.add("log_files/mqtt.log", filter=self._mqtt)
        self._logger.add("log_files/security.log", filter=self._security)
        self._logger.add("log_files/user_api.log", filter=self._user_api)
        self._logger.add("log_files/controller_api.log", filter=self._controller_api)

    @classmethod
    def _face_recon(cls, record):
        return record["class"].name == "FaceDetection"

    @classmethod
    def _mqtt(cls, record):
        return record["class"].name == "MQTTServer"

    @classmethod
    def _security(cls, record):
        return record["class"].name == "Security"

    @classmethod
    def _user_api(cls, record):
        return record["class"].name == "UserApi"

    @classmethod
    def _controller_api(cls, record):
        return record["class"].name == "ControllerApi"

    def get_logger(self):
        return self._logger
