from Domain.Shapes.Point import Point
from Domain.Utils.Coordinates import Dimensions3D
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Enums import ObjectsTypes


class Line(SGIObject):
    def __init__(self, pointOne: Point, pointTwo: Point) -> None:
        dimensions = Dimensions3D(1, 1, 1)

        self.__pointOne = pointOne
        self.__pointTwo = pointTwo

        super().__init__(ObjectsTypes.LINE, "Line", dimensions, pointOne.position)

    @property
    def pointOne(self) -> Point:
        return self.__pointOne
    
    @property
    def pointTwo(self) -> Point:
        return self.__pointTwo