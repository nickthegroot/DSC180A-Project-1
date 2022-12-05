from pathlib import Path

import click
import geopandas as gpd
import torch
from bs4 import BeautifulSoup
from torch_geometric.data import Data
from tqdm import tqdm

from .. import consts as Consts
from ..data.cubicasa5k import Cubicasa5k
from ..types.room import Room
from ..types.util import tag_to_shape


@click.command()
@click.argument("input", type=click.Path(exists=True), default=Consts.RAW_CUBICASA_DIR)
@click.argument("output", type=click.Path(), default=Consts.PROCESSED_CUBICASA_DIR)
@click.option("--buffer-pct", type=float, default=0.03, help="Buffer percentage")
def run(input: str, output: str, buffer_pct: float):
    input_path = Path(input)
    output_path = Path(output)

    processed_paths: dict[str, list[str]] = {"train": [], "val": [], "test": []}
    for stage in ["train", "val", "test"]:
        paths = _find_paths(input_path, stage)
        for path in tqdm(paths, desc=f"Processing {stage}"):
            graph = _generate_graph(path, buffer_pct)
            if graph is not None:
                save_path = output_path / path.relative_to(input_path) / "graph.pt"
                save_path.parent.mkdir(parents=True, exist_ok=True)
                torch.save(graph, str(save_path))
                processed_paths[stage].append(str(save_path.relative_to(output_path)))

    for stage, paths in processed_paths.items():
        paths_txt = output_path / f"{stage}.txt"
        paths_txt.write_text("\n".join(paths))


def _generate_graph(model_path: Path, buffer_pct: float):
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


def _find_paths(root_dir: Path, stage: str):
    paths_txt = root_dir / f"{stage}.txt"
    paths = paths_txt.read_text().splitlines()
    # Need to remove leading slash to make relative
    return [root_dir / path[1:] for path in paths]
