from datetime import datetime

from face_recognition_util.draw_face import Drawing
from util.program_codes import AuthorizationStatus, PicoEvents


class Security:
    def __init__(self):
        self._draw = Drawing()

    def drawing_based_on_authorization(self, person_authorization: AuthorizationStatus, draw,
                                       face_location, person_name):
        match person_authorization:
            case AuthorizationStatus.AUTHORIZED:
                self._draw.draw_face_box(draw, face_location, person_name, "green")
            case AuthorizationStatus.TEMPORARY:
                self._draw.draw_face_box(draw, face_location, person_name, "yellow")
            case AuthorizationStatus.NOT_AUTHORIZED:
                self._draw.draw_face_box(draw, face_location, person_name, "blue")
            case _:
                self._draw.draw_face_box(draw, face_location, "ACTION UNKNOWN", "black")

    @classmethod
    def lock_action_based_on_authorization(cls, detected_people, mqtt):
        authorized = False
        for person in detected_people:
            match person.authorization:
                case AuthorizationStatus.AUTHORIZED:
                    authorized = True
                    break
                case AuthorizationStatus.TEMPORARY:
                    timestamp_format = "%Y-%m-%d %H:%M:%S"
                    person_timestamp = datetime.strptime(person.access_remaining_date_time, timestamp_format)
                    if person_timestamp >= datetime.today():
                        authorized = True
                        break
                case AuthorizationStatus.NOT_AUTHORIZED:
                    pass

        if authorized:
            mqtt.send_message(str(PicoEvents.OPEN_LOCK), "magnetic_lock")
        else:
            mqtt.send_message(str(PicoEvents.CLOSE_LOCK), "magnetic_lock")