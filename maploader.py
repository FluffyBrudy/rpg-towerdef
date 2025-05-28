from typing import Any, Dict, List, Literal, Optional, Tuple, TypedDict, Union, cast
from pathlib import Path
from pytmx import TiledMap, TiledObject, TiledObjectGroup, TiledTileLayer
from constants import MAPS_PATH
from typedefs.globaltype import Coor, FCoor, ImageAreaCoor


class LayerProperties(TypedDict):
    zindex: int
    model: str


LayerType = Tuple[
    Optional[str],
    List[Tuple[Optional[str], Coor, ImageAreaCoor, Union[FCoor, None]]],
    LayerProperties,
]


def load_map(path: Union[str, Path]) -> Optional[TiledMap]:
    """
    Loads a TMX map file and returns a TiledMap object.

    Args:
        path (str | Path): path for tmx file

    Returns:
        Optional[TiledMap]: The loaded map object, or None if loading fails.
    """
    full_path = Path(MAPS_PATH / path)
    if full_path.exists():
        return TiledMap(str(full_path))
    return None


def load_layer(tmxfp: TiledMap, layername: str) -> Optional[LayerType]:
    """
    Loads a layer from a TiledMap and returns its image and structured data.

    Args:
        tmxfp (TiledMap): The TiledMap instance.
        layername (str): The name of the layer to load.

    Returns:
        Optional[LayerType]
        Returns None if the layer is missing or empty.
    """

    layer = tmxfp.layernames.get(layername)
    if layer is None:
        return None

    if isinstance(layer, TiledObjectGroup):
        if len(layer) == 0:
            return None
        image: str = str(layer[0].image[0])

        return (
            None,
            [get_tiledobj_data(tiledobj) for tiledobj in layer],
            cast(LayerProperties, layer.properties),
        )

    if isinstance(layer, TiledTileLayer):
        if layer.width == 0:
            return None
        image: str = next(layer.tiles())[2][0]
        return (
            image,
            [
                (
                    None,
                    (tile_data[0] * tmxfp.tilewidth, tile_data[1] * tmxfp.tileheight),
                    tile_data[2][1],
                    None,
                )
                for tile_data in layer.tiles()
            ],
            cast(LayerProperties, layer.properties),
        )
    return None


def get_tiledobj_data(
    tileobj: TiledObject,
) -> Tuple[str, Coor, ImageAreaCoor, FCoor]:
    """
    Extracts position and image area data from a TiledObject.

    Args:
        tileobj (TiledObject): The object from which to extract data.

    Returns:
        Tuple[Coor, ImageAreaCoor]: A tuple containing:
            - pos (Coor): The (x, y) position of the object.
            - area (ImageAreaCoor): The image area coordinates extracted from the object's image.
    """
    image: Any = tileobj.image
    pos = tileobj.x, tileobj.y
    imfile, area, _ = image
    size = (tileobj.width, tileobj.height)

    return imfile, pos, area, size


if __name__ == "__main__":
    import pygame

    pygame.init()
    fp = load_map(MAPS_PATH / "level1.tmx")
    if fp:
        pass
