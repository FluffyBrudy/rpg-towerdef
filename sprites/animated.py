from pygame import Surface
from pygame.image import load as imload
from PIL import Image

from utils.pathutils import list_files_sorted


class AnimatedSprite:
    def __init__(self, frames_dir: str, animation_speed=0.1):
        self.frame_speed = animation_speed
        self.frames = [
            imload(image).convert_alpha().subsurface() for image in list_files_sorted(frames_dir)
        ]
        self._frame_index = 0
        self._frames_len = len(self.frames)

    def update_frame(self) -> Surface:
        frame_index = self._frame_index + self.frame_speed
        if frame_index >= self._frames_len:
            frame_index = 0
        self._frame_index = frame_index
        return self.frames[frame_index]


class StateAnimationSprite:
    def __init__(self):
        pass
