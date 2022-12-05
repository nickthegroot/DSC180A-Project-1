from dataclasses import dataclass, field

from bs4 import Tag
from shapely.geometry import Polygon

from .util import tag_to_shape


@dataclass
class Room:
    __SPACE_NAME_PREFIX = "Space "

    # Modified from https://github.com/CubiCasa/CubiCasa5k/blob/master/floortrans/loaders/house.py#L139
    ROOM_CATEGORY_MAP = {
        "Alcove": "Room",
        "Attic": "Room",
        "Ballroom": "Room",
        "Bar": "Room",
        "Basement": "Room",
        "Bath": "Bath",
        "Bedroom": "Bedroom",
        "Below150cm": "Room",
        "CarPort": "Garage",
        "Church": "Room",
        "Closet": "Storage",
        "ConferenceRoom": "Room",
        "Conservatory": "Room",
        "Counter": "Room",
        "Den": "Room",
        "Dining": "Dining",
        "DraughtLobby": "Corridor",
        "DressingRoom": "Storage",
        "EatingArea": "Dining",
        "Elevated": "Room",
        "Elevator": "Room",
        "Entry": "Corridor",
        "ExerciseRoom": "Room",
        "Garage": "Garage",
        "Garbage": "Room",
        "Hall": "Corridor",
        "HallWay": "Corridor",
        "HotTub": "Room",
        "Kitchen": "Kitchen",
        "Library": "Room",
        "LivingRoom": "LivingRoom",
        "Loft": "Room",
        "Lounge": "LivingRoom",
        "MediaRoom": "Room",
        "MeetingRoom": "Room",
        "Museum": "Room",
        "Nook": "Room",
        "Office": "Room",
        "OpenToBelow": "Room",
        "Outdoor": "Outdoor",
        "Pantry": "Room",
        "Reception": "Room",
        "RecreationRoom": "Room",
        "RetailSpace": "Room",
        "Room": "Room",
        "Sanctuary": "Room",
        "Sauna": "Bath",
        "ServiceRoom": "Room",
        "ServingArea": "Room",
        "Skylights": "Room",
        "Stable": "Room",
        "Stage": "Room",
        "StairWell": "Room",
        "Storage": "Storage",
        "SunRoom": "Room",
        "SwimmingPool": "Room",
        "TechnicalRoom": "Room",
        "Theatre": "Room",
        "Undefined": "Room",
        "UserDefined": "Room",
        "Utility": "Room",
        "Wall": "Corridor",
        "Railing": "Corridor",
    }

    id: str
    geometry: Polygon
    space: str

    category: str = field(init=False)

    @property
    def category(self):
        tl_space = self.space.split(" ")[0]
        return self.ROOM_CATEGORY_MAP[tl_space]

    @category.setter
    def category(self, x):
        """Noop - readonly property"""
        pass

    width: float = field(init=False)

    @property
    def width(self):
        return self.geometry.bounds[2] - self.geometry.bounds[0]

    @width.setter
    def width(self, x):
        """Noop - readonly property"""
        pass

    height: float = field(init=False)

    @property
    def height(self):
        return self.geometry.bounds[3] - self.geometry.bounds[1]

    @width.setter
    def height(self, x):
        """Noop - readonly property"""
        pass

    area: float = field(init=False)

    @property
    def area(self):
        return self.geometry.area

    @area.setter
    def area(self, x):
        """Noop - readonly property"""
        pass

    @classmethod
    def from_tag(cls, tag: Tag):
        """Constructs a new room from a bs4 tag

        Args:
            tag (Tag): The bs4 "space" tag to construct from. Should have the "Space" class.
        """
        space = tag["class"][len(cls.__SPACE_NAME_PREFIX) :]
        id = tag["id"]
        poly = tag_to_shape(tag)

        return cls(
            space=space,
            id=id,
            geometry=poly,
        )
