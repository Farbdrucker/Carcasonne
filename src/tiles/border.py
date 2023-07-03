from enum import Enum
from dataclasses import dataclass
from typing import List, Dict
import numpy as np


class Border(int, Enum):
    STREET: int = 0
    FIELD: int = 1
    CITY: int = 2


STREET = Border.STREET
FIELD = Border.FIELD
CITY = Border.CITY

border_map: Dict[int, int] = {0: Border.STREET, 1: Border.FIELD, 2: Border.CITY}
border_acronym: Dict[str, int] = {
    "s": Border.STREET,
    "f": Border.FIELD,
    "c": Border.CITY,
}


@dataclass
class TileBorder:
    top: Border
    right: Border
    bottom: Border
    left: Border

    def trbl(self) -> List[Border]:
        return [self.top, self.right, self.bottom, self.left]

    def trbl_classes(self) -> List[int]:
        return [border.value for border in self.trbl()]

    @classmethod
    def cast(cls, border_classes: List[int]):
        return cls(*map(lambda x: border_map[x], border_classes))


def border_class_map(value: int) -> int:
    return border_map[value]


def transform_border_array(border_array: np.ndarray) -> List[int]:
    return list(map(border_class_map, border_array))


def transform_border_arrays(border_arrays: np.ndarray) -> List[TileBorder]:
    return list(map(lambda x: TileBorder(*transform_border_array(x)), border_arrays))
