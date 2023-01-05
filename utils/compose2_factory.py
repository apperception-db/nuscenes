import datetime
import itertools
import os
from datetime import timedelta
from typing import Any, List, Tuple

import cv2
import numpy as np
import numpy.typing as npt
from tqdm import tqdm

from .frame_with_best_alignments import frame_with_best_alignments
from .load_image import load_image
from .typings import Frame


def compose2_factory(
    fps: int, raw_dir: str, processed_dir: str, interpolate: bool
):
    spf = 1. / fps
    def compose(location: str, name: str, scene: "List[Frame]"):
        scene.sort(key=lambda s: s.timestamp)
        t_start = scene[0].timestamp

        img_cache = {}
        _frames: "list[Tuple[npt.NDArray, int | None]]" = [(load_image(img_cache, scene[0].filename, raw_dir), 0)]
        prev_frame = None
        for i, frame in tqdm(enumerate(scene), total=len(scene)):
            if prev_frame is not None:
                _time_diff = frame.timestamp - prev_frame.timestamp
                frame_diff = int(round(_time_diff.total_seconds() / spf))
                assert abs(frame_diff - (_time_diff.total_seconds() / spf)) < 0.2, _time_diff
                assert frame_diff < 10, frame_diff

                for t in range(1, frame_diff):
                    if t > frame_diff - t:
                        img = load_image(img_cache, frame.filename, raw_dir)
                    else:
                        img = load_image(img_cache, prev_frame.filename, raw_dir)
                    _frames.append((img, None))

            prev_frame = frame
            _frames.append((load_image(img_cache, frame.filename, raw_dir), i))

        t0 = t_start
        t0_tuple = (
            t0.year,
            t0.month,
            t0.day,
            t0.hour,
            t0.minute,
            t0.second,
            t0.microsecond,
        )
        filename = f'skipped-{name}-{"-".join([*map(str, t0_tuple)])}.mp4'
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

        return _frames, filename

    return compose
