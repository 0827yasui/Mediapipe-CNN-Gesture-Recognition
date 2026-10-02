from src.library.frame.frame import Frame, FlipDirection
from src.setting.setting import Setting

class Frame_use:
    def __init__(self, mode):
        self.frame = Frame()
        self.setting = Setting()
        self.frame_data_direction = self.setting.frame_data
        self.frame_data_size = self.setting.CNN_data

    def resize_(self, frame):
        size = self.frame_data_size["model"]["input"]

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
        }.get(self.frame_data_direction["flip"])

        if direction is None:
            return frame

        return self.frame.flip(frame, direction)

    def image_(self, frame):
        return self.frame.image(frame)

    def print_frame_dark_(self, frame):
        return self.frame.print_frame_dark(frame)

    def tensor_(self, frame):
        size = self.frame_data_size["model"]["input"]

        return self.frame.tensor(
            frame,
            size["width"],
            size["height"]
        )

    def crop_(self, frame, hand_landmarks):
        size = self.frame_data_size["model"]["input"]

        return self.frame.crop(
            frame,
            hand_landmarks,
            size["width"],
            size["height"]
        )