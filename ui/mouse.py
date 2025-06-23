from typing import Literal, Union
import pygame

from constants import GRAPHICS_PATH
from utils.imgutils import load_image
from utils.pathutils import convert_to_str_path


TCursors = Union[Literal["pointer", "move"]]
CURSOR_PATH = GRAPHICS_PATH / "cursors"
CURSOR_SIZE = 20


class CustomMouse:
    def __init__(self, init_post: tuple[int, int] = (0, 0)):
        self.image = pygame.transform.scale(
            load_image(convert_to_str_path(CURSOR_PATH / "pointer.png")),
            (CURSOR_SIZE, CURSOR_SIZE),
        )
        self._current_cursor: TCursors = "pointer"
        self.rect = self.image.get_rect(topleft=init_post)

    def change_cursor(self, cursor_type: TCursors):
        if cursor_type == self._current_cursor:
            return
        print("t")
        self.image = pygame.transform.scale(
            load_image(convert_to_str_path(CURSOR_PATH / f"{cursor_type}.png")),
            (CURSOR_SIZE, CURSOR_SIZE),
        )
        self._current_cursor = cursor_type

    def get_current_cursor(self) -> TCursors:
        return self._current_cursor

    def update(self):
        self.rect.topleft = pygame.mouse.get_pos()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    @property
    def pos(self):
        return self.rect.topleft
