import numpy
import itertools
from inovopy.logger import Logger
from transform import *
from calculation import *

def calibration_calculation():
    logger = Logger.default("Calibration - Calculation")

    transform_data = load_transform_data()

    uv = []
    xy = []
    
    for anchor_data in transform_data['anchors']:
        x = anchor_data['x']
        y = anchor_data['y']
        u = anchor_data['u']
        v = anchor_data['v']
        logger.info(f"anchor data: {anchor_data}")
        row1 = [u,v,1,0,0,0]
        row2 = [0,0,0,u,v,1]
        uv.append(row1)
        uv.append(row2)
        xy.append([x])
        xy.append([y])
    
    logger.info(f"uv :")
    for row in uv:
        logger.info(f"    {row}")
    logger.info(f"xy : {xy}")

    uv = numpy.asarray(uv)
    xy = numpy.asarray(xy)
    
    logger.info(f"uv : \n{uv}")
    logger.info(f"xy : \n{xy}")

    uv_inv = numpy.linalg.pinv(uv)

    logger.info(f"uv inv : \n{uv_inv}")

    sol = numpy.matmul(uv_inv, xy)

    logger.info(f"sol : \n{sol}")

    save_calculation_data(sol.tolist())

    uv_to_xy = get_calculation_func()
    
    for anchor_data in transform_data['anchors']:
        x,y = anchor_data['x'],anchor_data['y']
        u,v = anchor_data['u'],anchor_data['v']
        cx,cy = uv_to_xy(u,v)
        logger.info(f"{u:>5.1f}, {v:>5.1f}")
        logger.info(f"    recorded   : {x:5.1f}, {y:>5.1f}")
        logger.info(f"    calculated : {cx:5.1f}, {cy:>5.1f}")



if __name__ == "__main__":
    calibration_calculation()