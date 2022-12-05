from pathlib import Path
from typing import List

import torch
from torch.utils.data import Dataset

from ..types.room import Room


class Cubicasa5k(Dataset):
    ROOM_CATEGORY_INDEX = {category: i for i, category in enumerate(set(Room.ROOM_CATEGORY_MAP.values()))}
    NUM_FEATURES = 4  # area, width, height, doors

    def __init__(
        self,
        paths: List[Path],
    ) -> None:
        super().__init__()
        self.paths = paths

    def __len__(self) -> int:
        return len(self.paths)

    def __getitem__(self, index: int):
        path = self.paths[index]
        return torch.load(path)
