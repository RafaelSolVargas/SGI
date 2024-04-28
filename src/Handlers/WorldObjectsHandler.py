from copy import copy, deepcopy
from typing import List
from Domain.Management.CurvesPlotting import CurvesPlotter
from Domain.Management.Viewport import ViewPort
from Domain.Management.Window import Window
from Domain.Management.World import World
from Domain.Shapes.Curve import Curve
from Domain.Shapes.Point import Point
from Domain.Shapes.Line import Line
from Domain.Shapes.Wireframe import WireFrame
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Coordinates import Position3D
from Domain.Utils.Transforms import Translation, Rotation
from Domain.Utils.Enums import ClippingMethods, ObjectsTypes, RotationTypes, CurvePlottingMethods
from Domain.Management.Clipping import Clipper, CohenSutherlandStrategy, LiangBarskyStrategy
from Domain.Utils.Constants import Constants


class WorldObjectsHandler:
    def __init__(self, viewPort: ViewPort, window: Window, world: World) -> None:
        self.__window: Window = window
        self.__world: World = world
        self.__tempWireframePoints: List[Point] = []
        self.__tempCurvePoints: List[Point] = []
        self.__clipper = Clipper()

    def setClippingMethod(self, clippingMethod: ClippingMethods) -> None:
        if clippingMethod == ClippingMethods.COHEN:
            self.__clipper.setLineClippingStrategy(CohenSutherlandStrategy())
        elif clippingMethod == ClippingMethods.LIANG:
            self.__clipper.setLineClippingStrategy(LiangBarskyStrategy())
        else:
            print('Clipping method não encontrado')

    @property
    def windowPositionsPPC(self) -> List[Position3D]:
        arr = []
        
        for position in self.__window.getPositions():
            arr.append(self.__transformPositionToViewPort(position, self.__window.getPositions()))
            
        for position in arr:
            position.axisX += Constants.VIEWPORT_SLACK // 2
            position.axisY += Constants.VIEWPORT_SLACK // 2
            
        return arr
    
    @property
    def windowCenterPPC(self) -> Position3D:
        return self.__convertWorldPositionToPpcAndViewport(self.__window.centralPoint)

    def __convertWorldPositionToPpcAndViewport(self, positionPPC: Position3D) -> Position3D: 
        # Creates a point to follow the method interface
        point = Point(positionPPC.axisX, positionPPC.axisY, positionPPC.axisZ)

        # Convert to PPC
        windowPositions, objectsConvertedToPPC = self.__convertObjectToPPC([point])

        # Extract the position again
        positionPPC = objectsConvertedToPPC[0].position

        # Convert to Viewport
        positionVP = self.__transformPositionToViewPort(positionPPC, windowPositions)

        return positionVP 
    
    @property
    def worldCenterPPC(self) -> Position3D:
        worldCenterPoint = Position3D(0, 0, 0)

        return self.__convertWorldPositionToPpcAndViewport(worldCenterPoint)
    
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
        print(f'Ponto adicionado a curva {position.axisX}, {position.axisY}, {position.axisZ}')

        point = Point(position.axisX, position.axisY, position.axisZ, "Ponto da curva")
        
        self.__tempCurvePoints.append(point)
    
    def commitCurveCreation(self, name: str = "Curva", color: tuple[int, int, int] = (0, 0, 0), strategy: CurvePlottingMethods = CurvePlottingMethods.BEZIER) -> None:
        if len(self.__tempCurvePoints) < 4:
            print('Curva precisa de pelo menos 4 pontos para ser criada')
            return
        
        curve = Curve(name, copy(self.__tempCurvePoints), strategy)
        curve.setColor(color)

        self.__world.addObject(curve)

        self.__tempCurvePoints.clear()

    
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
            
            # Calculate the points for this curve
            if (obj.type == ObjectsTypes.CURVE):
                objPositions = CurvesPlotter.generatePoints(obj, 0.1)

            # Translate object 
            translateTransform = Translation(-self.__window.centralPoint.axisX, -self.__window.centralPoint.axisY, -self.__window.centralPoint.axisZ, objPositions)

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

    def __transformPositionToViewPort(self, position: Position3D, window_pos: Position3D) -> Position3D:
        xW = position.axisX

        xVP = ((xW - window_pos[0].axisX) / (self.__window.dimensions.length)) * (Constants.VIEWPORT_LENGTH)

        yW = position.axisY

        yVP = (1 - ((yW - window_pos[0].axisY) / (self.__window.dimensions.width))) * (Constants.VIEWPORT_WIDTH)
        
        pointTransformed = Position3D(round(xVP), round(yVP), 1)

        return pointTransformed

    def getObjectsTransformedToViewPortAndPPC(self) -> List[SGIObject]:
        windowPosition, objs = self.__convertObjectToPPC(self.__world.objects)

        clipped_objs = self.__clipper.clip(windowPosition, objs, self.__window.dimensions.length)
        
        objectsToShow: List[SGIObject] = []
        
        for obj in clipped_objs:
            # Creates a copy to not change the Domain value
            objCopy = deepcopy(obj)

            for position in objCopy.getPositions():
                transformedPosition = self.__transformPositionToViewPort(position, windowPosition)

                position.axisX = transformedPosition.axisX + Constants.VIEWPORT_SLACK // 2
                position.axisY = transformedPosition.axisY + Constants.VIEWPORT_SLACK // 2
                position.axisZ = transformedPosition.axisZ
        
            objectsToShow.append(objCopy)

        return objectsToShow

    
    def getObjectByName(self, name: str) -> SGIObject:
        for obj in self.__world.objects:
            if obj.name == name:
                return obj

        return None