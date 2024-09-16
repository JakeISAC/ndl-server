import cv2
import face_recognition
import numpy as np
from PIL import ImageDraw, Image

from face_recognition_util.compare_faces import CompareFaces
from database.db_operations import DatabaseOperations
from face_recognition_util.draw_face import Drawing
from util.program_codes import AuthorizationStatus


class FaceDetection:
    def __init__(self):
        self._video_capture = cv2.VideoCapture(0)
        self._video_box_name = "Face Detection"
        self._model = "hog"
        self._threshold = 0.9
        self._authorized_people = DatabaseOperations().get_all()
        self._draw = Drawing()


    def start(self):
        while self._video_capture.isOpened():
            ret, frame = self._video_capture.read()
            if not ret:
                break

            face_locations = face_recognition.face_locations(frame, model=self._model)
            if face_locations:
                face_encodings = face_recognition.face_encodings(frame, face_locations)

                image = Image.fromarray(frame)
                draw = ImageDraw.Draw(image)

                for face_location, face_encoding in zip(face_locations, face_encodings):
                    face_detected = False
                    for person in self._authorized_people:
                        compare = CompareFaces(person.face_encodings, face_encoding)
                        if self._assume_match(compare.compare_faces()):
                            self._action_based_on_authorization(person.authorization, draw, face_location, person.name)
                            face_detected = True
                            break
                    if not face_detected:
                        self._draw.draw_face_box(draw, face_location, "unknown person", "red")

                cv2.imshow(self._video_box_name, np.array(image))
            else:
                cv2.imshow(self._video_box_name, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self._video_capture.release()
        cv2.destroyAllWindows()

    def _assume_match(self, array: list[bool]):
        array_len = len(array)
        true_occurrences = 0
        for x in array:
            if x:
                true_occurrences += 1
        return (true_occurrences / array_len) >= self._threshold

    def _action_based_on_authorization(self, person_authorization: AuthorizationStatus, draw, face_location,
                                       person_name):
        match person_authorization:
            case AuthorizationStatus.AUTHORIZED:
                self._draw.draw_face_box(draw, face_location, person_name, "green")
            case AuthorizationStatus.PENDING:
                self._draw.draw_face_box(draw, face_location, person_name, "yellow")
            case AuthorizationStatus.NOT_AUTHORIZED:
                self._draw.draw_face_box(draw, face_location, person_name, "blue")
            case _:
                self._draw.draw_face_box(draw, face_location, "ACTION UNKNOWN", "black")
