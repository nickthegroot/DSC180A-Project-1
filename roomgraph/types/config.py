from enum import Enum

from pydantic import BaseModel

from .. import consts as Consts


class ModelType(str, Enum):
    """Enum for model type"""

    GAT = "gat"
    GCN = "gcn"
    GRAPHSAGE = "graphsage"
    MLP = "mlp"
    TAGCN = "tagcn"


class Config(BaseModel):
    """Configuration for one experiment / model training."""

    data_dir: str = str(Consts.PROCESSED_CUBICASA_DIR)
    num_workers: int = 1

    # All defaults taken from original paper: https://arxiv.org/pdf/2108.05947.pdf
    max_epochs: int = 100
    batch_size: int = 128
    name: str
    model: ModelType

    # Model parameters
    num_layers: int
    hidden_channels: int = 16
    lr: float = 0.004
    gamma: float = 0.8
