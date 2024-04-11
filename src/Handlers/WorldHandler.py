from Domain.Management.Viewport import ViewPort
from Domain.Management.Window import Window
from Domain.Management.World import World
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Enums import RotationTypes
from Domain.Utils.Transforms import GenericTransform, Rotation, Translation
from Handlers.WorldObjectsHandler import WorldObjectsHandler
from Domain.Utils.Constants import Constants
import math
from copy import deepcopy


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
        print("Before rotation")
        self.__window.printPositions()

        windowTranslationTransform = Translation(-self.__window.centralPoint.axisX, -self.__window.centralPoint.axisY, -self.__window.centralPoint.axisZ)
        windowRotationTransform = Rotation(angle, RotationTypes.CENTER_OBJECT)
        windowBackTranslationTransform = Translation(self.__window.centralPoint.axisX, self.__window.centralPoint.axisY, self.__window.centralPoint.axisZ)
        
        finalTransform = GenericTransform(positions=window_positions)
        finalTransform.add_transforms([windowTranslationTransform, windowRotationTransform, windowBackTranslationTransform])
        
        finalPositions = finalTransform.execute()
        self.__window.setPositions(finalPositions)
        self.__window.angle += angle % 360
        
        # Transform the objects of the world
        for obj in self.__world.objects:
            transform = GenericTransform(positions=obj.getPositions())
            
            rotation = Rotation(-angle, RotationTypes.CENTER_OBJECT)
                       
            transform.add_transforms([windowTranslationTransform, rotation, windowBackTranslationTransform])
            obj.setPositions(transform.execute())
        
        window_positions = self.__window.getPositions()
        print("After rotation")
        self.__window.printPositions()
