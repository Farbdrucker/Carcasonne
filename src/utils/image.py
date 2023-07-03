import cv2
import numpy as np


def imread(fname: str) -> np.ndarray:
    img = cv2.imread(fname)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


def imshow(image: np.ndarray, window_name: str = "image", wait_key: int = 200):
    cv2.imshow(window_name, image)
    cv2.waitKey(wait_key)


def rotate90(img: np.ndarray) -> np.ndarray:
    return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)


def rotate180(img: np.ndarray) -> np.ndarray:
    return cv2.rotate(img, cv2.ROTATE_180)


def rotate270(img: np.ndarray) -> np.ndarray:
    return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
