from typing import List
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QColor, QColor, QPixmap
from PyQt5.QtCore import QPointF, Qt
from Domain.Shapes.Wireframe import WireFrame
from Domain.Shapes.Point import Point
from Domain.Shapes.Line import Line
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Enums import ObjectsTypes
from Domain.Utils.Constants import Constants
from Handlers.WorldHandler import WorldHandler

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
    
    def __draw_grid(self, painter: QPainter):
        # Draw grid lines
        grid_size = 10
        pen = painter.pen()
        
        origin = WorldHandler.getHandler().objectHandler.originWorldViewport()
        
        for x in range(0, Constants.VIEWPORT_LENGTH, grid_size):
            if x == origin.axisX:
                pen.setColor(QColor(255, 0, 0))
                pen.setWidth(2)
                painter.setPen(pen)
            else:
                pen.setColor(QColor(200, 200, 200))
                pen.setWidth(1)
                painter.setPen(pen)
            
            painter.drawLine(x, 0, x, Constants.VIEWPORT_WIDTH)
            
        for y in range(0, Constants.VIEWPORT_WIDTH, grid_size):
            if y == origin.axisY:
                pen.setColor(QColor(255, 0, 0))
                pen.setWidth(2)
                painter.setPen(pen)
            else:
                pen.setColor(QColor(200, 200, 200))
                pen.setWidth(1)
                painter.setPen(pen)
            
            painter.drawLine(0, y, Constants.VIEWPORT_LENGTH, y)
    
    def paint(self):
        self.__clear_pixmap()
        
        painter = QPainter(self.pixmap())
        
        self.__draw_grid(painter)
        
        p = painter.pen()
        p.setColor(self.__pen_color)
        p.setWidth(2)
        painter.setPen(p)

        for obj in self.__obj_list:
            if obj.type == ObjectsTypes.POINT:
                self.__paintPoint(painter, obj)
            elif obj.type == ObjectsTypes.LINE:
                self.__paintLine(painter, obj)
            elif obj.type == ObjectsTypes.WIREFRAME:
                self.__paintWireframe(painter, obj)
    
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
        #print(f'Pintando ponto em {point.position.axisX}, {point.position.axisY}')

        canvas.drawPoint(QPointF(point.position.axisX, point.position.axisY))

    @classmethod
    def __paintLine(cls, canvas: QPainter, line: Line):
        #print(f'Pintando linha de {line.pointOne.position.axisX}, {line.pointOne.position.axisY} para {line.pointTwo.position.axisX}, {line.pointTwo.position.axisY}')
        canvas.drawLine(line.pointOne.position.axisX, line.pointOne.position.axisY,
                        line.pointTwo.position.axisX, line.pointTwo.position.axisY)
        
    @classmethod
    def __paintWireframe(cls, canvas: QPainter, wireFrame: WireFrame):
        #print(f'Pintando wireframe')
        positions = wireFrame.getPositions()
        
        if (len(positions) == 0):
            return

        if (len(positions) == 1):
            canvas.drawPoint(positions[0].axisX, positions[0].axisY)
            return

        if (len(positions) == 2):
            canvas.drawLine(positions[0].axisX, positions[0].axisY, positions[1].axisX, positions[1].axisY)

        # Adiciona o primeiro ponto como último ponto para fechar automaticamente o polígono
        positions.append(positions[0])

        for index, curPosition in enumerate(positions):
            # Não executa nada caso seja o último
            if index != len(positions) - 1:
                nextPosition = positions[index+1]

                canvas.drawLine(curPosition.axisX, curPosition.axisY, 
                                nextPosition.axisX, nextPosition.axisY)