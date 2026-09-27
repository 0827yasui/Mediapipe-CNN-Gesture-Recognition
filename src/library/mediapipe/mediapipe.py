from pathlib import Path

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

PROJECT_DIR = Path(__file__).resolve().parents[3]
MODEL_DIR = PROJECT_DIR / "model"

HAND_LANDMAEKER_PATH = MODEL_DIR / "hand_landmarker.task"
FACE_LANDMAEKER_PATH = MODEL_DIR / "face_landmarker.task"

class Mediapipe():
    def __init__(self):
        # /////////////////////////
        #   デバッグメッセージ
        # /////////////////////////
        pass

# /////////////////////////////////////////
#   オプション
# /////////////////////////////////////////

    def hand_option_setup(
            self,
            num_hands_,
            min_hand_detection_confidence_,
            min_hand_presence_confidence_,
            min_tracking_confidence_
        ):
        options = vision.HandLandmarkerOptions(
            base_options = python.BaseOptions(
                model_asset_path = str(HAND_LANDMAEKER_PATH)
            ),
            running_mode = vision.RunningMode.VIDEO,
            num_hands = num_hands_,
            min_hand_detection_confidence = min_hand_detection_confidence_,
            min_hand_presence_confidence = min_hand_presence_confidence_,
            min_tracking_confidence = min_tracking_confidence_
        )
        landmarker = vision.HandLandmarker.create_from_options(options)
        return landmarker

    def face_option_setup(
            self,
            num_faces_,
            min_face_detection_confidence_,
            min_face_presence_confidence_,
            min_tracking_confidence_
        ):
        options = vision.FaceLandmarkerOptions(
            base_options=python.BaseOptions(
                model_asset_path = str(FACE_LANDMAEKER_PATH)
            ),
            running_mode=vision.RunningMode.VIDEO,
            num_faces = num_faces_,
            min_face_detection_confidence = min_face_detection_confidence_,
            min_face_presence_confidence = min_face_presence_confidence_,
            min_tracking_confidence = min_tracking_confidence_
        )
        face_landmarker = vision.FaceLandmarker.create_from_options(options)
        return face_landmarker

    def hand_detect(self, landmarker, image, timestamp_ms):
        return landmarker.detect_for_video(image, timestamp_ms)

    def face_detect(self, landmarker, image, timestamp_ms):
        return landmarker.detect_for_video(image, timestamp_ms)