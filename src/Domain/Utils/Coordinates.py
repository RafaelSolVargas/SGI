class Dimensions3D:
    def __init__(self, lenght: int, width: int, height: int) -> None:
        self.__height = height
        self.__width = width
        self.__lenght = lenght

    @property
    def lenght(self) -> int:
        return self.__lenght
    
    @lenght.setter
    def lenght(self, value) -> None:
        self.__lenght = value

    @property
    def width(self) -> int:
        return self.__width
    
    @width.setter
    def width(self, value) -> None:
        self.__width = value

    @property
    def height(self) -> int:
        return self.__height
    
    @height.setter
    def height(self, value) -> None:
        self.__height = value

    def central_point(self) -> 'Dimensions3D':
        half_length = self.__length / 2
        half_width = self.__width / 2
        half_height = self.__height / 2
    
        return Dimensions3D(half_length, half_width, half_height)
    

class Position3D:
    __MOVE_LENGHT = 1
    def __init__(self, axisX: int, axisY: int, axisZ: int) -> None:
        self.__axisX = axisX
        self.__axisY = axisY
        self.__axisZ = axisZ

    @property
    def axisX(self) -> int:
        return self.__axisX
    
    @axisX.setter
    def axisX(self, value) -> None:
        self.__axisX = value

    def moveLeft(self, value = __MOVE_LENGHT) -> None:
        self.__axisX -= value

    def moveRight(self, value = __MOVE_LENGHT) -> None:
        self.__axisX += value

    @property
    def axisY(self) -> int:
        return self.__axisY
    
    @axisY.setter
    def axisY(self, value) -> None:
        self.__axisY = value

    def moveUp(self, value = __MOVE_LENGHT) -> None:
        self.__axisY -= value

    def moveDown(self, value = __MOVE_LENGHT) -> None:
        self.__axisY += value

    @property
    def axisZ(self) -> int:
        return self.__axisZ
    
    @axisZ.setter
    def axisZ(self, value) -> None:
        self.__axisZ = value

    def moveFront(self, value = __MOVE_LENGHT) -> None:
        self.__axisZ -= value

    def moveBack(self, value = __MOVE_LENGHT) -> None:
        self.__axisZ += value