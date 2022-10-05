import math

from pyquaternion import Quaternion

from .normalize_angle import normalize_angle


def get_heading_from_north(rotation: "Quaternion"):
    yaw = rotation.yaw_pitch_roll[0]
    return normalize_angle(yaw - (math.pi / 2))
