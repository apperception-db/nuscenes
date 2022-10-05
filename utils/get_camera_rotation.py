from typing import List

import numpy.typing as npt
from pyquaternion import Quaternion


def get_camera_rotation(
    camera_rotation: "List[float]", ego_rotation: "List[float]"
) -> "npt.NDArray":
    return (Quaternion(camera_rotation) * Quaternion(ego_rotation)).q
