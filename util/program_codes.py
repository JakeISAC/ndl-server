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

class AddMemberResponse(Enum):
    OK = 0,
    FAILED = 1

    def __str__(self):
        match self:
            case self.OK:
                return "OK"
            case self.FAILED:
                return "FAILED"

class DeleteResponse(Enum):
    OK = 0
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

    def __str__(self):
        match self:
            case self.AUTHORIZED:
                return "authorized"
            case self.NOT_AUTHORIZED:
                return "not authorized"
            case self.TEMPORARY:
                return "temporary"


class ControllerEvents(Enum):
    OPEN_LOCK = 0
    CLOSE_LOCK = 1

    def __str__(self):
        match self:
            case self.OPEN_LOCK:
                return "open"
            case self.CLOSE_LOCK:
                return "close"