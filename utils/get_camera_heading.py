import math

import numpy as np
from pyquaternion import Quaternion

from .get_heading import get_heading

ROT = Quaternion(axis=[1, 0, 0], angle=np.pi / 2)


def get_camera_heading(rotation: "Quaternion"):
    return -get_heading(ROT.rotate(rotation)) + math.pi / 2
