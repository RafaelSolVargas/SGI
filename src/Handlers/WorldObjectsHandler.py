from copy import copy
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
        self.__tempPolygon = []

    def addLine(self, pointOne: Position3D, pointTwo: Position3D) -> None:
        line = Line(pointOne, pointTwo)

        self.__world.addObject(line)

    def addPoint(self, position: Position3D) -> None:
        print(f'Ponto adicionado {position.axisX}, {position.axisY}, {position.axisZ}')

        point = Point(position.axisX, position.axisY, position.axisZ)

        self.__world.addObject(point)

        
    def addPointPolygon(self, position: Position3D) -> None:
        print(f'Ponto adicionado ao poligono {position.axisX}, {position.axisY}, {position.axisZ}')

        point = Point(position.axisX, position.axisY, position.axisZ)
        
        self.__tempPolygon.append(point)
        
    def commitPolygon(self) -> None:
        print('Confirmando poligono')
        polygon = Polygon('Poligono', self.__tempPolygon)
        self.__world.addObject(polygon)
        self.__tempPolygon = []
    
    def __viewportTransform(self, point: Position3D) -> Position3D:
        xW = point.axisX

        xVP = ((xW - self.__window.Xmin) / (self.__window.dimensions.lenght)) * (self.__viewport.dimensions.lenght)

        print(self.__window.Xmin)
        print(self.__window.dimensions.lenght)
        print(self.__viewport.dimensions.lenght)


        print(self.__window.Ymin)
        print(self.__window.dimensions.width)
        print(self.__viewport.dimensions.width)

        yW = point.axisY

        yVP = (1 - ((yW - self.__window.Ymin) / (self.__window.dimensions.width))) * (self.__viewport.dimensions.width)
       
        pointTransformed = Position3D(round(xVP), round(yVP), 1)

        print(f'Transforming ({point.axisX}, {point.axisY}, {point.axisZ}) into ({pointTransformed.axisX}, {pointTransformed.axisY}, {pointTransformed.axisZ})')

        return pointTransformed

    def getObjectsViewport(self) -> List[SGIObject]:
        objectsToShow: List[SGIObject] = []
        
        for obj in self.__world.objects:
            # Creates a copy to not change the Domain value
            objCopy = copy(obj)

            for position in objCopy.getPositions():
                transformedPosition = self.__viewportTransform(position)

                position.axisX = transformedPosition.axisX
                position.axisY = transformedPosition.axisY
                position.axisZ = transformedPosition.axisZ

            objectsToShow.append(objCopy)

        return objectsToShow