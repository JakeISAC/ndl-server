import uuid

from API.api import API
from core.face_detection import FaceDetection
from database.db_operations import DatabaseOperations
from domains.people import Person
from face_recognition_util.encode_faces import EncodeFaces
from util.program_codes import AuthorizationStatus

from flask import Flask, request
from flask_socketio import SocketIO, emit

if __name__ == '__main__':
    # new_encode = EncodeFaces("C:\\Users\\jakub\\PycharmProjects\\ndl\\authorized_faces\\images\\mikhail")
    # encode = new_encode.generate_encodings_from_file()
    # person = Person(id=uuid.uuid4(), name="Mikhail Ushakov",
    #                 images_path="C:\\Users\\jakub\\PycharmProjects\\ndl\\authorized_faces\\images\\mikhail",
    #                 authorization=AuthorizationStatus.AUTHORIZED, face_encodings=encode)
    # person.add(DatabaseOperations())
    # print(encode)

    api = API()
    api.run()

    face_detection = FaceDetection()
    face_detection.start()
