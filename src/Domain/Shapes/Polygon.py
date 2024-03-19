from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Enums import ObjectsTypes
from Domain.Shapes.Point import Point


class Polygon(SGIObject):
    def __init__(self, name: str) -> None:
        super().__init__(ObjectsTypes.POLYGON, name, Dimensions3D(0, 0, 0), Position3D(0, 0, 0))
        self.__positions: list[Point] = []
    
    def __init__(self, name: str, dimensions: Dimensions3D, position: Position3D) -> None:
        super().__init__(ObjectsTypes.POLYGON, name, dimensions, position)
        self.__positions = []
        
    def __init__(self, name: str, dimensions: Dimensions3D, position: Position3D, positions: list[Point]) -> None:
        super().__init__(ObjectsTypes.POLYGON, name, dimensions, position)
        self.__positions = positions
        
    def addPosition(self, position: Position3D) -> None:
        self.__positions.append(position)
        
    @property
    def positions(self) -> list[Position3D]:
        return self.__positions