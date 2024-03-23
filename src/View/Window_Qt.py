from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget, QMainWindow, QVBoxLayout, QGroupBox, QListWidget, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt, QRect
from Domain.Utils.Coordinates import Position3D
from View.Button import Button
from View.Console import Console
from View.ArrowButtonWidget import ArrowButtonWidget
from View.Painter import Canvas
from View.SideWindows import ObjectWindowFactory, ObjectTransformWindow
from Domain.Utils.Constants import Constants
from Handlers.WorldHandler import WorldHandler

class Window_Qt(QMainWindow):
    def __init__(self, w: int = 1280, h: int = 720):
        super().__init__()
        self._object_list_widget = None
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
    
    def update(self):
        print("Updating")
        
        obj_list = WorldHandler.getHandler().objectHandler.getObjectsViewport()
        
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
        
        window_control_box = QGroupBox()
        window_control_box.setStyleSheet("border: transparent;")
        window_control_box.setGeometry(0, 0, 180, 100)
        window_control_box.setLayout(QHBoxLayout())
        
        window_box.layout().addWidget(window_control_box)
        
        arrows = ArrowButtonWidget(self.update, "Mover", window_control_box)
        arrows.setGeometry(0, 10, 100, 100)
        
        zoom_window_box = QGroupBox(window_control_box)
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
        
    def __openTransformWindow(self, obj_list_widget: QListWidget) -> None:
        field = obj_list_widget.currentItem()
        
        if not field:
            print("Nenhum objeto selecionado")
            return
        
        obj_name = field.text().split(" ")[0]
        
        obj = WorldHandler.getHandler().objectHandler.getObjectByName(obj_name)
        
        if not obj:
            print(f"Objeto {obj_name} não encontrado")
            return
        
        ObjectTransformWindow(self, obj)
        