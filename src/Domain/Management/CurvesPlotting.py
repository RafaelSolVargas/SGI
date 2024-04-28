from enum import Enum
from Domain.Utils.Coordinates import Position3D
from Domain.Shapes.Curve import Curve
from Domain.Utils.Enums import CurvePlottingMethods
from abc import ABC, abstractmethod
from typing import List
import numpy as np

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
 
class BSplineCurvePlotting(CurvesPlottingStrategy):
    def __init__(self) -> None:
        super().__init__() 
    
    def __BSplineMatrix(self):
        return np.array([
                [-1 / 6, 1 / 2, -1 / 2, 1 / 6],
                [1 / 2, -1, 1 / 2, 0],
                [-1 / 2, 0, 1 / 2, 0],
                [1 / 6, 2 / 3, 1 / 6, 0],
            ])
    
    def __computeParams(self, positions: List[Position3D], t: float) -> tuple[float, float]:
        def calcDiffInit(delta: float, a: float, b: float, c: float, d: float) -> float:
            delta_2 = delta**2
            delta_3 = delta**3
            return [
                d,
                a * delta_3 + b * delta_2 + c * delta,
                6 * a * delta_3 + 2 * b * delta_2,
                6 * a * delta_3,
            ]
        
        GBS_x = []
        GBS_y = []
        
        MBS = self.__BSplineMatrix()
        
        for pos in positions:
            GBS_x.append(pos.axisX)
            GBS_y.append(pos.axisY)
            
        GBS_x = np.array([GBS_x]).T
        c_x = MBS.dot(GBS_x).T[0]
        print(c_x)
        diff_init_x = calcDiffInit(t, *c_x)
        
        GBS_y = np.array([GBS_y]).T
        c_y = MBS.dot(GBS_y).T[0]
        diff_init_y = calcDiffInit(t, *c_y)
        
        return diff_init_x, diff_init_y
    
    def generatePoints(self, curve: Curve, precision: float) -> List[Position3D]:
        positionsToPlot: List[Position3D] = []
        
        min_points = 4
        t = 0
        
        length = len(curve.getPositions())
        
        for i in range(length):
            upper_bound = i + min_points
            
            if upper_bound > length:
                break
            
            tmp = curve.getPositions()[i:upper_bound]
            
            delta_x, delta_y = self.__computeParams(tmp, precision)
            
            x = delta_x[0]
            y = delta_y[0]
            
            positionsToPlot.append(Position3D(x, y, 1))
            
            while t <= 1:
                x += delta_x[1]
                delta_x[1] += delta_x[2]
                delta_x[2] += delta_x[3]

                y += delta_y[1]
                delta_y[1] += delta_y[2]
                delta_y[2] += delta_y[3]
                
                positionsToPlot.append(Position3D(x, y, 1))
                
                t += precision
                
        return positionsToPlot
        
    
class CurvesPlotter:
    @classmethod
    def buildStrategy(cls, method: CurvePlottingMethods) -> CurvesPlottingStrategy:
        if method == CurvePlottingMethods.BEZIER:
            return BezierCurvePlotting()
        elif method == CurvePlottingMethods.BSPLINE:
            return BSplineCurvePlotting()

    @staticmethod
    def generatePoints(curve: Curve, precision: float) -> List[Position3D]:
        return CurvesPlotter.buildStrategy(curve.strategy).generatePoints(curve, precision)