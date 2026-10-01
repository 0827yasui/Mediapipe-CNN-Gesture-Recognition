import cv2 as cv
import csv
from pathlib import Path

class JPG_Input():
    def __init__(self, mode):
        self.data_dir = Path(__file__).resolve().parents[4] / "data"

        if mode == 0:       # train
            self.data = "train_data"
        elif mode == 1:     # test
            self.data = "test_data"

        self.image_dir = self.data_dir / self.data / "images"
        self.csv_path = self.data_dir / self.data / "labels.csv"

    def input(self, frame, label):
        file_name = self.create_file_name()
        image_path = self.image_dir / file_name

        cv.imwrite(str(image_path), frame)

        with open(
            self.csv_path,
            "a",
            encoding="utf-8",
            newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow([file_name, label])

    def create_file_name(self):
        number = len(list(self.image_dir.glob("*.jpg")))
        return f"{number:05d}.jpg"