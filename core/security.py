import json
from datetime import datetime
from typing import List

from domains.member import Member
from face_recognition_util.draw_face import Drawing
from util.codes.controller_codes import ControllerEvents
from util.codes.authorization_codes import AuthorizationStatus
from logs.logs import Logs


class Security:
    def __init__(self):
        self._draw = Drawing()
        self._logger = Logs().get_logger()

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

    def lock_action_based_on_authorization(self, detected_people: List[Member], mqtt):
        try:
            if not detected_people:
                mqtt.send_message(str(ControllerEvents.CLOSE_LOCK), "magnetic_lock")
            authorized = False
            found_member = None
            for member in detected_people:
                match member.authorization:
                    case AuthorizationStatus.AUTHORIZED:
                        authorized = True
                        found_member = member
                        self._logger.debug(f"Found authorized member {member.name}")
                        break
                    case AuthorizationStatus.TEMPORARY:
                        timestamp_format = "%Y-%m-%d %H:%M:%S"
                        member_timestamp = datetime.strptime(member.access_remaining_date_time, timestamp_format)
                        if member_timestamp >= datetime.today():
                            authorized = True
                            found_member = member
                            self._logger.debug(f"Found temporarily authorized member {member.name}")
                            break
                    case AuthorizationStatus.NOT_AUTHORIZED:
                        self._logger.debug(f"Found not authorized member {member.name}")
                        continue

            if authorized:
                mqtt.send_message(str(ControllerEvents.OPEN_LOCK), "magnetic_lock")
                mqtt.send_message(json.dumps(found_member.to_dict()), "last_active_person")
            else:
                mqtt.send_message(str(ControllerEvents.CLOSE_LOCK), "magnetic_lock")

        except Exception as e:
            self._logger.exception(f"Could not determine the user authorization: {e}")
            mqtt.send_message(str(ControllerEvents.CLOSE_LOCK), "magnetic_lock")