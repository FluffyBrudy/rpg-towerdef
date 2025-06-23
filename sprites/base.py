from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, cast
from pygame import Surface
from pygame.transform import scale, scale_by
from pygame.sprite import Sprite, Group
from constants import DEFAULT_ZOOM
from typedefs.globaltype import Coor, ImageAreaCoor
from utils.imgutils import scale_frames, scale_image


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

        self.scaled_image = scale_image(self.image, DEFAULT_ZOOM)

    def update(self, **kwargs):
        super().update(**kwargs)

    def get_scaled_image(self):
        return self.scaled_image


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


class AnimatedSprite(Sprite):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)
        self._frame_index = 0
        self.current_frames: Tuple[Surface] | List[Surface] = []
        self.scaled_frames: Tuple[Surface] | List[Surface] = []

    def get_scaled_frame(self) -> Surface:
        return self.scaled_frames[int(self._frame_index)]
