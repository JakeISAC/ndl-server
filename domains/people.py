import uuid
from dataclasses import dataclass
from datetime import datetime

from database import db_operations
from util.program_codes import AuthorizationStatus


@dataclass
class Person:
    id: uuid
    name: str
    images_path: str
    authorization: AuthorizationStatus
    access_remaining_date_time: str
    face_encodings: bytes.hex

    def add(self, db: db_operations.DatabaseOperations):
        db.upload_to_db(self)
