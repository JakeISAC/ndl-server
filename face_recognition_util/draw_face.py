class Drawing:
    @classmethod
    def draw_face_box(cls, draw, bounding_box, name, color):
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