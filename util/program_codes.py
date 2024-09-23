from enum import Enum


class AuthorizationStatus(Enum):
    AUTHORIZED = 0
    PENDING = 1
    NOT_AUTHORIZED = 2


class PicoEvents(Enum):
    OPEN_LOCK = 0
    CLOSE_LOCK = 1
    TURN_OFF_SCREEN = 2
    TURN_ON_SCREEN = 3

    def __str__(self):
        match self:
            case self.OPEN_LOCK:
                return "OPEN_LOCK"
            case self.CLOSE_LOCK:
                return "CLOSE_LOCK"
            case self.TURN_OFF_SCREEN:
                return "TURN_OFF_SCREEN"
            case self.TURN_ON_SCREEN:
                return "TURN_ON_SCREEN"
