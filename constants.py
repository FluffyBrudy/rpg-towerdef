from enum import Enum, auto
from pathlib import Path


class MapLayer(str, Enum):
    FLOOR = "floor"
    FLOORFIX = "floorfix"
    STAIR = "stair"
    WALL = "wall"
    BRIDGE = "bridge"
    CASTLES = "castles"
    TOWERS = "towers"
    HOUSES = "houses"
    DECORATION = "decoration"
    TREES = "trees"
    SHADOWS = "shadows"
    WARRIOR = "warrior"


BASE_PATH = Path().cwd()
MAPS_PATH = BASE_PATH / "maps" / "tmx"
GRAPHICS_PATH = BASE_PATH / "assets" / "graphics"

FPS = 60


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
