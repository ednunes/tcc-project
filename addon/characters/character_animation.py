import bpy
import numpy as np
from abc import ABC, abstractmethod


class CharacterAnimation(ABC):
    @abstractmethod
    def set_animation(self, shape: np.ndarray):
        pass
