from typing import Iterable, Optional, Type, Union
from pygame import Surface, sprite
import pygame
from pygame.image import load
from pytmx import TiledMap
from constants import MapLayer
from grid import ScreenGrid
from maploader import LayerType, load_layer, load_map
from sprites.groups import CameraGroup
from sprites.base import StaticCollidableEntity, StaticEntity
from sprites.troops.knights import Warrior


class Level:
    def __init__(self, level: int) -> None:
        map_path = f"level{level}.tmx"
        tmxfp = load_map(map_path)

        self.visible_group = CameraGroup()
        self.collision_group = sprite.Group()

        if tmxfp is not None:
            self.load_map_ui(tmxfp)

    def load_map_ui(self, tmxfp: TiledMap):
        tile_size = tmxfp.tilewidth
        map_size = (tmxfp.height, tmxfp.width)

        ScreenGrid.init_grid(tile_size, map_size)

        # layer name, class to model entity, groups to add(group or Iterable[Group], is_obstacle to mark if layer is obstacle or not)
        layers = [
            (MapLayer.FLOOR, StaticEntity, self.visible_group, False),
            (MapLayer.FLOORFIX, StaticEntity, self.visible_group, False),
            (MapLayer.STAIR, StaticCollidableEntity, self.visible_group, False),
            (MapLayer.WALL, StaticCollidableEntity, self.visible_group, True),
            (MapLayer.BRIDGE, StaticCollidableEntity, self.visible_group, False),
            (MapLayer.CASTLES, StaticEntity, self.visible_group, False),
            (MapLayer.TOWERS, StaticEntity, self.visible_group, True),
            (MapLayer.HOUSES, StaticEntity, self.visible_group, True),
            (MapLayer.DECORATION, StaticEntity, self.visible_group, False),
            (MapLayer.TREES, StaticEntity, self.visible_group, True),
            (MapLayer.SHADOWS, StaticEntity, self.visible_group, False),
            (MapLayer.WARRIOR, Warrior, self.visible_group, False),
        ]

        for name, tile_class, group, is_obstacle in layers:
            layer = load_layer(tmxfp, name)

            if layer:
                self.load_layer_ui(layer, tile_class, group, is_obstacle)
        self.visible_group.init_order()

    def load_layer_ui(
        self,
        layer: LayerType,
        Model: Union[Type[StaticEntity], Type[StaticCollidableEntity], Type[Warrior]],
        groups: Iterable[sprite.Group] | sprite.Group,
        is_obstacle=False,
    ):
        # sorry for this but this complexity came with my intention to return homogenous data for every layer of map

        # If the first argument is None, each tuple in the second argument must have a unique image (str) as the first element.

        # If the first argument is not None, the first element in each tuple of the second argument must be None.

        # Examples:
        # - (None, [(image1, ...), (image2, ...)])      # valid: images provided in tuples
        # - ('some_image', [(None, ...), (None, ...)])  # valid: images are implied by the first argument

        tilesheet_path, layer_data, properties = layer
        tilesheet = None
        if tilesheet_path is not None:
            tilesheet = load(tilesheet_path)

        zindex = properties.get("zindex", 0)

        for image_path, pos, area, correction in layer_data:
            image = None
            if tilesheet is not None:
                image = tilesheet
            else:
                assert type(image_path) == str  # throw later
                image = load(image_path)

            assert type(image) == Surface  # throw later
            if isinstance(groups, sprite.Group):
                groups = (groups,)
            if Model is StaticEntity:
                Model(pos, area, image, correction, zindex, *groups)
            elif Model is StaticCollidableEntity:
                Model(pos, area, image, correction, zindex, *groups)
            elif Model is Warrior:
                Model(pos, properties["zindex"], *groups)
            row = int(pos[1] // ScreenGrid.cell_size)  # type: ignore
            col = int(pos[0] // ScreenGrid.cell_size)  # type: ignore
            if is_obstacle:
                ScreenGrid.add_obstacle_at(row, col, -1)

    def update(self, global_event: Optional[pygame.Event]):
        self.visible_group.update(event=global_event)
        self.collision_group.update()

    def draw(self, surface: Surface):
        self.visible_group.draw(surface)
