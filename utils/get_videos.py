from datetime import datetime
from typing import Dict, List

import pandas as pd

from .typings import Frame


def get_videos(sample_data: "pd.DataFrame") -> "Dict[str, List[Frame]]":
    videos: "Dict[str, List[Frame]]" = {}
    for t in sample_data.itertuples(index=False):
        scene = t.scene_name
        file = t.filename.split("/")[1]
        key = f"{scene}-{file}"
        if key not in videos:
            videos[key] = []
        t = (
            t.scene_name,
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
        )
        videos[key].append(t)

    for video in videos.values():
        video.sort(key=lambda v: v[9])

    return videos
