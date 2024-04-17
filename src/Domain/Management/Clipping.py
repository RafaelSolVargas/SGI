from abc import ABC, abstractmethod
from Domain.Shapes.Point import Point
from Domain.Shapes.Line import Line
from Domain.Shapes.Wireframe import WireFrame
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Coordinates import Position3D
from Domain.Utils.Enums import ObjectsTypes
from copy import deepcopy

class LineClippingStrategy(ABC):
    def __init__(self) -> None:
        pass
            
    @abstractmethod
    def clip(self, line: Line, win_bottom_left: Position3D, win_top_left: Position3D, win_top_right: Position3D, win_bottom_right: Position3D) -> Line | None:
        pass
    

class LiangBarskyStrategy(LineClippingStrategy):
    def __init__(self) -> None:
        super().__init__()
    
    def clip(self, line: Line, winBottomLeft: Position3D, winTopLeft: Position3D, winTopRight: Position3D, winBottomRight: Position3D) -> Line | None:
        pointOne = line.getPositions()[0]
        pointTwo = line.getPositions()[1]
        
        x0, y0, z0 = pointOne.axisX, pointOne.axisY, pointOne.axisZ 
        x1, y1, z1 = pointTwo.axisX, pointTwo.axisY, pointTwo.axisZ 
        
        tMin, tMax = 0.0, 1.0
        dx = x1 - x0
        dy = y1 - y0

        xmin, xmax = winBottomLeft.axisX, winBottomRight.axisX
        ymin, ymax = winBottomLeft.axisY, winTopLeft.axisY

        p = [-dx, dx, -dy, dy]
        q = [x0 - (xmin), (xmax) - x0, y0 - (ymin), (ymax) - y0]

        for i in range(4):
            if p[i] == 0:
                if q[i] < 0:
                    return None
            else:
                t = q[i] / p[i]
                if p[i] < 0:
                    if t > tMin:
                        tMin = t
                else:
                    if t < tMax:
                        tMax = t

        if tMin < tMax:
            x0Clipped = x0 + tMin * dx
            y0Clipped = y0 + tMin * dy
            x1Clipped = x0 + tMax * dx
            y1Clipped = y0 + tMax * dy
        
            return Line(
                        Point(x0Clipped, y0Clipped, z0),
                        Point(x1Clipped, y1Clipped, z1),
                        line.name
                        )

        return None

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
        
        #print(f'Clipping line {line.name} with positions: {p1}, {p2}')
        
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
            else:
                x0, y0 = p1.axisX, p1.axisY
                    
            if code2 != 0:
                #print("Clipping point 2")
                temp = self.__intersection(p2, p1, win_bottom_left, win_top_left, win_top_right, code2)
                x1, y1 = temp.axisX, temp.axisY
            else:
                x1, y1 = p2.axisX, p2.axisY
                
            #print(f'Old points: ({p1.axisX}, {p1.axisY}) | ({p2.axisX}, {p2.axisY})')
            #print(f'New points: ({x0}, {y0}) | ({x1}, {y1})')
            
            # If the line is still outside the window
            if self.__compute_code(Position3D(x0, y0, 1), win_bottom_left, win_top_left, win_top_right) != 0 and self.__compute_code(Position3D(x1, y1, 1), win_bottom_left, win_top_left, win_top_right) != 0:
                return None
                
            return Line(Point(x0, y0, 0), Point(x1, y1, 0), line.name)


