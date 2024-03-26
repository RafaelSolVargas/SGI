from typing import List
from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Enums import ObjectsTypes
from Domain.Shapes.Point import Point


class WireFrame(SGIObject):
    def __init__(self, name: str, positions: List[Point]) -> None:
        super().__init__(ObjectsTypes.WIREFRAME, name, Dimensions3D(0, 0, 0), positions[0])
        self.__points = positions
        
    def addPoint(self, point: Point) -> None:
        self.__points.append(point)
        
    def getPositions(self) -> List[Position3D]:
        return [x.position for x in self.__points]
    
    def setPositions(self, positions: List[Position3D]) -> None:
        self.__points = []
        
        # For some reason, enumerate is not working here (changes order of or duplicates points in the wireframe)
        for i in range(len(positions)):
            self.__points.append(Point(positions[i].axisX, positions[i].axisY, positions[i].axisZ, f'{self.name}_{i}'))
        
    # TODO: correct this method
    @property
    def centralPoint(self) -> Position3D:
        x = sum([point.position.axisX for point in self.__points]) // len(self.__points)
        y = sum([point.position.axisY for point in self.__points]) // len(self.__points)
        z = sum([point.position.axisZ for point in self.__points]) // len(self.__points)
        
        return Position3D(x, y, z)