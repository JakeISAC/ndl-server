from enum import Enum


class ControllerEvents(Enum):
    OPEN_LOCK = 0
    CLOSE_LOCK = 1

    def __str__(self):
        match self:
            case self.OPEN_LOCK:
                return "open"
            case self.CLOSE_LOCK:
                return "close"