from typing import List

from Domain.Shapes.SGIObject import SGIObject


class World:
    """
    Should keep all objects in the world
    """
    def __init__(self) -> None:
        self.__objects: List[SGIObject] = []

    def addObject(self, object: SGIObject):
        self.__objects.append(object)

    @property
    def objects(self):
        return self.__objects
    
    def removeObjectById(self, objectId: int):
        for object in self.__objects:
            if object.id == objectId:
                self.__objects.remove(object)

    def getObjectById(self, objectId: int):
        for object in self.__objects:
            if object.id == objectId:
                return object
