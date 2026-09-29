from enum import Enum
import random

from src.library.data.tensor_data_set import Data
from src.setting.use.CNN_use import CNN_use
from src.setting.setting import Setting

class LearningMode(Enum):
    TRAIN = 0
    TEST = 1

class Learning():
    def __init__(self, mode):

        self.mode = LearningMode(mode)
        self.data = Data(self.mode.value)
        self.cnn = CNN_use(self.mode.value)
        self.setting = Setting()

        self.tensor_data = []
        self.tensor_labels = []

        self.data_create()
        self.file_read()

    def data_create(self):
        self.tensor_data, self.tensor_labels = self.data.compute()

    def file_read(self):
        if self.mode == LearningMode.TRAIN:
            learning_data = self.setting.learning_data["train"]
        else:
            learning_data = self.setting.learning_data["test"]
        self.epoch = learning_data["epoch"]
        self.shuffle = learning_data["shuffle"]

    def learning(self):
        data = list(zip(self.tensor_data, self.tensor_labels))

        for _ in range(self.epoch):
            if self.shuffle:
                random.shuffle(data)
            for tensor, label in data:
                self.cnn.train(tensor, label)