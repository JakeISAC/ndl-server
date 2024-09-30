from dataclasses import dataclass


@dataclass(frozen=True)
class Endpoints:
    AUTHORIZED_IMAGES_PATH = "./authorized_faces/images/"
    KEYSPACE = "face_recognition"
    USER_TABLE = "people"
    # security
    PRIVATE_KEY_PATH = "./dh-keys/local/private_key.pem"
    PUBLIC_KEY_PATH = "./dh-keys/local/public_key.pem"
