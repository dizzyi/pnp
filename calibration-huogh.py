import numpy
from inovopy.robot import InovoRobot
from inovopy.geometry.transform import Transform
from inovopy.logger import Logger
from realsense import RealSense
from hough import *
import cv2

RED = 255,0,0

def calibration_hough():
    logger = Logger.default("Calibration - Hough")
    rs = RealSense()
    bot = InovoRobot.default_iva("192.168.1.114")

    HOME = bot.get_current_transform().set_euler(180,0,0)
    logger.info(HOME)
    
    hough_data = load_hough_data()

    param1 = hough_data["param1"]
    param2 = hough_data["param2"]

    while True:
        src = rs.get_frame()[0]

        circles, hough_in = hough_circle(src, param1, param2)

        cv2.imshow("hough_in", hough_in)

        marked = src.copy()
        try:
            circles = numpy.uint16(numpy.round(circles))

            for circle in circles[0]:
                center = circle[0],circle[1]
                radius = circle[2]
                cv2.circle(marked, center, 1, (0,100,100), 2)
                cv2.circle(marked, center, radius, (255,0,255), 3)       
                cv2.putText(marked,f"{center} : {radius}",center, 1, 1, RED, 1, cv2.LINE_AA)

        except:
            pass
        cv2.putText(marked,f"param1 : {param1:5.1f}, param2: {param2:5.1f}",(20,20), 1, 2, RED, 1, cv2.LINE_AA)
        cv2.imshow("img",marked)
        key = cv2.waitKey(100)

        if key == 119:
            param1 *= 1.01
        elif key == 115:
            param1 /= 1.01

        elif key == 97:
            param2 *= 1.01
        elif key == 100:
            param2 /= 1.01

        elif key == 27:
            break

        elif key == -1:
            continue

        else:
            logger.warn(f"unknonw key {key}")

        if hough_data["param1"] != param1 or hough_data["param2"] != param2:
            hough_data["param1"] = param1
            hough_data["param2"] = param2
            save_hough_data(hough_data)

    cv2.destroyAllWindows()


def crop():
    rs = RealSense()

    x = 0
    y = 0
    w = 100
    h = 100

    # H  72 J  74 K  75 L  76
    # h 104 j 106 k 107 l 108

    # r 114 R 82

    while True:
        src = rs.get_frame()

        marked = src.copy()

        cv2.rectangle(marked,(x,y),(x+w,y+h),RED,2)

        cv2.imshow("rs stream", marked)
        
        key = cv2.waitKey(1)

        if key == 104 and x > 0:
            x -= 1
        elif key == 108 and x < 640:
            x += 1
        elif key == 106 and y < 480:
            y += 1
        elif key == 107 and y > 0:
            y -= 1
        

        elif key == 119 and h > 10:
            h -= 1
        elif key == 115 and h < 500:
            h += 1
        
        elif key == 97 and w > 10:
            w -= 1
        elif key == 100 and w < 500:
            w += 1

        elif key == 114:
            break
    
        elif key == -1:
            continue

        else:
            print(key)

    cv2.destroyAllWindows()
    
    cv2.imwrite("./target.jpg",src[y:y+h,x:x+w])


if __name__ == "__main__":
    calibration_hough()