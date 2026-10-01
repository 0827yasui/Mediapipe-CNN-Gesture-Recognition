from ...library.CNN.CNN import CNN
from ...setting.setting import Setting
import torch
import torch.nn as nn

class CNN_use():
    def __init__(self, mode):
        self.setting = Setting()
        self.CNN_dat = self.setting.CNN_data
        self.CNN = CNN()

        self.layer_create()
        self.optimizer_create()
        self.loss_fn_create()

    def layer_create(self):
        for layer in self.CNN_dat["model"]["layers"]:

            if layer["type"] == "Conv2d":
                self.CNN.layer_cov_add(
                    input_channel=layer["input_channel"],
                    output_channel=layer["output_channel"],
                    kernel_size=layer["kernel_size"],
                    stride=layer["stride"]
                )

            elif layer["type"] == "ReLU":
                self.CNN.layer_relu_add()

            elif layer["type"] == "MaxPool2d":
                self.CNN.layer_pool_add(
                    kernel_size=layer["kernel_size"],
                    padding=layer["padding"],
                    stride=layer["stride"]
                )

            elif layer["type"] == "Flatten":
                self.CNN.layer_flatten_add()

            elif layer["type"] == "Linear":
                self.CNN.layer_linear_add(
                    input_size=layer["input_size"],
                    output_size=layer["output_size"]
                )

    def forward(self, input):
        logits = self.CNN.forward(input)
        if self.CNN_dat["model"]["softmax"]:
            logits = self.CNN.softmax(logits)
        return logits

    def train(self, frame, label):
        logits, loss = self.CNN.train_step(frame, label, self.optimizer, self.loss_fn)
        prediction = logits.argmax(dim=1)
        result = (prediction == label)
        return logits, loss, result

    def test(self, frame, label):
        with torch.no_grad():
            logits = self.CNN.forward(frame)
            prediction = logits.argmax(dim=1)
            result = (prediction == label)

        return logits, result

    def save(self):
        torch.save(
            self.CNN.state_dict(),
            "model/cnn.pth"
        )

    def load(self):
        self.CNN.load_state_dict(
            torch.load("model/cnn.pth")
        )
        self.CNN.eval()

# -----------------------------------------------------------------------------------------------------

    def optimizer_create(self):
        optimizer_type = self.CNN_dat["learning"]["optimizer"]["type"]
        learning_rate = self.CNN_dat["learning"]["optimizer"]["learning_rate"]

        if optimizer_type == "Adam":
            self.optimizer = torch.optim.Adam(
                self.CNN.parameters(),
                lr=learning_rate
            )
        
        elif optimizer_type == "SGD":
            self.optimizer = torch.optim.SGD(
                self.CNN.parameters(),
                lr=learning_rate
            )

        else:
            raise ValueError(f"現在のoptimizerはサポートしていません: {optimizer_type}")

    def loss_fn_create(self):
        loss_type = self.CNN_dat["learning"]["loss"]["type"]

        if loss_type == "CrossEntropyLoss":
            self.loss_fn = nn.CrossEntropyLoss()
        elif loss_type == "MSELoss":
            self.loss_fn = nn.MSELoss()
        else:
           raise ValueError(f"現在のloss関数はサポートしていません: {loss_type}")
                            