import sys
import os
import cv2
import numpy as np

addon_path = os.path.expanduser("/home/eduardonunes/workspace/project_tcc/addon")
if addon_path not in sys.path:
   sys.path.append(addon_path)

from algorithms import DlibOpenCVStrategy, OpenCVStrategy

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
# algorithm = DlibOpenCVStrategy(*landmarks_algorithm_params)
algorithm = OpenCVStrategy(*landmarks_algorithm_params)

def normalize_landmark(landmarks: np.ndarray) -> np.ndarray:
    center = np.mean(landmarks, axis=0)
    landmarks_norm = landmarks - center
    return landmarks_norm + 200

def draw_landmarks(frame: np.ndarray, shape: np.ndarray) -> None:
    for (x, y) in shape:
        cv2.circle(frame, (round(x), round(y)), 2, (0, 255, 255), -1)

# Main loop
la = np.array([0,0])
ll = np.array([0,0])

def smooth_shapes(shape: np.ndarray) -> np.ndarray:
    global ll, la
    s = (shape + ll + la) / 3
    s = s.astype(int)
    ll = la 
    la = shape

    return s

while(video_capture is not None and video_capture.isOpened()):
    checked_frame, frame = video_capture.read()

    shape = algorithm.get_face_landmarks(frame)

    # Show image captured with landmarks draw
    cv2.imshow("Read face from json", frame)

    result = np.zeros((500, 500, 3), np.uint8)
    smooth = np.zeros((500, 500, 3), np.uint8)
    if shape is not None:
        s = smooth_shapes(shape)
        draw_landmarks(smooth, s)
        cv2.imshow("Smooth", smooth)

        new_shape = normalize_landmark(shape)
        draw_landmarks(result, new_shape)
        cv2.imshow("Result", result)


    key_pressed = cv2.waitKey(1)
    if(key_pressed == 27 # Esc key == 27
        or key_pressed == ord('q')):
        if video_capture is not None:
            video_capture.release()
            video_capture = None

            cv2.destroyAllWindows()
