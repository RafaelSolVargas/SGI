from Domain.Management.Viewport import ViewPort
from Domain.Management.Window import Window


class WorldHandler:
    VIEWPORT_LENGHT = 600
    VIEWPORT_WIDTH = 800
    VIEWPORT_HEIGHT = 600


    @classmethod
    def createWorld() -> 'WorldHandler':
        return WorldHandler()
    
    def __init__(self) -> None:
        self.__viewport = None
        self.__window = None

    def startViewPort(self):
        self.__viewport = ViewPort(self.VIEWPORT_LENGHT, self.VIEWPORT_WIDTH, self.VIEWPORT_HEIGHT)
    
    def startWindow(self):
        self.__window = Window(self.VIEWPORT_LENGHT, self.VIEWPORT_WIDTH, self.VIEWPORT_HEIGHT)
