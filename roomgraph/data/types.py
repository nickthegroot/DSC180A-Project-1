from dataclasses import dataclass
from shapely.geometry import Polygon
from bs4 import Tag

@dataclass
class Room:
    __SPACE_NAME_PREFIX = "Space "

    space: str
    id: str
    geometry: Polygon

    @classmethod
    def from_tag(cls, tag: Tag):
        """Constructs a new room from a bs4 tag

        Args:
            tag (Tag): The bs4 "space" tag to construct from. Should have the "Space" class.
        """
        space = tag["class"][len(cls.__SPACE_NAME_PREFIX):]
        id = tag["id"]

        points_str = tag.find("polygon")["points"].strip()
        points = [
            [float(x) for x in point.split(",")] for point in points_str.split(" ")
        ]
        poly = Polygon(points)

        return cls(space=space, id=id, geometry=poly)
