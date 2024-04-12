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
    
    for (i,j) in itertools.product([-1,1],[-1,1]):
        key = f"{i},{j}"
        val = transform_data[key]
        logger.info(f"key : {key:>6}, val {val}")
        u = val['circle'][0]
        v = val['circle'][1]
        row1 = [u,v,1,0,0,0]
        row2 = [0,0,0,u,v,1]
        uv.append(row1)
        uv.append(row2)
        xy.append([val['x']])
        xy.append([val['y']])
    
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

    def uv_to_xy(u,v):
        mat = numpy.asarray([
            [u,v,1,0,0,0],
            [0,0,0,u,v,1],
        ])
        
        xy = numpy.matmul(mat,sol)

        return (xy[0,0],xy[1,0])
    
    for (i,j) in itertools.product([-1,1],[-1,1]):
        key = f"{i},{j}"
        val = transform_data[key]
        x,y = val['x'],val['y']
        u,v = val['circle'][0],val['circle'][1]
        cx,cy = uv_to_xy(u,v)
        logger.info(f"{u:>5.1f}, {v:>5.1f}")
        logger.info(f"    recorded   : {x:5.1f}, {y:>5.1f}")
        logger.info(f"    calculated : {cx:5.1f}, {cy:>5.1f}")



if __name__ == "__main__":
    calibration_calculation()