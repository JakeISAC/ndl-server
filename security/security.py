from face_recognition_util.draw_face import Drawing
from util.program_codes import AuthorizationStatus


class Security:
    def __init__(self):
        self._draw = Drawing()

    def action_based_on_authorization(self, person_authorization: AuthorizationStatus, draw,
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