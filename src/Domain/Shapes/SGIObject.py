from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Utils.IdGenerator import IdGenerator

class SGIObject:
    def __init__(self, name: str, dimensions: Dimensions3D, position: Position3D) -> None:
        self.__id = IdGenerator.generate_id()
        self.__name = name
        self.__position: Position3D = position
        self.__dimensions: Dimensions3D = dimensions

    @property
    def centralPoint(self) -> Position3D:
        return self.__dimensions.central_point

    def setCentralPoint(self, central_point: Position3D) -> None:
        """ Define o ponto central das dimensões do objeto """
        # Calcula as coordenadas do canto inferior esquerdo com base no ponto central
        new_position = Position3D(
            central_point.axisX - self.dimensions.length / 2,
            central_point.axisY - self.dimensions.width / 2,
            central_point.axisZ - self.dimensions.height / 2
        )

        self.position = new_position        

    @property
    def dimensions(self) -> Dimensions3D:
        return self.__dimensions
    
    @property
    def position(self) -> Position3D:
        return self.__position
    
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def name(self) -> str:
        return self.__name