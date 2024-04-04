from copy import copy, deepcopy
from typing import List
from Domain.Management.Viewport import ViewPort
from Domain.Management.Window import Window
from Domain.Management.World import World
from Domain.Shapes.Point import Point
from Domain.Shapes.Line import Line
from Domain.Shapes.Wireframe import WireFrame
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Coordinates import Position3D
from Domain.Utils.Transforms import Translation, Rotation, GenericTransform
from Domain.Utils.Enums import RotationTypes
import numpy as np


class WorldObjectsHandler:
    def __init__(self, viewPort: ViewPort, window: Window, world: World) -> None:
        self.__viewport = viewPort
        self.__window = window
        self.__world = world
        self.__tempWireframePoints: List[Point] = []
        self.__windowPos = None
    
    def addObject(self, obj: SGIObject) -> None:
        self.__world.addObject(obj)
    
    def addLine(self, pointOne: Position3D, pointTwo: Position3D, name: str = "Linha") -> None:
        line = Line(pointOne, pointTwo, name)

        self.__world.addObject(line)

    def addPoint(self, position: Position3D, name: str = 'Ponto') -> None:
        print(f'Ponto adicionado {position.axisX}, {position.axisY}, {position.axisZ}')

        point = Point(position.axisX, position.axisY, position.axisZ, name)

        self.__world.addObject(point)

        
    def addTempPointWireframe(self, position: Position3D) -> None:
        print(f'Ponto adicionado ao wireframe {position.axisX}, {position.axisY}, {position.axisZ}')

        point = Point(position.axisX, position.axisY, position.axisZ, "Ponto do polígono")
        
        self.__tempWireframePoints.append(point)
        
    def commitWireframeCreation(self, name: str = "Wireframe") -> None:
        if len(self.__tempWireframePoints) == 0:
            return

        wireFrame = WireFrame(name, copy(self.__tempWireframePoints))

        self.__world.addObject(wireFrame)
        
        self.__tempWireframePoints.clear()
    
    def getWindowObjectsPPC(self) -> tuple[Position3D, list[SGIObject]]:
        # Compute v_up (vector of the left side of the window)
        window_positions = deepcopy(self.__window.getPositions())
        v_up = Position3D(window_positions[1].axisX - window_positions[0].axisX, window_positions[1].axisY - window_positions[0].axisY, 0)
        
        angle = np.rad2deg(np.arccos(v_up.axisY / np.linalg.norm([v_up.axisX, v_up.axisY])))
        
        print(f'Angle: {angle}')
        print(f'v_up: {v_up.axisX}, {v_up.axisY}, {v_up.axisZ}')
        
        # Window center to origin (translate objs accordingly)
        # Rotate window and objs by -(angle between Y and v_up)
        translate_window = Translation(-self.__window.centralPoint.axisX, -self.__window.centralPoint.axisY, -self.__window.centralPoint.axisZ)
        translate_objs = Translation(-self.__window.centralPoint.axisX, -self.__window.centralPoint.axisY, -self.__window.centralPoint.axisZ)
        rotate_window = Rotation(-angle, RotationTypes.CENTER_WORLD)
        rotate_objs = Rotation(-angle, RotationTypes.CENTER_WORLD)
        
        objs = deepcopy(self.__world.objects)
        
        final_transform_window = GenericTransform(positions=window_positions)
        final_transform_window.add_transforms([translate_window, rotate_window])
        
        final_obj_positions = []
        
        for obj in objs:
            positions = obj.getPositions()
            centralPoint = obj.centralPoint
            
            translate_to_origin = Translation(-centralPoint.axisX, -centralPoint.axisY, -centralPoint.axisZ)
            translate_back = Translation(centralPoint.axisX - self.__window.centralPoint.axisX, centralPoint.axisY - self.__window.centralPoint.axisY, centralPoint.axisZ - self.__window.centralPoint.axisZ)
            
            final_transform_obj = GenericTransform(positions=positions)
            final_transform_obj.add_transforms([translate_to_origin, rotate_objs, translate_back])
            
            final_obj_positions.append(final_transform_obj.execute())
            
        final_objs = []
        for obj, positions in zip(self.__world.objects, final_obj_positions):
            obj_copy = deepcopy(obj)
            obj_copy.setPositions(positions)
            
            final_objs.append(obj_copy)
        
        # Return new window and objs
        return final_transform_window.execute(), final_objs
    
    def originWorldViewport(self) -> Position3D:
        return self.__transformPositionToViewPortPPC(Position3D(0, 0, 1), self.__windowPos)
    
    def originWorldViewport(self) -> Position3D:
        return self.__transformPositionToViewPort(Position3D(0, 0, 1))
        
    def __transformPositionToViewPort(self, position: Position3D) -> Position3D:
        xW = position.axisX

        xVP = ((xW - self.__window.Xmin) / (self.__window.dimensions.length)) * (self.__viewport.dimensions.length)

        yW = position.axisY

        yVP = (1 - ((yW - self.__window.Ymin) / (self.__window.dimensions.width))) * (self.__viewport.dimensions.width)
       
        pointTransformed = Position3D(round(xVP), round(yVP), 1)

        return pointTransformed

    def __transformPositionToViewPortPPC(self, position: Position3D, window_pos: Position3D) -> Position3D:
        xW = position.axisX

        xVP = ((xW - window_pos[0].axisX) / (self.__window.dimensions.length)) * (self.__viewport.dimensions.length)

        yW = position.axisY

        yVP = (1 - ((yW - window_pos[0].axisY) / (self.__window.dimensions.width))) * (self.__viewport.dimensions.width)
       
        pointTransformed = Position3D(round(xVP), round(yVP), 1)

        return pointTransformed
    
    def getObjectsViewportPPC(self) -> List[SGIObject]:
        windowPosition, objs = self.getWindowObjectsPPC()
        
        self.__windowPos = windowPosition
        
        objectsToShow: List[SGIObject] = []
        
        for obj in objs:
            # Creates a copy to not change the Domain value
            objCopy = deepcopy(obj)

            for position in objCopy.getPositions():
                transformedPosition = self.__transformPositionToViewPortPPC(position, windowPosition)

                position.axisX = transformedPosition.axisX
                position.axisY = transformedPosition.axisY
                position.axisZ = transformedPosition.axisZ

            objectsToShow.append(objCopy)

        return objectsToShow
        
    
    def getObjectsViewport(self) -> List[SGIObject]:
        objectsToShow: List[SGIObject] = []

        for obj in self.__world.objects:
            # Creates a copy to not change the Domain value
            objCopy = deepcopy(obj)

            for position in objCopy.getPositions():
                transformedPosition = self.__transformPositionToViewPort(position)

                position.axisX = transformedPosition.axisX
                position.axisY = transformedPosition.axisY
                position.axisZ = transformedPosition.axisZ

            objectsToShow.append(objCopy)

        return objectsToShow
    
    def getObjectByName(self, name: str) -> SGIObject:
        for obj in self.__world.objects:
            if obj.name == name:
                return obj

        return None