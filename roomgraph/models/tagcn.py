from torch_geometric.nn import GATConv

from .base_gnn import BaseGNNClassifier


class TAGCNModel(BaseGNNClassifier):
    """Topology Adaptive Graph Convolutional Network, based on the paper: https://arxiv.org/abs/1710.10370"""

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
            Conv=GATConv,
            num_features=num_features,
            num_classes=num_classes,
            hidden_channels=hidden_channels,
            num_layers=num_layers,
            lr=lr,
            gamma=gamma,
        )
