from Domain.Management.Viewport import ViewPort
from Domain.Management.Window import Window
from Domain.Management.World import World
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

