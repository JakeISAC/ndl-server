from enum import Enum


class AuthorizationStatus(Enum):
    AUTHORIZED = 0
    TEMPORARY = 1
    NOT_AUTHORIZED = 2


class AesMode(Enum):
    USER = 0
    PICO = 1


class PicoEvents(Enum):
    OPEN_LOCK = 0
    CLOSE_LOCK = 1

    def __str__(self):
        match self:
            case self.OPEN_LOCK:
                return "OPEN_LOCK"
            case self.CLOSE_LOCK:
                return "CLOSE_LOCK"
