from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Utils.Enums import ObjectsTypes


class ViewPort(SGIObject):
    """
    Space to be drawn in the View
    """
    def __init__(self, lenght: int, width: int) -> None:
        dimensions = Dimensions3D(lenght, width, 1)
        position = Position3D(0, 0, 0)    

        super().__init__(ObjectsTypes.VIEWPORT, "ViewPort", dimensions, position)

    @property
    def Xmin(self) -> float:
        return self.position.axisX
    
    @property
    def Xmax(self) -> float:
        return self.position.axisX + self.dimensions.lenght
    
    @property
    def Ymin(self) -> float:
        return self.position.axisY
    
    @property
    def Ymax(self) -> float:
        return self.position.axisY + self.dimensions.width