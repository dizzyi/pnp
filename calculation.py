import json
import numpy

CALCULATION_DATA_FILE = "./calibration-calculation.json"

def get_calculation_func():
    sol = numpy.asarray(load_calculation_data())

    def uv_to_xy(u,v):
        mat = numpy.asarray([
            [u,v,1,0,0,0],
            [0,0,0,u,v,1],
        ])
        
        xy = numpy.matmul(mat,sol)

        return (xy[0,0],xy[1,0])

    return uv_to_xy

def load_calculation_data():
    with open(CALCULATION_DATA_FILE,"r") as f:
        return json.load(f)
    
def save_calculation_data(data):
    with open(CALCULATION_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)