import uuid

from API.mqtt import MQTTServer
from API.pico_api import API
from core.face_detection import FaceDetection
from security.aes import AESecurity
from security.dh import generate_keys, get_public_key
from database.db_operations import DatabaseOperations
from domains.people import Person
from face_recognition_util.encode_faces import EncodeFaces
from util.program_codes import AuthorizationStatus, AesMode

from flask import Flask, request
from flask_socketio import SocketIO, emit

if __name__ == '__main__':
    # new_encode = EncodeFaces("/home/ndl/ndl/authorized_faces/images/masha")
    # encode = new_encode.generate_encodings_from_file()
    # person = Person(id=uuid.uuid4(), name="Masha Ushakova",
    #                 images_path="/home/ndl/ndl/authorized_faces/images/masha",
    #                 authorization=AuthorizationStatus.AUTHORIZED, face_encodings=encode)
    # person.add(DatabaseOperations())
    # print(encode)

    mqtt = MQTTServer()
    mqtt.run()

    face_detection = FaceDetection()
    face_detection.start()

    # here I use mine to just verify that it works
    # peer_public_key = get_public_key()
    # aes = AESecurity(AesMode.PICO)
    # text = b"My name is Jakub. HAHHAHAHAHA"
    # cipher, tag, nonce = aes.encrypt(text)
    # print(f"{cipher}")
    # print(f"{aes.decrypt(cipher, tag, nonce)}")

