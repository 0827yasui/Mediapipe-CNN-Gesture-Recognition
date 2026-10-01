import cv2 as cv

from src.setting.use.mediapipe_use import Mediapipe_use
from src.library.frame.draw import Draw
from src.setting.use.frame_use import Frame_use

from src.library.data.file_open.jpg_input import JPG_Input

class HandImage:
    def __init__(self):
        self.draw = Draw()
        self.frame = Frame_use()
        self.mediapipe = Mediapipe_use()
        self.jpg_input = JPG_Input()

    def create(self, frame, timestamp_ms, label):
        frame = self.frame.resize_(frame)
        frame = self.frame.flip_(frame)

        image = self.frame.image_(frame)
        hand_result = self.mediapipe.face_detect(frame, timestamp_ms)
        image = self.frame.print_frame_dark_(frame)

        self.draw.hand_landmarkers_dot(image, hand_result)
        self.draw.hand_landmarkers_line(image, hand_result)

        self.jpg_input.input(image, label)

        return image
