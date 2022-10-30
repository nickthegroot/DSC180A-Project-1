from dataclasses import dataclass
from shapely.geometry import Polygon
from bs4 import Tag

SPACE_NAME_PREFIX = "Space "


@dataclass
class Room:
    name: str
    id: str
    geometry: Polygon

    @classmethod
    def from_tag(cls, tag: Tag):
        """Constructs a new room from a bs4 tag"""
        name = tag["class"][len(SPACE_NAME_PREFIX):]
        id = tag["id"]

        points_str = tag.find("polygon")["points"].strip()
        points = [
            [float(x) for x in point.split(",")] for point in points_str.split(" ")
        ]
        poly = Polygon(points)

        return cls(name=name, id=id, geometry=poly)
