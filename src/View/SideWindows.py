from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGroupBox, QListWidget, QComboBox, QCheckBox
from Domain.Utils.Transforms import Rotation, Scale, Transform, Translation, GenericTransform
from Domain.Utils.Coordinates import Position3D
from Handlers.WorldHandler import WorldHandler
from Domain.Utils.Constants import Constants
from Domain.Utils.Enums import RotationTypes
from Domain.Shapes.SGIObject import SGIObject
from Domain.Shapes.Point import Point
from View.Button import Button
from typing import List
from Domain.Utils.Enums import CurvePlottingMethods
from Domain.Management.CurvesPlotting import CurvesPlotter

# Returns a function that creates a new window according to the object given
class ObjectWindowFactory:
    def __init__(self, parent: QWidget):
        self.__parent = parent
    
    # TODO: Change to Enum or Object after model is implemented
    def __call__(self, obj: str):
        if obj == "Ponto":
            return self.__createPointWindow()
        elif obj == "Reta":
            return self.__createLineWindow()
        elif obj == "Wireframe":
            return self.__createWireframeWindow()
        elif obj == "Curva":
            return self.__createCurveWindow()
    
    def __rgbHorizontalBoxes(self, layout: QVBoxLayout):
        color_label = QLabel("Cor:")
        layout.addWidget(color_label)
        
        box = QWidget()
        box.setLayout(QHBoxLayout())
        
        r_label = QLabel("R:")
        box.layout().addWidget(r_label)
        
        r_field = QLineEdit()
        r_field.setText("0")
        box.layout().addWidget(r_field)
        
        g_label = QLabel("G:")
        box.layout().addWidget(g_label)
        
        g_field = QLineEdit()
        g_field.setText("0")
        box.layout().addWidget(g_field)
        
        b_label = QLabel("B:")
        box.layout().addWidget(b_label)
        
        b_field = QLineEdit()
        b_field.setText("0")
        box.layout().addWidget(b_field)
        
        box.layout().addStretch()
        layout.addWidget(box)
        
        return r_field, g_field, b_field
    
    def __createPointWindow(self):
        window = QMainWindow(self.__parent)
        window.setWindowTitle("Criar Ponto")
        window.setGeometry(self.__parent.geometry().center().x() - 150, self.__parent.geometry().center().y() - 100, 300, 200)
        
        central_widget = QWidget(window)
        window.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        x_label = QLabel("Coordenada X:")
        layout.addWidget(x_label)
        
        x_field = QLineEdit()
        layout.addWidget(x_field)
        
        y_label = QLabel("Coordenada Y:")
        layout.addWidget(y_label)
        
        y_field = QLineEdit()
        layout.addWidget(y_field)
        
        z_label = QLabel("Coordenada Z:")
        layout.addWidget(z_label)
        
        z_field = QLineEdit()
        z_field.setText("0")
        layout.addWidget(z_field)
        
        name_label = QLabel("Nome do ponto:")
        layout.addWidget(name_label)
        
        name_field = QLineEdit()
        name_field.setText("Ponto")
        layout.addWidget(name_field)
        
        r_field, g_field, b_field = self.__rgbHorizontalBoxes(layout)

        confirm_button = Button("Confirmar", lambda:  (WorldHandler
                                                        .getHandler()
                                                        .objectHandler
                                                        .addPoint(
                                                            Position3D(int(x_field.text()), int(y_field.text()), int(z_field.text())), name_field.text(), 
                                                            (int(r_field.text()), int(g_field.text()), int(b_field.text()))
                                                        ), 
                                window.close(), self.__parent.update()))
        layout.addWidget(confirm_button)
          
        window.show()
        
    def __createLineWindow(self):
        window = QMainWindow(self.__parent)
        window.setWindowTitle("Criar Linha")
        window.setGeometry(self.__parent.geometry().center().x() - 150, self.__parent.geometry().center().y() - 100, 300, 200)
        
        central_widget = QWidget(window)
        window.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # First row
        x1_label = QLabel("Coordenada X1:")
        layout.addWidget(x1_label)
        
        x1_field = QLineEdit()
        layout.addWidget(x1_field)
        
        y1_label = QLabel("Coordenada Y1:")
        layout.addWidget(y1_label)
        
        y1_field = QLineEdit()
        layout.addWidget(y1_field)
        
        z1_label = QLabel("Coordenada Z1:")
        layout.addWidget(z1_label)
        
        z1_field = QLineEdit()
        layout.addWidget(z1_field)
        z1_field.setText("0")
        
        # Second row
        x2_label = QLabel("Coordenada X2:")
        layout.addWidget(x2_label)
        
        x2_field = QLineEdit()
        layout.addWidget(x2_field)
        
        y2_label = QLabel("Coordenada Y2:")
        layout.addWidget(y2_label)
        
        y2_field = QLineEdit()
        layout.addWidget(y2_field)
        
        z2_label = QLabel("Coordenada Z2:")
        layout.addWidget(z2_label)
        
        z2_field = QLineEdit()
        z2_field.setText("0")
        layout.addWidget(z2_field)
        
        # Line name
        name_label = QLabel("Nome da linha:")
        layout.addWidget(name_label)
        
        name_field = QLineEdit()
        name_field.setText("Linha")
        layout.addWidget(name_field)
        r_field, g_field, b_field = self.__rgbHorizontalBoxes(layout)
        
        confirm_button = Button("Confirmar", lambda: (WorldHandler
                    .getHandler()
                    .objectHandler
                    .addLine(
                        Point(int(x1_field.text()), int(y1_field.text()), int(z1_field.text())),
                        Point(int(x2_field.text()), int(y2_field.text()), int(z2_field.text())),
                        name_field.text(),
                        (int(r_field.text()), int(g_field.text()), int(b_field.text()))
                    ),
                window.close(), self.__parent.update()))
        layout.addWidget(confirm_button)
          
        window.show()
    
    def __createWireframeWindow(self):
        def addTempPoint(x, y, z):
            print(f"Adicionou ponto: ({x}, {y}, {z})")
            WorldHandler.getHandler().objectHandler.addTempPointWireframe(Position3D(int(x), int(y), int(z)))
        
        window = QMainWindow(self.__parent)
        window.setWindowTitle("Criar Wireframe")
        window.setGeometry(self.__parent.geometry().center().x() - 150, self.__parent.geometry().center().y() - 100, 300, 200)
        
        central_widget = QWidget(window)
        window.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        x_label = QLabel("Coordenada X:")
        layout.addWidget(x_label)
        
        x_field = QLineEdit()
        layout.addWidget(x_field)
        
        y_label = QLabel("Coordenada Y:")
        layout.addWidget(y_label)
        
        y_field = QLineEdit()
        layout.addWidget(y_field)
        
        z_label = QLabel("Coordenada Z:")
        layout.addWidget(z_label)
        
        z_field = QLineEdit()
        z_field.setText("0")
        layout.addWidget(z_field)
        
        # Wireframe name
        name_label = QLabel("Nome do Wireframe:")
        layout.addWidget(name_label)
        
        name_field = QLineEdit()
        name_field.setText("Wireframe")
        layout.addWidget(name_field)
        
        r_field, g_field, b_field = self.__rgbHorizontalBoxes(layout)
        
        fill_checkbox = QCheckBox("Preencher Wireframe")
        layout.addWidget(fill_checkbox)

        add_button = Button("Adicionar ponto ao wireframe", lambda: (addTempPoint(x_field.text(), y_field.text(), z_field.text()), x_field.clear(), y_field.clear()))
        layout.addWidget(add_button)
        
        confirm_button = Button("Confirmar criação", lambda: (WorldHandler.getHandler().objectHandler.commitWireframeCreation(name_field.text(), 
                                                                                                                              (int(r_field.text()), int(g_field.text()), int(b_field.text())),
                                                                                                                              fill_checkbox.isChecked()), 
                                                                window.close(), 
                                                                self.__parent.update()))
        layout.addWidget(confirm_button)
            
        window.show()
        
    def __createCurveWindow(self):
        def addTempPoint(x, y, z):
            print(f"Adicionou ponto: ({x}, {y}, {z})")
            WorldHandler.getHandler().objectHandler.addTempPointCurve(Position3D(int(x), int(y), int(z)))
        
        window = QMainWindow(self.__parent)
        window.setWindowTitle("Criar Curva")
        window.setGeometry(self.__parent.geometry().center().x() - 150, self.__parent.geometry().center().y() - 100, 300, 200)
        
        central_widget = QWidget(window)
        window.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        x_label = QLabel("Coordenada X:")
        layout.addWidget(x_label)
        
        x_field = QLineEdit()
        layout.addWidget(x_field)
        
        y_label = QLabel("Coordenada Y:")
        layout.addWidget(y_label)
        
        y_field = QLineEdit()
        layout.addWidget(y_field)
        
        z_label = QLabel("Coordenada Z:")
        layout.addWidget(z_label)
        
        z_field = QLineEdit()
        z_field.setText("0")
        layout.addWidget(z_field)
        
        # Curve name
        name_label = QLabel("Nome da curva:")
        layout.addWidget(name_label)
        
        name_field = QLineEdit()
        name_field.setText("Curva")
        layout.addWidget(name_field)
        
        r_field, g_field, b_field = self.__rgbHorizontalBoxes(layout)
        
        # Curve plotting strategy
        strategy_label = QLabel("Tipo de curva:")
        layout.addWidget(strategy_label)
        
        strategy_combo = QComboBox()
        strategy_combo.addItem(CurvePlottingMethods.BEZIER.value)
        strategy_combo.addItem(CurvePlottingMethods.BSPLINE.value)
        layout.addWidget(strategy_combo)

        add_button = Button("Adicionar ponto à curva", lambda: (addTempPoint(x_field.text(), y_field.text(), z_field.text()), x_field.clear(), y_field.clear()))
        layout.addWidget(add_button)
        
        confirm_button = Button("Confirmar criação", lambda: (WorldHandler.getHandler().objectHandler.commitCurveCreation(name_field.text(), 
                                                                                                                              (int(r_field.text()), int(g_field.text()), int(b_field.text())), CurvePlottingMethods.convertFromString(strategy_combo.currentText())),
                                                                window.close(), 
                                                                self.__parent.update()))
        layout.addWidget(confirm_button)
            
        window.show()
        
        
