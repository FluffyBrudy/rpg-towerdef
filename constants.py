from enum import Enum
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


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

DEFAULT_ZOOM = 1.0
ZOOM_ANIMATION_DURATION = 2
MIN_ZOOM_LIMIT = 0.5
MAX_ZOOM_LIMIT = 2
ZOOM_CHANGE_FACTOR = 0.1
