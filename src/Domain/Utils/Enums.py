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