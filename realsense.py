import pyrealsense2 as rs
import numpy

class RealSense():
    def  __init__(self) -> None:
        pipeline = rs.pipeline()
        config = rs.config()

        pipeline_wrapper = rs.pipeline_wrapper(pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()

        device_product_line = str(device.get_info(rs.camera_info.product_line))
        if not any([s.get_info(rs.camera_info.name) == 'RGB Camera' for s in device.sensors]):
            exit(0)

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        cfg = pipeline.start(config)
        device = cfg.get_device()
        self.pipeline = pipeline

        for i in range(50):
            self.get_frame()

    def get_frame(self):
        frame = self.pipeline.wait_for_frames()
        color_frame = numpy.asarray(frame.get_color_frame().get_data())
        depth_frame = numpy.asarray(frame.get_depth_frame().get_data())
        return (color_frame, depth_frame)