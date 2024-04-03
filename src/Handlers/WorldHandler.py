from Domain.Management.Viewport import ViewPort
from Domain.Management.Window import Window
from Domain.Management.World import World
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Enums import RotationTypes
from Domain.Utils.Transforms import GenericTransform, Rotation, Translation
from Handlers.WorldObjectsHandler import WorldObjectsHandler
from Domain.Utils.Constants import Constants
import math


class WorldHandler:
    __instance: 'WorldHandler' = None

    @classmethod
    def getHandler(cls) -> 'WorldHandler':
        if cls.__instance is None:
            cls.__instance = WorldHandler(Constants.VIEWPORT_LENGTH, Constants.VIEWPORT_WIDTH)

        return cls.__instance
    
    def __init__(self, viewport_length: int, viewport_width: int) -> None:
        self.__viewport = ViewPort(viewport_length, viewport_width)
        self.__window = Window(viewport_length, viewport_width, Constants.VIEWPORT_HEIGHT)
        self.__world = World()
        self.__objectsHandler = WorldObjectsHandler(self.__viewport, self.__window, self.__world)

    @property
    def objectHandler(self):
        return self.__objectsHandler

    @property
    def window(self):
        return self.__window

    @property
    def viewport(self):
        return self.__viewport

    def rotateWindow(self, angle: float):
        window_positions = self.__window.getPositions()
        
        print(f'Window position 0: {window_positions[0].axisX}, {window_positions[0].axisY}, {window_positions[0].axisZ}')
        print(f'Window position 1: {window_positions[1].axisX}, {window_positions[1].axisY}, {window_positions[1].axisZ}')
        

        windowTranslationTransform = Translation(-self.__window.centralPoint.axisX, -self.__window.centralPoint.axisY, -self.__window.centralPoint.axisZ)
        windowRotationTransform = Rotation(angle, RotationTypes.CENTER_OBJECT, window_positions)
        windowBackTranslationTransform = Translation(self.__window.centralPoint.axisX, self.__window.centralPoint.axisY, self.__window.centralPoint.axisZ)
        
        finalTransform = GenericTransform(positions=window_positions)
        finalTransform.add_transforms([windowTranslationTransform, windowRotationTransform, windowBackTranslationTransform])
        
        finalPositions = finalTransform.execute()
        self.__window.setPositions(finalPositions)

    def __calculateMatrixOfRotationOfWindowIntoObject(self, otherObj: SGIObject, angle: float, axis: str):
        # Calculates points of Window        
        centralPointWindow = self.__window.centralPoint
        Wx = centralPointWindow.axisX
        Wy = centralPointWindow.axisY
        Wz = centralPointWindow.axisZ

        # Calculate points of object
        centralPointObj = otherObj.centralPoint
        objX = centralPointObj.axisX
        objY = centralPointObj.axisY
        objZ = centralPointObj.axisZ

        # Diff between them
        diffX = objX - (objX - Wx)
        diffY = objY - (objY - Wy)
        diffZ = objZ - (objZ - Wz)

        # Angle convertion
        angleRadian = math.radians(angle)

        # Build all three transforms
        translationToOriginTransform = Translation(-diffX, -diffY, -diffZ)

        rotationTransform = Rotation(angleRadian, RotationTypes.CENTER_OBJECT, otherObj.getPositions())

        translationBackTransform = Translation(diffX, diffY, diffZ)

        # Pack them together 
        finalTransform = GenericTransform(positions=self.__obj.getPositions())
        finalTransform.add_transforms([translationToOriginTransform, rotationTransform, translationBackTransform])
        
        # Calculate the final matrix
        finalPositions = finalTransform.execute()

        # Apply into the object
        otherObj.setPositions(finalPositions)
