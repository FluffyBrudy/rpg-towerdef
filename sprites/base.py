from typing import Iterable, Optional, Tuple
from pygame import Surface
from pygame.transform import scale
from pygame.sprite import Sprite, Group
from typedefs.globaltype import Coor, ImageAreaCoor


class StaticEntity(Sprite):
    def __init__(
        self,
        pos: Coor,
        area: Optional[ImageAreaCoor],
        surface: Surface,
        size_correction=None,
        zindex=-1,
        *groups: Group
    ):
        super().__init__(*groups)

        image = surface
        if area:
            image = surface.subsurface(area)
        if size_correction:
            self.image = scale(image, size_correction)
        else:
            self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.zindex = zindex

    def update(self, **kwargs):
        pass


class StaticCollidableEntity(StaticEntity):
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

    def update(self, **kwargs):
        super().update(**kwargs)
