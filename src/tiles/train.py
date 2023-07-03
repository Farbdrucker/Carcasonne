import datetime
import json
import os.path
import uuid

from sklearn.metrics import confusion_matrix, balanced_accuracy_score
import random
import numpy as np
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, List, Dict
from sklearn import svm
from typer import Typer


from src.rlogging import log
from src.tiles.border import TileBorder
from src.tiles.features import get_border_classes
from src.tiles.model import Classifier
from src.utils.image import imread

app = Typer()


@dataclass
class Dataset:
    data: Dict[str, List[int]]

    @property
    def tiles(self):
        tiles: List["np.ndarray"] = [imread(file) for file in self.data.keys()]
        return tiles

    @property
    def tile_borders(self) -> List[TileBorder]:
        return [TileBorder.cast(classes) for classes in self.data.values()]

    def __len__(self):
        return len(self.data)


def load_ds(annotation_fname: Path) -> Dataset:
    with open(annotation_fname) as f:
        data = json.load(f)

    return Dataset(data)


def split_ds(ds: Dataset, p: float = 0.1) -> Tuple[Dataset, Dataset]:
    indices = np.array(list(range(len(ds))))
    random.shuffle(indices)
    data = ds.data
    fnames = np.array(list(data.keys()))
    classes = np.array(list(data.values()))

    num_train = int((1 - p) * len(ds))
    train_indices = indices[:num_train]
    eval_indiecs = indices[num_train:]

    train_fnames = fnames[train_indices]
    train_classes = classes[train_indices]

    eval_fnames = fnames[eval_indiecs]
    eval_classes = classes[eval_indiecs]

    ds_train = Dataset(dict(zip(train_fnames, train_classes)))
    ds_eval = Dataset(dict(zip(eval_fnames, eval_classes)))
    return ds_train, ds_eval


class TrainableModel(Classifier):
    def fit(self, ds_train: Dataset):
        super().fit(ds_train.tiles, ds_train.tile_borders)

    def eval(self, eval_ds: Dataset):
        log(f"evaluating {eval_ds}")
        prediction = self.predict(eval_ds.tiles)

        y_true = get_border_classes(eval_ds.tile_borders)
        y_pred = get_border_classes(prediction)

        cm = confusion_matrix(y_true, y_pred)
        bal_acc = balanced_accuracy_score(y_true, y_pred)

        print(f"Confusion matrix")
        print(cm)
        print("balanced accuracy")
        print(bal_acc)

    def save(self, checkpoint_fname: Path):
        log(f"saving model to {checkpoint_fname}")
        from joblib import dump

        dump(self.clf, checkpoint_fname)


def create_checkpoint_name(annotation_fname: Path):
    dir_name = os.path.dirname(annotation_fname)
    base_name = os.path.basename(annotation_fname).split(".")[0]
    _id = uuid.uuid4()
    now = datetime.datetime.now()

    checkpoint_name = f"{now.year}-{now.month}-{now.day}_{_id}_{base_name}.joblib"

    return os.path.join(dir_name, checkpoint_name)


@app.command()
def train(annotation_fname: Path, checkpoint_dir: Path = None):
    checkpoint_dir = checkpoint_dir or create_checkpoint_name(annotation_fname)
    ds = load_ds(annotation_fname)
    train_ds, eval_ds = split_ds(ds)

    svc = svm.SVC(kernel="poly", degree=3)
    model = TrainableModel(svc)

    model.fit(train_ds)
    model.eval(eval_ds)
    model.save(checkpoint_dir)


if __name__ == "__main__":
    app()
