from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Utils.Enums import ObjectsTypes


class Window(SGIObject):
    ZOOM_MOVE: int = 1
    MIN_SIZE: int = 50
    MAX_SIZE: int = 600
    """
    The space from the world to be drawn, it should be available to zoom in and zoom out
    and move in all 3 dimensions
    """
    def __init__(self, lenght: int, width: int, height: int) -> None:
        dimensions = Dimensions3D(lenght, width, height)
        position = Position3D(0, 0, 0)

        super().__init__(ObjectsTypes.WINDOW, "Window", dimensions, position)

    def zoomIn(self) -> None:
        """
        Decrease the dimensions from the window keeping the central point        
        """
        # Armazena o ponto central atual
        central_point = self.dimensions.central_point()

        if self.dimensions.width > self.MIN_SIZE:
            self.dimensions.width -= self.ZOOM_MOVE

        if self.dimensions.lenght > self.MIN_SIZE:
            self.dimensions.lenght -= self.ZOOM_MOVE
        
        if self.dimensions.height > self.MIN_SIZE:
            self.dimensions.height -= self.ZOOM_MOVE

        # Reset the central point with the previous
        self.setCentralPoint(central_point)

    def zoomOut(self) -> None:
        """
        Increase the dimensions from the window keeping the central point        
        """
        # Save the current central point
        central_point = self.dimensions.central_point

        if self.dimensions.width < self.MIN_SIZE:
            self.dimensions.width += self.ZOOM_MOVE

        if self.dimensions.lenght < self.MIN_SIZE:
            self.dimensions.lenght += self.ZOOM_MOVE
        
        if self.dimensions.height < self.MIN_SIZE:
            self.dimensions.height += self.ZOOM_MOVE

        # Reset the central point with the previous
        self.setCentralPoint(central_point)