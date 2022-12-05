import pytorch_lightning as pl
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
from torch.optim.lr_scheduler import ExponentialLR
from torch_geometric.data import Batch, Data
from torchmetrics import Accuracy


class MLPModel(pl.LightningModule):
    """
    Basic Multilayer Perceptron (MLP) model for classification,
    only using the node features.
    """

    def __init__(
        self,
        num_features: int,
        num_classes: int,
        hidden_channels: int,
        num_layers: int,
        lr: float,
        gamma: float,
    ):
        super().__init__()
        self.lr = lr
        self.gamma = gamma
        self.criterion = nn.CrossEntropyLoss()
        self.acc = Accuracy("multiclass", num_classes=num_classes)

        self.layers = nn.ModuleList()
        self.layers.append(nn.Linear(num_features, hidden_channels))
        for _ in range(num_layers - 1):
            self.layers.append(nn.Linear(hidden_channels, hidden_channels))
        self.classifier = nn.Linear(hidden_channels, num_classes)

    def forward(self, x: Data):
        x = x.x
        for layer in self.layers:
            x = layer(x)
            x = F.relu(x)
        return self.classifier(x)

    def training_step(self, x: Batch, batch_idx: int):
        pred = self(x)
        loss = self.criterion(pred, x.y)
        self.log("tr_loss", loss, batch_size=x.num_graphs)
        return loss

    def validation_step(self, x: Batch, batch_idx: int):
        y_hat = self(x)
        loss = self.criterion(y_hat, x.y)
        self.log("val_loss", loss, batch_size=x.num_graphs)
        acc = self.acc(y_hat, x.y)
        self.log("val_acc", acc, batch_size=x.num_graphs)
        return loss

    def configure_optimizers(self):
        optimizer = Adam(self.parameters(), lr=self.lr)
        scheduler = ExponentialLR(optimizer, gamma=self.gamma)
        return [optimizer], [scheduler]
