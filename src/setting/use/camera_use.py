from ...library.camera.camera import Camera
from ...setting.setting import Setting

class camera_use():
    def __init__(self):
        self.setting = Setting()
        self.camera_dat = self.setting.camera_data

        self.camera = Camera()

    def camera_open(self):
        self.cap = self.camera.camera_open(self.camera_dat["index"])

    def camera_frame_get(self):
        frame = self.camera.frame_get(self.cap)
        return frame