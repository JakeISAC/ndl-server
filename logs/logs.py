from loguru import logger

logging = logger
logging.add("/home/ubuntu/ndl/logs/general.log", rotation="100 MB", level="ERROR")

class Logs:
    @classmethod
    def get_logger(cls):
        logger.trace("Logger instance initialized")
        return logging
