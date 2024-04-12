import json
import os
import cv2
from realsense import RealSense

HOUGH_DATA_FILE = "./calibration-hough.json"

def hough_circle(src, param1:float=250, param2:float=25):    
    gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    equalized = cv2.equalizeHist(blurred)
    #_,thresholded = cv2.threshold(equalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #canny = cv2.Canny(thresholded, 50, 100)
    hough_in = equalized#thresholded#canny

    cv2.imshow("hough_in", hough_in)

    circles = cv2.HoughCircles(hough_in, 
        cv2.HOUGH_GRADIENT, 1, hough_in.shape[0] / 8,
        param1=param1, param2=param2, minRadius=30, maxRadius=80
    )

    return circles, hough_in

def load_hough_data() -> dict:
    if os.path.isfile(HOUGH_DATA_FILE):
        try:
            with open(HOUGH_DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass 
    return {
        "param1" : 200,
        "param2" : 25
    }

def save_hough_data(data: dict):
    with open(HOUGH_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
