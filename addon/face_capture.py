import bpy
import cv2
import json
import codecs
import numpy as np

from addon.model_animation import ModelAnimation
from addon.algorithms.strategy import LandmarksDetectionStrategy

from abc import ABC, abstractmethod
from bpy.app.handlers import persistent


class FaceCapture():
    WINDOW_NAME = "Captured frame"
    shapes = []
    frames = []

    model_animation = None 

    # TODO alterar _cap para nome mais significativo
    _video_capture = None

    settings = {
        'width': 640,
        'height': 480,
        'capture_mode': 'camera',
        'device_option': '0',
        'want_to_export_json': False,
        'want_to_record': False,
        'output_video': '',
        'input_video': '',
        'landmarks_json_export': '',
        'landmarks_algorithm_option': 'opencv',
        'landmarks_model_path': "../models_prediction/lbfmodel.yaml"
    }

    # @persistent
    # def get_model_animation(self):
    #     self.model_animation = ModelAnimation()

    def __init__(self,
            landmarks_detection_strategy: LandmarksDetectionStrategy,
            settings={}) -> None:
        self._landmarks_detection_strategy = landmarks_detection_strategy
        self._recording = False 
        if len(settings) != 0:
            self.settings = settings
        # bpy.app.handlers.load_post.append(self.get_model_animation)
        self.model_animation = ModelAnimation()

    def init_camera(self) -> None:
        device_option = self.settings['device_option']

        if device_option.isdigit():
            device_option = int(device_option)

        self._video_capture = cv2.VideoCapture(device_option)
        self._video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.settings['width'])
        self._video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.settings['height'])
        self._video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def close_camera(self) -> None:
        if self._video_capture != None:
            self._video_capture.release()
            self._video_capture = None

            cv2.destroyAllWindows()

    @property
    def recording(self) -> bool:
        return self._recording

    @recording.setter
    def recording(self, recording: bool) -> None:
        self._recording = recording 

    @property
    def landmarks_detection_strategy(self) -> LandmarksDetectionStrategy:
        return self._landmarks_detection_strategy

    @landmarks_detection_strategy.setter
    def landmarks_detection_strategy(
            self, landmarks_detection_strategy: LandmarksDetectionStrategy) -> None:
        self._landmarks_detection_strategy = landmarks_detection_strategy

    def get_face_landmarks(self, frame: np.ndarray) -> np.ndarray:
        return self._landmarks_detection_strategy.get_face_landmarks(frame)

    def save_json_format( self, landmarks_json_file: str, shapes: np.ndarray) -> bool:
        has_error = False
        new_shapes = []
        for shape in shapes:
            try:
                new_shapes.append(shape.tolist())
            except:
                continue

        shapes_json = {'shapes': new_shapes}

        print('SAVING JSON...')
        try:
            json.dump(
                shapes_json,
                codecs.open(
                    self.settings['landmarks_json_export'],
                    'w',
                    encoding='utf-8'
                ),
                separators=(',', ':'),
                sort_keys=True,
                indent=4
            )

            print('JSON SAVED SUCCESSFULLY!')
            self.shapes.clear()

        except Exception as e:
            print('ERROR WHEN SAVING JSON:', e)
            has_error = True 

        return has_error

    def save_video(self, output_video: str, video_dimensions: tuple) -> None:
            video_output = cv2.VideoWriter(
                output_video,
                cv2.VideoWriter_fourcc(*'MJPG'),
                60,
                video_dimensions 
            )

            for frame in self.frames:
                resized_frame = cv2.resize(frame, video_dimensions)
                video_output.write(resized_frame)

            video_output.release()
            video_output = None
            self.frames.clear()

            print('VIDEO SAVED SUCCESSFULLY!')

    def save_data(self) -> None:
        if self.settings['want_to_export_json']:
            self.save_json_format(
                self.settings['landmarks_json_export'],
                self.shapes
            )
        if self.settings['want_to_record']:
            self.save_video(
                self.settings['output_video'],
                (self.settings['width'], self.settings['height'])
            )

    def show_mode(self, frame, recording) -> None:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        color = (255, 255, 0)
        capture_state = "NORMAL"

        if recording:
            color = (0, 0, 255)
            capture_state = "RECORDING"

        cv2.putText(frame, capture_state, (10, 30), font,
                    font_scale, color, thickness, cv2.LINE_AA, False)

    def main(self):
        no_errors = True
        if not self._video_capture is None:
            _, frame = self._video_capture.read()
            if not frame is None:
                if self.settings['want_to_record']:
                    self.frames.append(frame)

                if self.settings['capture_mode'] == 'video':
                    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                
                frame_clone = frame.copy()
                shape = self.get_face_landmarks(frame_clone)

                if not shape is None:
                    self.model_animation.set_animation(shape)
                    if (self.settings['want_to_export_json'] and 
                        (self.recording or self.settings['capture_mode'] == 'video')):
                        self.shapes.append(shape)

                key_pressed = cv2.waitKey(1)

                self.show_mode(frame_clone, self.recording)

                cv2.imshow(self.WINDOW_NAME, frame_clone)
            else:
                no_errors = False

        return no_errors

