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

        return tensor

    def crop(self, frame, hand_result, width, height):
        if hand_result.hand_landmarks:
            hand_landmarks = hand_result.hand_landmarks[0]

            x_min = min(
                landmark.x for landmark in hand_landmarks
            )
            x_max = max(
                landmark.x for landmark in hand_landmarks
            )
            y_min = min(
                landmark.y for landmark in hand_landmarks
            )
            y_max = max(
                landmark.y for landmark in hand_landmarks
            )

            frame_height, frame_width = frame.shape[:2]

            x_min = int(x_min * frame_width)
            x_max = int(x_max * frame_width)
            y_min = int(y_min * frame_height)
            y_max = int(y_max * frame_height)

            # 画像範囲内に収める
            x_min = max(0, min(x_min, frame_width))
            x_max = max(0, min(x_max, frame_width))
            y_min = max(0, min(y_min, frame_height))
            y_max = max(0, min(y_max, frame_height))

            # 切り出し範囲が存在するか確認
            if x_min < x_max and y_min < y_max:
                cropped_frame = frame[
                    y_min:y_max,
                    x_min:x_max
                ]

                return cv.resize(
                    cropped_frame,
                    (width, height)
                )

        return cv.resize(
            frame,
            (width, height)
        )

    def print_frame_dark(self, frame):
        dark_frame = np.zeros_like(frame)
        return dark_frame