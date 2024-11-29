from enum import Enum

class UserLoginResponse(Enum):
    OK = 0,
    FAILED = 1

    def __str__(self):
        match self:
            case self.OK:
                return "OK"
            case self.FAILED:
                return "FAILED"


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
                return "open"
            case self.CLOSE_LOCK:
                return "close"
