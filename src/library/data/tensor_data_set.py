from src.library.data.file_open.jpg import data_set
from src.setting.use.frame_use import Frame_use


class Data():
    def __init__(self, mode):
        self.data_set = data_set()
        self.frame = Frame_use(mode)
        self.mode = mode

        self.jpg_data = []
        self.labels_data = []
        self.tensor_data = []
        self.tensor_labels = []

    def compute(self):
        self.jpg_data, self.labels_data = self.data_set.compute(
            self.mode
        )

        for i in range(len(self.jpg_data)):
            frame = self.jpg_data[i]
            label = self.labels_data[i]

            frame = self.frame.resize_(frame)
            frame = self.frame.flip_(frame)
            frame = self.frame.tensor_(frame)

            self.tensor_data.append(frame)
            self.tensor_labels.append(label)

        return self.tensor_data, self.tensor_labels