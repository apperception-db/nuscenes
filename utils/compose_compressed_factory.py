import os
from typing import List, Tuple

import cv2
import numpy.typing as npt
from tqdm import tqdm

from .load_image import load_image
from .typings import Frame


def compose_compressed_factory(
    fps: int, raw_dir: str, processed_dir: str, interpolate: bool
):
    def compose(location: str, name: str, scene: "List[Frame]", img_cache: "dict[str, npt.NDArray] | None" = None):
        scene.sort(key=lambda s: s.timestamp)

        if img_cache is None:
            img_cache = {}

        _frames: "list[Tuple[npt.NDArray, int]]" = []
        for i, frame in tqdm(enumerate(scene), total=len(scene)):
            _frames.append((load_image(img_cache, frame.filename, raw_dir), i))

        filename = f'compressed-{name}.mp4'
        base = os.path.join(processed_dir, "videos", location)
        if not os.path.exists(base):
            os.makedirs(base)
        out = cv2.VideoWriter(
            os.path.join(base, filename),
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            _frames[0][0].shape[1::-1],
        )
        print(f"Writing scene ({os.path.join(base, filename)}):")
        for frame, i in tqdm(_frames):
            out.write(frame)
        out.release()
        cv2.destroyAllWindows()

        return _frames, filename, [0]

    return compose
