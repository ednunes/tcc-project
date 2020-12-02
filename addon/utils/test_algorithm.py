import sys
import os
import cv2

addon_path = os.path.expanduser("/home/eduardonunes/workspace/project_tcc/addon")
if addon_path not in sys.path:
   sys.path.append(addon_path)

from algorithms import DlibOpenCVStrategy

# Init camera
video_capture = cv2.VideoCapture(0)
video_capture.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    640
)
video_capture.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    480
)
video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Algorithm instance
algorithm = DlibOpenCVStrategy()

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
