import itertools
import os
from datetime import timedelta
from typing import List

import cv2
import numpy as np
import numpy.typing as npt
from tqdm import tqdm

from .frame_with_best_alignments import frame_with_best_alignments
from .load_image import load_image
from .typings import Frame


def compose_factory(
    fps: int, raw_dir: str, processed_dir: str, interpolate: bool
):
    def compose(location: str, name: str, scene: "List[Frame]"):
        t_start = scene[0][9]
        t_end = scene[-1][9]

        frame_idx, frame_t = frame_with_best_alignments(scene, fps)

        frames_before = int((frame_t - t_start).total_seconds() * fps)

        def get_timestamp(idx: int):
            return frame_t - timedelta(seconds=(frames_before - idx) / fps)

        assert get_timestamp(0) >= t_start, f"{get_timestamp(0)} {t_start}"

        frames: "List[npt.NDArray]" = []
        frame_idx = 0
        img_cache = {}
        print("Reading scene:", name)
        n = 0
        while get_timestamp(n) < t_end:
            t = get_timestamp(n)
            n += 1

        for i in tqdm(itertools.count(), total=n):
            if get_timestamp(i) >= t_end:
                break

            t = get_timestamp(i)
            while scene[frame_idx + 1][9] < t:
                frame_idx += 1
            f_curr = scene[frame_idx][3]
            f_next = scene[frame_idx + 1][3]

            t_curr = scene[frame_idx][9]
            t_next = scene[frame_idx + 1][9]

            img_curr = load_image(img_cache, f_curr, raw_dir)
            img_next = load_image(img_cache, f_next, raw_dir)

            ratio = (t - t_curr).total_seconds() / (
                t_next - t_curr
            ).total_seconds()

            if interpolate:
                img = (img_curr * (1 - ratio) + img_next * ratio).astype(
                    np.uint8
                )
            else:
                if ratio < 0.5:
                    img = img_curr
                else:
                    img = img_next
            frames.append(img)

        t0 = get_timestamp(0)
        t0_tuple = (
            t0.year,
            t0.month,
            t0.day,
            t0.hour,
            t0.minute,
            t0.second,
            t0.microsecond,
        )
        filename = f'{name}-{"-".join([*map(str, t0_tuple)])}.mp4'
        base = os.path.join(processed_dir, "videos", location)
        if not os.path.exists(base):
            os.makedirs(base)
        out = cv2.VideoWriter(
            os.path.join(base, filename),
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            frames[0].shape[1::-1],
        )
        print(f"Writing scene ({os.path.join(base, filename)}):")
        for frame in tqdm(frames):
            out.write(frame)
        out.release()
        cv2.destroyAllWindows()

        return frames, filename, get_timestamp(0)

    return compose
