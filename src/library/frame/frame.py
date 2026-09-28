import cv2 as cv
import mediapipe as mp
import numpy as np
from enum import Enum
import torch

class FlipDirection(Enum):
    VERTICAL = 0
    HORIZONTAL = 1
    BOTH = -1

class Frame():
    def __init__(self):
        pass

    def flip(self, frame, direction):
        return cv.flip(frame, direction.value)

    def resize(self, frame, width, height):
        return cv.resize(frame, (width, height))

    def convert(self, frame, code):
        return cv.cvtColor(frame, code)

    def image(self, frame):
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        return mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )
    
    def tensor(self, frame, width, height):
        resized = cv.resize(
            frame,
            (width, height)
        )

        rgb = cv.cvtColor(
            resized,
            cv.COLOR_BGR2RGB
        )

        tensor = torch.from_numpy(
            rgb
        ).permute(
            2, 0, 1
        ).float() / 255.0

        tensor = tensor.unsqueeze(0)

        return tensor

    def print_frame_dark(self, frame):
        dark_frame = np.zeros_like(frame)
        return dark_frame