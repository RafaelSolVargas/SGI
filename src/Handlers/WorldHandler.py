from Domain.Management.Viewport import ViewPort
from Domain.Management.Window import Window
from Domain.Management.World import World
from Domain.Utils.Enums import ObjectsTypes
from Handlers.WorldObjectsHandler import WorldObjectsHandler


class WorldHandler:
    VIEWPORT_LENGHT = 600
    VIEWPORT_WIDTH = 800
    VIEWPORT_HEIGHT = 600

    __instance: 'WorldHandler' = None

    @classmethod
    def getHandler(cls) -> 'WorldHandler':
        if cls.__instance is None:
            cls.__instance = WorldHandler()

        return cls.__instance
    
    def __init__(self) -> None:
        self.__viewport = ViewPort(self.VIEWPORT_LENGHT, self.VIEWPORT_WIDTH, self.VIEWPORT_HEIGHT)
        self.__window = Window(self.VIEWPORT_LENGHT, self.VIEWPORT_WIDTH, self.VIEWPORT_HEIGHT)
        self.__world = World()
        self.__objectsHandler = WorldObjectsHandler(self.__viewport, self.__window, self.__world)

    @property
    def objectHandler(self):
        return self.__objectsHandler

    @property
    def window(self):
        return self.__window

    @property
    def viewPort(self):
        return self.__viewport

