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
    
    def clip(self, line: Line, win_bottom_left: Position3D, win_top_left: Position3D, win_top_right: Position3D, win_bottom_right: Position3D) -> Line | None:
        p1 = line.getPositions()[0]
        p2 = line.getPositions()[1]
        
        print(f'Clipping line {line.name} with positions: {p1}, {p2}')
        
        code1 = self.__compute_code(p1, win_bottom_left, win_top_left, win_top_right)
        code2 = self.__compute_code(p2, win_bottom_left, win_top_left, win_top_right)
        
        while True:
            # Fully inside
            if code1 == 0 and code2 == 0:
                return Line(Point.fromPosition(p1), Point.fromPosition(p2), line.name)
            
            # Fully outside
            elif code1 & code2 != 0:
                return None
            
            # Partially
            else:
                # Select the point outside
                code_out = code1 if code1 != 0 else code2
                
                x = 0
                y = 0
                
                # Compute intersection point
                # Top | Bottom | Right | Left
                if code_out & 8:
                    x = p1.axisX + (p2.axisX - p1.axisX) * (win_top_left.axisY - p1.axisY) / (p2.axisY - p1.axisY)
                    y = win_top_left.axisY
                
                elif code_out & 4:
                    x = p1.axisX + (p2.axisX - p1.axisX) * (win_bottom_left.axisY - p1.axisY) / (p2.axisY - p1.axisY)
                    y = win_bottom_left.axisY
                
                elif code_out & 2:
                    y = p1.axisY + (p2.axisY - p1.axisY) * (win_top_right.axisX - p1.axisX) / (p2.axisX - p1.axisX)
                    x = win_top_right.axisX
                
                elif code_out & 1:
                    y = p1.axisY + (p2.axisY - p1.axisY) * (win_top_left.axisX - p1.axisX) / (p2.axisX - p1.axisX)
                    x = win_top_left.axisX
                
                # Update the point
                if code_out == code1:
                    p1 = Position3D(x, y, 0)
                    code1 = self.__compute_code(p1, win_bottom_left, win_top_left, win_top_right)
                    
                    
class Clipper:
    def __init__(self) -> None:
        self.__lineClippingStrategy: LineClippingStrategy = CohenSutherlandStrategy()
        self.__polygongClip = None
    
    def __clipPoint(self, point: Position3D, win_bottom_left: Position3D, win_top_left: Position3D, win_top_right: Position3D, win_bottom_right: Position3D) -> Position3D | None:
        if point.axisX >= win_bottom_left.axisX and point.axisX <= win_top_right.axisX and point.axisY >= win_bottom_left.axisY and point.axisY <= win_top_right.axisY:
            return point
        
        return None
    
    def setLineClippingStrategy(self, strategy: LineClippingStrategy) -> None:
        self.__lineClippingStrategy = strategy
        
    def clip(self, window_v_up: list[Position3D], objs: list[SGIObject], length: int) -> list[SGIObject]:
        win_bottom_left = window_v_up[0]
        win_top_left = window_v_up[1]
        
        win_top_right = Position3D(win_top_left.axisX + length, win_top_left.axisY, 0)
        win_bottom_right = Position3D(win_bottom_left.axisX + length, win_bottom_left.axisY, 0)
        
        clipped_objs = []
        
        print(f'Clipping window with positions: {win_bottom_left}, {win_top_left}, {win_top_right}, {win_bottom_right}')
        
        for obj in objs:
            temp = None
            
            print(f'Clipping object {obj.name}')
            
            # TODO: Add wireframe clipping when polygon algorithm is implemented
            if obj.type == ObjectsTypes.POINT:
                temp = self.__clipPoint(obj.getPositions()[0], win_bottom_left, win_top_left, win_top_right, win_bottom_right)
            elif obj.type == ObjectsTypes.LINE:
                temp = self.__lineClippingStrategy.clip(obj, win_bottom_left, win_top_left, win_top_right, win_bottom_right)
            elif obj.type == ObjectsTypes.WIREFRAME:
                temp = obj
                
            if temp is not None:
                clipped_objs.append(temp)
        
        return clipped_objs