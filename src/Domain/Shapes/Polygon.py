from typing import List
from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Enums import ObjectsTypes
from Domain.Shapes.Point import Point


class Polygon(SGIObject):
    def __init__(self, name: str, positions: List[Point]) -> None:
        super().__init__(ObjectsTypes.POLYGON, name, Dimensions3D(0, 0, 0), positions[0])
        self.__points = positions
        
    def addPoint(self, point: Point) -> None:
        self.__points.append(point)
        
    def getPositions(self) -> List[Position3D]:
        return [x.position for x in self.__points]