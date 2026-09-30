import cv2 as cv
import csv
from pathlib import Path

class data_set():
    def __init__(self):
        self.data_dir = Path(__file__).resolve().parents[3] / "data"

        self.reader = []
        self.jpg_list = []
        self.labels_list = []
        self.jpg_data = []
        self.labels_data = []

    def compute(self, mode):
        self.open_file(mode)
        self.save_csv_data()
        self.save_jpg_data()
        self.save_label_data()
        return self.get_data()
        
    def open_file(self, mode):
        if mode == 0: # train
            self.data = "train_data"
        elif mode == 1: # test
            self.data = "test_data"
        csv_path = self.data_dir / self.data / "labels.csv"
        with open(csv_path, "r", encoding="utf-8", newline="") as file:
            self.reader = list(csv.reader(file))

    # ///////////////////////////////////////////////////////////////////////
    #   データの取得
    # ///////////////////////////////////////////////////////////////////////

    def save_csv_data(self):
        for row in self.reader:
            self.jpg_list.append(row[0])
            self.labels_list.append(row[1])
    def save_jpg_data(self):
        image_dir = self.data_dir / self.data / "images"

        for i in range(len(self.jpg_list)):
            image_path = image_dir / self.jpg_list[i]
            self.jpg_data.append(cv.imread(str(image_path)))
    def save_label_data(self):
        for i in range(len(self.labels_list)):
            self.labels_data.append(int(self.labels_list[i]))

    def get_data(self):
        return self.jpg_data, self.labels_data