# 192.168.1.11 (blade)
# 192.168.1.26 (raspi)

# flipped version
# -vf -hf -t 0 -o -

# raspivid -n -w 800 -h 600 -b 5000000 -fps 25 -t 0 -o - | gst-launch-1.0 -v fdsrc !  h264parse ! tee name=splitter ! queue ! rtph264pay config-interval=10 pt=96 ! udpsink host=192.168.178.69 port=9000 splitter. ! queue ! filesink location="videofile.h264"
# gst-launch-1.0 -v udpsrc port=9000 caps='application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264' ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false

# ip hurrican/office 192.168.178.69
# ip raspi/wlan/office 192.168.178.88

# test

import cv2
from backend.gst_streamer import GSTVideo
from backend.webcam_streamer import WebCamStream
from backend.face_detector import FaceDetector

import cv2
import numpy as np
import sys

person = "paps"
dl_src_path = "dl_src/faces/train"
cascade_path = "dl_src/fd_models/haarcascade_frontalface_default.xml"

still_size = 250
still_cap_counter = 0

# 0 = webcam, 1 = gstreamer from pi
input_stream = 0

pi_gst_port = 9000

if __name__ == '__main__':

    capture_size = [1280, 720]
    roi_padding = 50

    gst_cap = GSTVideo(port=pi_gst_port)
    webcam_cap = WebCamStream(cap_source=0, cap_size=capture_size)
    face_detector = FaceDetector(cascade_path=cascade_path,
                                 roi_offset=roi_padding,
                                 output_size=(still_size, still_size))

    cap_frame = None
    frame = None
    crop_frame = None

    while True:

        if input_stream == 0:
            cap_frame = webcam_cap.frame()
        elif input_stream == 1:
            cap_frame = gst_cap.frame()

        if type(cap_frame) is np.ndarray:
            frame, crop_frame = face_detector.get_face(cap_frame)
            cv2.imshow('Video', frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key == 32:
            if type(crop_frame) is np.ndarray:
                still_cap_counter += 1
                cv2.imwrite(dl_src_path + "/" + person + "/" + str(still_cap_counter) + ".jpg", crop_frame)


