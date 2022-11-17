import pytorch_lightning as pl
from torch.utils.data import DataLoader
from pathlib import Path
from .cubicasa5k import Cubicasa5k

class CubicasaDataModule(pl.LightningDataModule):
    def __init__(
        self,
        root_dir: Path,
        buffer_pct: float = .03,
        batch_size=1,
        num_workers=0,
    ):
        super().__init__()
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.buffer_pct = buffer_pct
        self.train_paths = self._find_paths(root_dir, "train")
        self.val_paths = self._find_paths(root_dir, "val")
        self.test_paths = self._find_paths(root_dir, "test")

    def setup(self, stage: str):
        match stage:
            case "fit":
                self.train_dataset = Cubicasa5k(self.train_paths, self.buffer_pct)
                self.val_dataset = Cubicasa5k(self.val_paths, self.buffer_pct)
            case "test":
                self.test_dataset = Cubicasa5k(self.test_paths, self.buffer_pct)

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            collate_fn=self._collate,
            shuffle=True,
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            collate_fn=self._collate,
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            collate_fn=self._collate,
        )

    def _find_paths(self, root_dir: Path, stage: str):
        paths_txt = root_dir / f"{stage}.txt"
        paths = paths_txt.read_text().splitlines()
        # Need to remove leading slash to make relative
        paths = [root_dir / path[1:]  for path in paths]
        return paths

    def _collate(self, batch):
        # Override default collate - return as list of torch_geometric Data objects
        return batch