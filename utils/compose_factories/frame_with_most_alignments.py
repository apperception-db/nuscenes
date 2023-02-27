from typing import List

from ..typings import Frame


def frame_with_most_alignments(scene: "List[Frame]", fps: int):
    max_aligned_frames = -1
    frame_idx = None
    frame_t = None
    for idx, frame in enumerate(scene):
        t = frame[9]
        aligned_frames = 0
        for _frame in scene:
            _t = _frame[9]
            sec_diff = (t - _t).total_seconds()
            if (sec_diff * fps).is_integer():
                aligned_frames += 1
        if aligned_frames > max_aligned_frames:
            max_aligned_frames = aligned_frames
            frame_idx = idx
            frame_t = t
    if frame_idx is None or frame_t is None:
        raise Exception()
    return frame_idx, frame_t, max_aligned_frames
