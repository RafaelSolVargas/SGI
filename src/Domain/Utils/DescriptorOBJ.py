from Domain.Shapes.SGIObject import SGIObject
from Domain.Shapes.Wireframe import WireFrame
from Domain.Shapes.Point import Point
from Domain.Utils.Enums import ObjectsTypes

class DescriptorOBJ:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def readOBJFile(file_path) -> WireFrame:
        if file_path[-4:] != ".obj":
            file_path += ".obj"
        
        file = open(file_path, "r")
        lines = file.readlines()
        name = ""
        positions: list[Point] = []
        
        # Do nothing for now, will use later when 3D is needed
        faces = []
        
        i_points = 0
        
        for line in lines:
            if line[0] == "g":
                name = ' '.join(line.split()[1:])
            elif line[0] in ["v", "vt", "vn", "vp"]:
                _, x, y, z = line.split()
                positions.append(Point(float(x), float(y), float(z), f"{name}_{i_points}"))
                i_points += 1
            elif line[0] == "f":
                faces.append([int(x) for x in line.split()[1::]])
            elif line[0] == "a":
                break
            
        return WireFrame(name, positions)
    
    @staticmethod
    def writeOBJFile(obj: SGIObject) -> None:
        with open(f"tests/{obj.name}.obj", "w") as file:
            file.write(f"g {obj.name}\n")
            file.write("\n")
            
            for pos in obj.getPositions():
                file.write(f"v {pos.axisX} {pos.axisY} {pos.axisZ}\n")
                