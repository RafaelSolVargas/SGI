from typing import List
from PyQt5.QtGui import QPainter
from Domain.Shapes.Line import Line
from Domain.Shapes.Point import Point
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Enums import ObjectsTypes


class CanvasPainter:
    @classmethod
    def paintObjects(cls, canvas: QPainter, objects: List[SGIObject]):
        for object in objects:
            if (object.type == ObjectsTypes.POINT):
                cls.__paintPoint(canvas, objects)
            elif (object.type == ObjectsTypes.LINE):
                cls.__paintLine(canvas, objects)


    @classmethod
    def __paintPoint(cls, canvas: QPainter, point: Point):
        canvas.drawPoint(point.position.axisX, point.position.axisY)

    @classmethod
    def __paintLine(cls, canvas: QPainter, line: Line):
        canvas.drawLine(line.pointOne.position.axisX, line.pointOne.position.axisY,
                        line.pointTwo.position.axisX, line.pointTwo.position.axisY)