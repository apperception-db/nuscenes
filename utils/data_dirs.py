import os

DATA = "/work/apperception/data"
TRAINVAL = "nuScenes/full-dataset-v1.0/Trainval"
EXPERIMENT_DATA = "EXPERIMENT_DATA"
NUSCENES_RAW_DATA = "NUSCENES_RAW_DATA"
NUSCENES_PROCESSED_DATA = "NUSCENES_PROCESSED_DATA"


def data_dirs(experiment: bool):
    experiment_dir = os.path.join(DATA, "raw/scenic/experiment_data")
    if EXPERIMENT_DATA in os.environ:
        experiment_dir = os.environ[EXPERIMENT_DATA]
    experiment_dir

    if experiment:
        suffix = "_experiment"
    else:
        suffix = ""

    if NUSCENES_RAW_DATA in os.environ:
        raw_dir = os.environ[NUSCENES_RAW_DATA]
    else:
        raw_dir = os.path.join(DATA, "raw", TRAINVAL)
    raw_dir

    if NUSCENES_PROCESSED_DATA in os.environ:
        processed_dir = os.environ[NUSCENES_PROCESSED_DATA]
    else:
        processed_dir = os.path.join(DATA, "processed", TRAINVAL)
    processed_dir

    for d in os.listdir(raw_dir):
        if d.startswith("v1.0-"):
            folder = d
            break
    folder

    return (raw_dir, processed_dir, folder, experiment_dir, suffix)
