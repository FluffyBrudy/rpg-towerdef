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


BASE_PATH = Path().cwd()
MAPS_PATH = BASE_PATH / "maps" / "tmx"
GRAPHICS_PATH = BASE_PATH / "assetes" / "graphics"

FPS = 60


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000

INTERACTIVE_WINDOW_WIDTH = 1000
STATS_BOX_WIDTH = SCREEN_WIDTH - INTERACTIVE_WINDOW_WIDTH

NUM_CELLS = 29
NUM_ROWS = SCREEN_HEIGHT // NUM_CELLS
NUM_COLS = INTERACTIVE_WINDOW_WIDTH // NUM_CELLS
