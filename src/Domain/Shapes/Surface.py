from Domain.Shapes.SGIObject import SGIObject
from typing import List
from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Utils.Enums import ObjectsTypes
from Domain.Shapes.Point import Point
import numpy as np

class Surface(SGIObject):
    def __init__(self, name: str, positions: list[Point], filled: bool = False) -> None:
        super().__init__(ObjectsTypes.SURFACE, name, Dimensions3D(0, 0, 0), positions[0])
        self.__points = positions
        self.__filled = filled
        
        self.__X_matrix = self.__geometryBezierMatrix('x')
        self.__Y_matrix = self.__geometryBezierMatrix('y')
        self.__Z_matrix = self.__geometryBezierMatrix('z')

    @property
    def filled(self) -> bool:
        return self.__filled

    @filled.setter
    def filled(self, value: bool) -> None:
        self.__filled = value

    def __geometryBezierMatrix(self, axis: str) -> np.ndarray:
        matrix = []
        if axis == 'x':
            for i in range(4):
                row = []
                for j in range(4):
                    ij = i * 4 + j
                    row.append(self.__points[ij].position.axisX)
                matrix.append(row)
        elif axis == 'y':
            for i in range(4):
                row = []
                for j in range(4):
                    ij = i * 4 + j
                    row.append(self.__points[ij].position.axisY)
                matrix.append(row)
        elif axis == 'z':
            for i in range(4):
                row = []
                for j in range(4):
                    ij = i * 4 + j
                    row.append(self.__points[ij].position.axisZ)
                matrix.append(row)
                
        return np.array(matrix)
    
    def getPositions(self) -> List[Position3D]:
        return [x.position for x in self.__points]
    
    def generatePositions(self, step: float) -> List[Position3D]:
        positions = []
        s = 0
        t = 0
        
        bezierMatrix = np.array([
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]
        ])
        
        while s <= 1:
            S_matrix = np.array([1, s, s**2, s**3])
            while t <= 1:
                T_matrix = np.array([1, t, t**2, t**3])
                x = S_matrix @ bezierMatrix @ self.__X_matrix @ bezierMatrix.T @ T_matrix.T
                y = S_matrix @ bezierMatrix @ self.__Y_matrix @ bezierMatrix.T @ T_matrix.T
                z = S_matrix @ bezierMatrix @ self.__Z_matrix @ bezierMatrix.T @ T_matrix.T
                
                positions.append(Position3D(x, y, z))
                
                t += step
            t = 0
            s += step

        return positions
    
    def setPositions(self, positions: List[Position3D]) -> None:
        self.__points = []
        
        for i, pos in enumerate(positions):
            self.__points.append(Point(pos.axisX, pos.axisY, pos.axisZ, f'{self.name}_{i}'))
            
        self.__X_matrix = self.__geometryBezierMatrix('x')
        self.__Y_matrix = self.__geometryBezierMatrix('y')
        self.__Z_matrix = self.__geometryBezierMatrix('z')
            
    @property
    def centralPoint(self) -> Position3D:
        x = sum([point.position.axisX for point in self.__points]) // len(self.__points)
        y = sum([point.position.axisY for point in self.__points]) // len(self.__points)
        z = sum([point.position.axisZ for point in self.__points]) // len(self.__points)
        
        return Position3D(x, y, z)