import cv2 as cv
import numpy as np

class Camera():
    def __init__(self):
        pass

    def camera_open(self, camera_num):
        cap = cv.VideoCapture(camera_num)
        if False == cap.isOpened():
            raise ValueError("カメラが開けませんでした。")
        return cap

    def frame_get(self, cap):
        ret, frame = cap.read()
        if False == ret:
            raise ValueError("カメラ画像が取得できませんでした。")
        return frame