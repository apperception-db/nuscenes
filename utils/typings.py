from datetime import datetime
from typing import Tuple

Float3 = Tuple[float, float, float]
Float4 = Tuple[float, float, float, float]
Float33 = Tuple[Float3, Float3, Float3]
Frame = Tuple[str, str, int, str, Float3, Float4, Float33, Float3, Float4, datetime, float, float]