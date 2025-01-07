from loguru import logger

logging = logger
logging.add("logs/general.log", rotation="100 MB", level="ERROR")


class Logs:
    @classmethod
    def get_logger(cls):
        return logging
