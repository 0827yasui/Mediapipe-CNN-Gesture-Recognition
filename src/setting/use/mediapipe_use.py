from ...library.mediapipe.mediapipe import Mediapipe
from ...setting.setting import Setting

class Mediapipe_use():
    def __init__(self):
        self.setting = Setting()
        self.Mediapipe_dat = self.setting.Mediapipe_data

        self.Mediapipe = Mediapipe()

        self.hand_create()
        self.face_create()

    def hand_create(self):
        hand = self.Mediapipe_dat["hand"]

        self.hand_landmarker = self.Mediapipe.hand_option_setup(
            num_hands_=hand["Number_of_hands_"],
            min_hand_detection_confidence_=hand["min_hand_detection_confidence_"],
            min_hand_presence_confidence_=hand["min_hand_presence_confidence_"],
            min_tracking_confidence_=hand["min_tracking_confidence_"]
        )

    def face_create(self):
        face = self.Mediapipe_dat["face"]

        self.face_landmarker = self.Mediapipe.face_option_setup(
            num_faces_=face["Number_of_faces_"],
            min_face_detection_confidence_=face["min_face_detection_confidence_"],
            min_face_presence_confidence_=face["min_face_presence_confidence_"],
            min_tracking_confidence_=face["min_tracking_confidence_"]
        )

    def hand_detect(self, image, timestamp_ms):
        return self.Mediapipe.hand_detect(
            self.hand_landmarker,
            image,
            timestamp_ms
        )

    def face_detect(self, image, timestamp_ms):
        return self.Mediapipe.face_detect(
            self.face_landmarker,
            image,
            timestamp_ms
        )