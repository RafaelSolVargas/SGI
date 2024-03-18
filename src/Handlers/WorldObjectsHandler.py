from Domain.Management.Viewport import ViewPort
from Domain.Management.Window import Window
from Domain.Management.World import World
from Domain.Shapes.Line import Line
from Domain.Shapes.Point import Point
from Domain.Utils.Coordinates import Position3D


class WorldObjectsHandler:
    def __init__(self, viewPort: ViewPort, window: Window, world: World) -> None:
        self.__viewport = viewPort
        self.__window = window
        self.__world = world

    def addLine(self, pointOne: Position3D, pointTwo: Position3D) -> None:
        line = Line(pointOne, pointTwo)

        self.__world.addObject(line)

    def addPoint(self, position: Position3D) -> None:
        print(f'Ponto adicionado {position.axisX}, {position.axisY}, {position.axisZ}')

        point = Point(position.axisX, position.axisY, position.axisZ)

        self.__world.addObject(point)