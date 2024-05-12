import math
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
        self.__positions = [Position3D(-Constants.VIEWPORT_LENGTH / 2, -Constants.VIEWPORT_WIDTH / 2, 1), 
                            Position3D(-Constants.VIEWPORT_LENGTH / 2, Constants.VIEWPORT_WIDTH / 2, 1), 
                            Position3D(Constants.VIEWPORT_LENGTH / 2, Constants.VIEWPORT_WIDTH / 2, 1), 
                            Position3D(Constants.VIEWPORT_LENGTH / 2, -Constants.VIEWPORT_WIDTH / 2, 1)]


        super().__init__(ObjectsTypes.WINDOW, "Window", dimensions, self.__positions[0])
    
    @staticmethod
    def getVPN(positions: list[Position3D]) -> np.ndarray:
        bottomLeft = positions[0]
        topRight = positions[2]
        
        half_length = (topRight.axisX - bottomLeft.axisX) / 2 + bottomLeft.axisX
        half_width = (topRight.axisY - bottomLeft.axisY) / 2 + bottomLeft.axisY
        half_height = (topRight.axisZ - bottomLeft.axisZ) / 2 + bottomLeft.axisZ
        center = np.array([half_length, half_width, half_height, 0])
        
        x = np.add(center, positions[2].homogenous() - positions[1].homogenous())
        y = np.add(center, positions[1].homogenous() - positions[0].homogenous())
        
        x = x / np.linalg.norm(x)
        y = y / np.linalg.norm(y)
        vpn = np.cross(x[:3], y[:3])
        vpn = vpn / np.linalg.norm(vpn)
        
        return vpn
    
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
    
    def getCOP(self) -> Position3D:
        """
        Center of Projection
        """
        vpn = Window.getVPN(self.__positions)

        cop = vpn * -1500
        return Position3D(cop[0], cop[1], cop[2])
    
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
        print("Starting Zoom In")
        self.dimensions.printDimensions()
        [x.printPosition() for x in self.__positions]
        centralPoint = self.centralPoint
        
        translate = Translation(-centralPoint.axisX, -centralPoint.axisY, -centralPoint.axisZ)
        scale = Scale(1 - self.__SCALE, 1 - self.__SCALE, 1 - self.__SCALE)
        translate_back = Translation(centralPoint.axisX, centralPoint.axisY, centralPoint.axisZ)
        
        final_transform = GenericTransform(positions=self.__positions)
        final_transform.add_transforms([translate, scale, translate_back])
        self.__positions = final_transform.execute()
        
        self.dimensions.printDimensions()

        self.recalculateDimensionsWithPositions()

        [x.printPosition() for x in self.__positions]

        self.dimensions.printDimensions()
        

    def recalculateDimensionsWithPositions(self):
        self.dimensions.length = abs(self.distanceBetweenPoints(self.__positions[0], self.__positions[3]))
        self.dimensions.width = abs(self.distanceBetweenPoints(self.__positions[1], self.__positions[0]))
    
    def distanceBetweenPoints(self, point1, point2):
        # Extrai as coordenadas dos pontos
        x1, y1, z1 = point1.axisX, point1.axisY, point1.axisZ
        x2, y2, z2 = point2.axisX, point2.axisY, point2.axisZ
        
        # Calcula a diferença entre as coordenadas em cada dimensão
        diff_x = x2 - x1
        diff_y = y2 - y1
        diff_z = z2 - z1
        
        # Calcula a distância euclidiana
        distance = math.sqrt(diff_x**2 + diff_y**2 + diff_z**2)
        
        return int(distance)

    def zoomOut(self) -> None:
        """
        Increase the dimensions from the window keeping the central point        
        """
        centralPoint = self.centralPoint

        print("Starting Zoom Out")
        [x.printPosition() for x in self.__positions]

        translate = Translation(-centralPoint.axisX, -centralPoint.axisY, -centralPoint.axisZ)
        scale = Scale(1 + self.__SCALE, 1 + self.__SCALE, 1 + self.__SCALE)
        translate_back = Translation(centralPoint.axisX, centralPoint.axisY, centralPoint.axisZ)
        
        final_transform = GenericTransform(positions=self.__positions)
        final_transform.add_transforms([translate, scale, translate_back])
        self.__positions = final_transform.execute()

        self.dimensions.printDimensions()

        self.recalculateDimensionsWithPositions()
        
        [x.printPosition() for x in self.__positions]
        self.dimensions.printDimensions()

    def get_left_vector(self):
        """
        Retorna o vetor de direção que representa a direção para a esquerda da janela,
        considerando a rotação atual.
        """
        # Supondo que self.angleX, self.angleY e self.angleZ representam os ângulos de rotação
        # da janela em torno dos eixos X, Y e Z, respectivamente.
        # Você precisa converter esses ângulos para radianos para usar as funções trigonométricas.
        angle_x_rad = math.radians(self.angleX)
        angle_y_rad = math.radians(self.angleY)
        angle_z_rad = math.radians(self.angleZ)
        
        # Calcula as componentes do vetor de direção
        x_component = -math.cos(angle_y_rad) * math.cos(angle_z_rad)
        y_component = math.sin(angle_z_rad)
        z_component = math.sin(angle_y_rad) * math.cos(angle_z_rad)
        
        return (x_component, y_component, z_component)

    def get_up_vector(self):
        angle_x_rad = math.radians(self.angleX)
        angle_y_rad = math.radians(self.angleY)
        angle_z_rad = math.radians(self.angleZ)
        
        # Calcula as componentes do vetor de direção
        x_component = math.sin(angle_y_rad) * math.cos(angle_z_rad)
        y_component = math.cos(angle_x_rad) * math.cos(angle_z_rad) * math.cos(angle_y_rad) - math.sin(angle_x_rad) * math.sin(angle_z_rad)
        z_component = math.cos(angle_x_rad) * math.sin(angle_z_rad) * math.cos(angle_y_rad) + math.sin(angle_x_rad) * math.cos(angle_z_rad)
        
        return (x_component, y_component, z_component)

    def moveUp(self) -> None:
        up_vector = self.get_up_vector()
        for position in self.__positions:
            position.axisX += int(self.ZOOM_MOVE * up_vector[0])
            position.axisY += int(self.ZOOM_MOVE * up_vector[1])
            position.axisZ += int(self.ZOOM_MOVE * up_vector[2])
        self.setCentralPoint(self.dimensions.central_point(self.__positions[0]))
        self.printPositions()
        self.dimensions.printDimensions()

    def moveDown(self) -> None:
        up_vector = self.get_up_vector()
        for position in self.__positions:
            position.axisX -= int(self.ZOOM_MOVE * up_vector[0])
            position.axisY -= int(self.ZOOM_MOVE * up_vector[1])
            position.axisZ -= int(self.ZOOM_MOVE * up_vector[2])
        self.setCentralPoint(self.dimensions.central_point(self.__positions[0]))
        self.printPositions()
        self.dimensions.printDimensions()
    
    def moveLeft(self) -> None:
        left_vector = self.get_left_vector()
        for position in self.__positions:
            position.axisX += int(self.ZOOM_MOVE * left_vector[0])
            position.axisY += int(self.ZOOM_MOVE * left_vector[1])
            position.axisZ += int(self.ZOOM_MOVE * left_vector[2])
        self.setCentralPoint(self.dimensions.central_point(self.__positions[0]))
        self.printPositions()
        self.dimensions.printDimensions()
        
    def moveRight(self) -> None:
        left_vector = self.get_left_vector()
        for position in self.__positions:
            position.axisX -= int(self.ZOOM_MOVE * left_vector[0])
            position.axisY -= int(self.ZOOM_MOVE * left_vector[1])
            position.axisZ -= int(self.ZOOM_MOVE * left_vector[2])
        self.setCentralPoint(self.dimensions.central_point(self.__positions[0]))       
        self.printPositions()
        self.dimensions.printDimensions()
