import bpy
import cv2
import numpy
from .character_animation import CharacterAnimation 


class RainModel(CharacterAnimation):
    def __init__(self, dimensions=(640, 480)):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.bones = bpy.data.objects["RIG-rain"].pose.bones

    def set_animation(self, shape):
        self.set_mouth_position(shape) 

    def set_mouth_position(self, shape):
        distance = (shape[62] - shape[66])[1]

        if abs(distance) > 12:
            self.bones["MSTR-Jaw"].rotation_euler = (
                0.29698485136032104, -5.720967449773795e-11, -9.295835212697057e-10
            )
        else:
            self.bones["MSTR-Jaw"].rotation_euler = (0,0,0)

        # self.bones["MSTR-Jaw"].keyframe_insert(data_path="rotation_euler", index=-1)
