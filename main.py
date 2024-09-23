import uuid

from core.face_detection import FaceDetection
from database.db_operations import DatabaseOperations
from domains.people import Person
from face_recognition_util.encode_faces import EncodeFaces
from util.program_codes import AuthorizationStatus

if __name__ == '__main__':
    # new_encode = EncodeFaces("C:\\Users\\jakub\\PycharmProjects\\ndl\\authorized_faces\\images\\mikhail")
    # encode = new_encode.generate_encodings_from_file()
    # person = Person(id=uuid.uuid4(), name="Mikhail Ushakov",
    #                 images_path="C:\\Users\\jakub\\PycharmProjects\\ndl\\authorized_faces\\images\\mikhail",
    #                 authorization=AuthorizationStatus.AUTHORIZED, face_encodings=encode)
    # person.add(DatabaseOperations())
    # print(encode)

    face_detection = FaceDetection()
    face_detection.start()
