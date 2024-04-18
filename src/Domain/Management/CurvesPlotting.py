from enum import Enum
from Domain.Utils.Coordinates import Position3D
from Domain.Shapes.Curve import Curve
from abc import ABC, abstractmethod
from typing import List
import numpy as np

class CurvesPlotterStrategies(Enum):
    HERMITE = 0
    BEZIER = 1

class CurvesPlottingStrategy(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def generatePoints(self, curve: Curve, precision: float) -> List[Position3D]:
        pass

class HermiteCurvePlotting(CurvesPlottingStrategy):
    def __init__(self) -> None:
        super().__init__()

    def generatePoints(self, curve: Curve, precision: float) -> List[Position3D]:
        if precision < 0:
            precision = 0.01
        elif precision > 1:
            precision = 1

        objPositions = curve.getPositions()
        p1 = objPositions[0]
        p4 = objPositions[1]
        r1 = objPositions[2]
        r4 = objPositions[3]

        positionsToPlot: List[Position3D] = []
        t = 0
        while t <= 1:
            componentXOne = p1.axisX * ((2 * t**3) - (3 * t**2) + 1) 
            componentXTwo = p4.axisX * (-(2 * t**3) + (3 * t**2)) 
            componentXThree = r1.axisX * ((t**3) - (2 * t**2) + t) 
            componentXFour = r4.axisX * ((t**3) - (t**2))

            positionX = componentXOne + componentXTwo + componentXThree + componentXFour

            componentYOne = p1.axisX * ((2 * t**3) - (3 * t**2) + 1) 
            componentYTwo = p4.axisX * (-(2 * t**3) + (3 * t**2)) 
            componentYThree = r1.axisX * ((t**3) - (2 * t**2) + t) 
            componentYFour = r4.axisX * ((t**3) - (t**2))

            positionY = componentYOne + componentYTwo + componentYThree + componentYFour

            positionsToPlot.append(Position3D(positionX, positionY, 1))

            t += precision

        return positionsToPlot

class BezierCurvePlotting(CurvesPlottingStrategy):
    def __init__(self) -> None:
        super().__init__()

    def __bezierMatrix(self) -> np.ndarray:
        return np.array([
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]
        ])
    
    def generatePoints(self, curve: Curve, precision: float) -> List[Position3D]:
        if precision < 0:
            precision = 0.01
        elif precision > 1:
            precision = 1
        
        positionsToPlot: List[Position3D] = []

        objPositions = curve.getPositions()
        
        i = 0
        while i + 3 < len(objPositions):
        
            p1 = objPositions[i]
            p2 = objPositions[i + 1]
            p3 = objPositions[i + 2]
            p4 = objPositions[i + 3]
            
            t = 0
            
            mat_x = np.array([p1.axisX, p2.axisX, p3.axisX, p4.axisX])
            mat_y = np.array([p1.axisY, p2.axisY, p3.axisY, p4.axisY])
            
            aux_mat_x = np.matmul(self.__bezierMatrix(), mat_x)
            aux_mat_y = np.matmul(self.__bezierMatrix(), mat_y)
            
            while t <= 1:
                t_mat = np.array([t**3, t**2, t, 1])
                
                positionX = np.matmul(t_mat, aux_mat_x)
                positionY = np.matmul(t_mat, aux_mat_y)

                positionsToPlot.append(Position3D(positionX, positionY, 1))

                t += precision
                
            i += 3

        return positionsToPlot
 
class CurvesPlotter:
    __STRATEGY: CurvesPlottingStrategy = BezierCurvePlotting()

    @classmethod
    def setStrategy(cls, strategy: CurvesPlotterStrategies):
        if strategy == CurvesPlotterStrategies.HERMITE:
            CurvesPlotter.__STRATEGY = HermiteCurvePlotting()
        elif strategy == CurvesPlotterStrategies.BEZIER:
            CurvesPlotter.__STRATEGY = BezierCurvePlotting()

    @staticmethod
    def generatePoints(curve: Curve, precision: float) -> List[Position3D]:
        return CurvesPlotter.__STRATEGY.generatePoints(curve, precision)