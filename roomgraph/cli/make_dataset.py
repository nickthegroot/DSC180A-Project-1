from pathlib import Path

import click
import torch
from tqdm import tqdm

from .. import consts as Consts
from ..data.util import generate_graph


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
            graph = generate_graph(path, buffer_pct)
            if graph is not None:
                save_path = output_path / path.relative_to(input_path) / "graph.pt"
                save_path.parent.mkdir(parents=True, exist_ok=True)
                torch.save(graph, str(save_path))
                processed_paths[stage].append(str(save_path.relative_to(output_path)))

    for stage, paths in processed_paths.items():
        paths_txt = output_path / f"{stage}.txt"
        paths_txt.write_text("\n".join(paths))


def _find_paths(root_dir: Path, stage: str):
    paths_txt = root_dir / f"{stage}.txt"
    paths = paths_txt.read_text().splitlines()
    # Need to remove leading slash to make relative
    return [root_dir / path[1:] for path in paths]
