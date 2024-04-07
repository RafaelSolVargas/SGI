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
from Domain.Management.Clipping import Clipper
import numpy as np


class WorldObjectsHandler:
    def __init__(self, viewPort: ViewPort, window: Window, world: World) -> None:
        self.__viewport: ViewPort = viewPort
        self.__window: Window = window
        self.__world: World = world
        self.__tempWireframePoints: List[Point] = []
        self.__windowPos: Position3D = None
        self.__clipper = Clipper()
    
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
    
    def __convertObjectToPPC(self, inputObjects: List[SGIObject]) -> tuple[Position3D, list[SGIObject]]:
        # Get the left bottom and left up positions from Window
        window_positions = deepcopy(self.__window.getPositions())
 
        # Compute v_up (vector of the left side of the window)
        v_up = Position3D(window_positions[1].axisX - window_positions[0].axisX, 
                          window_positions[1].axisY - window_positions[0].axisY, 
                          0)
        
        # Get the angle to the aixs Y
        cosine = v_up.axisY / np.linalg.norm([v_up.axisX, v_up.axisY])
        angle = np.rad2deg(np.arccos(cosine))
        
        # Build the translation of the window
        translateWindowTransform = Translation(-self.__window.centralPoint.axisX, 
                                       -self.__window.centralPoint.axisY, 
                                       -self.__window.centralPoint.axisZ, 
                                       window_positions)
        
        translateWindowMatrix = translateWindowTransform.execute()
        
        # Build the rotation to be applied to all objects
        rotateTransform = Rotation(-angle, RotationTypes.CENTER_WORLD)
        
        objectToConvert = deepcopy(inputObjects)
        finalObjPositions: List[List[Position3D]] = []
        
        # Build the transform for each object
        for obj in objectToConvert:
            objPositions = obj.getPositions()
            objCentralPoint = obj.centralPoint
            
            diffAxisX = objCentralPoint.axisX - self.__window.centralPoint.axisX
            diffAxisY = objCentralPoint.axisY - self.__window.centralPoint.axisY
            diffAxisZ = objCentralPoint.axisZ - self.__window.centralPoint.axisZ
            
            # Translate object to origin
            translateToOriginTransform = Translation(-objCentralPoint.axisX, -objCentralPoint.axisY, -objCentralPoint.axisZ)
            
            # Translate object back
            translateBackTransform = Translation(diffAxisX, diffAxisY, diffAxisZ)

            # Stack up the transform for the obj             
            finalTransform = GenericTransform(positions=objPositions)
            finalTransform.add_transforms([translateToOriginTransform, rotateTransform, translateBackTransform])
            
            finalObjPositions.append(finalTransform.execute())
            
        # Apply the transform to a copy of each object
        transformedObjects: List[SGIObject] = []
        for obj, objPositions in zip(inputObjects, finalObjPositions):
            objCopy = deepcopy(obj)
            objCopy.setPositions(objPositions)
            
            transformedObjects.append(objCopy)
        
        # Return new window matrix and transformed objects
        return translateWindowMatrix, transformedObjects
    
    def originWorldViewportPPC(self) -> Position3D:
        return self.__transformPositionToViewPortPPC(Position3D(0, 0, 1), self.__windowPos)

    def getAxisLinesToDrawPPC(self) -> tuple[Line, Line]:
        # Create points that will represent both axis 
        axisXLeftPoint = Point(-1000, 0, 1)
        axisXRightPoint = Point(1000, 0, 1)
        axisYBottomPoint = Point(0, -600, 1)
        axisYUpperPoint = Point(0, 600, 1)

        # Convert to lines
        axisXLine = Line(axisXLeftPoint, axisXRightPoint)
        axisYLine = Line(axisYBottomPoint, axisYUpperPoint)
        
        # Convert to the PPC
        #_, convertedList = self.__convertObjectToPPC([axisXLine])
        #convertedAxisXLine = convertedList[0] 

        #_, convertedList = self.__convertObjectToPPC([axisYLine])
        #convertedAxisYLine = convertedList[0]

        # return convertedAxisXLine, convertedAxisYLine

        # Get the left bottom and left up positions from Window
        window_positions = deepcopy(self.__window.getPositions())
 
        # Compute v_up (vector of the left side of the window)
        v_up = Position3D(window_positions[1].axisX - window_positions[0].axisX, 
                          window_positions[1].axisY - window_positions[0].axisY, 
                          0)
        
        # Get the angle to the aixs Y
        cosine = v_up.axisY / np.linalg.norm([v_up.axisX, v_up.axisY])
        angle = np.rad2deg(np.arccos(cosine))
        
        # Build the rotation to be applied to both lines
        rotateTransform = Rotation(-angle, RotationTypes.CENTER_WORLD)
        
        # Convert the axis X to PPC
        axisXLineTransform = GenericTransform(positions=axisXLine.getPositions())
        axisXLineTransform.add_transforms([rotateTransform])

        lineXConvertedPositions = axisXLineTransform.execute()

        axisXLine.setPositions(lineXConvertedPositions)

        # Convert the axis Y to PPC
        axisYLineTransform = GenericTransform(positions=axisYLine.getPositions())
        axisYLineTransform.add_transforms([rotateTransform])

        lineXConvertedPositions = axisYLineTransform.execute()

        axisYLine.setPositions(lineXConvertedPositions)
        
        return axisXLine, axisYLine

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
    
    def getObjectsTransformedToViewPortAndPPC(self) -> List[SGIObject]:
        windowPosition, objs = self.__convertObjectToPPC(self.__world.objects)
        
        self.__windowPos = windowPosition
        
        objectsToShow: List[SGIObject] = []
        
        clipped_objs = self.__clipper.clip(windowPosition, objs, self.__window.dimensions.length)
        
        for obj in clipped_objs:
            # Creates a copy to not change the Domain value
            objCopy = deepcopy(obj)

            for position in objCopy.getPositions():
                transformedPosition = self.__transformPositionToViewPortPPC(position, windowPosition)

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