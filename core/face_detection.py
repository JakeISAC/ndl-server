import cv2
import face_recognition
import numpy as np
import subprocess
from PIL import ImageDraw, Image
from picamera2 import Picamera2

from logs.logs import Logs
from mqtt.mqtt import MQTTServer
from face_recognition_util.compare_faces import CompareFaces
from database.members_db import DbOperationsMembers
from face_recognition_util.draw_face import Drawing
from core.security import Security


class FaceDetection:
    def __init__(self, mqtt: MQTTServer):
        self._logger = Logs().get_logger()
        self._member_db = DbOperationsMembers().get_all()
        self._cam = Picamera2()
        self._video_box_name = "Face Detection"
        self._model = "hog"
        self._threshold = 0.9
        self._base_people = self._member_db.get_all()
        self._authorized_people = self._base_people
        self._draw = Drawing()
        self._security = Security()
        self._mqtt = mqtt

    def run(self):
        try:
            self._cam.start()
            self._logger.debug("Started camera")
            while True:
                pil_image = self._cam.capture_image()
                rgb_image = pil_image.convert('RGB')
                self._logger.debug("Image captured")
                frame = np.array(rgb_image)
                if not frame.any():
                    self._logger.error("Failed to create an array from captured frame")
                    continue

                try:
                    face_locations = face_recognition.face_locations(frame, model=self._model)
                except Exception as e:
                    self._logger.exception(f"Failed to find face locations: {e}")
                    continue

                if face_locations:
                    # Since a user can update a status or delete a member we need to always get new authorized people
                    try:
                        self._authorized_people = self._member_db.get_all()
                        self._logger.debug("Authorized people updated")
                    except Exception as e:
                        self._authorized_people = self._base_people
                        self._logger.debug(f"Base people restored --- initial state when server started: {e}")
                        
                    self._logger.debug("Faces found")
                    detected_people_authorization = []

                    try:
                        face_encodings = face_recognition.face_encodings(frame, face_locations)
                    except Exception as e:
                        self._logger.exception(f"Failed to encode faces: {e}")
                        continue

                    self._logger.debug("Faces encoded")
                    image = Image.fromarray(frame)
                    draw = ImageDraw.Draw(image)

                    for face_location, face_encoding in zip(face_locations, face_encodings):
                        face_recognised = False
                        for person in self._authorized_people:
                            compare = CompareFaces(person.face_encodings, face_encoding)
                            if self._assume_match(compare.compare_faces()):
                                self._security.face_bounding_box_authorization(person.authorization, draw,
                                                                            face_location, person.name)
                                detected_people_authorization.append(person)
                                face_recognised = True
                                break
                        if not face_recognised:
                            self._draw.draw_face_box(draw, face_location, "unknown person", "red")

                    # send the mqtt message based on person authorization
                    self._security.lock_action_based_on_authorization(detected_people_authorization, self._mqtt)
                    cv2.imshow(self._video_box_name, np.array(image))
                else:
                    cv2.imshow(self._video_box_name, frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self._logger.info("Keyboard interauption deteted, exiting")
                    break

            cv2.destroyAllWindows()
        except Exception as e:
            self._logger.critical(f"Exiting the program and rebooting computer: {e}")
            subprocess.run(["reboot", "-i"])

    def _assume_match(self, array: list[bool], threshold: int = None):
        try:
            if threshold is None:
                threshold = self._threshold
            array_len = len(array)
            true_occurrences = 0
            for x in array:
                if x:
                    true_occurrences += 1
            return (true_occurrences / array_len) >= threshold
        except Exception as e:
            self._logger.exception(f"Failed to check authorized face against found face: {e}")
            return None