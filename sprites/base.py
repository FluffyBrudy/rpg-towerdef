from abc import ABC, abstractmethod
from typing import Optional, cast
from pygame import Surface
from pygame.transform import scale, scale_by
from pygame.sprite import Sprite, Group
from typedefs.globaltype import Coor, ImageAreaCoor


class StaticEntity(Sprite):
    @classmethod
    def scale_image(cls, sprite: "StaticEntity", scale_size: float):
        image = cast(Surface, sprite.image)
        sprite.scaled_image = scale_by(image, scale_size)

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

        self.scaled_image = image

        StaticEntity.scale_image(self, 1)

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


class AnimatedSprite(Sprite, ABC):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)
        self._frame_index = 0
        self._current_frames = []
        self._scaled_frames = []

    @abstractmethod
    def get_scaled_frame(self) -> Surface:
        ...

    @classmethod
    @abstractmethod
    def scale_frames(cls, sprite: "AnimatedSprite", scale_size: float):
        ...
