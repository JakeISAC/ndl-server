from logs.logs import Logs


class Drawing:
    def __init__(self):
        self._logger = Logs().get_logger()

    def draw_face_box(self, draw, bounding_box, name, color):
        self._logger.trace("Attempting to draw a face bounding box")
        try:
            top, right, bottom, left = bounding_box
            draw.rectangle(((left, top), (right, bottom)), outline=color)
            text_left, text_top, text_right, text_bottom = draw.textbbox(
                (left, bottom), name
            )
            draw.rectangle(
                ((text_left, text_top), (text_right, text_bottom)),
                fill=color,
                outline=color,
            )
            draw.text(
                (text_left, text_top),
                name,
                fill="white",
            )
            self._logger.debug("Face bounding box drawn successfully")
        except Exception as e:
            self._logger.exception(f"Failed to draw a face bounding box: {e}")
