from typing import List

from tiles.border import TileBorder, transform_border_arrays

import numpy as np

from tiles.features import get_features_from_tiles, get_border_classes


class Classifier:
    def __init__(self, clf):
        """

        Args:
            clf: sklearn-classifier with `fit()` and `predict()` method
        """
        self.clf = clf

    def fit(self, tiles: List[np.ndarray], tile_borders: List[TileBorder]):
        x = get_features_from_tiles(tiles)
        y = get_border_classes(tile_borders)

        assert len(x) == len(
            y
        ), f"number of tiles x 4 := {len(x)} != {len(y)} =: tile borders"

        self.clf.fit(x, y)

    def predict(self, tiles: List[np.ndarray]) -> List[TileBorder]:
        x = get_features_from_tiles(tiles)
        y = self.clf.predict(x)
        if len(y) > len(TileBorder.__annotations__):
            y = np.split(y, len(TileBorder.__annotations__))
        else:
            y = [y]

        tile_borders: List[TileBorder] = transform_border_arrays(y)

        return tile_borders
