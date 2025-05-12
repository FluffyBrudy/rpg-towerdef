from typing import Tuple
from pygame import sprite, Surface
from pygame.transform import scale
from typedefs.globaltype import Coor, ImageAreaCoor


class StaticTile(sprite.Sprite):
    def __init__(
        self, pos: Coor, area: ImageAreaCoor, surface: Surface, size_correction=None
    ):
        super().__init__()
        image = surface.subsurface(area)
        if size_correction:
            self.image = scale(image, size_correction)
        else:
            self.image = image
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, scroll: Tuple[int, int]):
        self.rect.x += scroll[0]
        self.rect.y += scroll[1]
