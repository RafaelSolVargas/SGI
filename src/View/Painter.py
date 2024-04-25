from typing import List
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QColor, QColor, QPixmap, QPolygonF
from PyQt5.QtCore import QPointF, Qt
from Domain.Shapes.Wireframe import WireFrame
from Domain.Shapes.Curve import Curve
from Domain.Shapes.Point import Point
from Domain.Shapes.Line import Line
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Enums import ObjectsTypes
from Domain.Utils.Constants import Constants
from Handlers.WorldHandler import WorldHandler
from Domain.Utils.Coordinates import Position3D

class Canvas(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__obj_list: List[SGIObject] = []
        
        pixmap = QPixmap(Constants.VIEWPORT_LENGTH + Constants.VIEWPORT_SLACK, Constants.VIEWPORT_WIDTH + Constants.VIEWPORT_SLACK)
        pixmap.fill(Qt.white)
        
        self.setPixmap(pixmap)
        self.setGeometry(Constants.SIDEBAR_SIZE, 0, Constants.VIEWPORT_LENGTH + Constants.VIEWPORT_SLACK, Constants.VIEWPORT_WIDTH + Constants.VIEWPORT_SLACK)
        
    def draw(self, obj_list: List[SGIObject]):
        self.__obj_list = obj_list
        
        self.paint()
    
    def __draw_grid(self, painter: QPainter):
        # Draw grid lines
        grid_size = 10
        pen = painter.pen()
        
        slack = Constants.VIEWPORT_SLACK // 2

        for x in range(slack, Constants.VIEWPORT_LENGTH + slack, grid_size):
            pen.setColor(QColor(200, 200, 200))
            pen.setWidth(1)
            painter.setPen(pen)
            
            painter.drawLine(x, slack, x, Constants.VIEWPORT_WIDTH + slack)

        for y in range(slack, Constants.VIEWPORT_WIDTH + slack, grid_size):
            pen.setColor(QColor(200, 200, 200))
            pen.setWidth(1)
            painter.setPen(pen)

            painter.drawLine(slack, y, Constants.VIEWPORT_LENGTH + slack, y)
        
        # Draw point of the center of the window
        pen.setWidth(2)
        pen.setColor(QColor(0, 125, 125))
        painter.setPen(pen)
        
        windowCenterPoint = WorldHandler.getHandler().objectHandler.windowCenterPPC
        slack = Constants.VIEWPORT_SLACK // 2
        
        windowCenterPoint.axisX += slack 
        windowCenterPoint.axisY += slack 

        painter.drawPoint(windowCenterPoint.axisX, windowCenterPoint.axisY)
        painter.drawLine(windowCenterPoint.axisX - 5, windowCenterPoint.axisY, windowCenterPoint.axisX + 5, windowCenterPoint.axisY)
        painter.drawLine(windowCenterPoint.axisX, windowCenterPoint.axisY - 5, windowCenterPoint.axisX, windowCenterPoint.axisY + 5)

        # Window points
        window = WorldHandler.getHandler().objectHandler.windowPositionsPPC
        pen.setColor(QColor(0, 255, 0))
        painter.setPen(pen)
        pen.setWidth(2)
        
        painter.drawPoint(window[0].axisX, window[0].axisY)
        painter.drawPoint(window[1].axisX, window[1].axisY)
        painter.drawPoint(window[2].axisX, window[2].axisY)
        painter.drawPoint(window[3].axisX, window[3].axisY)
        
        pen.setColor(QColor(255, 0, 0))
        painter.setPen(pen)

        painter.drawLine(slack, Constants.VIEWPORT_WIDTH + slack, Constants.VIEWPORT_LENGTH + slack, Constants.VIEWPORT_WIDTH + slack)
        painter.drawLine(Constants.VIEWPORT_LENGTH + slack, slack, Constants.VIEWPORT_LENGTH + slack, Constants.VIEWPORT_WIDTH + slack)
        painter.drawLine(Constants.VIEWPORT_LENGTH + slack, slack, slack, slack)
        painter.drawLine(slack, slack, slack, Constants.VIEWPORT_WIDTH + slack)


    def paint(self):
        self.__clear_pixmap()
        
        painter = QPainter(self.pixmap())
        
        self.__draw_grid(painter)
        
        p = painter.pen()
        p.setWidth(2)
        
        for obj in self.__obj_list:
            p.setColor(QColor(*obj.color))
            painter.setPen(p)
            
            if obj.type == ObjectsTypes.POINT:
                self.__paintPoint(painter, obj)
            elif obj.type == ObjectsTypes.LINE:
                self.__paintLine(painter, obj)
            elif obj.type == ObjectsTypes.WIREFRAME:
                self.__paintWireframe(painter, obj)
            elif obj.type == ObjectsTypes.CURVE:
                self.__paintCurve(painter, obj)
    
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
    def __drawWireframe(cls, canvas: QPainter, positions: list[Position3D], color: tuple[int, int, int], filled: bool = False):
        if (len(positions) == 0):
            return

        if (len(positions) == 1):
            canvas.drawPoint(positions[0].axisX, positions[0].axisY)
            return

        if (len(positions) == 2):
            canvas.drawLine(positions[0].axisX, positions[0].axisY, positions[1].axisX, positions[1].axisY)

        for n in range(-1, len(positions) - 1):
            # Desenha a linha entre os pontos
            canvas.drawLine(positions[n].axisX, positions[n].axisY, positions[n + 1].axisX, positions[n + 1].axisY)
        
        if filled:
            brush = canvas.brush()
            brush.setColor(QColor(color[0], color[1], color[2], 100))
            brush.setStyle(Qt.SolidPattern)  # Solid pattern
            canvas.setBrush(brush)
            canvas.drawPolygon(QPolygonF([QPointF(x.axisX, x.axisY) for x in positions]))
            
    @classmethod
    def __paintWireframe(cls, canvas: QPainter, wireFrame: WireFrame):
        #print(f'Pintando wireframe')
        positions = wireFrame.getPositions()
        
        if wireFrame.is3D():
            for face in wireFrame.faces:
                face_positions = [positions[x - 1] for x in face]
                cls.__drawWireframe(canvas, face_positions, wireFrame.color, wireFrame.filled)
        else:
            cls.__drawWireframe(canvas, positions, wireFrame.color, wireFrame.filled)
        

    @classmethod
    def __paintCurve(cls, canvas: QPainter, curve: Curve):
        print(f'Pintando Curva')
        positions = curve.getPositions()
        
        if (len(positions) == 0):
            return

        if (len(positions) == 1):
            canvas.drawPoint(positions[0].axisX, positions[0].axisY)
            return

        if (len(positions) == 2):
            canvas.drawLine(positions[0].axisX, positions[0].axisY, positions[1].axisX, positions[1].axisY)

        for n in range(0, len(positions) - 1):
            # Desenha a linha entre os pontos
            canvas.drawLine(positions[n].axisX, positions[n].axisY, positions[n + 1].axisX, positions[n + 1].axisY)