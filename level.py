from typing import Iterable, Optional, Type, Union
from pygame import Surface, sprite
import pygame
from pygame.image import load
from pytmx import TiledMap
from constants import MapLayer
from maploader import LayerType, load_layer, load_map
from sprites.buildings import Building
from sprites.groups import CameraGroup
from sprites.base import StaticCollidableEntity, StaticEntity


class Level:
    def __init__(self, level: int) -> None:
        map_path = f"level{level}.tmx"
        tmxfp = load_map(map_path)

        self.visible_group = CameraGroup()
        self.collision_group = sprite.Group()

        if tmxfp is not None:
            self.load_map_ui(tmxfp)

    def load_map_ui(self, tmxfp: TiledMap):
        layers = [
            (MapLayer.FLOOR, StaticEntity, self.visible_group),
            (MapLayer.FLOORFIX, StaticEntity, self.visible_group),
            (MapLayer.STAIR, StaticCollidableEntity, self.visible_group),
            (MapLayer.WALL, StaticCollidableEntity, self.visible_group),
            (MapLayer.BRIDGE, StaticCollidableEntity, self.visible_group),
            (MapLayer.CASTLES, Building, self.visible_group),
            (MapLayer.TOWERS, Building, self.visible_group),
            (MapLayer.HOUSES, Building, self.visible_group),
            (MapLayer.DECORATION, StaticEntity, self.visible_group),
            (MapLayer.TREES, StaticEntity, self.visible_group),
            (MapLayer.SHADOWS, StaticEntity, self.visible_group),
        ]

        for name, tile_class, group in layers:
            layer = load_layer(tmxfp, name)
            if layer:
                self.load_layer_ui(layer, tile_class, group)
        self.visible_group.init_order()

    def load_layer_ui(
        self,
        layer: LayerType,
        Model: Union[Type[StaticEntity], Type[Building], Type[StaticCollidableEntity]],
        groups: Iterable[sprite.Group] | sprite.Group,
    ):
        layer_file, layer_data, properties = layer
        layer_tile = load(layer_file)

        for pos, area, correction in layer_data:
            if isinstance(groups, sprite.Group):
                groups = (groups,)
            if (Model is StaticEntity) or (Model is Building):
                Model(pos, area, layer_tile, correction, properties["zindex"], *groups)
            if Model is StaticCollidableEntity:
                Model(pos, area, layer_tile, correction, properties["zindex"], *groups)

    def update(self, global_event: Optional[pygame.Event]):
        self.visible_group.update(event=global_event)
        self.collision_group.update()

    def draw(self, surface: Surface):
        self.visible_group.draw(surface)
