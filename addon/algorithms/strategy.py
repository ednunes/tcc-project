from abc import ABC, abstractmethod
from typing import List

class LandmarksDetectionStrategy(ABC):
    @abstractmethod
    def draw_face_landmarks(self, frame: List, shape: List) -> List:
        pass

    @abstractmethod
    def get_face_landmarks(self, frame: List) -> List:
        pass
