from pathlib import Path
from typing import List
import geopandas as gpd
import networkx as nx
from bs4 import BeautifulSoup
from torch.utils.data import Dataset
from torch_geometric.utils import from_networkx
from .types import Room


class Cubicasa5k(Dataset):
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
        bs_rooms = bs.select(".Space")
        gdf = gpd.GeoDataFrame([Room.from_tag(tag) for tag in bs_rooms]).set_index("id")

        minX, minY, maxX, maxY = gdf.total_bounds
        buffer_amt = (maxX - minX) * self.buffer_pct
        buffer_df = gpd.GeoDataFrame(geometry=gdf.buffer(buffer_amt))

        adjacency_df = gdf.sjoin(buffer_df)
        # Get rid of self-intersections
        adjacency_df = adjacency_df[adjacency_df.index != adjacency_df.index_right]

        graph = nx.Graph()
        graph.add_nodes_from(gdf.index)
        graph.add_edges_from(adjacency_df["index_right"].items())
        return from_networkx(graph), gdf
        



