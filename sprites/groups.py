from typing import Any, Optional, List, cast, override
from pygame import MOUSEWHEEL, Event, Surface, Vector2
import pygame
from pygame.sprite import Group, Sprite


class CameraGroup(Group):
    def __init__(self, *sprites: Sprite) -> None:
        super().__init__(*sprites)
        self.sorted_sprites: List[Sprite] = []
        self.camera_offset = Vector2(0, 0)
        self.zoom_scale = 1.0

    def init_order(self):
        self.sorted_sprites = sorted(
            self.sprites(), key=lambda s: getattr(s, "zindex", 0)
        )

    def set_camera(self, offset_x: int, offset_y: int):
        self.camera_offset.x = offset_x
        self.camera_offset.y = offset_y

    def handle_camera_movement(self):
        motion_x, motion_y = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[0]:
            adjusted_x = max(-15, min(motion_x, 15))
            adjusted_y = max(-15, min(motion_y, 15))
            self.camera_offset.x += adjusted_x
            self.camera_offset.y += adjusted_y

    def handle_camera_zoom(self, zoom_dir: int):
        self.zoom_scale = max(0.5, min(self.zoom_scale + 0.1 * zoom_dir, 2))

    def update(self, *args: Any, **kwargs: Any) -> None:
        zoom_event = cast(Optional[Event], kwargs.get("event"))
        if zoom_event is not None:
            if zoom_event.type == MOUSEWHEEL:
                self.handle_camera_zoom(zoom_event.y)
        self.handle_camera_movement()
        return super().update(*args, **kwargs)

    @override
    def draw(self, surface: Surface) -> None:  # type: ignore
        for sprite in self.sorted_sprites:
            original_rect = sprite.rect  # type: ignore
            original_image = sprite.image  # type: ignore

            new_size = (
                int(original_image.get_width() * self.zoom_scale + 1),  # type: ignore
                int(original_image.get_height() * self.zoom_scale + 1),  # type: ignore
            )
            scaled_image = pygame.transform.scale(original_image, new_size)  # type: ignore
            scaled_pos = (
                original_rect.x * self.zoom_scale + self.camera_offset.x,  # type: ignore
                original_rect.y * self.zoom_scale + self.camera_offset.y,  # type: ignore
            )

            surface.blit(scaled_image, scaled_pos)
