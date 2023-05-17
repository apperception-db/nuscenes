from datetime import datetime
from typing import Dict, List

import pandas as pd

from .typings import Frame


def get_videos(
    sample_data: "pd.DataFrame",
    only_keyframe: "bool" = False
) -> "Dict[str, List[Frame]]":
    videos: "Dict[str, List[Frame]]" = {}
    for t in sample_data.itertuples(index=False):
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

    return videos
