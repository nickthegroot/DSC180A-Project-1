from pathlib import Path

import pytorch_lightning as pl
from torch_geometric.loader import DataLoader

from .cubicasa5k import Cubicasa5k


class CubicasaDataModule(pl.LightningDataModule):
    def __init__(
        self,
        root_dir: str,
        batch_size: int,
        num_workers: int,
    ):
        super().__init__()
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.train_paths = self._find_paths(root_dir, "train")
        self.val_paths = self._find_paths(root_dir, "val")
        self.test_paths = self._find_paths(root_dir, "test")

    def setup(self, stage: str):
        match stage:
            case "fit":
                self.train_dataset = Cubicasa5k(self.train_paths)
                self.val_dataset = Cubicasa5k(self.val_paths)
            case "test":
                self.test_dataset = Cubicasa5k(self.test_paths)

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=True,
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
        )

    def _find_paths(self, root_dir: str, stage: str):
        root = Path(root_dir)
        paths_txt = root / f"{stage}.txt"
        paths = paths_txt.read_text().splitlines()
        return [root / path for path in paths]
