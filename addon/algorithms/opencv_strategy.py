from typing import List
import cv2
import numpy
from addon.algorithms.strategy import LandmarksDetectionStrategy

class OpenCVStrategy(LandmarksDetectionStrategy):
    def __init__(self, frame_dimensions=(640, 480), landmark_model_path="/home/eduardonunes/workspace/org_tcc/GSOC2017/data/lbfmodel.yaml"):
        self.width = frame_dimensions[0]
        self.height = frame_dimensions[1]

        face_detect_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.cas = cv2.CascadeClassifier(face_detect_path)

        self.face_markers = cv2.face.createFacemarkLBF()
        self.face_markers.loadModel(landmark_model_path)

    def get_the_closest_face(self, faces):
        closest_face = numpy.zeros(shape=(1,4))
        for face in faces:
            if face[2] > closest_face[0][2]:
                closest_face[0] = face
        return closest_face 
             
    def draw_detected_faces(self, frame, faces):
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)

    def draw_face_landmarks_numbers(self, frame, shape):
        label = 0
        for (x, y) in shape:
            font = cv2.FONT_HERSHEY_SIMPLEX 
            fontScale = 0.3
            color = (0, 255, 255) 
            thickness = 1
            cv2.putText(frame, str(label), (round(x),round(y)), font, fontScale, color, thickness, cv2.LINE_AA, False)
            label += 1

    def draw_face_landmarks(self, frame, shape):
        for (x, y) in shape:
            cv2.circle(frame, (round(x), round(y)), 2, (0, 255, 255), -1)

    def get_face_landmarks(self, frame: List) -> List:
        faces = self.cas.detectMultiScale(frame, 
            scaleFactor=1.05,  
            minNeighbors=3, 
            flags=cv2.CASCADE_SCALE_IMAGE, 
            minSize=(int(self.width/5), int(self.width/5)))

        shape = None 

        if type(faces) is numpy.ndarray and faces.size > 0: 
            closest_face = self.get_the_closest_face(faces)

            _, landmarks = self.face_markers.fit(frame, faces=closest_face)

            shape = landmarks[0][0]

            self.draw_face_landmarks(frame, shape)
        
        self.draw_detected_faces(frame, faces)
        
        return shape
