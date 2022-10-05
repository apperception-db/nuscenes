from typing import List

import numpy as np
import numpy.typing as npt
from pyquaternion import Quaternion


def get_camera_position(
    camera_translation: "List[float]",
    ego_translation: "List[float]",
    ego_rotation: "List[float]",
) -> "npt.NDArray":
    rotated_offset = Quaternion(ego_rotation).rotate(
        np.array(camera_translation)
    )
    return np.array(ego_translation) + rotated_offset
