from enum import Enum
from Domain.Utils.Coordinates import Position3D
from Domain.Shapes.Curve import Curve
from abc import ABC, abstractmethod
from typing import List

class CurvesPlotterStrategies(Enum):
    HERMITE = 0

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
        for t in range(0, 1, precision):
            componentOne = p1.axisX * ((2 * t**3) - (3 * t**2) + 1) 
            componentTwo = p4.axisX * (-(2 * t**3) + (3 * t**2)) 
            componentThree = r1.axisX * ((t**3) - (2 * t**2) + t) 
            componentFour = r4.axisX * ((t**3) - (t**2))

            positionX = componentOne + componentTwo + componentThree + componentFour

            positionsToPlot.append(Position3D(positionX, 1, 1))

        return positionsToPlot
    
class CurvesPlotter:
    __STRATEGY: CurvesPlottingStrategy = HermiteCurvePlotting()

    @classmethod
    def setStrategy(cls, strategy: CurvesPlotterStrategies):
        if strategy == CurvesPlotterStrategies.HERMITE:
            CurvesPlotter.__STRATEGY = HermiteCurvePlotting()

    @staticmethod
    def generatePoints(curve: Curve, precision: float) -> List[Position3D]:
        return CurvesPlotter.__STRATEGY.generatePoints(curve, precision)