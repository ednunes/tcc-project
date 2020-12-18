import bpy
import cv2
import numpy
from .character_animation import CharacterAnimation 


class VincentModel(CharacterAnimation):
    def __init__(self, dimensions=(640, 480)):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.bones = bpy.data.objects["RIG-Vincent"].pose.bones

    # Camera internals
    def set_head_rotation(self, shape):
        # 2D image points. If you change the image, you need to change vector
        image_points = numpy.array([shape[30],     # Nose tip - 31
                                    shape[8],      # Chin - 9
                                    shape[36],     # Left eye left corner - 37
                                    shape[45],     # Right eye right corne - 46
                                    shape[48],     # Left Mouth corner - 49
                                    shape[54]      # Right mouth corner - 55
                                ], dtype = numpy.float32)
        camera_matrix = numpy.array(
                                [[self.height, 0.0, self.width/2],
                                [0.0, self.height, self.height/2],
                                [0.0, 0.0, 1.0]], dtype = numpy.float32
                                )
                                
        # 3D model points. 
        model_points = numpy.array([
                                    (0.0, 0.0, 0.0),             # Nose tip
                                    (0.0, -330.0, -65.0),        # Chin
                                    (-225.0, 170.0, -135.0),     # Left eye left corner
                                    (225.0, 170.0, -135.0),      # Right eye right corne
                                    (-150.0, -150.0, -125.0),    # Left Mouth corner
                                    (150.0, -150.0, -125.0)      # Right mouth corner
                                ], dtype = numpy.float32)


        dist_coeffs = numpy.zeros((4,1)) # Assuming no lens distortion

        if hasattr(self, 'rotation_vector'):
            (success, self.rotation_vector, self.translation_vector) = cv2.solvePnP(model_points, 
                image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE, 
                rvec=self.rotation_vector, tvec=self.translation_vector, 
                useExtrinsicGuess=True)
        else:
            (success, self.rotation_vector, self.translation_vector) = cv2.solvePnP(model_points, 
                image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE, 
                useExtrinsicGuess=False)
     
        if not hasattr(self, 'first_angle'):
            self.first_angle = numpy.copy(self.rotation_vector)

        self.bones["head_fk"].rotation_euler[0] = self.smooth_value("h_x", 5, (self.rotation_vector[0] - self.first_angle[0])) / 1   # Up/Down
        self.bones["head_fk"].rotation_euler[2] = self.smooth_value("h_y", 5, -(self.rotation_vector[1] - self.first_angle[1])) / 1.5  # Rotate
        self.bones["head_fk"].rotation_euler[1] = self.smooth_value("h_z", 5, (self.rotation_vector[2] - self.first_angle[2])) / 1.3   # Left/Right
        
        self.bones["head_fk"].keyframe_insert(data_path="rotation_euler", index=-1)
        

    def set_eyebrows_position(self, shape):
        self.bones["brow_ctrl_L"].location[2] = self.smooth_value("b_l", 3, (self.get_range("brow_left", numpy.linalg.norm(shape[19] - shape[27])) -0.5) * 0.04)
        self.bones["brow_ctrl_R"].location[2] = self.smooth_value("b_r", 3, (self.get_range("brow_right", numpy.linalg.norm(shape[24] - shape[27])) -0.5) * 0.04)
        
        self.bones["brow_ctrl_L"].keyframe_insert(data_path="location", index=2)
        self.bones["brow_ctrl_R"].keyframe_insert(data_path="location", index=2)
        

    def set_eyelids_position(self, shape):
        l_open = self.smooth_value("e_l", 2, self.get_range("l_open", -numpy.linalg.norm(shape[48] - shape[44]))  )
        r_open = self.smooth_value("e_r", 2, self.get_range("r_open", -numpy.linalg.norm(shape[41] - shape[39]))  )
        eyes_open = (l_open + r_open) / 2.0 # looks weird if both eyes aren't the same...
        
        self.bones["eyelid_up_ctrl_R"].location[2] = -eyes_open * 0.025 + 0.005
        self.bones["eyelid_low_ctrl_R"].location[2] = eyes_open * 0.025 - 0.005
        self.bones["eyelid_up_ctrl_L"].location[2] = -eyes_open * 0.025 + 0.005
        self.bones["eyelid_low_ctrl_L"].location[2] = eyes_open * 0.025 - 0.005
        
        self.bones["eyelid_up_ctrl_R"].keyframe_insert(data_path="location", index=2)
        self.bones["eyelid_low_ctrl_R"].keyframe_insert(data_path="location", index=2)
        self.bones["eyelid_up_ctrl_L"].keyframe_insert(data_path="location", index=2)
        self.bones["eyelid_low_ctrl_L"].keyframe_insert(data_path="location", index=2)


    def set_animation(self, shape):
        #self.set_head_rotation(shape) 
        self.set_mouth_position(shape) 

        # self.set_eyebrows_position(shape) 

        # self.set_eyelids_position(shape)

    def set_mouth_position(self, shape):
        mouth_height = (-self.get_range("mouth_height", numpy.linalg.norm(shape[62] - shape[66])) * 0.06)
        self.bones["mouth_ctrl"].location[2] = self.smooth_value("m_h", 2, mouth_height)
        mouth_width = ((self.get_range("mouth_width", numpy.linalg.norm(shape[54] - shape[48])) - 0.5) * -0.04)
        self.bones["mouth_ctrl"].location[0] = self.smooth_value("m_w", 2, mouth_width)

        self.bones["mouth_ctrl"].keyframe_insert(data_path="location", index=-1)

    # Keeps a moving average of given length
    def smooth_value(self, name, length, value):
        if not hasattr(self, 'smooth'):
            self.smooth = {}
        if not name in self.smooth:
            self.smooth[name] = numpy.array([value])
        else:
            self.smooth[name] = numpy.insert(arr=self.smooth[name], obj=0, values=value)
            if self.smooth[name].size > length:
                self.smooth[name] = numpy.delete(self.smooth[name], self.smooth[name].size-1, 0)
        sum = 0
        for val in self.smooth[name]:
            sum += val
        return sum / self.smooth[name].size

    # Keeps min and max values, then returns the value in a range 0 - 1
    def get_range(self, name, value):
        if not hasattr(self, 'range'):
            self.range = {}
        if not name in self.range:
            self.range[name] = numpy.array([value, value])
        else:
            self.range[name] = numpy.array([min(value, self.range[name][0]), max(value, self.range[name][1])] )
        val_range = self.range[name][1] - self.range[name][0]
        if val_range != 0:
            return (value - self.range[name][0]) / val_range
        else:
            return 0.0
