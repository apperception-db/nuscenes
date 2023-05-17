import os
from datetime import datetime

import cv2
import numpy.typing as npt
import pandas as pd
from tqdm import tqdm

from .load_image import load_image
from .typings import Frame


def get_compose_and_videos(
    fps: int, raw_dir: str, processed_dir: str, only_keyframe: bool, interpolate: bool
):
    sample_data = pd.read_pickle(os.path.join(processed_dir, 'sample_data.pkl'))
    videos: "dict[str, list[Frame]]" = {}
    for t in tqdm(sample_data.itertuples(index=False), total=len(sample_data)):
        if only_keyframe and not t.is_key_frame:
            continue

        scene = t.scene_name
        key = f"{scene}-{t.channel}"
        if key not in videos:
            videos[key] = []
        t = Frame(
            key,
            t.token,
            t.frame_order,
            t.filename,
            t.camera_translation,
            t.camera_rotation,
            t.camera_intrinsic,
            t.ego_translation,
            t.ego_rotation,
            datetime.fromtimestamp(t.timestamp / 1_000_000),
            t.camera_heading,
            t.ego_heading,
            t.location
        )
        videos[key].append(t)

    for video in videos.values():
        video.sort(key=lambda v: v[9])


    def compose(location: str, name: str, scene: "list[Frame]", img_cache: "dict[str, npt.NDArray] | None" = None):
        scene.sort(key=lambda s: s.timestamp)

        if img_cache is None:
            img_cache = {}

        _frames: "list[tuple[npt.NDArray, int]]" = []
        for i, frame in tqdm(enumerate(scene), total=len(scene)):
            _frames.append((load_image(img_cache, frame.filename, raw_dir), i))

        filename = f'{location}-{name}.mp4'
        if only_keyframe:
            filename = 'keyframe-' + filename
        base = os.path.join(processed_dir, "videos")
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

    return compose, videos
