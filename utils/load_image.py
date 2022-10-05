import os
from typing import Dict

import cv2
import numpy.typing as npt


def load_image(
    cache: "Dict[str, npt.NDArray]", name: str, raw_dir: str
) -> "npt.NDArray":
    if name not in cache:
        cache[name] = cv2.imread(os.path.join(raw_dir, name))
    return cache[name]
