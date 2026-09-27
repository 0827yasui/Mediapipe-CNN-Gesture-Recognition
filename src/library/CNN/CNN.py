import torch
import torch.nn as nn

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.ModuleList()

    def layer_cov_add(
        self,
        input_channel,
        output_channel,
        kernel_size,
        stride
        ):
        self.layers.append(
            nn.Conv2d(
                in_channels=input_channel,
                out_channels=output_channel,
                kernel_size=kernel_size,
                stride=stride
            )
        )

    def layer_relu_add(self):

        self.layers.append(
            nn.ReLU()
        )

    def layer_pool_add(
            self,
            kernel_size,
            padding,
            stride,
        ):
        self.layers.append(
            nn.MaxPool2d(
                kernel_size=kernel_size,
                padding=padding,
                stride=stride
            )
        )

    def layer_flatten_add(self):

        self.layers.append(
            nn.Flatten()
        )

    def layer_linear_add(
            self,
            input_size,
            output_size
        ):

        self.layers.append(
            nn.Linear(
                in_features=input_size,
                out_features=output_size
            )
        )

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)

        return x

    def train_step(self, frame,  label, optimizer, loss_fn):
        optimizer.zero_grad()
        logits = self.forward(frame)

        label = torch.tensor([label], dtype=torch.long)
        loss = loss_fn(
            logits,
            label
        )
        loss.backward()
        optimizer.step()
        return logits, loss
    

    def softmax(self, logits):
        probability = torch.softmax(
            logits,
            dim=1
        )
        return probability