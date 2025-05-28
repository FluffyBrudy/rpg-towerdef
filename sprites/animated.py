from enum import Enum
from pygame import Surface
from pygame.sprite import Sprite
from utils.imgutils import (
    load_image,
)
from utils.pathutils import list_files_sorted


class AnimatedSprite:
    def __init__(self, frames_dir: str, animation_speed=0.1):
        self.frame_speed = animation_speed
        self.frames = [load_image(image) for image in list_files_sorted(frames_dir)]
        self._frame_index = 0
        self._frames_len = len(self.frames)

    def update_frame(self) -> Surface:
        frame_index = self._frame_index + self.frame_speed
        if frame_index >= self._frames_len:
            frame_index = 0
        self._frame_index = frame_index
        return self.frames[frame_index]
