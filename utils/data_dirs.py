import os
from typing import NamedTuple

DATA = "/work/apperception/data"
EXPERIMENT_DATA = "EXPERIMENT_DATA"

TRAINVAL = "nuScenes/full-dataset-v1.0/Trainval"
NUSCENES_RAW_DATA = "NUSCENES_RAW_DATA"
NUSCENES_PROCESSED_DATA = "NUSCENES_PROCESSED_DATA"

ROAD = "road-network"
NUSCENES_RAW_ROAD = "NUSCENES_RAW_ROAD"
NUSCENES_PROCESSED_ROAD = "NUSCENES_PROCESSED_ROAD"

MAP = "nuScenes/Map-expansion"
NUSCENES_RAW_MAP = "NUSCENES_RAW_MAP"
NUSCENES_PROCESSED_MAP = "NUSCENES_PROCESSED_MAP"


class Dirs(NamedTuple):
    raw_dir: str
    processed_dir: str
    folder: str
    experiment_dir: str
    suffix: str
    raw_road: str
    processed_road: str
    raw_map: str
    processed_map: str


def data_dirs(experiment: bool = False):
    experiment_dir = os.path.join(DATA, "raw/scenic/experiment_data")
    if EXPERIMENT_DATA in os.environ:
        experiment_dir = os.environ[EXPERIMENT_DATA]

    if experiment:
        suffix = "_experiment"
    else:
        suffix = ""

    if NUSCENES_RAW_DATA in os.environ:
        raw_dir = os.environ[NUSCENES_RAW_DATA]
    else:
        raw_dir = os.path.join(DATA, "raw", TRAINVAL)

    if NUSCENES_PROCESSED_DATA in os.environ:
        processed_dir = os.environ[NUSCENES_PROCESSED_DATA]
    else:
        processed_dir = os.path.join(DATA, "processed", TRAINVAL)

    for d in os.listdir(raw_dir):
        if d.startswith("v1.0-"):
            folder = d
            break

    if NUSCENES_RAW_ROAD in os.environ:
        raw_road = os.environ[NUSCENES_RAW_ROAD]
    else:
        raw_road = os.path.join(DATA, "raw", ROAD)

    if NUSCENES_PROCESSED_ROAD in os.environ:
        processed_road = os.environ[NUSCENES_PROCESSED_ROAD]
    else:
        processed_road = os.path.join(DATA, "processed", ROAD)

    if NUSCENES_RAW_MAP in os.environ:
        raw_map = os.environ[NUSCENES_RAW_MAP]
    else:
        raw_map = os.path.join(DATA, "raw", MAP)

    if NUSCENES_PROCESSED_MAP in os.environ:
        processed_map = os.environ[NUSCENES_PROCESSED_MAP]
    else:
        processed_map = os.path.join(DATA, "processed", MAP)

    return Dirs(
        raw_dir,
        processed_dir,
        folder,
        experiment_dir,
        suffix,
        raw_road,
        processed_road,
        raw_map,
        processed_map,
    )
