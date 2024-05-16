from copy import copy, deepcopy
import math
from typing import List
from Domain.Management.CurvesPlotting import CurvesPlotter
from Domain.Management.Viewport import ViewPort
from Domain.Management.Window import Window
from Domain.Management.World import World
from Domain.Shapes.Curve import Curve
from Domain.Shapes.Point import Point
from Domain.Shapes.Line import Line
from Domain.Shapes.Wireframe import WireFrame
from Domain.Shapes.Surface import Surface
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Coordinates import Position3D
from Domain.Utils.Transforms import Translation, Rotation, GenericTransform
from Domain.Utils.Enums import ClippingMethods, ObjectsTypes, RotationTypes, CurvePlottingMethods
from Domain.Management.Clipping import Clipper, CohenSutherlandStrategy, LiangBarskyStrategy
from Domain.Utils.Constants import Constants
import numpy as np


class WorldObjectsHandler:
    def __init__(self, viewPort: ViewPort, window: Window, world: World) -> None:
        self.__window: Window = window
        self.__world: World = world
        self.__tempWireframePoints: List[Point] = []
        self.__tempCurvePoints: List[Point] = []
        self.__clipper = Clipper()
        self.__debugWindowPos = []

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
        
        for position in self.__debugWindowPos:
            arr.append(self.__transformPositionToViewPort(position, self.__debugWindowPos))
            
        for position in arr:
            position.axisX += Constants.VIEWPORT_SLACK // 2
            position.axisY += Constants.VIEWPORT_SLACK // 2
            
        return arr
    
    @property
    def windowCenterPPC(self) -> Position3D:
        x_center = sum([p.axisX for p in self.__debugWindowPos]) / 4
        y_center = sum([p.axisY for p in self.__debugWindowPos]) / 4
        z_center = sum([p.axisZ for p in self.__debugWindowPos]) / 4
        
        return self.__transformPositionToViewPort(Position3D(x_center, y_center, z_center), self.__debugWindowPos)

    def __convertWorldPositionToPpcAndViewport(self, positionPPC: Position3D) -> Position3D: 
        # Creates a point to follow the method interface
        point = Point(positionPPC.axisX, positionPPC.axisY, positionPPC.axisZ)

        # Convert to PPC
        windowPositions, objectsConvertedToPPC = self.__convertObjectToPPC([point], self.__window.getPositions())

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
        
    def addSurface(self, positions: List[Position3D], name: str = 'Superfície', color: tuple[int, int, int] = (0, 0, 0), fill: bool = False) -> None:
        print(f'Superfície adicionada {name} com {len(positions)} pontos. Fill: {fill}')
        
        surface = Surface(name, [Point.fromPosition(p) for p in positions], fill)
        surface.setColor(color)
        
        self.__world.addObject(surface)

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
    
    def __perspectiveProjection(self, inputObjects: List[SGIObject]) -> tuple[List[Position3D], List[SGIObject]]:
        # Get the left bottom and left up positions from Window
        windowPositions = deepcopy(self.__window.getPositions())
        objectToConvert = deepcopy(inputObjects)
        
        # Get COP
        cop = self.__window.getCOP()
        
        toOrigin = Translation(-cop.axisX, -cop.axisY, -cop.axisZ)
        operations = [toOrigin]
        
        newWindowPositions = Translation(-cop.axisX, -cop.axisY, -cop.axisZ, windowPositions).execute()
        
        x = self.__window.dimensions.length / 2 + cop.axisX
        y = self.__window.dimensions.width / 2 + cop.axisY
        d = 1000
        perspectiveMatrix = np.asarray([
            [1, 0, -x/d, 0],
            [0, 1, -y/d, 0],
            [0, 0, 0, 0],
            [0, 0, -1/d, 1]
        ])
        
        print(f"Perspective matrix: {perspectiveMatrix}")
        perspectiveTransform = GenericTransform(matrix=perspectiveMatrix)
        operations.append(perspectiveTransform)
        
        # Apply the transform to a copy of each object
        transformedObjects: List[SGIObject] = []
        for obj in objectToConvert:
            objPositions = obj.getPositions()
            
            # Calculate the points for this curve
            if (obj.type == ObjectsTypes.CURVE):
                objPositions = CurvesPlotter.generatePoints(obj, 0.1)
            elif (obj.type == ObjectsTypes.SURFACE):
                objPositions = obj.generatePositions(0.1)
            
            
            finalTransform = GenericTransform(positions=objPositions)
            finalTransform.add_transforms(operations)
            #print("Final Perspective transform: ", finalTransform.matrix())
            
            objFinalPositions = finalTransform.execute()
            
            objCopy = deepcopy(obj)
            objCopy.setPositions(objFinalPositions)
            
            transformedObjects.append(objCopy)
            
        return newWindowPositions, transformedObjects
    
    def __parallelProjection(self, inputObjects: List[SGIObject]) -> tuple[List[Position3D], List[SGIObject]]:
        # Get the left bottom and left up positions from Window
        windowPositions = deepcopy(self.__window.getPositions())
       
        objectToConvert = deepcopy(inputObjects)
        
        # VPR to origin
        toOrigin = Translation(-self.__window.centralPoint.axisX, -self.__window.centralPoint.axisY, -self.__window.centralPoint.axisZ)
        
        operations = [toOrigin]
        
        # Get VPN
        vpn = Window.getVPN(windowPositions)
        
        # Angle between vpn, x and y
        alpha = np.pi / 2 - np.arccos(np.clip(np.dot(vpn, [1, 0, 0]), -1, 1))
        beta = np.pi / 2 - np.arccos(np.clip(np.dot(vpn, [0, 1, 0]), -1, 1))
        
        alpha = np.degrees(alpha)
        beta = np.degrees(beta)
        
        #print(f"Window angles: {self.__window.angles}")
        #print(f"Alpha: {alpha}, Beta: {beta}")
        
        rotateX, rotateY = None, None
        if alpha != 0:
            rotateX = Rotation(-alpha, RotationTypes.CENTER_WORLD, axis="X")
            operations.append(rotateX)
        
        if beta != 0:
            rotateY = Rotation(-beta, RotationTypes.CENTER_WORLD, axis="Y")
            operations.append(rotateY)
        
        windowTransform = GenericTransform(positions=windowPositions)
        windowTransform.add_transforms([toOrigin])
        newWindowPositions = windowTransform.execute()
        
        # Apply the transform to a copy of each object
        transformedObjects: List[SGIObject] = []
        for obj in objectToConvert:
            objPositions = obj.getPositions()
            
            # Calculate the points for this curve
            if (obj.type == ObjectsTypes.CURVE):
                objPositions = CurvesPlotter.generatePoints(obj, 0.1)
            elif (obj.type == ObjectsTypes.SURFACE):
                objPositions = obj.generatePositions(0.1)
                print(f"Object {obj.name} has {len(objPositions)} points")
                print([f"{p.axisX}, {p.axisY}, {p.axisZ}" for p in objPositions])
            finalTransform = GenericTransform(positions=objPositions)
            finalTransform.add_transforms(operations)
            
            objFinalPositions = finalTransform.execute()
            objFinalPositions = [Position3D(p.axisX, p.axisY, 0) for p in objFinalPositions]
            
            objCopy = deepcopy(obj)
            objCopy.setPositions(objFinalPositions)
            
            transformedObjects.append(objCopy)
            
        return newWindowPositions, transformedObjects
         
    def __convertObjectToPPC(self, inputObjects: List[SGIObject], windowPos: List[Position3D]) -> tuple[Position3D, list[SGIObject]]:
        # Get the left bottom and left up positions from Window
        windowPositions = deepcopy(windowPos)
        
        x_center = sum([p.axisX for p in windowPositions]) / 4
        y_center = sum([p.axisY for p in windowPositions]) / 4
        z_center = sum([p.axisZ for p in windowPositions]) / 4
       
        objectToConvert = deepcopy(inputObjects)
        
        # Apply the transform to a copy of each object
        transformedObjects: List[SGIObject] = []
        for obj in objectToConvert:
            objPositions = obj.getPositions()
            
            # Calculate the points for this curve
            if (obj.type == ObjectsTypes.CURVE):
                objPositions = CurvesPlotter.generatePoints(obj, 0.1)
            elif (obj.type == ObjectsTypes.SURFACE):
                objPositions = obj.generatePositions(0.1)

            # Translate object 
            translateTransform = Translation(-x_center, -y_center, -z_center, objPositions)

            # Execute the matrix calculus
            objFinalPositions = translateTransform.execute()

            # Create a new object with the new positions and add to the list
            objCopy = deepcopy(obj)
            objCopy.setPositions(objFinalPositions)

            transformedObjects.append(objCopy)

        # Translate the window
        translateWindowTransform = Translation(-x_center, -y_center, -z_center, windowPositions)

        newWindowsPositions = translateWindowTransform.execute()

        # Rotate the window
        rotations = [Rotation(-angle, RotationTypes.CENTER_WORLD, axis=axis) for axis, angle in self.__window.angles.items()]
        rotateWindowTransform = GenericTransform(positions=newWindowsPositions)
        rotateWindowTransform.add_transforms(rotations)
        newWindowsPositions = rotateWindowTransform.execute()

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
        windowPos, objs2d = self.__perspectiveProjection(self.__world.objects)
        #objs2d, windowPos = self.__world.objects, self.__window.getPositions()
        windowPosition, objs = self.__convertObjectToPPC(objs2d, windowPos)
        
        self.__debugWindowPos = windowPosition

        clipped_objs = self.__clipper.clip(windowPosition, objs, self.__window.dimensions.length)
        
        objectsToShow: List[SGIObject] = []
        
        for obj in clipped_objs:
            # Creates a copy to not change the Domain value
            objCopy = deepcopy(obj)
            print(f"Object {objCopy.name} has {len(objCopy.getPositions())} points")

            for position in objCopy.getPositions():
                transformedPosition = self.__transformPositionToViewPort(position, windowPosition)

                position.axisX = transformedPosition.axisX + Constants.VIEWPORT_SLACK // 2
                position.axisY = transformedPosition.axisY + Constants.VIEWPORT_SLACK // 2
                position.axisZ = transformedPosition.axisZ
        
            if objCopy.type == ObjectsTypes.WIREFRAME and objCopy.is3D():
                for line in objCopy.lines3D:
                    posOne = line.pointOne.position
                    posTwo = line.pointTwo.position

                    transformedPosOne = self.__transformPositionToViewPort(posOne, windowPosition)
                    line.pointOne.position.axisX = transformedPosOne.axisX + Constants.VIEWPORT_SLACK // 2
                    line.pointOne.position.axisY = transformedPosOne.axisY + Constants.VIEWPORT_SLACK // 2
                    line.pointOne.position.axisZ = transformedPosOne.axisZ

                    transformedPosTwo = self.__transformPositionToViewPort(posTwo, windowPosition)
                    line.pointTwo.position.axisX = transformedPosTwo.axisX + Constants.VIEWPORT_SLACK // 2
                    line.pointTwo.position.axisY = transformedPosTwo.axisY + Constants.VIEWPORT_SLACK // 2
                    line.pointTwo.position.axisZ = transformedPosTwo.axisZ

            objectsToShow.append(objCopy)

        return objectsToShow
    def getObjectByName(self, name: str) -> SGIObject:
        for obj in self.__world.objects:
            if obj.name == name:
                return obj

        return None