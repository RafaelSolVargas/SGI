from typing import List
from Domain.Shapes.Point import Point
from Domain.Utils.Coordinates import Dimensions3D
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Enums import ObjectsTypes
from Domain.Utils.Coordinates import Position3D


class Line(SGIObject):
    def __init__(self, pointOne: Point, pointTwo: Point, name: str = "Linha") -> None:
        dimensions = Dimensions3D(1, 1, 1)

        self.__pointOne = pointOne
        self.__pointTwo = pointTwo

        super().__init__(ObjectsTypes.LINE, name, dimensions, pointOne.position)

    def getPositions(self) -> List[Position3D]:
        return [self.pointOne.position, self.pointTwo.position]

    def setPositions(self, positions: List[Position3D]) -> None:
        self.__pointOne.position = positions[0]
        self.__pointTwo.position = positions[1]

    @property
    def pointOne(self) -> Point:
        return self.__pointOne

    @property
    def pointTwo(self) -> Point:
        return self.__pointTwo
    
    @property
    def centralPoint(self) -> Position3D:
        # Find the central point between the two points
        return Position3D(
            (self.__pointOne.position.axisX + self.__pointTwo.position.axisX) // 2,
            (self.__pointOne.position.axisY + self.__pointTwo.position.axisY) // 2,
            (self.__pointOne.position.axisZ + self.__pointTwo.position.axisZ) // 2
        )
        
        