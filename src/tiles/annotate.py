import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from typer import Typer

from src.tiles.border import TileBorder, border_acronym
from src.utils.image import imread, imshow

app = Typer()


def cast_border_types(border_types: str) -> TileBorder:
    return TileBorder(*map(lambda x: border_acronym[x], border_types))


@dataclass
class Annotate:
    dir_name: Path
    annotation_fname: Path = "annotation.json"
    number_images: int = 10

    def __post_init__(self):
        self.annotation: Dict[str, List[int]] = {}

    def __iter__(self) -> str:
        tile_names = list(
            os.path.join(self.dir_name, v.name)
            for v in os.scandir(self.dir_name)
            if v.name.endswith(".png")
        )

        for k, tile_name in enumerate(tile_names):
            if k < self.number_images:
                yield tile_name

    def __enter__(self):
        self.annotation = {}

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(os.path.join(self.dir_name, self.annotation_fname), "w") as f:
            json.dump(self.annotation, f)

    def __call__(self, img_name: Path):
        image = imread(img_name)
        imshow(image, f"Annotate {os.path.basename(img_name)}", 0)

        border_types = input("border classes top,right,bottom,left as {s,f,c}")

        borders = cast_border_types(border_types)

        self.annotation[str(os.path.basename(img_name))] = borders.trbl_classes()


@app.command()
def annotate(dir_name: Path, number_images: int = 10):
    annotator = Annotate(dir_name=dir_name, number_images=number_images)

    with annotator:
        for img in annotator:
            annotator(img)


if __name__ == "__main__":
    app()
