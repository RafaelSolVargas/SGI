import sys
from typing import List
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QColor, QPixmap
from PyQt5.QtCore import QPointF, Qt
from Domain.Shapes.Polygon import Polygon
from Domain.Shapes.Point import Point
from Domain.Shapes.Line import Line
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Enums import ObjectsTypes
from Domain.Utils.Constants import Constants

class Canvas(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__obj_list: List[SGIObject] = []
        
        pixmap = QPixmap(Constants.VIEWPORT_LENGTH, Constants.VIEWPORT_WIDTH)
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)
        self.setGeometry(Constants.SIDEBAR_SIZE, 0, Constants.VIEWPORT_LENGTH, Constants.VIEWPORT_WIDTH)
        
        self.__pen_color = QColor(0, 0, 0)
        
    def draw(self, obj_list: List[SGIObject]):
        self.__obj_list = obj_list
        self.paint()
        
    def paint(self):
        self.__clear_pixmap()
        
        painter = QPainter(self.pixmap())
        p = painter.pen()
        p.setColor(self.__pen_color)
        p.setWidth(2)
        painter.setPen(p)

        for obj in self.__obj_list:
            if obj.type == ObjectsTypes.POINT:
                self.__paintPoint(painter, obj)
            elif obj.type == ObjectsTypes.LINE:
                self.__paintLine(painter, obj)
            elif obj.type == ObjectsTypes.POLYGON:
                self.__paintPolygon(painter, obj)
    
        painter.end()
        self.update()
        
    def __clear_pixmap(self):
        # Create a new blank pixmap with the same size as the original
        new_pixmap = QPixmap(self.pixmap().size())
        # Fill the new pixmap with transparent color
        new_pixmap.fill(QColor(0, 0, 0, 0))  # Transparent color

        # Assign the new pixmap to the original one
        self.pixmap().swap(new_pixmap)
            
    @classmethod
    def __paintPoint(cls, canvas: QPainter, point: Point):
        print(f'Pintando ponto em {point.position.axisX}, {point.position.axisY}')
        canvas.drawPoint(QPointF(point.position.axisX, point.position.axisY))

    @classmethod
    def __paintLine(cls, canvas: QPainter, line: Line):
        print(f'Pintando linha de {line.pointOne.position.axisX}, {line.pointOne.position.axisY} para {line.pointTwo.position.axisX}, {line.pointTwo.position.axisY}')
        canvas.drawLine(line.pointOne.position.axisX, line.pointOne.position.axisY,
                        line.pointTwo.position.axisX, line.pointTwo.position.axisY)
        
    @classmethod
    def __paintPolygon(cls, canvas: QPainter, polygon: Polygon):
        print(f'Pintando poligono')
        positions = polygon.getPositions()
        qpositions = [QPointF(position.axisX, position.axisY) for position in positions]
        
        canvas.drawPolygon(qpositions)