from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Utils.Enums import ObjectsTypes


class Window(SGIObject):
    ZOOM_MOVE: int = 10
    MIN_SIZE: int = 50
    MAX_SIZE: int = 8000
    __SCALE: float = 0.1
    """
    The space from the world to be drawn, it should be available to zoom in and zoom out
    and move in all 3 dimensions
    """
    def __init__(self, lenght: int, width: int, height: int) -> None:
        self.__BASE_LENGHT: int = lenght
        self.__BASE_WIDTH: int = width

        dimensions = Dimensions3D(lenght, width, height)
        position = Position3D(0, 0, 0)

        super().__init__(ObjectsTypes.WINDOW, "Window", dimensions, position)

    @property
    def Xmin(self) -> float:
        return self.position.axisX
    
    @property
    def Xmax(self) -> float:
        return self.position.axisX + self.dimensions.length
    
    @property
    def Ymin(self) -> float:
        return self.position.axisY
    
    @property
    def Ymax(self) -> float:
        return self.position.axisY + self.dimensions.width

    def zoomIn(self) -> None:
        """
        Decrease the dimensions from the window keeping the central point        
        """
        # Increases the dimension and decrease the position to move the window to both left and right
        self.dimensions.length -= self.__SCALE * self.__BASE_LENGHT
        self.position.axisX += self.__SCALE * self.__BASE_LENGHT

        # Increases the dimension and decrease the position to move the window to both up and down
        self.dimensions.width -= self.__SCALE * self.__BASE_WIDTH
        self.position.axisY += self.__SCALE * self.__BASE_WIDTH

    def zoomOut(self) -> None:
        """
        Increase the dimensions from the window keeping the central point        
        """
        # Increases the dimension and decrease the position to move the window to both left and right
        self.dimensions.length += self.__SCALE * self.__BASE_LENGHT
        self.position.axisX -= self.__SCALE * self.__BASE_LENGHT

        # Increases the dimension and decrease the position to move the window to both up and down
        self.dimensions.width += self.__SCALE * self.__BASE_WIDTH
        self.position.axisY -= self.__SCALE * self.__BASE_WIDTH

    def moveUp(self) -> None:
        self.position.axisY += self.ZOOM_MOVE
        self.setCentralPoint(self.dimensions.central_point(self.position))
    
    def moveDown(self) -> None:
        self.position.axisY -= self.ZOOM_MOVE
        self.setCentralPoint(self.dimensions.central_point(self.position))
    
    def moveLeft(self) -> None:
        self.position.axisX -= self.ZOOM_MOVE
        self.setCentralPoint(self.dimensions.central_point(self.position))
        
    def moveRight(self) -> None:
        self.position.axisX += self.ZOOM_MOVE
        self.setCentralPoint(self.dimensions.central_point(self.position))