import random
from dataclasses import dataclass
from enum import Enum
from typing import List

import numpy as np

"""
https://dev.to/kavinbharathi/the-fascinating-wave-function-collapse-algorithm-4nc3
"""


class Direction(Enum):
    UP = "up"
    LEFT = "left"
    DOWN = "down"
    RIGHT = "right"


@dataclass()
class Tile:
    img: np.ndarray
    edges: List[Direction]
    up: List["Tile"]
    right: List["Tile"]
    down: List["Tile"]
    left: List["Tile"]
    index: int = -1

    def set_rules(self, tiles: List["Tile"]):
        for tile in tiles:
            pass


@dataclass
class Cell:
    x: int
    y: int
    resolution: int
    options: List[Tile]
    collapsed: bool = False

    def entropy(self):
        """
        return the entropy/the length of the options
        """
        return len(self.options)

    def update(self):
        """
        update the collapsed variable
        """
        self.collapsed = bool(self.entropy() == 1)

    def observe(self):
        """
        observe the cell/collapse cell
        """
        if self.options:
            self.options = [random.choice(self.options)]
            self.collapsed = True

        return None


@dataclass
class Grid:
    width: int
    height: int
    resolution: int
    options: List[Tile]

    def __post_init__(self):
        self.grid = np.empty((self.height, self.width), dtype=Cell)

    @property
    def w(self):
        return self.width // self.resolution

    @property
    def h(self):
        return self.height // self.resolution
