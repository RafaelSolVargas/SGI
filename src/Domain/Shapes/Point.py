from typing import List
from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Enums import ObjectsTypes


class Point(SGIObject):
    def __init__(self, axisX: int, axisY: int, axisZ: int, name: str = "Ponto") -> None:
        dimensions = Dimensions3D(1, 1, 1)
        position = Position3D(axisX, axisY, axisZ)
        
        super().__init__(ObjectsTypes.POINT, name, dimensions, position)
    
    @staticmethod
    def fromPosition(position: Position3D, name: str = "Ponto") -> 'Point':
        return Point(position.axisX, position.axisY, position.axisZ, name)
    
    def getPositions(self) -> List[Position3D]:
        return [self.position]
    