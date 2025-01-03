import json
import uuid
from dataclasses import dataclass

from logs.logs import Logs
from util.codes.authorization_codes import AuthorizationStatus


@dataclass
class Member:
    id: uuid
    name: str
    images_path: str
    authorization: AuthorizationStatus
    access_remaining_date_time: str
    face_encodings: bytes.hex

    def __post_init__(self):
        self._logger = Logs().get_logger()

    def validate(self):
        self._logger.trace("Attempting to validate Member struct")
        try:
            if type(self.id) != uuid.UUID:
                return False
            if type(self.name) != str:
                return False
            if type(self.images_path) != str:
                return False
            if type(self.authorization) != AuthorizationStatus:
                return False
            if type(self.access_remaining_date_time) != str:
                return False
            if type(self.face_encodings) != bytes.hex:
                return False
            self._logger.debug("Member struct validated successfully")
            return True
        except Exception as e:
            self._logger.exception(f"Failed to validate a Member: {e}")
            return False

    @staticmethod
    def extract_member(json_data):
        logger = Logs().get_logger()
        logger.trace("Attempting to serializing JSON to Member")
        try:
            data = json.loads(json_data)
            member = Member(
                id=uuid.uuid4(),
                name=data["name"],
                images_path=data["images_path"],
                authorization=data["authorization"],
                access_remaining_date_time=data["access_remaining_date_time"] if data["access_remaining_date_time"] else None,
                face_encodings=None
            )
            logger.debug(f"Member extracted successfully from JSON: {member}")
            return member
        except Exception as e:
            logger.exception(f"Failed to extract a Member from JSON data: {e}")
            return None

    def to_dict(self):
        self._logger.trace("Attempting to serialize Member to dict")
        try:
            member = {
                "id": str(self.id),
                "name": str(self.name),
                "images_path": str(self.images_path),
                "authorization": str(self.authorization),
                "access_remaining": str(self.access_remaining_date_time)
            }
            self._logger.debug(f"Member serialized to dict: {member}")
            return member
        except Exception as e:
            self._logger.exception(f"Failed to serialize Member to dict: {e}")
            return None
