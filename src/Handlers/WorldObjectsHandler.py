from copy import copy, deepcopy
from typing import List
from Domain.Management.Viewport import ViewPort
from Domain.Management.Window import Window
from Domain.Management.World import World
from Domain.Shapes.Point import Point
from Domain.Shapes.Line import Line
from Domain.Shapes.Polygon import Polygon
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Coordinates import Position3D


class WorldObjectsHandler:
    def __init__(self, viewPort: ViewPort, window: Window, world: World) -> None:
        self.__viewport = viewPort
        self.__window = window
        self.__world = world
        self.__tempPolygonPoints: List[Point] = []

    def addLine(self, pointOne: Position3D, pointTwo: Position3D) -> None:
        line = Line(pointOne, pointTwo)

        self.__world.addObject(line)

    def addPoint(self, position: Position3D) -> None:
        print(f'Ponto adicionado {position.axisX}, {position.axisY}, {position.axisZ}')

        point = Point(position.axisX, position.axisY, position.axisZ)

        self.__world.addObject(point)

        
    def addTempPointPolygon(self, position: Position3D) -> None:
        print(f'Ponto adicionado ao poligono {position.axisX}, {position.axisY}, {position.axisZ}')

        point = Point(position.axisX, position.axisY, position.axisZ)
        
        self.__tempPolygonPoints.append(point)
        
    def commitPolygonCreation(self) -> None:
        if len(self.__tempPolygonPoints) == 0:
            return

        polygon = Polygon('Poligono', copy(self.__tempPolygonPoints))

        self.__world.addObject(polygon)
        
        self.__tempPolygonPoints.clear()
    
    def __transformPositionToViewPort(self, position: Position3D) -> Position3D:
        xW = position.axisX

        xVP = ((xW - self.__window.Xmin) / (self.__window.dimensions.length)) * (self.__viewport.dimensions.length)

        yW = position.axisY

        yVP = (1 - ((yW - self.__window.Ymin) / (self.__window.dimensions.width))) * (self.__viewport.dimensions.width)
       
        pointTransformed = Position3D(round(xVP), round(yVP), 1)

        print(f'Transforming ({position.axisX}, {position.axisY}, {position.axisZ}) into ({pointTransformed.axisX}, {pointTransformed.axisY}, {pointTransformed.axisZ})')

        return pointTransformed

    def getObjectsViewport(self) -> List[SGIObject]:
        objectsToShow: List[SGIObject] = []

        print(f'Starting the transformantions of {len(self.__world.objects)} objects')

        for obj in self.__world.objects:
            # Creates a copy to not change the Domain value
            objCopy = deepcopy(obj)

            for position in objCopy.getPositions():
                position.axisX = position.axisX - self.__window.Xmin
                position.axisY = position.axisY - self.__window.Ymin
                
                transformedPosition = self.__transformPositionToViewPort(position)

                position.axisX = transformedPosition.axisX
                position.axisY = transformedPosition.axisY
                position.axisZ = transformedPosition.axisZ

            objectsToShow.append(objCopy)

        return objectsToShow