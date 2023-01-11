import json
import datetime

import numpy as np

class FrameJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, datetime.datetime):
            return str(o)
        return super().default(o)