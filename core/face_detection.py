import cv2
import face_recognition
import numpy as np
from PIL import ImageDraw, Image
from picamera2 import Picamera2, Preview

from API.mqtt import MQTTServer
from face_recognition_util.compare_faces import CompareFaces
from database.faces_db import DbOperationsPeople
from face_recognition_util.draw_face import Drawing
from security.security import Security


class FaceDetection:
    def __init__(self, mqtt: MQTTServer):
        self._cam = Picamera2()
        self._video_box_name = "Face Detection"
        self._model = "hog"
        self._threshold = 0.9
        self._authorized_people = DbOperationsPeople().get_all()
        self._draw = Drawing()
        self._security = Security()
        self._mqtt = mqtt

    def start(self):
        self._cam.start()
        while True:
            pil_image = self._cam.capture_image()
            rgb_image = pil_image.convert('RGB')
            frame = np.array(rgb_image)
            if not frame.any():
                continue

            face_locations = face_recognition.face_locations(frame, model=self._model)
            if face_locations:
                detected_people_authorization = []

                face_encodings = face_recognition.face_encodings(frame, face_locations)
                image = Image.fromarray(frame)
                draw = ImageDraw.Draw(image)

                for face_location, face_encoding in zip(face_locations, face_encodings):
                    face_detected = False
                    for person in self._authorized_people:
                        compare = CompareFaces(person.face_encodings, face_encoding)
                        if self._assume_match(compare.compare_faces()):
                            # TODO: Fully implement this in the Security module
                            self._security.drawing_based_on_authorization(person.authorization, draw,
                                                                          face_location, person.name)
                            detected_people_authorization.append(person)
                            face_detected = True
                            break
                    if not face_detected:
                        self._draw.draw_face_box(draw, face_location, "unknown person", "red")

                # send the mqtt message based on person authorization
                self._security.lock_action_based_on_authorization(detected_people_authorization, self._mqtt)
                cv2.imshow(self._video_box_name, np.array(image))
            else:
                cv2.imshow(self._video_box_name, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def _assume_match(self, array: list[bool], threshold: int = None):
        if threshold is None:
            threshold = self._threshold
        array_len = len(array)
        true_occurrences = 0
        for x in array:
            if x:
                true_occurrences += 1
        return (true_occurrences / array_len) >= threshold