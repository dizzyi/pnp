import os
import json
from inovopy.robot import InovoRobot
from inovopy.geometry.transform import Transform
import cv2
import numpy
from inovopy.logger import Logger
from realsense import RealSense
from hough import *
from transform import *

def calibration_transfrom():
    logger = Logger.default("Calibration - Transform")
    rs = RealSense()
    bot = InovoRobot.default_iva("192.168.8.103")

    transform_data = load_transform_data()
    
    if 'HOME' in transform_data:
        HOME = transform_data["HOME"]
    else:
        HOME = bot.get_current_transform().set_euler(180,0,180)
        transform_data["HOME"] = HOME
        save_transform_data(transform_data)
    bot.linear(HOME)

    bot.gipper_activate()
    bot.sleep(5)

    calibration_height(logger, bot, transform_data)
    calibration_dst(logger,bot,transform_data)
    calibration_grid(logger, bot, transform_data, rs)

       
def calibration_height(logger: Logger, bot: InovoRobot, transform_data: dict) -> float:
    if 'height' in transform_data:
        logger.info("reclibrate height? (Y/N)")
        if not "Y" in input(":"):
            return
    logger.info("starting height calibration")

    command_control(logger,bot)
        
    transform_data["height"] = bot.get_current_transform().vec_mm[2]
    save_transform_data(transform_data)

    bot.gripper_set("close")

    bot.linear_relative(Transform.from_z(100))
    bot.linear(transform_data["HOME"])
    return 

def calibration_grid(logger:Logger, bot: InovoRobot, transform_data: dict, rs: RealSense):
    logger.info("reclibrate grid? (Y/N)")
    if not "Y" in input(":"):
        return
    
    logger.info("starting calibrate grid . . .")
    
    hough_data = load_hough_data()

    HOME : Transform = transform_data["HOME"]
    CENTER = HOME.clone().set_z(transform_data["height"])

    bot.linear(CENTER)
    bot.gripper_set("open")

    while True:
        logger.info("ready for grid calibration? (Y/N)")
        if "Y" in input(":"):
            break
    
    bot.gripper_set("close")

    bot.linear(HOME)

    transform_data['anchors'] = []
    save_transform_data(transform_data)

    for i in [-1,1]:
        for j in [-1,1]:
            x = i * 150
            y = j * 100 + 55
            anchor = CENTER.clone().then_x(x).then_y(y)
            anchor_up = anchor.clone().then_z(100) 
            bot.linear(anchor_up)
            bot.linear(anchor)

            bot.gripper_set("open")
            bot.linear(anchor_up)
            bot.linear(HOME)

            bot.sleep(1)

            circle = get_coord(logger, rs, hough_data)

            anchor_data = {
                'x': x,
                'y': y,
                'u': circle[0],
                'v': circle[1],
                'r': circle[2],
            }
            transform_data['anchors'].append(anchor_data)
            save_transform_data(transform_data)

            bot.linear(anchor_up)
            bot.linear(anchor)

            bot.gripper_set("close")
            bot.linear(anchor_up)
            bot.linear(HOME)

    bot.linear(CENTER.clone().then_z(100))
    bot.linear(CENTER)
    bot.gripper_set("open")

    bot.linear(CENTER.clone().then_z(100))
    bot.linear(HOME)

def get_coord(logger: Logger, rs:RealSense, hough_data: dict):
    while True:
        src = rs.get_frame()[0]

        circles, hough_in = hough_circle(src,hough_data["param1"], hough_data["param2"])

        marked = src.copy()

        try:
            circles = numpy.uint16(numpy.round(circles))

            for circle in circles[0]:
                logger.debug(f"{circle}")


            for i, circle in enumerate(circles[0]):
                center = (circle[0],circle[1])
                radius = circle[2]
                cv2.circle(marked, center, 1, (0,100,100), 2)
                cv2.circle(marked, center, radius, (255,0,0), 2)
                cv2.putText(marked, f"{i}", center, 1, 1, (255,0,0), 1, cv2.LINE_AA)
        except Exception as e:
            logger.debug(f"{circles}")
            logger.warn(f"{e}")
        cv2.imshow("img", marked)
        cv2.waitKey(10)

        logger.info("enter id")
        _in = input(":")
        try:
            _in = float(_in)
            circle : numpy.ndarray = circles[0][i]
            logger.info(f"{circle}")
            return circle.tolist()
        except:
            pass

def calibration_dst(logger: Logger, bot: InovoRobot, transform_data: dict) -> float:
    logger.info("reclibrate dst? (Y/N)")
    if not "Y" in input(":"):
        return

    logger.info("starting calibrate dst . . .")

    bot.linear(transform_data['HOME'])

    command_control(logger,bot)

    DST = bot.get_current_transform()

    if 'height' in transform_data:
        DST.set_z(transform_data['height'])

    save_transform_data()
if __name__ == "__main__":
    calibration_transfrom()