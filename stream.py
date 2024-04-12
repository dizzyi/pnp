from realsense import RealSense
import cv2


def main():
    rs = RealSense()

    while True:
        src = rs.get_frame()
        cv2.imshow("realsense stream", src)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()