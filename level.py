from typing import Optional, Type
from pygame import Surface, sprite
import pygame
from pygame.image import load
from pytmx import TiledMap
from maploader import LayerType, load_layer, load_map
from sprites.tiles import StaticTile


class Level:
    def __init__(self, level: int) -> None:
        map_path = f"level{level}.tmx"
        tmxfp = load_map(map_path)

        self.static_group = sprite.Group()
        self.collision_group = sprite.Group()

        if tmxfp is not None:
            self.load_map_ui(tmxfp)

    def load_map_ui(self, tmxfp: TiledMap):
        layers = [
            ("floor", StaticTile, self.static_group),
            ("wall", StaticTile, self.collision_group),
            ("stair", StaticTile, self.static_group),
            ("floorfix", StaticTile, self.static_group),
            ("bridge", StaticTile, self.collision_group),
        ]
        for name, tile_class, group in layers:
            layer = load_layer(tmxfp, name)
            if layer:
                self.load_layer_ui(layer, tile_class, group)

    def load_layer_ui(
        self, layer: LayerType, Model: Type[StaticTile], group: sprite.Group
    ):
        layer_file, layer_data = layer
        layer_tile = load(layer_file)

        for pos, area, correction in layer_data:
            tile = Model(pos, area, layer_tile, correction)
            group.add(tile)

    def update(self, global_event: Optional[pygame.Event]):
        if global_event is None:
            return
        if global_event.type == pygame.MOUSEWHEEL:
            x, y = global_event.x, global_event.y
            print(x, y)
            self.static_group.update((x * 5, y * 5))
            self.collision_group.update((x * 5, y * 5))

    def draw(self, surface: Surface):
        self.collision_group.draw(surface)
        self.static_group.draw(surface)
