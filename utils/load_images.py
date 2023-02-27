import multiprocessing
from .load_image import load_image

import numpy.typing as npt
from tqdm import tqdm


def load_images(raw_dir: "str", files: "list[str]") -> "dict[str, npt.NDArray]":

    # TODO: should we just use async-io instead of 
    print("Reading images")
    with multiprocessing.Pool() as pool:
        out = tqdm(pool.imap_unordered(_load, map(lambda name: (name, raw_dir), files)), total=len(files))

        return {
            name: image
            for name, image
            in out
        }


def _load(args: "tuple[str, str]"):
    name, raw_dir = args
    return name, load_image({}, name, raw_dir)
