import os
import json
from inovopy.geometry.transform import Transform

TRANSFORM_DATA_FILE = "./calibration-transform.json"

def load_transform_data() -> dict:
    transform_data = {}
    if os.path.isfile(TRANSFORM_DATA_FILE):
        with open(TRANSFORM_DATA_FILE, "r") as f:
            transform_data = json.load(f)
    
    for key in transform_data:
        val = transform_data[key]
        if not isinstance(val, dict):
            continue
        if "target" not in val:
            continue
        if val["target"] == "transform":
            transform_data[key] = Transform.from_dict(val)
    
    return transform_data

def save_transform_data(data:dict):
    data = data.copy()
    for key in data:
        val = data[key]
        if isinstance(val, Transform):
            data[key] = val.to_dict()
    
    with open(TRANSFORM_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)