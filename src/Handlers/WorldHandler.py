from Domain.Management.Viewport import ViewPort
from Domain.Management.Window import Window
from Domain.Management.World import World
from Domain.Utils.Enums import RotationTypes
from Domain.Utils.Transforms import GenericTransform, Rotation, Translation
from Handlers.WorldObjectsHandler import WorldObjectsHandler
from Domain.Utils.Constants import Constants


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

    def rotateWindow(self, angle: float, axis: str) -> None:
        window_positions = self.__window.getPositions()

        windowTranslationTransform = Translation(-self.__window.centralPoint.axisX, -self.__window.centralPoint.axisY, -self.__window.centralPoint.axisZ)
        windowRotationTransform = Rotation(angle, RotationTypes.CENTER_OBJECT, axis=axis)
        windowBackTranslationTransform = Translation(self.__window.centralPoint.axisX, self.__window.centralPoint.axisY, self.__window.centralPoint.axisZ)
        
        finalTransform = GenericTransform(positions=window_positions)
        finalTransform.add_transforms([windowTranslationTransform, windowRotationTransform, windowBackTranslationTransform])
        
        finalPositions = finalTransform.execute()
        self.__window.setPositions(finalPositions)
        newAngle = (self.__window.angles[axis] + angle) % 360
        self.__window.setAngle(newAngle, axis)
        print(f"Window angle {axis}: {newAngle}")

        self.__window.printPositions()
        self.__window.dimensions.printDimensions()
        
        # Transform the objects of the world
        for obj in self.__world.objects:
            transform = GenericTransform(positions=obj.getPositions())
            
            rotation = Rotation(-angle, RotationTypes.CENTER_OBJECT, axis=axis)
                       
            transform.add_transforms([windowTranslationTransform, rotation, windowBackTranslationTransform])
            obj.setPositions(transform.execute())
        
        