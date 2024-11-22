import uuid

from API.mqtt import MQTTServer
from core.face_detection import FaceDetection
from database.faces_db import DbOperationsPeople
from domains.people import Person
from face_recognition_util.encode_faces import EncodeFaces
from util.program_codes import AuthorizationStatus

# "%Y-%m-%d %H:%M:%S"

if __name__ == '__main__':
    # new_encode = EncodeFaces("/home/ndl/ndl/authorized_faces/images/anastasija")
    # encode = new_encode.generate_encodings_from_file()
    # person = Person(id=uuid.uuid4(), name="Anastasija Ananjeva",
    #                 images_path="/home/ndl/ndl/authorized_faces/images/anastasija",
    #                 authorization=AuthorizationStatus.TEMPORARY, face_encodings=encode, access_remaining_date_time="2024-11-08 12:00:00")
    # person.add(DatabaseOperations())
    # print(encode)

    mqtt = MQTTServer()
    mqtt.run()

    # face_detection = FaceDetection(mqtt)
    # face_detection.start()