class WeilerAthertonStrategy:
    def __init__(self) -> None:
        pass
    
    def __intersection_lb(self, p1: Position3D, p2: Position3D, win_bottom_left: Position3D, win_top_left: Position3D, win_top_right: Position3D, win_bottom_right: Position3D) -> list[str, Position3D, str, Position3D] | list[str, Position3D] | None:
        if self.__wireframe_inside([p1, p2], win_bottom_left, win_top_right):
            return None
        
        x0, y0, z0 = p1.axisX, p1.axisY, p1.axisZ
        x1, y1, z1 = p2.axisX, p2.axisY, p2.axisZ
        
        dx = x1 - x0
        dy = y1 - y0
        xmax, ymax = win_top_right.axisX, win_top_right.axisY
        xmin, ymin = win_bottom_left.axisX, win_bottom_left.axisY

        p = [-dx, dx, -dy, dy]
        q = [x0 - xmin, xmax - x0, y0 - ymin, ymax - y0]
        # checks if line is parallel to border
        if (
            (p[0] == 0 and q[0] < 0)
            or (p[1] == 0 and q[1] < 0)
            or (p[2] == 0 and q[2] < 0)
            or (p[3] == 0 and q[3] < 0)
        ):
            return None

        # From outside to inside
        zeta1 = [q[n] / p[n] for n in range(4) if p[n] < 0]

        # From inside to outside
        zeta2 = [q[n] / p[n] for n in range(4) if p[n] > 0]
        
        zeta1.append(0)
        zeta2.append(1)
        # from outside to inside
        zeta1 = max(zeta1)

        # from inside to outside
        zeta2 = min(zeta2)

        # Removes line if its completely out of window
        if zeta1 > zeta2:
            return None

        if zeta1 != 0 and zeta2 != 1:
            xn0 = x0 + dx * zeta1
            yn0 = y0 + dy * zeta1
            xn1 = x0 + dx * zeta2
            yn1 = y0 + dy * zeta2
            return ["out-in", Position3D(xn0, yn0, 1), "in_out", Position3D(xn1, yn1, 1)]

        elif zeta1 == 0:
            xn1 = x0 + dx * zeta2
            yn1 = y0 + dy * zeta2
            return ["in-out", Position3D(xn1, yn1, 1)]

        elif zeta2 == 1:
            xn0 = x0 + dx * zeta1
            yn0 = y0 + dy * zeta1
            return ["out-in", Position3D(xn0, yn0, 1)]
        
    
    def __wireframe_inside(self, positions: list[Position3D], win_bottom_left: Position3D, win_top_right: Position3D) -> bool:
        for position in positions:
            if position.axisX < win_bottom_left.axisX or position.axisX > win_top_right.axisX or position.axisY < win_bottom_left.axisY or position.axisY > win_top_right.axisY:
                #print(f'Position {position} is outside window')
                return False
        
        return True
    
    def clip(self, polygon: WireFrame, win_bottom_left: Position3D, win_top_left: Position3D, win_top_right: Position3D, win_bottom_right: Position3D) -> WireFrame:
        # Deepcopy because we change Z coordinate
        positions = deepcopy(polygon.getPositions())
        
        if self.__wireframe_inside(positions, win_bottom_left, win_top_right):
            return polygon
        
        subject = []
        cr_i = [[], [], [], []]
        c_length = len(positions)
        
        # Set to 1 to avoid removing at the end
        for p in positions:
            p.axisZ = 1
        
        counter = 0
        for i in range(-1, c_length - 1):
            intersection = self.__intersection_lb(positions[i], positions[i + 1], win_bottom_left, win_top_left, win_top_right, win_bottom_right)
            #print(f'Intersection: {intersection} for positions: {positions[i]} and {positions[i + 1]}')
            
            if intersection:
                counter += 1
                subject.append(positions[i])
                
                if len(intersection) == 2:
                    subject.append(intersection)
                        
                    x = round(intersection[1].axisX, 5)
                    y = round(intersection[1].axisY, 5)
                    
                    # bottom
                    if y == win_bottom_left.axisY:
                        cr_i[0].append(intersection)
                    # right
                    if x == win_top_right.axisX:
                        cr_i[1].append(intersection)
                    # top
                    if y == win_top_right.axisY:
                        cr_i[2].append(intersection)
                    # left
                    if x == win_bottom_left.axisX:
                        cr_i[3].append(intersection)
                else:
                    x0 = round(intersection[1].axisX, 5)
                    y0 = round(intersection[1].axisY, 5)
                    x1 = round(intersection[3].axisX, 5)
                    y1 = round(intersection[3].axisY, 5)
                    
                    subject.append(intersection[2:])

                    # bottom
                    if y1 == win_bottom_left.axisY:
                        cr_i[0].append(intersection[2:])
                    # right
                    elif x1 == win_top_right.axisX:
                        cr_i[1].append(intersection[2:])
                    # top
                    elif y1 == win_top_right.axisY:
                        cr_i[2].append(intersection[2:])
                    # left
                    elif x1 == win_bottom_left.axisX:
                        cr_i[3].append(intersection[2:])
                        
                    subject.append(intersection[:2])
                    
                    
                    # bottom
                    if y0 == win_bottom_left.axisY:
                        cr_i[0].append(intersection[:2])
                    # right
                    elif x0 == win_top_right.axisX:
                        cr_i[1].append(intersection[:2])
                    # top
                    elif y0 == win_top_right.axisY:
                        cr_i[2].append(intersection[:2])
                    # left
                    elif x0 == win_bottom_left.axisX:
                        cr_i[3].append(intersection[:2])

                    counter += 1
                        
            else:
                subject.append(positions[i])
                
        # unpack intersections on
        cr_i.insert(0, [Position3D(win_bottom_left.axisX, win_bottom_left.axisY, 0)])
        cr_i.insert(2, [Position3D(win_bottom_right.axisX, win_bottom_right.axisY, 0)])
        cr_i.insert(4, [Position3D(win_top_right.axisX, win_top_right.axisY, 0)])
        cr_i.insert(6, [Position3D(win_top_left.axisX, win_top_left.axisY, 0)])
        
        #print(cr_i)
        
        # sort intersections according to window border
        cr_i[1].sort(key=lambda x: x[1].axisX if type(x) is list else x.axisX)
        cr_i[3].sort(key=lambda x: x[1].axisY if type(x) is list else x.axisY)
        cr_i[5].sort(key=lambda x: x[1].axisX if type(x) is list else x.axisX, reverse=True)
        cr_i[7].sort(key=lambda x: x[1].axisY if type(x) is list else x.axisY, reverse=True)

        # flatten intersections
        cr = [j for i in cr_i for j in i]
        
        """ for i in range(len(cr)):
            if type(cr[i]) is list:
                print((cr[i][1].axisX, cr[i][1].axisY, cr[i][1].axisZ), end=' ')
            else:
                print((cr[i].axisX, cr[i].axisY, cr[i].axisZ), end=' ')
        print() """

        # No intersections, simply return and remove element
        if counter == 0:
            return None 
        
        # get iteraton index
        i = None
        for n in range(len(subject)):
            #print(f'Subject: {subject[n]}')
            if type(subject[n]) is list:
                # mark first intersection index
                if subject[n][0] == "out-in":
                    i = n
                    break
        # check if subject is oriented clockwise
        # if subject[n]:
        # the clipped polygon coordinates
        clipped = [subject[i][1]]
        # boolean to check where to iterate
        on_polygon = True
        
        # iterate over polygon and window
        while True:
            i += 1
            if on_polygon:
                i = i % len(subject)
                
                #print('Subject: ', subject[i])

                if type(subject[i]) is not list:
                    if self.__wireframe_inside([subject[i]], win_bottom_left, win_top_right):
                        clipped.append(subject[i])
                else:
                    x_subject, y_subject, z_subject = subject[i][1].axisX, subject[i][1].axisY, subject[i][1].axisZ
                    x_clipped, y_clipped, z_clipped = clipped[0].axisX, clipped[0].axisY, clipped[0].axisZ
                    
                    if x_subject == x_clipped and y_subject == y_clipped:
                        break
                    on_polygon = False
                    clipped.append(subject[i][1])
                    #print(cr)
                    for n in range(len(cr)):
                        if type(cr[n]) is list:
                            if cr[n][1].axisX == x_subject and cr[n][1].axisY == y_subject:
                                i = n
                                break
                                
            else:
                i = i % len(cr) 

                #print('CR: ', cr[i])
                
                if type(cr[i]) is not list:
                    clipped.append(cr[i])

                else:
                    x_cr, y_cr, z_cr = cr[i][1].axisX, cr[i][1].axisY, cr[i][1].axisZ
                    x_clipped, y_clipped, z_clipped = clipped[0].axisX, clipped[0].axisY, clipped[0].axisZ
                    
                    if x_cr == x_clipped and y_cr == y_clipped:
                        clipped.append(cr[i][1])
                        break
                    on_polygon = True
                    
                    clipped.append(cr[i][1])
                    #print(subject)
                    for n in range(len(subject)):
                        if type(subject[n]) is list:
                            if subject[n][1].axisX == x_cr and subject[n][1].axisY == y_cr:
                                i = n
                                break
        
        #print([(p.axisX, p.axisY, p.axisZ) for p in clipped])
        
        return WireFrame(polygon.name, [Point.fromPosition(p) for p in clipped])
                
              
class Clipper:
    def __init__(self) -> None:
        self.__lineClippingStrategy: LineClippingStrategy = CohenSutherlandStrategy()
        self.__polygongClip = WeilerAthertonStrategy()
    
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
            positions = obj.getPositions()

            temp = None
            
            #print(f'Clipping object {obj.name}')
            
            # TODO: Add wireframe clipping when polygon algorithm is implemented
            if obj.type == ObjectsTypes.POINT:
                temp = self.__clipPoint(obj, win_bottom_left, win_top_left, win_top_right, win_bottom_right)
            elif obj.type == ObjectsTypes.LINE or (obj.type == ObjectsTypes.WIREFRAME and len(obj.getPositions()) == 2):
                temp = self.__lineClippingStrategy.clip(obj, win_bottom_left, win_top_left, win_top_right, win_bottom_right)
            elif obj.type == ObjectsTypes.WIREFRAME:
                temp = self.__polygongClip.clip(obj, win_bottom_left, win_top_left, win_top_right, win_bottom_right)
                #temp = obj
                
            if temp is not None:
                temp.setColor(obj.color)
                clipped_objs.append(temp)
        
        return clipped_objs