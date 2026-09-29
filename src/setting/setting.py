from pathlib import Path

from .yaml_read.yaml_read import YAML_READ

PROJECT_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_DIR / "config"

CAMERA_YAML_PATH = CONFIG_DIR / "camera_dat.yaml"
FRAME_YAML_PATH = CONFIG_DIR / "frame_dat.yaml"
MEDIAPIPE_YAML_PATH = CONFIG_DIR / "mediapipe_dat.yaml"
CNN_YAML_PATH = CONFIG_DIR / "CNN_dat.yaml"
LEARNING_YAML_PATH = CONFIG_DIR / "learning.yaml"


class Setting():
    def __init__(self):
        self.yaml_read = YAML_READ()
        self.camera_data = self.yaml_read.Set_Yaml(CAMERA_YAML_PATH)
        self.frame_data = self.yaml_read.Set_Yaml(FRAME_YAML_PATH)
        self.Mediapipe_data = self.yaml_read.Set_Yaml(MEDIAPIPE_YAML_PATH)
        self.CNN_data = self.yaml_read.Set_Yaml(CNN_YAML_PATH)
        self.learning_data = self.yaml_read.Set_Yaml(LEARNING_YAML_PATH)
