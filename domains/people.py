import uuid
from dataclasses import dataclass
from datetime import datetime

from database.members_db import DbOperationsMembers
from util.program_codes import AuthorizationStatus


@dataclass
class Person:
    id: uuid
    name: str
    images_path: str
    authorization: AuthorizationStatus
    access_remaining_date_time: str
    face_encodings: bytes.hex

    def add(self, db: DbOperationsMembers):
        db.upload_to_db(self)
