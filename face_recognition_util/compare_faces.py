from typing import Any

import face_recognition
from numpy import ndarray, dtype


class CompareFaces:
    def __init__(self, source_face_encodings: ndarray[Any, dtype], face_to_check_encodings: ndarray[Any, dtype]):
        self._source = source_face_encodings
        self._to_check = face_to_check_encodings
        self._tolerance = 0.65

    def compare_faces(self):
        return face_recognition.compare_faces(self._source, self._to_check, tolerance=self._tolerance)