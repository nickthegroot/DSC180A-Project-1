from pathlib import Path
from bs4 import BeautifulSoup
from .types import Room
import geopandas as gpd
import networkx as nx


def generate_graph(
    svg_path: Path,
    buffer_pct=0.03,
):
    """Takes in a vectorized floor plan, and returns a room adjacency matrix"""
    bs = BeautifulSoup(svg_path.read_text(), "xml")
    bs_rooms = bs.select(".Space")
    gdf = gpd.GeoDataFrame(
        [Room.from_tag(tag) for tag in bs_rooms]
    ).set_index("id")

    minX, minY, maxX, maxY = gdf.total_bounds
    buffer_amt = (maxX - minX) * buffer_pct
    buffer_df = gpd.GeoDataFrame(geometry=gdf.buffer(buffer_amt))

    adjacency_df = gdf.sjoin(buffer_df)
    # Get rid of self-intersections
    adjacency_df = adjacency_df[adjacency_df.index != adjacency_df.index_right]

    graph = nx.Graph()
    graph.add_nodes_from(gdf.to_dict("index").items())
    graph.add_edges_from(adjacency_df["index_right"].items())
    return graph
