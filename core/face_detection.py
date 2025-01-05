import random
import time

import face_recognition
import numpy as np
# import cv2
from PIL import ImageDraw, Image

from core.security import Security
from database.members_db import DbOperationsMembers
from face_recognition_util.compare_faces import CompareFaces
from face_recognition_util.draw_face import Drawing
from mqtt.mqtt import MQTTServer


# from picamera2 import Picamera2


class FaceDetection:
    def __init__(self, mqtt: MQTTServer):
        # self._cam = Picamera2()
        self._video_box_name = "Face Detection"
        self._model = "hog"
        self._threshold = 0.9
        self._authorized_people = DbOperationsMembers().get_all()
        self._draw = Drawing()
        self._security = Security()
        self._mqtt = mqtt
        # TODO: remove before production
        self._test_images = ['authorized_faces/images/anastasija/photo_2024-09-24_09-09-44.jpg',
                             'authorized_faces/images/anastasija/photo_2024-09-24_09-09-44.jpg',
                             'authorized_faces/images/jakub/photo_2024-09-15_19-58-56.jpg',
                             'authorized_faces/images/masha/img_1.png',
                             'authorized_faces/images/anastasija/photo_2024-09-24_09-09-44.jpg']

    def run(self):
        # self._cam.start()
        while True:
            # pil_image = self._cam.capture_image()
            pil_image = Image.open(random.choice(self._test_images))
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
                    face_recognised = False
                    for person in self._authorized_people:
                        compare = CompareFaces(person.face_encodings, face_encoding)
                        if self._assume_match(compare.compare_faces()):
                            # TODO: Fully implement this in the Security module
                            self._security.face_bounding_box_authorization(person.authorization, draw,
                                                                           face_location, person.name)
                            detected_people_authorization.append(person)
                            face_recognised = True
                            break
                    if not face_recognised:
                        self._draw.draw_face_box(draw, face_location, "unknown person", "red")

                # send the mqtt message based on person authorization
                self._security.lock_action_based_on_authorization(detected_people_authorization, self._mqtt)
                # cv2.imshow(self._video_box_name, np.array(image))
            else:
                # cv2.imshow(self._video_box_name, frame)
                pass

            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            time.sleep(5)

        # cv2.destroyAllWindows()

    def _assume_match(self, array: list[bool], threshold: int = None):
        if threshold is None:
            threshold = self._threshold
        array_len = len(array)
        true_occurrences = 0
        for x in array:
            if x:
                true_occurrences += 1
        return (true_occurrences / array_len) >= threshold
