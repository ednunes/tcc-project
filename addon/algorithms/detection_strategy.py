from abc import ABC, abstractmethod
from typing import List
import numpy as np
import json, codecs

class LandmarksDetectionStrategy(ABC):
    @abstractmethod
    def draw_face_landmarks(self, frame: List, shape: List) -> List:
        pass

    @abstractmethod
    def get_face_landmarks(self, frame: List) -> List:
        pass

    def save_landmarks(self,
                         landmarks_file: str, shapes: np.ndarray) -> bool:
        has_error = False

        shapes_json = {
            "shapes": [shape.tolist() for shape in shapes]
        }

        print("SAVING JSON...")

        try:
            json.dump(
                shapes_json,
                codecs.open(
                    landmarks_file,
                    "w",
                    encoding="utf-8"
                ),
                separators=(",", ":"),
                sort_keys=True,
                indent=4
            )
            print("JSON SAVED SUCCESSFULLY!")
        except Exception as e:
            print("ERROR WHEN SAVING JSON:", e)
            has_error = True

        return has_error
