from typing import Any

import face_recognition
from numpy import ndarray, dtype
from logs.logs import Logs


class CompareFaces:
    def __init__(self, source_face_encodings: ndarray[Any, dtype], face_to_check_encodings: ndarray[Any, dtype]):
        self._source = source_face_encodings
        self._to_check = face_to_check_encodings
        self._tolerance = 0.65
        self._logger = Logs().get_logger()

    def compare_faces(self):
        self._logger.info("Attempting to compare faces")
        try:
            return face_recognition.compare_faces(self._source, self._to_check, tolerance=self._tolerance)
        except Exception as e:
            self._logger.exception(f"Failed to compare faces: {e}")
            return None