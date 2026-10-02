from enum import Enum
import random
import torch
import cv2 as cv
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
        self.batch = learning_data["batch"]
        self.shuffle = learning_data["shuffle"]

    def learning(self):
        if self.mode == LearningMode.TEST:
            self.cnn.load()

        data = list(zip(self.data.data_set.jpg_list, self.tensor_data, self.tensor_labels))
        acc_list = []

        for epoch in range(self.epoch):
            if self.shuffle:
                random.shuffle(data)

            correct_count = 0
            total = 0

            for start in range(0, len(data), self.batch):
                batch_data = data[start:start + self.batch]

                file_names, tensors, labels = zip(*batch_data)

                frame = torch.stack(tensors)

                show_frame = frame[0].detach().cpu().permute(1, 2, 0).numpy()
                show_frame = (show_frame * 255).clip(0, 255).astype("uint8")
                show_frame = cv.cvtColor(show_frame, cv.COLOR_RGB2BGR)

                cv.imshow("Learning Frame", show_frame)
                cv.waitKey(1)

                label = torch.tensor(labels, dtype=torch.long)

                if self.mode == LearningMode.TRAIN:
                    logits, loss, result = self.cnn.train(frame, label)
                elif self.mode == LearningMode.TEST:
                    logits, result = self.cnn.test(frame, label)

                correct_count += result.sum().item()
                total += len(label)

            acc = correct_count / total if total > 0 else 0.0
            acc_list.append({"epoch": epoch + 1, "acc": acc})

        if self.mode == LearningMode.TRAIN:
            self.cnn.save()
        return acc_list
