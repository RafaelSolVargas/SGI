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
from Domain.Utils.Enums import ClippingMethods, RotationTypes
from Domain.Management.Clipping import Clipper, CohenSutherlandStrategy, LiangBarskyStrategy
from Domain.Utils.Constants import Constants
import numpy as np


class WorldObjectsHandler:
    def __init__(self, viewPort: ViewPort, window: Window, world: World) -> None:
        self.__viewport: ViewPort = viewPort
        self.__window: Window = window
        self.__world: World = world
        self.__tempWireframePoints: List[Point] = []
        self.__windowPos: Position3D = None
        self.__clipper = Clipper()

    def setClippingMethod(self, clippingMethod: ClippingMethods) -> None:
        if clippingMethod == ClippingMethods.COHEN:
            self.__clipper.setLineClippingStrategy(CohenSutherlandStrategy())
        elif clippingMethod == ClippingMethods.LIANG:
            self.__clipper.setLineClippingStrategy(LiangBarskyStrategy())
        else:
            print('Clipping method não encontrado')

    @property
    def windowPosPPC(self) -> Position3D:
        arr = []
        
        for pos in self.__windowPos:
            arr.append(self.__transformPositionToViewPortPPC(pos, self.__windowPos))
            
        for pos in arr:
            pos.axisX += Constants.VIEWPORT_SLACK // 2
            pos.axisY += Constants.VIEWPORT_SLACK // 2
            
        return arr
    
    @property
    def windowCenterPPC(self) -> Position3D:
        print(f'Window center: {self.__window.centralPoint}')
        pos = self.__transformPositionToViewPortPPC(self.__window.centralPoint, self.__windowPos)
        
        print(f"Window center PPC: {pos.axisX}, {pos.axisY}")
        
        #pos.axisX += Constants.VIEWPORT_SLACK // 2
        #pos.axisY += Constants.VIEWPORT_SLACK // 2
        
        return pos 
    
    def addObject(self, obj: SGIObject) -> None:
        self.__world.addObject(obj)
    
    def addLine(self, pointOne: Position3D, pointTwo: Position3D, name: str = "Linha", color: tuple[int, int, int] = (0, 0, 0)) -> None:
        line = Line(pointOne, pointTwo, name)
        line.setColor(color)

        self.__world.addObject(line)

    def addPoint(self, position: Position3D, name: str = 'Ponto', color: tuple[int, int, int] = (0, 0, 0)) -> None:
        print(f'Ponto adicionado {position.axisX}, {position.axisY}, {position.axisZ}')

        point = Point(position.axisX, position.axisY, position.axisZ, name)
        point.setColor(color)

        self.__world.addObject(point)

    def addTempPointCurve(self, position: Position3D) -> None:
        pass
    
    # TODO: Don't create if len < 4
    def commitCurveCreation(self, name: str = "Curva", color: tuple[int, int, int] = (0, 0, 0)) -> None:
        pass
    
    def addTempPointWireframe(self, position: Position3D) -> None:
        print(f'Ponto adicionado ao wireframe {position.axisX}, {position.axisY}, {position.axisZ}')

        point = Point(position.axisX, position.axisY, position.axisZ, "Ponto do polígono")
        
        self.__tempWireframePoints.append(point)
        
    def commitWireframeCreation(self, name: str = "Wireframe", color: tuple[int, int, int] = (0, 0, 0), fill: bool = False) -> None:
        if len(self.__tempWireframePoints) == 0:
            return

        wireFrame = WireFrame(name, copy(self.__tempWireframePoints), fill)
        wireFrame.setColor(color)

        self.__world.addObject(wireFrame)
        
        self.__tempWireframePoints.clear()
    
    def __convertObjectToPPC(self, inputObjects: List[SGIObject]) -> tuple[Position3D, list[SGIObject]]:
        # Get the left bottom and left up positions from Window
        windowPositions = deepcopy(self.__window.getPositions())
       
        objectToConvert = deepcopy(inputObjects)
        
        # Apply the transform to a copy of each object
        transformedObjects: List[SGIObject] = []
        for obj in objectToConvert:
            objPositions = obj.getPositions()
            
            # Translate object 
            translateTransform = Translation(self.__window.centralPoint.axisX, self.__window.centralPoint.axisY, self.__window.centralPoint.axisZ, objPositions)

            # Execute the matrix calculus
            objFinalPositions = translateTransform.execute()

            # Create a new object with the new positions and add to the list
            objCopy = deepcopy(obj)
            objCopy.setPositions(objFinalPositions)
            
            transformedObjects.append(objCopy)

        # Translate the window
        translateWindowTransform = Translation(-self.__window.centralPoint.axisX, 
                                       -self.__window.centralPoint.axisY, 
                                       -self.__window.centralPoint.axisZ, 
                                       windowPositions)

        newWindowsPositions = translateWindowTransform.execute()

        # Rotate the window
        newWindowsPositions = Rotation(-self.__window.angle, RotationTypes.CENTER_WORLD, newWindowsPositions).execute()

        # Return new window matrix and transformed objects
        return newWindowsPositions, transformedObjects
    
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

        xVP = ((xW - window_pos[0].axisX) / (self.__window.dimensions.length)) * (Constants.VIEWPORT_LENGTH)

        yW = position.axisY

        yVP = (1 - ((yW - window_pos[0].axisY) / (self.__window.dimensions.width))) * (Constants.VIEWPORT_WIDTH)
        
        pointTransformed = Position3D(round(xVP), round(yVP), 1)

        return pointTransformed
    
    def getObjectsTransformedToViewPortAndPPC(self) -> List[SGIObject]:
        windowPosition, objs = self.__convertObjectToPPC(self.__world.objects)
        clipped_objs = self.__clipper.clip(windowPosition, objs, self.__window.dimensions.length)
        
        print(windowPosition[0], windowPosition[1])
        
        objectsToShow: List[SGIObject] = []
        
        for obj in clipped_objs:
            # Creates a copy to not change the Domain value
            objCopy = deepcopy(obj)

            for position in objCopy.getPositions():
                transformedPosition = self.__transformPositionToViewPortPPC(position, windowPosition)

                position.axisX = transformedPosition.axisX + Constants.VIEWPORT_SLACK // 2
                position.axisY = transformedPosition.axisY + Constants.VIEWPORT_SLACK // 2
                position.axisZ = transformedPosition.axisZ
        
            objectsToShow.append(objCopy)

        self.__windowPos = windowPosition
        
        #print(f'Window center: {self.__window.centralPoint}')
        #self.__window.printPositions()
        
        return objectsToShow

    
    def getObjectByName(self, name: str) -> SGIObject:
        for obj in self.__world.objects:
            if obj.name == name:
                return obj

        return None