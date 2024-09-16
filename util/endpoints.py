from dataclasses import dataclass


@dataclass(frozen=True)
class Endpoints:
    AUTHORIZED_IMAGES_PATH = "../authorized_faces/images/"
    KEYSPACE = "face_recognition"
    USER_TABLE = "people"
