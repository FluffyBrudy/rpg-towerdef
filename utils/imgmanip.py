from PIL import Image
import os


def get_cropable_rect(fp: str) -> Tuple[int, int, int, int]:
    if os.path.splitext(fp)[0] != "png":
        raise ValueError("Invalid file require png")
    if not os.path.exists(fp):
        raise FileNotFoundError("Image not found")
    img = Image.open(fp).convert("RGBA")
    rectbox = img.getbbox()
    if rectbox is not None:
        return rectbox
    return (0, 0, *img.size)
