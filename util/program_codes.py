from enum import Enum


class AuthorizationStatus(Enum):
    AUTHORIZED = 0
    PENDING = 1
    NOT_AUTHORIZED = 2