from Domain.Utils.Coordinates import Position3D
from Domain.Utils.Enums import RotationTypes
from abc import ABC, abstractmethod
import numpy as np

class Transform(ABC):
    def __init__(self, positions: list[Position3D] = []) -> None:
        self.__positions = positions

    @abstractmethod
    def getName(self) -> str:
        pass

    def __do_transform(self, position: Position3D) -> np.ndarray:
        
        pos = position.homogenous()
        
        print(f"Position: {pos}, shape: {pos.shape}")
        
        matrix = self.matrix()
        
        print(f"Matrix: {matrix}, shape: {matrix.shape}")
        #print(f"Element types: {matrix.dtype}")
        
        result = pos @ matrix
        
        print(f"Result: {result}, shape: {result.shape}")
        
        
        return result
    
    def __matrix_homogenous_to_position(self, positions: np.ndarray) -> Position3D:
        return Position3D(np.round(positions[0]), np.round(positions[1]), np.round(positions[2]))
    
    @abstractmethod
    def matrix(self) -> np.ndarray:
        return Transform.identity()
        
    @staticmethod
    def identity() -> np.ndarray:
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
        
    def getName(self) -> str:
        return f"Translation({self.__x}, {self.__y}, {self.__z})"

    def matrix(self) -> np.ndarray:
        return np.array([   [1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [self.__x, self.__y, self.__z, 1]])
        
class Rotation(Transform):
    def __init__(self, angle: float, type: RotationTypes, positions: list[Position3D] = []) -> None:
        super().__init__(positions)
        self.__type = type
        self.__angle = np.radians(angle)
        
    def getName(self) -> str:
        return f"Rotation {self.__type}({self.__angle})"

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
        
    def getName(self) -> str:
        return f"Scale({self.__x}, {self.__y}, {self.__z})"

    def matrix(self) -> np.ndarray:
        return np.array([   [self.__x, 0, 0, 0],
                            [0, self.__y, 0, 0],
                            [0, 0, self.__z, 0],
                            [0, 0, 0, 1]])

class GenericTransform(Transform):
    def __init__(self, matrix: np.ndarray = Transform.identity(), positions: list[Position3D] = [], name: str = "GenericTransform") -> None:
        super().__init__(positions)
        self.__matrix = matrix
        self.__name = name
    
    def getName(self) -> str:
        if self.__name == "Scale":
            return f"{self.__name}({self.__matrix[0][0]}, {self.__matrix[1][1]}, {self.__matrix[2][2]})"
        elif self.__name == "Translation":
            return f"{self.__name}({self.__matrix[3][0]}, {self.__matrix[3][1]}, {self.__matrix[3][2]})"
        elif self.__name == "Rotation":
            return f"{self.__name}({np.degrees(np.arccos(self.__matrix[0][0]))}°)"
        else:
            return f"{self.__name}({self.__matrix})"

    def matrix(self) -> np.ndarray:
        return self.__matrix
    
    def add_transforms(self, transforms: list[Transform]) -> None:
        for transform in transforms:
            self.__matrix = self.__matrix @ transform.matrix()