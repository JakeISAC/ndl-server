import os
import face_recognition
from util.endpoints import Endpoints


class EncodeFaces:
    def __init__(self, path):
        self._path = path
        self._model = "hog"
        self._paths = Endpoints()

    def encode_face_file(self):
        encodings = []

        if os.path.isdir(self._path):
            for filepath in os.listdir(self._path):
                name = str(filepath)
                image_path = os.path.join(self._path, name)
                image = face_recognition.load_image_file(image_path)

                face_locations = face_recognition.face_locations(image, model=self._model)
                face_encodings = face_recognition.face_encodings(image, face_locations)

                for encoding in face_encodings:
                    encodings.append(encoding)
        else:
            image = face_recognition.load_image_file(self._path)

            face_locations = face_recognition.face_locations(image, model=self._model)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            for encoding in face_encodings:
                encodings.append(encoding)

        return encodings




