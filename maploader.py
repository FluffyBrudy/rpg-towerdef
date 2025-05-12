from typing import Any, List, Optional, Tuple, Union
from pathlib import Path
from pytmx import TiledMap, TiledObject, TiledObjectGroup, TiledTileLayer
from constants import MAPS_PATH
from typedefs.globaltype import Coor, ImageAreaCoor
from pprint import pprint as print


LayerType = Tuple[str, List[Tuple[Coor, ImageAreaCoor]]]


def maploader(path: Union[str, Path]):
    return TiledMap(str(path))


def load_layer(tmxfp: TiledMap, layername: str) -> Optional[LayerType]:
    layer = tmxfp.layernames.get(layername)
    if layer is None:
        return None

    if isinstance(layer, TiledObjectGroup):
        if len(layer) == 0:
            return None
        image: str = str(layer[0].image[0])
        return image, [get_tiledobj_data(tiledobj) for tiledobj in layer]

    if isinstance(layer, TiledTileLayer):
        if layer.width == 0:
            return None
        image: str = next(layer.tiles())[2][0]
        return (
            image,
            [
                (
                    (tile_data[0] * tmxfp.tilewidth, tile_data[1] * tmxfp.tileheight),
                    tile_data[2][1],
                )
                for tile_data in layer.tiles()
            ],
        )
    return None


def get_tiledobj_data(
    tileobj: TiledObject,
) -> Tuple[Coor, ImageAreaCoor]:
    image: Any = tileobj.image
    pos = tileobj.x, tileobj.y
    _, area, _ = image
    return pos, area


if __name__ == "__main__":
    import pygame

    pygame.init()
    fp = maploader(MAPS_PATH / "level1.tmx")
    layernames = list(fp.layernames.keys())
    print(load_layer(fp, "floorlayer"))
    print(layernames)
