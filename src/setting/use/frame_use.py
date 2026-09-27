from src.library.frame.frame import Frame, FlipDirection
from src.setting.setting import Setting


class Frame_use:
    def __init__(self):
        self.frame = Frame()
        self.setting = Setting()
        self.frame_data = self.setting.frame_data

    def resize_(self, frame):
        size = self.frame_data["size"]

        return self.frame.resize(
            frame,
            size["width"],
            size["height"]
        )

    def flip_(self, frame):
        direction = {
            "vertical": FlipDirection.VERTICAL,
            "horizontal": FlipDirection.HORIZONTAL,
            "both": FlipDirection.BOTH
        }.get(self.frame_data["flip"])

        if direction is None:
            return frame

        return self.frame.flip(frame, direction)

    def image_(self, frame):
        return self.frame.image(frame)

    def print_frame_dark_(self, frame):
        return self.frame.print_frame_dark(frame)