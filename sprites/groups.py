from math import isclose
import sys
from typing import Any, Optional, List, cast, override, Union, Iterable
from pygame import MOUSEWHEEL, SRCALPHA, Event, Surface, Vector2
import pygame
from pygame.sprite import Group, Sprite

from constants import DEFAULT_ZOOM, MAX_ZOOM_LIMIT, MIN_ZOOM_LIMIT, ZOOM_CHANGE_FACTOR
from sprites.base import AnimatedSprite, StaticEntity
from sprites.troops.knights import Warrior
from ui.mouse import CustomMouse
from utils.imgutils import scale_frames, scale_image


class CameraGroup(Group):
    def __init__(self, *sprites: Sprite) -> None:
        super().__init__(*sprites)
        self.sorted_static_tiles: List[Sprite] = []
        self.camera_offset = Vector2(0, 0)
        self.zoom_scale = DEFAULT_ZOOM
        self.has_zoom_change = False

        self.mouse = CustomMouse()

        self.static_tiles_group: Group = Group()
        self.warrior_group: Group = Group()

        self.static_layer_surface = pygame.Surface((0, 0))
        self.static_layer_offset = (0, 0)

    @override
    def add(self, *sprites: Union[Sprite, Iterable[Sprite]], sort=False) -> None:
        for sprite in sprites:
            if isinstance(sprite, StaticEntity):
                self.static_tiles_group.add(sprite)
            elif isinstance(sprite, Warrior):
                self.warrior_group.add(sprite)
                return super().add(sprite)
        if sort:
            self.init_order()

    def init_order(self):
        self.sorted_static_tiles = sorted(
            self.static_tiles_group.sprites(), key=lambda s: getattr(s, "zindex", 0)
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
        next_zoom = self.zoom_scale + ZOOM_CHANGE_FACTOR * zoom_dir
        new_zoom = max(MIN_ZOOM_LIMIT, min(next_zoom, MAX_ZOOM_LIMIT))
        if isclose(self.zoom_scale, new_zoom):
            return

        self.has_zoom_change = True
        mouse_pos = pygame.mouse.get_pos()
        zoom_ratio = round(new_zoom / self.zoom_scale, 2)
        self.camera_offset = mouse_pos - (mouse_pos - self.camera_offset) * zoom_ratio
        self.zoom_scale = new_zoom

    def apply_zoom_if_needed(self):
        if not self.has_zoom_change:
            return
        for sprite in self.warrior_group:
            if isinstance(sprite, AnimatedSprite):
                sprite.scaled_frames = scale_frames(
                    sprite.current_frames, self.zoom_scale
                )
        self.prerender_static_tiles()

    def prerender_static_tiles(self):
        w, h = pygame.display.get_surface().size
        size = int(w * 1.5), int(h * 1.5)
        self.static_layer_surface = pygame.Surface(size, SRCALPHA)

        for sprite in self.sorted_static_tiles:
            if isinstance(sprite, StaticEntity):
                pos = sprite.rect.topleft  # type: ignore
                scaled_pos_x = int(pos[0] * self.zoom_scale)
                scaled_pos_y = int(pos[1] * self.zoom_scale)
                scaled_image = scale_image(sprite.image, self.zoom_scale)  # type: ignore
                self.static_layer_surface.blit(
                    scaled_image, (scaled_pos_x, scaled_pos_y)
                )

    @override
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.mouse.update()
        zoom_event = cast(Optional[Event], kwargs.get("event"))
        if zoom_event is not None:
            if zoom_event.type == MOUSEWHEEL:
                self.handle_camera_zoom(zoom_event.y)
        self.handle_camera_movement()
        return super().update(*args, **kwargs)

    @override
    def draw(self, surface: Surface) -> None:  # type: ignore
        zoom_changed = self.has_zoom_change

        self.apply_zoom_if_needed()

        new_cursor_type = self.mouse.get_current_cursor()

        visible_rect = surface.blit(self.static_layer_surface, self.camera_offset)
        for sprite in self.sprites():
            original_rect = sprite.rect

            scaled_pos_x = original_rect.x * self.zoom_scale + self.camera_offset.x  # type: ignore
            scaled_pos_y = original_rect.y * self.zoom_scale + self.camera_offset.y  # type: ignore
            scaled_pos = (round(scaled_pos_x), round(scaled_pos_y))

            new_size_x = original_rect.width * self.zoom_scale  # type: ignore
            new_size_y = original_rect.height * self.zoom_scale  # type: ignore
            new_size = (round(new_size_x), round(new_size_y))

            new_rect = pygame.Rect(scaled_pos, new_size)
            if not new_rect.colliderect(visible_rect):
                continue

            scaled_image: Any = None

            if isinstance(sprite, AnimatedSprite):
                scaled_image = sprite.get_scaled_frame()
                if new_rect.collidepoint(self.mouse.pos):
                    new_cursor_type = "move"

            else:
                print("Something's off: not all sprite types covered.")
                pygame.quit()
                sys.exit()

            surface.blit(scaled_image, scaled_pos)

        self.mouse.change_cursor(new_cursor_type)

        self.mouse.draw(surface)

        if zoom_changed:
            self.has_zoom_change = False
