from typing import List
from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Enums import ObjectsTypes


class Point(SGIObject):
    def __init__(self, axisX: int, axisY: int, axisZ: int) -> None:
        dimensions = Dimensions3D(1, 1, 1)
        position = Position3D(axisX, axisY, axisZ)
        
        super().__init__(ObjectsTypes.POINT, "Point", dimensions, position)

    def getPositions(self) -> List[Position3D]:
        return [self.position]
    