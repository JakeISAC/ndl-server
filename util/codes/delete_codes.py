from enum import Enum

class DeleteCodes(Enum):
    OK = 0
    FAILED = 1

    def __str__(self):
        match self:
            case self.OK:
                return "OK"
            case self.FAILED:
                return "FAILED"