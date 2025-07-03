import datetime
import os
from constants import DEFAULT_FILE_NAME_PREFFIX

def get_distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return int(((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5)


def get_timestamp_filename(prefix=DEFAULT_FILE_NAME_PREFFIX, ext=".png"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{prefix}_{timestamp}{ext}"


def get_unique_filename(base_name=DEFAULT_FILE_NAME_PREFFIX, ext=".png"):
    i = 1
    filename = f"{base_name}{ext}"
    while os.path.exists(filename):
        filename = f"{base_name}_{i}{ext}"
        i += 1
    return filename
