from typing import List

from ..typings import Frame


def frame_with_best_alignments(scene: "List[Frame]", fps: int):
    min_misalignment = float('inf')
    max_misalignment_value = None
    misalignments = None
    frame_idx = None
    frame_t = None
    for idx, frame in enumerate(scene):
        t = frame[9]
        misalignment = 0.
        _max_misalignment_value = -float('inf')
        _misalignments = []
        for _frame in scene:
            _t = _frame[9]
            sec_diff = (t - _t).total_seconds()
            _misalignment = sec_diff * fps
            _m = _misalignment - round(_misalignment)
            _misalignments.append(_m)
            m = abs(_m)
            misalignment += m
            _max_misalignment_value = max(_max_misalignment_value, m)
        if misalignment < min_misalignment:
            min_misalignment = misalignment
            frame_idx = idx
            frame_t = t
            max_misalignment_value = _max_misalignment_value
            misalignments = _misalignments
    if frame_idx is None or frame_t is None or max_misalignment_value is None or misalignments is None:
        raise Exception(f'frame_idx: {frame_idx}, frame_t: {frame_t}, max_misalignment_value: {max_misalignment_value}, misalignments: {misalignments}')

    print(f"misalignment: {(min_misalignment * 100 / len(scene)):.10f} %")
    print(f"max misalignment: {(max_misalignment_value * 100):.3f} %")
    assert max_misalignment_value < 0.15
    return frame_idx, frame_t, misalignments
