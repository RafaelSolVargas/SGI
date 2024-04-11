from Domain.Shapes.SGIObject import SGIObject
from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Utils.Enums import ObjectsTypes
from Domain.Utils.Constants import Constants
from Domain.Utils.Transforms import Translation, Scale, GenericTransform
from copy import deepcopy

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
        
        self.__angle = 0
        
        # Bottom left, top left, top right, bottom right
        self.__positions = [Position3D(-Constants.VIEWPORT_LENGTH / 2, -Constants.VIEWPORT_WIDTH / 2, 0), Position3D(-Constants.VIEWPORT_LENGTH / 2, Constants.VIEWPORT_WIDTH / 2, 0), Position3D(Constants.VIEWPORT_LENGTH / 2, Constants.VIEWPORT_WIDTH / 2, 0), Position3D(Constants.VIEWPORT_LENGTH / 2, -Constants.VIEWPORT_WIDTH / 2, 0)]

        super().__init__(ObjectsTypes.WINDOW, "Window", dimensions, self.__positions[0])
    
    @property
    def angle(self) -> float:
        return self.__angle
    
    @angle.setter
    def angle(self, value: float) -> None:
        self.__angle = value
    
    def getPositions(self) -> list[Position3D]:
        return self.__positions
    
    def setPositions(self, positions: list[Position3D]) -> None:
        self.__positions = positions
    
    @property
    def centralPoint(self) -> Position3D:
        bottom_left = self.__positions[0]
        top_right = self.__positions[2]
        
        half_length = (top_right.axisX - bottom_left.axisX) / 2 + bottom_left.axisX
        half_width = (top_right.axisY - bottom_left.axisY) / 2 + bottom_left.axisY
        half_height = (top_right.axisZ - bottom_left.axisZ) / 2 + bottom_left.axisZ
        
        #print(f'Center: {half_length}, {half_width}, {half_height}')
        
        return Position3D(half_length, half_width, half_height)
        
    
    def printPositions(self):
        print('Posições Window:')
        print(self.__positions[0])
        print(self.__positions[1])
        print(self.__positions[2])
        print(self.__positions[3])

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
    
    def __centerV_up(self) -> Position3D:
        v_up_middle = Position3D((self.__positions[1].axisX - self.__positions[0].axisX) / 2, 
                     (self.__positions[1].axisY - self.__positions[0].axisY) / 2, 
                     (self.__positions[1].axisZ - self.__positions[0].axisZ) / 2)

        # Walks from the bottom middle left to the central point of the window
        return Position3D(self.__positions[0].axisX + v_up_middle.axisX, 
                  self.__positions[0].axisY + v_up_middle.axisY, 
                  self.__positions[0].axisZ + v_up_middle.axisZ)

    def __getOffsetVertical(self, value: int) -> Position3D:
        # V_up to origin
        v_up = deepcopy(self.__positions)
        print([v_up[0].axisX, v_up[0].axisY], [v_up[1].axisX, v_up[1].axisY])
        translate_v_up = Translation(-v_up[0].axisX, -v_up[0].axisY, 0, v_up)
        v_up = translate_v_up.execute()
        mag = (v_up[1].axisX ** 2 + v_up[1].axisY ** 2) ** 0.5
        
        # New vector with mod == value
        new_v = Position3D(v_up[1].axisX * value / mag, v_up[1].axisY * value / mag, 0)

        return new_v        
        
    
    def zoomIn(self) -> None:
        """
        Decrease the dimensions from the window keeping the central point        
        """
        # Increases the dimension and decrease the position to move the window to both left and right
        self.dimensions.length -= self.__SCALE * self.__BASE_LENGHT
        # Increases the dimension and decrease the position to move the window to both up and down
        self.dimensions.width -= self.__SCALE * self.__BASE_WIDTH

        #center = self.__centerV_up()
        centralPoint = self.centralPoint
        
        translate = Translation(-centralPoint.axisX, -centralPoint.axisY, -centralPoint.axisZ)
        scale = Scale(1 - self.__SCALE, 1 - self.__SCALE, 1)
        translate_back = Translation(centralPoint.axisX, centralPoint.axisY, centralPoint.axisZ)
        
        final_transform = GenericTransform(positions=self.__positions)
        final_transform.add_transforms([translate, scale, translate_back])
        self.__positions = final_transform.execute()
        
        novoPontoCentral = self.centralPoint

        print(f'ZOOM OUT - Ponto anterior: ({centralPoint.axisX}, {centralPoint.axisY}, {centralPoint.axisZ})')
        print(f'ZOOM OUT - Novo ponto: ({novoPontoCentral.axisX}, {novoPontoCentral.axisY}, {novoPontoCentral.axisZ})')
        
    
    def zoomOut(self) -> None:
        """
        Increase the dimensions from the window keeping the central point        
        """
        # Increases the dimension and decrease the position to move the window to both left and right
        self.dimensions.length += self.__SCALE * self.__BASE_LENGHT
        # Increases the dimension and decrease the position to move the window to both up and down
        self.dimensions.width += self.__SCALE * self.__BASE_WIDTH
        
        # Scale positions to keep the central point
        #center = self.__centerV_up()
        
        centralPoint = self.centralPoint

        translate = Translation(-centralPoint.axisX, -centralPoint.axisY, -centralPoint.axisZ)
        scale = Scale(1 + self.__SCALE, 1 + self.__SCALE, 1)
        translate_back = Translation(centralPoint.axisX, centralPoint.axisY, centralPoint.axisZ)
        
        final_transform = GenericTransform(positions=self.__positions)
        final_transform.add_transforms([translate, scale, translate_back])
        self.__positions = final_transform.execute()

        novoPontoCentral = self.centralPoint

        print(f'ZOOM OUT - Ponto anterior: ({centralPoint.axisX}, {centralPoint.axisY}, {centralPoint.axisZ})')
        print(f'ZOOM OUT - Novo ponto: ({novoPontoCentral.axisX}, {novoPontoCentral.axisY}, {novoPontoCentral.axisZ})')

    def moveUp(self) -> None:
        for position in self.__positions:
            position.axisY -= self.ZOOM_MOVE
        self.setCentralPoint(self.dimensions.central_point(self.__positions[0]))
    
    def moveDown(self) -> None:
        for position in self.__positions:
            position.axisY += self.ZOOM_MOVE
        self.setCentralPoint(self.dimensions.central_point(self.__positions[0]))
    
    def moveLeft(self) -> None:
        for position in self.__positions:
            position.axisX += self.ZOOM_MOVE
        self.setCentralPoint(self.dimensions.central_point(self.__positions[0]))
        
    def moveRight(self) -> None:
        for position in self.__positions:
            position.axisX -= self.ZOOM_MOVE
        self.setCentralPoint(self.dimensions.central_point(self.__positions[0]))


        
    