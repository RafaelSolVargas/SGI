from typing import List
from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Utils.Enums import ObjectsTypes
from Domain.Utils.Constants import Constants


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
        
        # v_up (vector of the left side of the window)
        self.__positions = [Position3D(-Constants.VIEWPORT_LENGTH / 2, -Constants.VIEWPORT_WIDTH / 2, 0), Position3D(-Constants.VIEWPORT_LENGTH / 2, Constants.VIEWPORT_WIDTH / 2, 0)]

        super().__init__(ObjectsTypes.WINDOW, "Window", dimensions, self.__positions[0])
        
    
    def getPositions(self) -> List[Position3D]:
        return self.__positions
    
    def setPositions(self, positions: List[Position3D]) -> None:
        self.__positions = positions
    
    @property
    def centralPoint(self) -> Position3D:
        v_up_middle = Position3D((self.__positions[1].axisX - self.__positions[0].axisX) / 2, (self.__positions[1].axisY - self.__positions[0].axisY) / 2, 0)

        # Walks from the bottom middle left to the central point of the window
        return Position3D(self.__positions[0].axisX + v_up_middle.axisX, self.__positions[0].axisY + v_up_middle.axisY, 0)
    
    @property
    def Xmin(self) -> float:
        return self.__positions[0].axisX
    
    @property
    def Xmax(self) -> float:
        return self.__positions[0].axisX + self.dimensions.length
    
    @property
    def Ymin(self) -> float:
        return self.__positions[0].axisY
    
    @property
    def Ymax(self) -> float:
        return self.__positions[0].axisY + self.dimensions.width

    def zoomIn(self) -> None:
        """
        Decrease the dimensions from the window keeping the central point        
        """
        # Increases the dimension and decrease the position to move the window to both left and right
        self.dimensions.length -= self.__SCALE * self.__BASE_LENGHT
        for position in self.__positions:
            position.axisX += self.__SCALE * self.__BASE_LENGHT // 2

        # Increases the dimension and decrease the position to move the window to both up and down
        self.dimensions.width -= self.__SCALE * self.__BASE_WIDTH
        self.__positions[1].axisY -= self.__SCALE * self.__BASE_WIDTH // 2
        self.__positions[0].axisY += self.__SCALE * self.__BASE_WIDTH // 2

    def zoomOut(self) -> None:
        """
        Increase the dimensions from the window keeping the central point        
        """
        # Increases the dimension and decrease the position to move the window to both left and right
        self.dimensions.length += self.__SCALE * self.__BASE_LENGHT
        for position in self.__positions:
            position.axisX -= self.__SCALE * self.__BASE_LENGHT // 2

        # Increases the dimension and decrease the position to move the window to both up and down
        self.dimensions.width += self.__SCALE * self.__BASE_WIDTH
        self.__positions[1].axisY += self.__SCALE * self.__BASE_WIDTH // 2
        self.__positions[0].axisY -= self.__SCALE * self.__BASE_WIDTH // 2

    def moveUp(self) -> None:
        for position in self.__positions:
            position.axisY += self.ZOOM_MOVE
        self.setCentralPoint(self.dimensions.central_point(self.__positions[0]))
    
    def moveDown(self) -> None:
        for position in self.__positions:
            position.axisY -= self.ZOOM_MOVE
        self.setCentralPoint(self.dimensions.central_point(self.__positions[0]))
    
    def moveLeft(self) -> None:
        for position in self.__positions:
            position.axisX -= self.ZOOM_MOVE
        self.setCentralPoint(self.dimensions.central_point(self.__positions[0]))
        
    def moveRight(self) -> None:
        for position in self.__positions:
            position.axisX += self.ZOOM_MOVE
        self.setCentralPoint(self.dimensions.central_point(self.__positions[0]))


        
    