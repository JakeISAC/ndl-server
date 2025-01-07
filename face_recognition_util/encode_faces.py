import os

import face_recognition
import numpy as np
from PIL import Image

from logs.logs import Logs
from util.endpoints import Endpoints


class EncodeFaces:
    def __init__(self, path):
        self._path = path
        self._model = "hog"
        self._paths = Endpoints()
        self._logger = Logs().get_logger()

    def generate_encodings_from_file(self):
        self._logger.trace("Attempting to generate face encodings")
        try:
            encodings = []
            if os.path.isdir(self._path):
                for filename in os.listdir(self._path):
                    image_path = os.path.join(self._path, str(filename))
                    frame = self._get_image(image_path)
                    try:
                        face_locations = face_recognition.face_locations(frame, model=self._model)
                        face_encodings = face_recognition.face_encodings(frame, face_locations)
                    except Exception as e:
                        self._logger.exception(f"Failed to find face locations: {e}")
                        return None

                    for encoding in face_encodings:
                        encodings.append(encoding)
            else:
                frame = self._get_image(self._path)
                try:
                    face_locations = face_recognition.face_locations(frame, model=self._model)
                    face_encodings = face_recognition.face_encodings(frame, face_locations)
                except Exception as e:
                    self._logger.exception(f"Failed to find face locations: {e}")
                    return None

                for encoding in face_encodings:
                    encodings.append(encoding)

            self._logger.info("Successfully encode faces of the new user")
            return encodings
        except Exception as e:
            self._logger.exception(f"Failed to generate face encodings: {e}")
            return None

    def _get_image(self, path):
        try:
            image = Image.open(path)
            image_rgb = image.convert("RGB")
            frame = np.array(image_rgb)
            if not frame.any():
                raise Exception("No frame received")
            return frame
        except Exception as e:
            self._logger.exception(f"Failed to get image: {e}")
            return None
