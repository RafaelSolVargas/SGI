from Domain.Utils.Coordinates import Position3D
from abc import ABC, abstractmethod
from Domain.Utils.Enums import Axis
import numpy as np

class Transform(ABC):
    def __init__(self, positions: list[Position3D] = []) -> None:
        self.__positions = positions
    
    def __do_transform(self, position: Position3D) -> np.ndarray:
        return position.homogenous() @ self.matrix()
    
    def __matrix_homogenous_to_position(self, matrix: np.ndarray) -> Position3D:
        return Position3D(matrix[0, 3], matrix[1, 3], matrix[2, 3])
    
    @abstractmethod
    def matrix(self) -> np.ndarray:
        return np.array([   [1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])
        
    def execute(self) -> list[Position3D]:
        l = []
        
        for position in self.__positions:
            pos = self.__matrix_homogenous_to_position(self.__do_transform(position))
            l.append(pos)
        
        return l
    
    def set_positions(self, positions: list[Position3D]) -> None:
        self.__positions = positions

class Translation(Transform):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0, positions: list[Position3D] = []) -> None:
        super().__init__(positions)
        self.__x = x
        self.__y = y
        self.__z = z
        
    def matrix(self) -> np.ndarray:
        return np.array([   [1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [self.__x, self.__y, self.__z, 1]])
        
class Rotation(Transform):
    def __init__(self, angle: float, positions: list[Position3D] = []) -> None:
        super().__init__(positions)
        self.__angle = np.radians(angle)
        
    def matrix(self) -> np.ndarray:
        return np.array([   [np.cos(self.__angle), -np.sin(self.__angle), 0, 0],
                            [np.sin(self.__angle), np.cos(self.__angle), 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])
        
class Scale(Transform):
    def __init__(self, x: float, y: float, z: float, positions: list[Position3D] = []) -> None:
        super().__init__(positions)
        self.__x = x
        self.__y = y
        self.__z = z
        
    def matrix(self) -> np.ndarray:
        return np.array([   [self.__x, 0, 0, 0],
                            [0, self.__y, 0, 0],
                            [0, 0, self.__z, 0],
                            [0, 0, 0, 1]])
    