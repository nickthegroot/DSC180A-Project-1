from pathlib import Path

import geopandas as gpd
import torch
from bs4 import BeautifulSoup
from torch_geometric.data import Data

from ..types.room import Room
from ..types.util import tag_to_shape
from .cubicasa5k import Cubicasa5k


def generate_graph(model_path: Path, buffer_pct: float):
    svg_path = model_path / "model.svg"
    bs = BeautifulSoup(svg_path.read_text(), "xml")
    room_tags = bs.select(".Space")
    rooms = [Room.from_tag(tag) for tag in room_tags]
    if len(rooms) == 0:
        return

    room_df = gpd.GeoDataFrame(rooms).set_index("id")

    # Calculate Room Adjacency Matrix (AKA: edges)
    minX, minY, maxX, maxY = room_df.total_bounds
    buffer_amt = (maxX - minX) * buffer_pct
    buffer_df = room_df.buffer(buffer_amt)
    buffer_df = gpd.GeoDataFrame(geometry=buffer_df, index=room_df.index)

    room_adjacency_df = buffer_df.sjoin(room_df)
    room_adjacency = room_adjacency_df[room_adjacency_df.index != room_adjacency_df.index_right]["index_right"]

    # Calculate Doors Per Room
    door_tags = bs.find_all(id="Door")
    door_df = gpd.GeoDataFrame(geometry=[tag_to_shape(tag) for tag in door_tags])

    door_adjacency_df = buffer_df.sjoin(door_df)
    room_doors = door_adjacency_df.groupby("id")["index_right"].count()
    room_df["doors"] = room_doors
    room_df["doors"].fillna(0, inplace=True)

    # Translate to PyG
    index_map = {id: i for i, id in enumerate(room_df.index)}
    x = torch.tensor(
        [[room.area, room.width, room.height, room.doors] for room in room_df.itertuples()], dtype=torch.float
    )
    edge_index = torch.tensor([[index_map[a], index_map[b]] for a, b in room_adjacency.items()], dtype=torch.long)
    y = torch.tensor(
        [Cubicasa5k.ROOM_CATEGORY_INDEX[category] for _, category in room_df.category.items()], dtype=torch.long
    )

    return Data(
        x=x,
        edge_index=edge_index.t().contiguous(),
        y=y,
    )
