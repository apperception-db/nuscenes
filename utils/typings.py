from datetime import datetime
from typing import NamedTuple, Tuple

Float3 = Tuple[float, float, float]
Float4 = Tuple[float, float, float, float]
Float33 = Tuple[Float3, Float3, Float3]

class Frame(NamedTuple):
    scene: str
    token: str
    frame_order: int
    filename: str
    camera_translation: Float3
    camera_rotation: Float4
    camera_intrinsic: Float33
    ego_translation: Float3
    ego_rotation: Float4
    timestamp: datetime
    camera_heading: float
    ego_heading: float
    location: 'str' = ''