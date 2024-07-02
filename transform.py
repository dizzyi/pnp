import os
import json
from inovopy.geometry.transform import Transform
from inovopy.logger import Logger
from inovopy.robot import InovoRobot

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

def command_control(logger: Logger, bot: InovoRobot):
    while True:
        in_tok = input(":").split(",")

        t = Transform()
        try:
            if "x" in in_tok[0]:
                val = float(in_tok[1])
                t.then_x(val)
            elif "y" in in_tok[0]:
                val = float(in_tok[1])
                t.then_y(val)
            elif "z" in in_tok[0]:
                val = float(in_tok[1])
                t.then_z(val)
            elif "q" in in_tok[0]:
                break
            else:
                logger.warn("unknown command")
        except (IndexError, ValueError) as e:
            logger.warn(f"{e}")

        bot.linear_relative(t)