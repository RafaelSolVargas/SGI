from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Utils.Enums import ObjectsTypes
from Domain.Utils.Constants import Constants
from Domain.Utils.Transforms import Translation, Scale, GenericTransform
import numpy as np

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
        dimensions = Dimensions3D(lenght, width, height)
        
        self.__angle = {
            "X": 0,
            "Y": 0,
            "Z": 0
        }
        
        # Bottom left, top left, top right, bottom right
        self.__positions = [Position3D(-Constants.VIEWPORT_LENGTH / 2, -Constants.VIEWPORT_WIDTH / 2, 1), Position3D(-Constants.VIEWPORT_LENGTH / 2, Constants.VIEWPORT_WIDTH / 2, 1), Position3D(Constants.VIEWPORT_LENGTH / 2, Constants.VIEWPORT_WIDTH / 2, 1), Position3D(Constants.VIEWPORT_LENGTH / 2, -Constants.VIEWPORT_WIDTH / 2, 1)]

        super().__init__(ObjectsTypes.WINDOW, "Window", dimensions, self.__positions[0])
    
    @property
    def angles(self) -> dict[str, float]:
        return self.__angle
    
    @property
    def angleZ(self) -> float:
        return self.__angle["Z"]
    
    @property
    def angleY(self) -> float:
        return self.__angle["Y"]

    @property
    def angleX(self) -> float:
        return self.__angle["X"]
    
    def setAngle(self, angle: float, axis: str) -> None:
        self.__angle[axis] = angle
    
    def getPositions(self) -> list[Position3D]:
        return self.__positions
    
    def setPositions(self, positions: list[Position3D]) -> None:
        self.__positions = positions

    @property
    def centralPoint(self) -> Position3D:
        bottomLeft = self.__positions[0]
        topRight = self.__positions[2]
        
        half_length = (topRight.axisX - bottomLeft.axisX) / 2 + bottomLeft.axisX
        half_width = (topRight.axisY - bottomLeft.axisY) / 2 + bottomLeft.axisY
        half_height = (topRight.axisZ - bottomLeft.axisZ) / 2 + bottomLeft.axisZ
        
        return Position3D(half_length, half_width, half_height)
    
    def printPositions(self):
        print('Posições Window:')
        print('LB: ', self.__positions[0])
        print('LT: ', self.__positions[1])
        print('RT: ', self.__positions[2])
        print('RB: ', self.__positions[3])

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
        centralPoint = self.centralPoint
        
        translate = Translation(-centralPoint.axisX, -centralPoint.axisY, -centralPoint.axisZ)
        scale = Scale(1 - self.__SCALE, 1 - self.__SCALE, 1)
        translate_back = Translation(centralPoint.axisX, centralPoint.axisY, centralPoint.axisZ)
        
        final_transform = GenericTransform(positions=self.__positions)
        final_transform.add_transforms([translate, scale, translate_back])
        self.__positions = final_transform.execute()
        
        novoPontoCentral = self.centralPoint

        self.dimensions.length = abs(self.__positions[3].axisX - self.__positions[0].axisX)
        self.dimensions.width = abs(self.__positions[1].axisY - self.__positions[0].axisY)

        print(f'ZOOM OUT - Ponto anterior: ({centralPoint.axisX}, {centralPoint.axisY}, {centralPoint.axisZ})')
        print(f'ZOOM OUT - Novo ponto: ({novoPontoCentral.axisX}, {novoPontoCentral.axisY}, {novoPontoCentral.axisZ})')
        
    
    def zoomOut(self) -> None:
        """
        Increase the dimensions from the window keeping the central point        
        """
        centralPoint = self.centralPoint

        translate = Translation(-centralPoint.axisX, -centralPoint.axisY, -centralPoint.axisZ)
        scale = Scale(1 + self.__SCALE, 1 + self.__SCALE, 1)
        translate_back = Translation(centralPoint.axisX, centralPoint.axisY, centralPoint.axisZ)
        
        final_transform = GenericTransform(positions=self.__positions)
        final_transform.add_transforms([translate, scale, translate_back])
        self.__positions = final_transform.execute()

        novoPontoCentral = self.centralPoint

        self.dimensions.length = abs(self.__positions[3].axisX - self.__positions[0].axisX)
        self.dimensions.width = abs(self.__positions[1].axisY - self.__positions[0].axisY)

        print(f'ZOOM OUT - Ponto anterior: ({centralPoint.axisX}, {centralPoint.axisY}, {centralPoint.axisZ})')
        print(f'ZOOM OUT - Novo ponto: ({novoPontoCentral.axisX}, {novoPontoCentral.axisY}, {novoPontoCentral.axisZ})')

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
    