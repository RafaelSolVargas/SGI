from PyQt5.QtGui import QWheelEvent, QKeyEvent, QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget, QMainWindow, QVBoxLayout, QGroupBox, QListWidget, QHBoxLayout, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt, QSize
from View.Button import Button
from View.Console import Console
from View.ArrowButtonWidget import ArrowButtonWidget
from View.Painter import Canvas
from View.SideWindows import ObjectWindowFactory, ObjectTransformWindow
from Domain.Utils.Constants import Constants
from Handlers.WorldHandler import WorldHandler
from Domain.Utils.DescriptorOBJ import DescriptorOBJ
import os

class Window_Qt(QMainWindow):
    def __init__(self, w: int = 1280, h: int = 720):
        super().__init__()
        self._object_list_widget = None

        # Get the path to the tests folder
        tests_folder = os.path.join(os.getcwd(), "tests")

        # Iterate over all files in the tests folder
        for file_name in os.listdir(tests_folder):
            # Check if the file is an .obj file
            if file_name.endswith(".obj"):
                # Construct the full path to the .obj file
                obj_file_path = os.path.join(tests_folder, file_name)
                
                # Read the .obj file and add it to the object handler
                wireframe = DescriptorOBJ.readOBJFile(obj_file_path)
                WorldHandler.getHandler().objectHandler.addObject(wireframe)

        self.__objWinFactory = ObjectWindowFactory(self)
        
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2
        self.setGeometry(x, y, w, h)
        self.setWindowTitle("MySGI")
        
        self.__sidebar = QWidget(self)
        self.__sidebar.setGeometry(0, 0, Constants.SIDEBAR_SIZE, Constants.SCREEN_HEIGHT)
        self.__sidebar.setStyleSheet("border: 1px solid black;")
        
        self.__sidebar.setLayout(QVBoxLayout(self.__sidebar))
        
        # TODO: Change to Enum or Object after model is implemented
        self.__addSidebarObjBox("Objetos", ["Ponto", "Reta", "Wireframe"])
        self.__addSidebarWindowBox()
                
        self.__console = Console(self)
        self.__console.setGeometry(Constants.SIDEBAR_SIZE, h - Constants.SIDEBAR_SIZE, w - Constants.SIDEBAR_SIZE, Constants.SIDEBAR_SIZE)
        
        self.__canvas = Canvas(self)
        self.__canvas.setStyleSheet("background-color: white; border: 1px solid black;")

        self.show()
        self.update()

    def wheelEvent(self, a0: QWheelEvent | None) -> None:
        if a0 is not None:
            if a0.angleDelta().y() > 0:
                WorldHandler.getHandler().window.zoomIn()
                print('ZoomIn - Mouse')
            else:
                WorldHandler.getHandler().window.zoomOut()
                print('ZoomOut - Mouse')

            self.update()
        
        return super().wheelEvent(a0)
    
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()

        if key is not None:
            if key == Qt.Key.Key_Up or key == Qt.Key.Key_W:
                WorldHandler.getHandler().window.moveUp()
            elif key == Qt.Key.Key_Down or key == Qt.Key.Key_S:
                WorldHandler.getHandler().window.moveDown()
            elif key == Qt.Key.Key_Left or key == Qt.Key.Key_A:
                WorldHandler.getHandler().window.moveLeft()
            elif key == Qt.Key.Key_Right or key == Qt.Key.Key_D:
                WorldHandler.getHandler().window.moveRight()
            
            self.update()

        super().keyPressEvent(event)

    def update(self):
        print("Updating")

        obj_list = WorldHandler.getHandler().objectHandler.getObjectsTransformedToViewPortAndPPC()

        self.__object_list_widget.clear()
        for obj in obj_list:
            self.__object_list_widget.addItem(f"{obj.name} ({obj.type.name})")
        
        self.__canvas.draw(obj_list)
    
    def __addSidebarWindowBox(self):
        window_box = QLabel("Window")
        window_box.setLayout(QVBoxLayout())
        window_box.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        window_box.setGeometry(0, 0, 180, 200)
        self.__sidebar.layout().addWidget(window_box)
        
        window_zoom_move_box = QGroupBox()
        window_zoom_move_box.setStyleSheet("border: transparent;")
        window_zoom_move_box.setGeometry(0, 0, 180, 100)
        window_zoom_move_box.setLayout(QHBoxLayout())
        
        window_box.layout().addWidget(window_zoom_move_box)
        
        arrows = ArrowButtonWidget(self.update, "Mover", window_zoom_move_box)
        arrows.setGeometry(0, 10, 100, 100)
        
        zoom_window_box = QGroupBox(window_zoom_move_box)
        zoom_window_box.setLayout(QVBoxLayout())
        zoom_window_box.setGeometry(100, 0, 100, 100)
        
        zoom_window_label = QLabel("Zoom")
        zoom_window_label.setAlignment(Qt.AlignCenter)
        zoom_window_box.layout().addWidget(zoom_window_label)
        
        zoom_window_layout = QHBoxLayout()
        zoom_window_layout.addWidget(Button("+", lambda: (WorldHandler.getHandler().window.zoomIn(), self.update())))
        zoom_window_layout.addWidget(Button("-", lambda: (WorldHandler.getHandler().window.zoomOut(), self.update())))
        
        zoom_window_widget = QWidget(zoom_window_box)
        zoom_window_widget.setLayout(zoom_window_layout)
        zoom_window_box.layout().addWidget(zoom_window_widget)
        
        rotate_window_box = QGroupBox(window_box)
        rotate_window_box.setLayout(QVBoxLayout())
        rotate_window_box.setStyleSheet("border: transparent;")
        rotate_window_box.setGeometry(10, 100, 200, 160)
        
        rotate_window_label = QLabel("Rotacionar")
        rotate_window_label.setAlignment(Qt.AlignCenter)
        rotate_window_box.layout().addWidget(rotate_window_label)

        rotation_angle_input = QLineEdit()
        rotation_angle_widget = QWidget(rotate_window_box)
        rotation_angle_layout = QHBoxLayout(rotation_angle_widget)
        rotation_angle_layout.addWidget(rotation_angle_input)
        rotation_angle_layout.addWidget(QLabel("°"))
        rotate_window_box.layout().addWidget(rotation_angle_widget)

        confirm_button = Button("Confirmar", lambda: (self.__rotateWindow(float(rotation_angle_input.text()))))
        rotate_window_box.layout().addWidget(confirm_button)

        # Adding the rotate windows with default value buttons
        rotate_window_left_button = Button("", lambda: (self.__rotateWindow(float(45))))
        rotate_window_left_button.setFixedHeight(35)
        rotate_window_left_button.setFixedWidth(35)
        rotate_window_left_button.setIconSize(QSize(35, 35))
        rotate_window_left_button.setIcon(QIcon("View/Images/rotate_left.png"))
        rotation_angle_widget.layout().addWidget(rotate_window_left_button)

        rotate_window_right_button = Button("", lambda: (self.__rotateWindow(float(-45))))
        rotate_window_right_button.setFixedHeight(35)
        rotate_window_right_button.setFixedWidth(35)
        rotate_window_right_button.setIconSize(QSize(35, 35))
        rotate_window_right_button.setIcon(QIcon("View/Images/rotate_right.png"))
        rotation_angle_widget.layout().addWidget(rotate_window_right_button)
                
    def __addSidebarObjBox(self, title: str, items: list):
        box = QGroupBox(title, self.__sidebar)
        box.setGeometry(0, 0, 180, 150)
        box.setFixedSize(Constants.SIDEBAR_SIZE - 17, 350)
        self.__sidebar.layout().addWidget(box)
        
        layout = QVBoxLayout(box)
        
        for item in items:
            button = Button(item, lambda checked, item=item: self.__objWinFactory(item))
            layout.addWidget(button)

        # Add a box to list the objects drawn
        self.__object_list_widget = QListWidget(box)
        box.layout().addWidget(self.__object_list_widget)
        self.__object_list_widget.setFixedSize(215, 150)

        transform_button = Button("Transformar", lambda: (self.__openTransformWindow(self.__object_list_widget)))
        layout.addWidget(transform_button)
        
        import_button = Button("Importar", lambda: (self.__importDescriptorOBJ()))
        layout.addWidget(import_button)

    def __importDescriptorOBJ(self):
        import_dialog = QFileDialog()
        file_name, _ = import_dialog.getOpenFileName(self, "Importar Arquivo", "", "OBJ Files (*.obj)")

        if file_name:
            wireframe = DescriptorOBJ.readOBJFile(file_name)
            WorldHandler.getHandler().objectHandler.addObject(wireframe)
            self.update()
    
    def __rotateWindow(self, angle: float) -> None:
        WorldHandler.getHandler().rotateWindow(angle)
        self.update()
    
    def __openTransformWindow(self, obj_list_widget: QListWidget) -> None:
        field = obj_list_widget.currentItem()
        
        if not field:
            print("Nenhum objeto selecionado")
            return
        
        obj_names = field.text().split(" ")
        obj_names.pop()
        obj_name = ' '.join(obj_names)

        obj = WorldHandler.getHandler().objectHandler.getObjectByName(obj_name)
        
        if not obj:
            print(f"Objeto {obj_name} não encontrado")
            return
        
        ObjectTransformWindow(self, obj)
        