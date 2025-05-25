from typing import Optional
from pygame import Surface
from pygame.sprite import Group
from sprites.base import StaticEntity
from typedefs.globaltype import Coor, ImageAreaCoor


class Building(StaticEntity):
    def __init__(
        self,
        pos: Coor,
        area: Optional[ImageAreaCoor],
        surface: Surface,
        size_correction=None,
        zindex=-1,
        *groups: Group
    ):
        super().__init__(pos, area, surface, size_correction, zindex, *groups)
