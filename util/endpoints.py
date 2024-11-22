from dataclasses import dataclass


@dataclass(frozen=True)
class Endpoints:
    AUTHORIZED_IMAGES_PATH = "./authorized_faces/images/"
    # People Database
    KEYSPACE_PEOPLE = "face_recognition"
    PEOPLE_TABLE = "people"
    # User Database
    KEYSPACE_USERS = "users"
    USERS_TABLE = "users"
    # security
    PRIVATE_KEY_PATH = "./dh-keys/local/private_key.pem"
    PUBLIC_KEY_PATH = "./dh-keys/local/public_key.pem"
    # MQTT
    MQTT_USERNAME = "server"
    MQTT_PASSWORD = "ndl@group3"
