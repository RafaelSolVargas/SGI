from enum import Enum


class ObjectsTypes(Enum):
    POINT = 0
    LINE = 1
    WIREFRAME = 2
    VIEWPORT = 3
    WINDOW = 4
    
class RotationTypes(Enum):
    CENTER_WORLD = "Centro do mundo"
    CENTER_OBJECT = "Centro do objeto"
    POINT = "Ponto arbitrário"

    @classmethod
    def convertFromString(cls, type_str: str) -> 'RotationTypes':
        for enum_member in cls:
            if enum_member.value == type_str:
                return enum_member
            
        raise ValueError(f"No such enum member with value {type_str}")
    
class ClippingMethods(Enum):
    LIANG = "Liang-Barsky"
    COHEN = "Cohen-Sutherland"

    @classmethod
    def convertFromString(cls, type_str: str) -> 'ClippingMethods':
        for enum_member in cls:
            if enum_member.value == type_str:
                return enum_member
            
        raise ValueError(f"No such enum member with value {type_str}")