from loguru import logger


class Logs:
    def __init__(self):
        self._logger = logger
        self._logger.add("/home/ubuntu/ndl/logs/general.log", rotation="100 MB", level="EXCEPTION")

    def get_logger(self):
        return self._logger
