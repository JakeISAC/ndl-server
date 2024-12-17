import json
from datetime import datetime
from typing import List

from domains.member import Member
from face_recognition_util.draw_face import Drawing
from util.program_codes import AuthorizationStatus, ControllerEvents


class Security:
    def __init__(self):
        self._draw = Drawing()

    def face_bounding_box_authorization(self, person_authorization: AuthorizationStatus, draw,
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
    def lock_action_based_on_authorization(cls, detected_people: List[Member], mqtt):
        if not detected_people:
            mqtt.send_message(str(ControllerEvents.CLOSE_LOCK), "magnetic_lock")
        authorized = False
        found_member = None
        for member in detected_people:
            match member.authorization:
                case AuthorizationStatus.AUTHORIZED:
                    found_member = member
                    authorized = True
                    break
                case AuthorizationStatus.TEMPORARY:
                    found_member = member
                    timestamp_format = "%Y-%m-%d %H:%M:%S"
                    member_timestamp = datetime.strptime(member.access_remaining_date_time, timestamp_format)
                    if member_timestamp >= datetime.today():
                        authorized = True
                        break
                case AuthorizationStatus.NOT_AUTHORIZED:
                    pass

        if authorized:
            mqtt.send_message(str(ControllerEvents.OPEN_LOCK), "magnetic_lock")
            mqtt.send_message(json.dumps(found_member.to_dict()), "last_active_person")
        else:
            mqtt.send_message(str(ControllerEvents.CLOSE_LOCK), "magnetic_lock")