class ObjectTransformWindow(QMainWindow):
    class TransformBox(QGroupBox):
        def __init__(self, parent: QWidget, name: str, transform_callback: callable = lambda: None):
            super().__init__(parent)
            self.__parent = parent
            self.__transform_callback = transform_callback
            
            self.setTitle(name)
            self.setGeometry(0, 0, 180, 150)
            
            self.__layout = QHBoxLayout(self)
            
            if name == "Rotação":
                self.__addFieldsAngle()
            else:
                self.__addFieldsXYZ()
            
        def __addFieldsXYZ(self):
            x_label = QLabel("X:")
            self.__layout.addWidget(x_label)

            x_field = QLineEdit()
            self.__layout.addWidget(x_field)

            y_label = QLabel("Y:")
            self.__layout.addWidget(y_label)

            y_field = QLineEdit()
            self.__layout.addWidget(y_field)

            z_label = QLabel("Z:")
            self.__layout.addWidget(z_label)

            z_field = QLineEdit()
            z_field.setText("1")
            self.__layout.addWidget(z_field)

            add_button = Button("Adicionar", lambda: (self.__transform_callback(x_field.text(), y_field.text(), z_field.text())))
            self.__layout.addWidget(add_button)
            
        def __addFieldsAngle(self):
            angle_label = QLabel("Ângulo (graus):")
            self.__layout.addWidget(angle_label)
            
            angle_field = QLineEdit()
            self.__layout.addWidget(angle_field)
            
            # Dropdown for selecting the transformation type
            rotation_type_label = QLabel("Tipo de Rotação:")
            self.__layout.addWidget(rotation_type_label)

            rotation_type_dropdown = QComboBox()
            
            for rotation_type in RotationTypes:
                rotation_type_dropdown.addItem(rotation_type.value)
            
            self.__layout.addWidget(rotation_type_dropdown)
            
            rotation_axis_label = QLabel("Eixo de Rotação:")
            self.__layout.addWidget(rotation_axis_label)
            
            rotation_axis_dropdown = QComboBox()
            rotation_axis_dropdown.addItem("X")
            rotation_axis_dropdown.addItem("Y")
            rotation_axis_dropdown.addItem("Z")
            rotation_axis_dropdown.setCurrentIndex(2)
            self.__layout.addWidget(rotation_axis_dropdown)
            
            add_button = Button("Adicionar", lambda: (self.__transform_callback(angle_field.text(), rotation_type_dropdown.currentText(), rotation_axis_dropdown.currentText())))
            self.__layout.addWidget(add_button)
    
    class RotationSpecificPointInputBox(QMainWindow):
        def __init__(self, parent: QWidget, name: str, angle: float, axis: str, transform_callback: callable = lambda: None):
            super().__init__(parent)
            self.__parent = parent
            self.__angle = angle
            self.__transform_callback = transform_callback
            self.__axis = axis
            
            self.setWindowTitle(name)
            self.setGeometry(parent.geometry().center().x() - 90, parent.geometry().center().y() - 75, 180, 150)
            
            self.__central_widget = QWidget(self)
            self.setCentralWidget(self.__central_widget)
            self.__central_widget.setLayout(QHBoxLayout())
            
            
            
            self.__layout = self.__central_widget.layout()
            
            self.__addFieldsXYZ()
            
        def __addFieldsXYZ(self):
            x_label = QLabel("X:")
            self.__layout.addWidget(x_label)

            x_field = QLineEdit()
            self.__layout.addWidget(x_field)

            y_label = QLabel("Y:")
            self.__layout.addWidget(y_label)

            y_field = QLineEdit()
            self.__layout.addWidget(y_field)

            z_label = QLabel("Z:")
            self.__layout.addWidget(z_label)

            z_field = QLineEdit()
            z_field.setText("1")
            self.__layout.addWidget(z_field)

            add_button = Button("Utilizar ponto", lambda: (self.__transform_callback(self.__angle, 
                                                            Position3D(
                                                                int(x_field.text()), 
                                                                int(y_field.text()), 
                                                                int(z_field.text())
                                                                )
                                                            ), self.close()))
            self.__layout.addWidget(add_button)
    
    def __init__(self, parent: QWidget, obj: SGIObject):
        super().__init__(parent)
        self.__obj = obj
        self.__transforms: List[Transform] = []
        self.__parent = parent
        
        self.setWindowTitle(f"Transformar {self.__obj.name} ({self.__obj.type.name.lower()})")
        
        self.setGeometry(parent.geometry().center().x() - 150, parent.geometry().center().y() - 100, Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2)
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        central_widget.setLayout(QHBoxLayout())
        
        # Create the QGroupBox with vertical layout
        group_box = QGroupBox(central_widget)
        group_box_layout = QVBoxLayout()
        group_box.setLayout(group_box_layout)
        central_widget.layout().addWidget(group_box)
        
        group_box_layout.addWidget(self.TransformBox(central_widget, "Translação", self.__translation_callback))
        group_box_layout.addWidget(self.TransformBox(central_widget, "Escalonamento", self.__scale_callback))
        group_box_layout.addWidget(self.TransformBox(central_widget, "Rotação", self.__rotation_callback))
        
        # Create the QListWidget and Confirm Button
        list_and_confirm_widget = QWidget(central_widget)
        list_and_confirm_widget.setLayout(QVBoxLayout())
        
        self.__list_widget = QListWidget(list_and_confirm_widget)
        list_and_confirm_widget.layout().addWidget(self.__list_widget)
        
        confirm_button = Button("Confirmar", lambda: (self.__confirmTransformations()))
        list_and_confirm_widget.layout().addWidget(confirm_button)
        
        central_widget.layout().addWidget(list_and_confirm_widget)
        
        self.show()

    def __confirmTransformations(self):
        transform = GenericTransform(positions=self.__obj.getPositions())
        transform.add_transforms(self.__transforms)
        
        final_positions = transform.execute()
                  
        print(f"Final matrix for {[transform.getName() for transform in self.__transforms]}: {transform.matrix()}")    

        self.__obj.setPositions(final_positions)

        self.close()

        self.__parent.update()

    def __translation_callback(self, x: str, y: str, z: str) -> None:
        transform = Translation(float(x), float(y), float(z), self.__obj.getPositions())

        self.__transforms.append(transform)
        self.__update_transform_list()

    def __rotation_callback(self, angle: str, type_str: str, axis: str) -> None:
        transform = GenericTransform(name="Rotation")

        typeEnum = RotationTypes.convertFromString(type_str)

        if (typeEnum == RotationTypes.CENTER_OBJECT):
            translate_to_origin = Translation(-self.__obj.centralPoint.axisX, -self.__obj.centralPoint.axisY, -self.__obj.centralPoint.axisZ)
            rotation = Rotation(float(angle), type, self.__obj.getPositions(), axis)
            translate_back = Translation(self.__obj.centralPoint.axisX, self.__obj.centralPoint.axisY, self.__obj.centralPoint.axisZ)

            transform.add_transforms([translate_to_origin, rotation, translate_back])
        
        elif (typeEnum == RotationTypes.CENTER_WORLD):
            rotation = Rotation(float(angle), type_str, self.__obj.getPositions(), axis)
            transform.add_transforms([rotation])

        elif (typeEnum == RotationTypes.POINT):
            self.__rotation_point_input_box = self.RotationSpecificPointInputBox(self, "Ponto arbitrário", angle, axis, self.__rotation_specific_point_callback)
            self.__rotation_point_input_box.show()
            return

        self.__transforms.append(transform)
        self.__update_transform_list()

    def __rotation_specific_point_callback(self, angle: str, specific_point: Position3D, axis: str) -> None:
        """
        Callback to be used when user is adding a rotation transform but a point was required to be inserted
        """
        movementAxisX = specific_point.axisX - self.__obj.centralPoint.axisX 
        movementAxisY = specific_point.axisY - self.__obj.centralPoint.axisY 
        movementAxisZ = specific_point.axisZ - self.__obj.centralPoint.axisZ 

        translate_to_origin = Translation(movementAxisX, movementAxisY, movementAxisZ)

        rotation = Rotation(float(angle), RotationTypes.POINT.value, self.__obj.getPositions(), axis)

        translate_back = Translation(-movementAxisX, -movementAxisY, -movementAxisZ)
        
        self.__transforms.extend([translate_to_origin, rotation, translate_back])
        self.__update_transform_list()

    def __scale_callback(self, x: str, y: str, z: str) -> None:
        total_transform = GenericTransform(positions=self.__obj.getPositions(), name="Scale")
        
        translate_to_origin = Translation(-self.__obj.centralPoint.axisX, -self.__obj.centralPoint.axisY, -self.__obj.centralPoint.axisZ)
        scale_transform = Scale(float(x), float(y), float(z))
        translate_back = Translation(self.__obj.centralPoint.axisX, self.__obj.centralPoint.axisY, self.__obj.centralPoint.axisZ)
        
        total_transform.add_transforms([translate_to_origin, scale_transform, translate_back])

        self.__transforms.append(total_transform)
        self.__update_transform_list()

    def __update_transform_list(self):
        self.__list_widget.clear()
        for transform in self.__transforms:
            self.__list_widget.addItem(str(transform.getName()))