import json
import uuid
from dataclasses import dataclass
from util.program_codes import AuthorizationStatus


@dataclass
class Member:
    id: uuid
    name: str
    images_path: str
    authorization: AuthorizationStatus
    access_remaining_date_time: str
    face_encodings: bytes.hex

    def validate(self):
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
        return True

    @staticmethod
    def extract_member(json_data):
        data = json.loads(json_data)
        return Member(
            id=uuid.uuid4(),
            name=data["name"],
            images_path=data["images_path"],
            authorization=data["authorization"],
            access_remaining_date_time=data["access_remaining_date_time"] if data["access_remaining_date_time"] else None,
            face_encodings=None
        )

    def to_json(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "images_path": str(self.images_path),
            "authorization": str(self.authorization),
            "access_remaining": str(self.access_remaining_date_time)
        }