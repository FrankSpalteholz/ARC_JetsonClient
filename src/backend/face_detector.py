import cv2
import numpy as np


class FaceDetector:

    def __init__(self, cascade_path='', roi_offset=50, output_size=(255, 255)):
        self._cascade_path = cascade_path
        self._face_cascade = None
        self._roi_offset = roi_offset
        self._output_size = output_size

        self._crop_array = np.array([0, 0, 0, 0])
        self._input_frame = None
        self._crop_frame = None

        self.init_cascade()

    def init_cascade(self):
        self._face_cascade = cv2.CascadeClassifier(self._cascade_path)

    def detect_face(self):
        gray = cv2.cvtColor(self._input_frame, cv2.COLOR_BGR2GRAY)

        faces = self._face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            self._crop_array[0] = x - self._roi_offset
            self._crop_array[1] = x + w + self._roi_offset
            self._crop_array[2] = y - self._roi_offset
            self._crop_array[3] = y + h + self._roi_offset

            cv2.rectangle(self._input_frame,
                          (self._crop_array[0] - 1, self._crop_array[2] - 1),
                          (self._crop_array[1], self._crop_array[3]),
                          (0, 200, 255), 1)

            self._crop_frame = self._input_frame[self._crop_array[2]:self._crop_array[3],
                               self._crop_array[0]:self._crop_array[1]]

    def scale_face(self):
        if type(self._crop_frame) is np.ndarray:
            crop_frame = cv2.resize(self._crop_frame, (self._output_size[0], self._output_size[1]))
            return crop_frame
        return False

    def get_image(self, frame):
        self._input_frame = frame

    def get_face(self, frame):

        self.get_image(frame)
        self.detect_face()
        crop_frame_out = self.scale_face()
        return self._input_frame, crop_frame_out
