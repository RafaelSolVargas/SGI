from abc import ABC, abstractmethod
from Domain.Management.Window import Window
from Domain.Shapes.Line import Line
from Domain.Shapes.SGIObject import SGIObject

class LineClippingStrategy(ABC):
    def __init__(self) -> None:
        pass
            
    @abstractmethod
    def __clip_line(self, line: Line, window: Window) -> Line | None:
        pass
    
    # TODO: define if objs should be a list of SGIObject or Line (conversion here or in the caller?)
    def clip(self, window: Window, objs: list[Line]) -> list[Line]:
        clipped_objs = []
        
        for obj in objs:
            temp = self.__clip_line(obj, window)
            
            if temp is not None:
                clipped_objs.append(temp)
        
        return clipped_objs