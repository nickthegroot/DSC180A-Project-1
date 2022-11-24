import geopandas as gpd
import networkx as nx
import torch
from pathlib import Path
from typing import List
from bs4 import BeautifulSoup
from torch.utils.data import Dataset
from torch_geometric.utils import from_networkx
from torch_geometric.data import Data
from ..types import Room, tag_to_shape


class Cubicasa5k(Dataset):
    ROOM_CATEGORY_INDEX = { category: i for i, category in enumerate(set(Room.ROOM_CATEGORY_MAP.values())) }

    def __init__(
        self,
        paths: List[Path],
        buffer_pct=0.03,
    ) -> None:
        super().__init__()
        self.paths = paths
        self.buffer_pct = buffer_pct
    
    def __len__(self) -> int:
        return len(self.paths)

    def __getitem__(self, index: int):
        svg_path = self.paths[index] / 'model.svg'
        bs = BeautifulSoup(svg_path.read_text(), "xml")
        room_tags = bs.select('.Space')
        room_df = gpd.GeoDataFrame([Room.from_tag(tag) for tag in room_tags]).set_index("id")

        # Calculate Room Adjacency Matrix (AKA: edges)
        minX, minY, maxX, maxY = room_df.total_bounds
        buffer_amt = (maxX - minX) * self.buffer_pct
        buffer_df = room_df.buffer(buffer_amt)
        buffer_df = gpd.GeoDataFrame(geometry=buffer_df, index=room_df.index)

        room_adjacency_df = buffer_df.sjoin(room_df)
        room_adjacency = room_adjacency_df[room_adjacency_df.index != room_adjacency_df.index_right]["index_right"]

        # Calculate Doors Per Room
        door_tags = bs.find_all(id='Door')
        door_df = gpd.GeoDataFrame(geometry=[tag_to_shape(tag) for tag in door_tags])

        door_adjacency_df = buffer_df.sjoin(door_df)
        room_doors = door_adjacency_df.groupby('id')['index_right'].count()
        room_df['doors'] = room_doors
        room_df['doors'].fillna(0, inplace=True)

        # Translate to PyG
        index_map = { id: i for i, id in enumerate(room_df.index) }
        x = torch.tensor([
            [room.area, room.width, room.height, room.doors]
            for room in room_df.itertuples()
        ], dtype=torch.float)
        edge_index = torch.tensor([[index_map[a], index_map[b]] for a, b in room_adjacency.items()], dtype=torch.long)
        y = torch.tensor([self.ROOM_CATEGORY_INDEX[category] for _, category in room_df.category.items()], dtype=torch.int)
        return Data(
            x = x,
            edge_index = edge_index.t().contiguous(),
            y = y,
        )
