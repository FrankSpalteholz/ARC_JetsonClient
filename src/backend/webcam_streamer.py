import cv2
import numpy as np


class WebCamStream:

    def __init__(self, cap_source='/dev/video0', cap_size=(800, 600), ):
        self._capture_size = cap_size
        self._capture_source = cap_source

        self._frame = None
        self._video_pipe = cv2.VideoCapture(self._capture_source, cv2.CAP_ANY)

        # setting capture width and height
        self._video_pipe.set(3, cap_size[0])
        self._video_pipe.set(4, cap_size[1])

        # setting brightness
        self._video_pipe.set(10, 40)

        # setting saturation
        self._video_pipe.set(12, 50)

        # setting contrast
        self._video_pipe.set(11, 50)

        # setting auto exposure
        self._video_pipe.set(21, 0)

        # setting gain
        self._video_pipe.set(14, 25)



    def run_capture(self):
        _, frame = self._video_pipe.read()
        self._frame = frame

    def frame_available(self):
        if type(self._frame) is np.ndarray:
            return True
        return False

    def frame(self):
        self.run_capture()
        return self._frame
