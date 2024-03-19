from typing import List
from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Enums import ObjectsTypes
from Domain.Shapes.Point import Point


class Polygon(SGIObject):
    def __init__(self, name: str) -> None:
        super().__init__(ObjectsTypes.POLYGON, name, Dimensions3D(0, 0, 0), Position3D(0, 0, 0))
        self.__points: list[Point] = []
    
    def __init__(self, name: str, dimensions: Dimensions3D, position: Position3D) -> None:
        super().__init__(ObjectsTypes.POLYGON, name, dimensions, position)
        self.__points = []
        
    def __init__(self, name: str, dimensions: Dimensions3D, position: Position3D, positions: list[Point]) -> None:
        super().__init__(ObjectsTypes.POLYGON, name, dimensions, position)
        self.__points = positions
        
    def addPoint(self, point: Point) -> None:
        self.__points.append(point)
        
    @property
    def getPositions(self) -> List[Position3D]:
        positions: List[Position3D] = []
        
        for point in self.__points:
            positions.append(point.position) 

        return positions