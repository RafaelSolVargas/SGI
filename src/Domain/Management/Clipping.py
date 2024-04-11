from abc import ABC, abstractmethod
from Domain.Shapes.Point import Point
from Domain.Shapes.Line import Line
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Coordinates import Position3D
from Domain.Utils.Enums import ObjectsTypes

class LineClippingStrategy(ABC):
    def __init__(self) -> None:
        pass
            
    @abstractmethod
    def clip(self, line: Line, win_bottom_left: Position3D, win_top_left: Position3D, win_top_right: Position3D, win_bottom_right: Position3D) -> Line | None:
        pass
    
    
class CohenSutherlandStrategy(LineClippingStrategy):
    def __init__(self) -> None:
        super().__init__()
    
    def __compute_code(self, p: Position3D, win_bottom_left: Position3D, win_top_left: Position3D, win_top_right: Position3D) -> int:
        code = 0
        
        if p.axisY > win_top_left.axisY:
            code |= 8
        elif p.axisY < win_bottom_left.axisY:
            code |= 4
        
        if p.axisX > win_top_right.axisX:
            code |= 2
        elif p.axisX < win_top_left.axisX:
            code |= 1
        
        return code
    
    def __intersection(self, p1: Position3D, p2: Position3D, win_bottom_left: Position3D, win_top_left: Position3D, win_top_right: Position3D, code: int) -> Position3D:
        x0, y0 = p1.axisX, p1.axisY
        x1, y1 = p2.axisX, p2.axisY
        
        m = (y1 - y0) / (x1 - x0)
        
        if code & 8:
            y = win_top_left.axisY
            x = x0 + (1 / m) * (y - y0)
            
            if code & 2 and (x < win_bottom_left.axisX or x > win_top_right.axisX):
                x = win_top_right.axisX
                y = y0 + m * (x - x0)
            elif code & 1 and (x < win_bottom_left.axisX or x > win_top_right.axisX):
                x = win_bottom_left.axisX
                y = y0 + m * (x - x0)
                
        elif code & 4:
            y = win_bottom_left.axisY
            x = x0 + (1 / m) * (y - y0)
            
            if code & 2 and (x < win_bottom_left.axisX or x > win_top_right.axisX):
                x = win_top_right.axisX
                y = y0 + m * (x - x0)
            elif code & 1 and (x < win_bottom_left.axisX or x > win_top_right.axisX):
                x = win_bottom_left.axisX
                y = y0 + m * (x - x0)
        
        elif code & 2:
            x = win_top_right.axisX
            y = y0 + m * (x - x0)

        elif code & 1:
            x = win_bottom_left.axisX
            y = y0 + m * (x - x0)
            
        return Position3D(x, y, 1)
    
    def clip(self, line: Line, win_bottom_left: Position3D, win_top_left: Position3D, win_top_right: Position3D, win_bottom_right: Position3D) -> Line | None:
        p1 = line.getPositions()[0]
        p2 = line.getPositions()[1]
        
        print(f'Clipping line {line.name} with positions: {p1}, {p2}')
        
        code1 = self.__compute_code(p1, win_bottom_left, win_top_left, win_top_right)
        code2 = self.__compute_code(p2, win_bottom_left, win_top_left, win_top_right)
        
        print(f'Code 1: {int(code1):04b} | Code 2: {int(code2):04b}')
        # Fully inside
        if code1 == 0 and code2 == 0:
            return Line(Point.fromPosition(p1), Point.fromPosition(p2), line.name)
        
        # Fully outside
        elif code1 & code2 != 0:
            return None
        
        # Partially
        else:
            if code1 != 0:
                #print("Clipping point 1")
                temp = self.__intersection(p1, p2, win_bottom_left, win_top_left, win_top_right, code1)
                x0, y0 = temp.axisX, temp.axisY
                    
            if code2 != 0:
                #print("Clipping point 2")
                temp = self.__intersection(p2, p1, win_bottom_left, win_top_left, win_top_right, code2)
                x1, y1 = temp.axisX, temp.axisY
                
            #print(f'Old points: ({p1.axisX}, {p1.axisY}) | ({p2.axisX}, {p2.axisY})')
            #print(f'New points: ({x0}, {y0}) | ({x1}, {y1})')
            
            # If the line is still outside the window
            if self.__compute_code(Position3D(x0, y0, 1), win_bottom_left, win_top_left, win_top_right) != 0 and self.__compute_code(Position3D(x1, y1, 1), win_bottom_left, win_top_left, win_top_right) != 0:
                return None
                
            return Line(Point(x0, y0, 0), Point(x1, y1, 0), line.name)
                        
class Clipper:
    def __init__(self) -> None:
        self.__lineClippingStrategy: LineClippingStrategy = CohenSutherlandStrategy()
        self.__polygongClip = None
    
    def __clipPoint(self, point: Point, win_bottom_left: Position3D, win_top_left: Position3D, win_top_right: Position3D, win_bottom_right: Position3D) -> Point | None:
        if point.position.axisX >= win_bottom_left.axisX and point.position.axisX <= win_top_right.axisX and point.position.axisY >= win_bottom_left.axisY and point.position.axisY <= win_top_right.axisY:
            return point
        
        return None
    
    def setLineClippingStrategy(self, strategy: LineClippingStrategy) -> None:
        self.__lineClippingStrategy = strategy
        
    def clip(self, window_v_up: list[Position3D], objs: list[SGIObject], length: int) -> list[SGIObject]:
        win_bottom_left = window_v_up[0]
        win_top_left = window_v_up[1]
        win_top_right = window_v_up[2]
        win_bottom_right = window_v_up[3]
        
        clipped_objs = []
        
        #print(f'Clipping window with positions: {win_bottom_left}, {win_top_left}, {win_top_right}, {win_bottom_right}')
        
        for obj in objs:
            temp = None
            
            #print(f'Clipping object {obj.name}')
            
            # TODO: Add wireframe clipping when polygon algorithm is implemented
            if obj.type == ObjectsTypes.POINT:
                temp = self.__clipPoint(obj, win_bottom_left, win_top_left, win_top_right, win_bottom_right)
            elif obj.type == ObjectsTypes.LINE or (obj.type == ObjectsTypes.WIREFRAME and len(obj.getPositions()) == 2):
                temp = self.__lineClippingStrategy.clip(obj, win_bottom_left, win_top_left, win_top_right, win_bottom_right)
            elif obj.type == ObjectsTypes.WIREFRAME:
                temp = obj
                
            if temp is not None:
                clipped_objs.append(temp)
        
        return clipped_objs