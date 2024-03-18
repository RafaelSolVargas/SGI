import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen
from Domain.Shapes.Point import Point
from Domain.Shapes.Line import Line
from Domain.Utils.Enums import ObjectsTypes


class Painter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__obj_list = []
        
    def setObjList(self, obj_list):
        self.__obj_list = obj_list

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set pen color and width
        pen = QPen()
        pen.setColor(QColor(0, 0, 0))
        pen.setWidth(20)
        painter.setPen(pen)

        for obj in self.__obj_list:
            if obj.type == ObjectsTypes.POINT:
                self.__paintPoint(painter, obj)
            elif obj.type == ObjectsTypes.LINE:
                self.__paintLine(painter, obj)
    
        painter.end()
            
    @classmethod
    def __paintPoint(cls, canvas: QPainter, point: Point):
        print(f'Pintando ponto em {point.position.axisX}, {point.position.axisY}')
        canvas.drawPoint(point.position.axisX, point.position.axisY)

    @classmethod
    def __paintLine(cls, canvas: QPainter, line: Line):
        print(f'Pintando linha de {line.pointOne.position.axisX}, {line.pointOne.position.axisY} para {line.pointTwo.position.axisX}, {line.pointTwo.position.axisY}')
        canvas.drawLine(line.pointOne.position.axisX, line.pointOne.position.axisY,
                        line.pointTwo.position.axisX, line.pointTwo.position.axisY)