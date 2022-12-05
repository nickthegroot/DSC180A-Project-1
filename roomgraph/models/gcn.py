from torch_geometric.nn import GCNConv

from .base_gnn import BaseGNNClassifier


class GCNModel(BaseGNNClassifier):
    """Graph Convolutional Network Model, based on the paper: https://arxiv.org/abs/1609.02907"""

    def __init__(
        self,
        num_features: int,
        num_classes: int,
        hidden_channels: int,
        num_layers: int,
        lr: float,
        gamma: float,
    ):
        super().__init__(
            Conv=GCNConv,
            num_features=num_features,
            num_classes=num_classes,
            hidden_channels=hidden_channels,
            num_layers=num_layers,
            lr=lr,
            gamma=gamma,
        )
