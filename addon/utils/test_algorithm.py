import sys
import os
import cv2

addon_path = os.path.expanduser("/home/eduardonunes/workspace/project_tcc/addon")
if addon_path not in sys.path:
   sys.path.append(addon_path)

from algorithms import OpenCVStrategy

WIDTH = 640
HEIGHT = 480 

# Init camera
video_capture = cv2.VideoCapture(0)
video_capture.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    WIDTH
)
video_capture.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    HEIGHT
)
video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

landmarks_algorithm_params = (
    (WIDTH, HEIGHT),
    "../../models_prediction/lbfmodel.yaml"
)

# Algorithm instance
algorithm = OpenCVStrategy(*landmarks_algorithm_params)

# Main loop
while(video_capture is not None and video_capture.isOpened()):
    checked_frame, frame = video_capture.read()

    shape = algorithm.get_face_landmarks(frame)

    # Show image captured with landmarks draw
    cv2.imshow("Read face from json", frame)

    key_pressed = cv2.waitKey(1)
    if(key_pressed == 27 # Esc key == 27
        or key_pressed == ord('q')):
        if video_capture is not None:
            video_capture.release()
            video_capture = None

            cv2.destroyAllWindows()
