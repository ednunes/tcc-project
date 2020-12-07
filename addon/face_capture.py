import cv2
import codecs
import numpy as np
import time

from addon.model_animation import ModelAnimation
from addon.algorithms.detection_strategy import LandmarksDetectionStrategy


class FaceCapture():
    WINDOW_NAME = "Captured frame"
    shapes = []
    frames = []

    model_animation = None

    _video_capture = None

    settings = {
        "width": 640,
        "height": 480,
        "input_video": "",
        "output_video": "",
        "device_option": "0",
        "landmarks_export": "",
        "want_to_record": False,
        "capture_mode": "camera",
        "want_to_export_data": False,
        "landmarks_algorithm_option": "opencv",
        "landmarks_model_path": "../models_prediction/lbfmodel.yaml"
    }

    def __init__(self,
                 landmarks_detection_strategy: LandmarksDetectionStrategy,
                 settings={}) -> None:
        self._landmarks_detection_strategy = landmarks_detection_strategy
        self.model_animation = ModelAnimation()
        self._recording = False

        if not settings:
            self.settings = settings

    def init_camera(self) -> None:
        device_option = self.settings["device_option"]
        if device_option.isdigit():
            device_option = int(device_option)

        self._video_capture = cv2.VideoCapture(device_option)
        self._video_capture.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            self.settings["width"]
        )
        self._video_capture.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            self.settings["height"]
        )
        self._video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def close_camera(self) -> None:
        if self._video_capture is not None:
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
    def landmarks_detection_strategy(self,
                                     land_strategy: LandmarksDetectionStrategy
                                     ) -> None:
        self._landmarks_detection_strategy = land_strategy

    def get_face_landmarks(self, frame: np.ndarray) -> np.ndarray:
        return self._landmarks_detection_strategy.get_face_landmarks(frame)

    def save_video(self,
                   output_video: str,
                   video_dimensions: tuple,
                   frames: np.ndarray) -> None:

        video_output = cv2.VideoWriter(
            output_video,
            cv2.VideoWriter_fourcc(*"MJPG"),
            60,
            video_dimensions
        )

        for frame in frames:
            resized_frame = cv2.resize(frame, video_dimensions)
            video_output.write(resized_frame)

        video_output.release()
        video_output = None

        print("VIDEO SAVED SUCCESSFULLY!")

    def save_data(self) -> None:
        if self.settings["want_to_export_data"]:
            self._landmarks_detection_strategy.save_landmarks(
                self.settings["landmarks_export"],
                self.shapes
            )
            self.shapes.clear()

        if self.settings["want_to_record"]:
            self.save_video(
                self.settings["output_video"],
                (self.settings["width"], self.settings["height"]),
                self.frames
            )
            self.frames.clear()

    def draw_mode(self, frame: np.ndarray, recording: bool) -> None:
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

    def main_video(self, frame: np.ndarray) -> None:
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        shape = self.get_face_landmarks(frame)

        if shape is not None:
            self.model_animation.set_animation(shape)
            if self.settings["want_to_export_data"]:
                self.shapes.append(shape)

        cv2.waitKey(1)
        self.draw_mode(frame, self.recording)
        cv2.imshow(self.WINDOW_NAME, frame)

    def main_camera(self, frame: np.ndarray) -> None:
        if self.settings["want_to_record"]:
            self.frames.append(frame)

        frame_clone = frame.copy()
        shape = self.get_face_landmarks(frame_clone)

        if shape is not None:
            self.model_animation.set_animation(shape)
            if self.settings["want_to_export_data"] and self.recording:
                self.shapes.append(shape)

        cv2.waitKey(1)
        self.draw_mode(frame_clone, self.recording)
        cv2.imshow(self.WINDOW_NAME, frame_clone)

    def main(self) -> bool:
        checked_frame = True
        if self._video_capture is not None:
            checked_frame, frame = self._video_capture.read()

            if checked_frame:
                if self.settings["capture_mode"] == "camera":
                    time_start = time.time()
                    self.main_camera(frame)
                    print("TIME CAMERA: %.4f sec" % (time.time() - time_start))
                else:
                    time_start = time.time()
                    self.main_video(frame)
                    print("TIME VIDEO: %.4f sec" % (time.time() - time_start))
            else:
                checked_frame = False

        return checked_frame
