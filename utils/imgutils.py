from enum import Enum
from pathlib import Path
from posixpath import dirname
from typing import Dict, List, Optional, Tuple, cast
from PIL import Image
import pygame
from pygame.image import frombytes, load as imload
import os, pprint

from typedefs.globaltype import StateFrames
from utils.pathutils import list_files_sorted

"""
Purpose is to: 
    manipulate images, 
    optimize image loading by removin unnecessary rectangular area of transparent pixels
"""


def imload_cropped(fp: str, /) -> Tuple[bytes, Tuple[int, int]]:
    """
    Return bytes after cropping image if there are empty croppable transparent pixel rect

    Args:
        fp: str path of png image file to be loaded
    Returns:
        Tuple[bytes, Tuple[int, int]] returns byte of cropped image and size of cropped image
    """
    if os.path.splitext(fp)[1] != ".png":
        raise ValueError("Invalid file require png")
    if not os.path.exists(fp):
        raise FileNotFoundError("Image not found")
    img = Image.open(fp).convert("RGBA")
    cropped_img = img.crop(img.getbbox())
    return cropped_img.tobytes(), cropped_img.size


def load_image(fp: str, /, crop=False) -> pygame.Surface:
    """
    load image from bytes and returns pygame surface
    """
    if crop:
        image_bytes, size = imload_cropped(fp)
        surface = frombytes(image_bytes, size, "RGBA")
        return surface
    else:
        return imload(fp).convert_alpha()


def load_frames(frame_dir: str | Path, /, crop=False) -> Tuple[pygame.Surface]:
    surfaces = []

    for imgfile in list_files_sorted(frame_dir, filter="*.png"):
        imgpath = os.path.join(frame_dir, imgfile)
        surface = load_image(imgpath, crop)
        surfaces.append(surface)

    return tuple(surfaces)


def load_uniform_state_frames(frames_dir: str) -> StateFrames:
    """
    load state based images

    Args:
        frames_dir: str directory for state lookup
    Returns:
        return dictionary of state as key and list of frames associated with state
    """
    frame_subdirs = [
        frame_dir for frame_dir in os.listdir(frames_dir) if os.path.isdir(frames_dir)
    ]

    state_frames_map: StateFrames = {}

    for _dir in frame_subdirs:
        surfaces = []
        dir_path = os.path.join(frames_dir, _dir)
        for imfile in os.listdir(dir_path):
            image_path = os.path.join(dir_path, imfile)
            surfaces.append(load_image(image_path))
        state_frames_map[_dir] = tuple(surfaces)

    return state_frames_map
