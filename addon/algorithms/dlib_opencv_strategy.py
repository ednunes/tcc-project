from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2

from .strategy import LandmarksDetectionStrategy
from typing import List


class DlibOpenCVStrategy(LandmarksDetectionStrategy):
    SHAPE_PREDICTOR = "/home/eduardonunes/workspace/org_tcc/dlib/shape_predictor_68_face_landmarks.dat"
    # construct the argument parser and parse the arguments
    #ap = argparse.ArgumentParser()
    #ap.add_argument("-p", "--shape-predictor", default= SHAPE_PREDICTOR,
    #        help="path to facial landmark predictor")
    #ap.add_argument("-i", "--image", required=True,
    #        help="path to input image")
    #args = vars(ap.parse_args())

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    def __init__(self, frame_dimensions=(640, 480), landmark_model_path=SHAPE_PREDICTOR):
        self.width = frame_dimensions[0]
        self.height = frame_dimensions[1]
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.SHAPE_PREDICTOR)

    def draw_face_landmarks(self, image, shape) -> None:
        for (x, y) in shape:
            cv2.circle(image, (round(x), round(y)), 2, (0, 255, 255), -1)

    def get_face_landmarks(self, frame: List) -> List:
        # load the input image, resize it, and convert it to grayscale
        #image = cv2.imread(frame)
        image = imutils.resize(frame, width=self.width)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale image
        rects = self.detector(gray, 1)

        # loop over the face detections
        shape = None
        for (i, rect) in enumerate(rects):
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = self.predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                # convert dlib's rectangle to a OpenCV-style bounding box
                # [i.e., (x, y, w, h)], then draw the face bounding box
                (x, y, w, h) = face_utils.rect_to_bb(rect)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # show the face number
                cv2.putText(frame, "Face #{}".format(i + 1), (x - 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                self.draw_face_landmarks(frame, shape)


        return shape
