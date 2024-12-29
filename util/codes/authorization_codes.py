from enum import Enum


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

    @staticmethod
    def from_string(code: str):
        match code:
            case "authorized":
                return AuthorizationStatus.AUTHORIZED
            case "not_authorized":
                return AuthorizationStatus.NOT_AUTHORIZED
            case "temporary":
                return AuthorizationStatus.TEMPORARY