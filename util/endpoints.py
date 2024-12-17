from dataclasses import dataclass


@dataclass(frozen=True)
class Endpoints:
    AUTHORIZED_IMAGES_PATH = "./authorized_faces/images/"

    # People Database
    KEYSPACE_MEMBER = "face_recognition"
    MEMBER_TABLE = "people"
    # User Database
    KEYSPACE_USERS = "users"
    USERS_TABLE = "users"
    # Session Database
    KEYSPACE_SESSION = "session"
    SESSION_TABLE = "tokens"
    # RFID Database
    KEYSPACE_RFID = "rfid"
    RFID_TABLE = "uid"

    # security
    PRIVATE_KEY_PATH = "./dh-keys/local/private_key.pem"
    PUBLIC_KEY_PATH = "./dh-keys/local/public_key.pem"

    # MQTT
    MQTT_USERNAME = "server"
    MQTT_PASSWORD = "ndl@group3"
