from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Coordinates import Dimensions3D, Position3D


class ViewPort(SGIObject):
    """
    Space to be drawn in the View
    """
    def __init__(self, lenght: int, width: int, height: int) -> None:
        dimensions = Dimensions3D(lenght, width, height)
        position = Position3D(0, 0, 0)    

        super().__init__("ViewPort", dimensions, position)
