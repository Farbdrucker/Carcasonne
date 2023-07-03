from typing import List

import numpy as np

from tiles.border import TileBorder
from utils.func import flatten
from utils.image import rotate270, rotate180, rotate90


def get_top_feature(img: np.ndarray) -> np.ndarray:
    return img[0:1].flatten()


def get_right_feature(img: np.ndarray) -> np.ndarray:
    return get_top_feature(rotate270(img))


def get_bottom_feature(img: np.ndarray) -> np.ndarray:
    return get_top_feature(rotate180(img))


def get_left_feature(img: np.ndarray) -> np.ndarray:
    return get_top_feature(rotate90(img))


def get_features(img: np.ndarray) -> List[np.ndarray]:
    extractors = (
        get_top_feature,
        get_right_feature,
        get_bottom_feature,
        get_left_feature,
    )
    return [extract(img) for extract in extractors]


def get_features_from_tiles(tiles: List[np.ndarray]) -> np.ndarray:
    return np.array(flatten([get_features(tile) for tile in tiles]))


def get_border_classes(tile_borders: List[TileBorder]) -> np.ndarray:
    return np.array(flatten([tile_boder.trbl_classes() for tile_boder in tile_borders]))
