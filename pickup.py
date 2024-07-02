from inovopy.robot import InovoRobot
from inovopy.logger import Logger
from inovopy.geometry.transform import Transform
from realsense import RealSense

from hough import *
from transform import *
from calculation import *

def pickup():
    logger = Logger.default("Pick Up")
    rs = RealSense()
    bot = InovoRobot.default_iva("192.168.8.103")

    bot.gipper_activate()
    bot.sleep(5)

    hough_data = load_hough_data()
    transform_data = load_transform_data()

    uv_to_xy = get_calculation_func()

    HOME : Transform = transform_data['HOME']
    CENTER = HOME.clone().set_z(transform_data["height"])
    param1 = hough_data['param1']
    param2 = hough_data['param2']

    while True:
        logger.info("ready for pick up?")
        if input() != 'Y':
            continue

        src = rs.get_frame()[0]
        circles,_ = hough_circle(src,param1,param2)

        try:
            circles = numpy.uint16(numpy.round(circles))
            circle = circles[0][0]
        except Exception as e:
            logger.warn(f"{e}")
            continue
    
        logger.info(f"{circle}")

        u,v = circle[0], circle[1]

        x,y = uv_to_xy(u,v)

        anchor = CENTER.clone().then_x(x).then_y(y)
        up = anchor.clone().then_z(200)

        bot.linear(HOME)
        bot.gripper_set('open')
        bot.linear(up)
        bot.linear(anchor)
        bot.gripper_set('close')
        bot.linear(anchor)
        bot.linear(up)
        bot.linear(HOME)
        bot.linear(CENTER)
        bot.gripper_set('open')
        bot.linear(HOME)

if __name__ == "__main__":
    pickup()