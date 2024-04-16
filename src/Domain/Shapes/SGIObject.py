from typing import List
from Domain.Utils.Coordinates import Dimensions3D, Position3D
from Domain.Utils.Enums import ObjectsTypes
from Domain.Utils.IdGenerator import IdGenerator

class SGIObject:
    def __init__(self, type: ObjectsTypes, name: str, dimensions: Dimensions3D, position: Position3D, color: tuple[int, int, int] = (0, 0, 0)) -> None:
        self.__id = IdGenerator.generate_id()
        self.__name = name 
        self.__position: Position3D = position
        self.__dimensions: Dimensions3D = dimensions
        self.__type = type
        self.__color = color

    def __str__(self) -> str:
        return f"{self.name} ({self.type.name}) -> {self.position}"
    
    @property
    def color(self) -> tuple[int, int, int]:
        return self.__color
    
    def setColor(self, color: tuple[int, int, int]) -> None:
        self.__color = color
    
    @property
    def type(self) -> ObjectsTypes:
        return self.__type
    
    def getPositions(self) -> List[Position3D]:
        return [self.__position]
    
    def setPositions(self, positions: List[Position3D]) -> None:
        self.__position = positions[0]

    @property
    def centralPoint(self) -> Position3D:
        return self.__dimensions.central_point(self.__position)

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
    
    @position.setter
    def position(self, value: Position3D) -> None:
        self.__position = value
    
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def name(self) -> str:
        return self.__name