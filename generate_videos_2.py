#!/usr/bin/env python
# coding: utf-8

# In[1]:


from typing import List, Tuple
from datetime import datetime, timedelta
import numpy.typing as npt
import numpy as np
import os
import cv2
import pickle
from tqdm import tqdm
import itertools
import json

from utils.compose2_factory import compose2_factory
from utils.data_dirs import data_dirs
from utils.get_videos import get_videos
from utils.frame_json_encoder import FrameJSONEncoder
from utils.typings import Frame


# In[2]:


raw_dir, processed_dir, folder, EXPERIMENT_DATA, suffix, *_ = data_dirs(False)
print(raw_dir)
print(processed_dir)
print(folder)
print(EXPERIMENT_DATA)
print(suffix)


# In[3]:


fps = 20


# In[4]:


interpolate = False


# In[5]:


partition_dir = os.path.join(processed_dir, 'partition')


# In[6]:


compose = compose2_factory(fps, raw_dir, processed_dir, interpolate)


# In[7]:


def iframe(timestamp: "datetime"):
    return Frame(None, None, None, None, None, None, None, None, None, timestamp, None, None)


# In[ ]:


for l in os.listdir(partition_dir):
    d = os.path.join(partition_dir, l)
    with open(os.path.join(d, 'sample_data.pickle'), "rb") as f:
        sample_data = pickle.load(f)
    videos = get_videos(sample_data)
    
    
    output = {}
    for name in videos:
        video = videos[name]
        frames, filename, misalignment = compose(l, name, video)
#         prev = video[0][9]
#         for v in video[1:]:
#             print(int(round((v[9] - prev).total_seconds() * 100,)))
#             prev = v[9] 
        output[name] = {
            "filename": filename,
            "start": video[0][9],
            "columns": [
                "cameraId",
                "frameId",
                "frameNum",
                "filename",
                "cameraTranslation",
                "cameraRotation",
                "cameraIntrinsic",
                "egoTranslation",
                "egoRotation",
                "timestamp",
                "cameraHeading",
                "egoHeading",
            ],
            "frames": [
                (iframe(f) if isinstance(f, datetime) else tuple(video[f]))
                for img, f in frames
            ]
        }
        print("done", filename)
    base = os.path.join(processed_dir, 'videos', l)
    with open(os.path.join(base, 'frames-skip.pickle'), "wb") as f:
        pickle.dump(output, f)
    
    with open(os.path.join(base, 'frames-skip.json'), "w") as f:
        json.dump(output, f, indent=2, sort_keys=True, cls=FrameJSONEncoder)


# In[ ]:





# In[ ]:




