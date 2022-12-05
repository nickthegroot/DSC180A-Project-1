import json
from pathlib import Path
from typing import Type

import click
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint

from .. import consts as Consts
from ..data.cubicasa5k import Cubicasa5k
from ..data.data_module import CubicasaDataModule
from ..models.gat import GATModel
from ..models.gcn import GCNModel
from ..models.graphsage import GraphSAGEModel
from ..models.mlp import MLPModel
from ..models.tagcn import TAGCNModel
from ..types.config import Config, ModelType

MODEL_MAP: dict[ModelType, Type[pl.LightningModule]] = {
    ModelType.GAT: GATModel,
    ModelType.GCN: GCNModel,
    ModelType.GRAPHSAGE: GraphSAGEModel,
    ModelType.MLP: MLPModel,
    ModelType.TAGCN: TAGCNModel,
}


@click.command()
@click.argument("config-path", type=click.Path(exists=True))
def run(config_path: str):
    with open(config_path, "r") as f:
        config = Config(**json.load(f), name=Path(config_path).parent.stem)
        f.close()

    model = MODEL_MAP[config.model](
        num_features=Cubicasa5k.NUM_FEATURES,
        num_classes=len(Cubicasa5k.ROOM_CATEGORY_INDEX),
        hidden_channels=config.hidden_channels,
        num_layers=config.num_layers,
        lr=config.lr,
        gamma=config.gamma,
    )

    model_dir = Consts.MODEL_DIR / config.name
    dm = CubicasaDataModule(config.data_dir, config.batch_size, config.num_workers)
    checkpoints = ModelCheckpoint(
        str(model_dir / "checkpoints"),
        monitor="val_acc",
        mode="max",
        save_top_k=1,
    )
    trainer = pl.Trainer(
        max_epochs=config.max_epochs,
        default_root_dir=str(model_dir),
        callbacks=[
            # EarlyStopping(monitor="val_acc", mode="max", patience=20),
            checkpoints,
        ],
        accelerator="gpu",
    )

    trainer.fit(model, dm)
    model_path = Path(checkpoints.best_model_path)
    model_path.rename(Path(model_dir) / "model.ckpt")
