from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget, QMainWindow, QVBoxLayout, QGroupBox, QMessageBox, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPixmap
from Domain.Utils.Coordinates import Position3D
from View.Button import Button
from View.Console import Console
from View.ArrowButtonWidget import ArrowButtonWidget
from View.Painter import Canvas
from Domain.Shapes.Point import Point
from Domain.Utils.Constants import Constants
from Handlers.WorldHandler import WorldHandler

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
        elif obj == "Polígono":
            return self.__createPolygonWindow()
    
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
        
        # TODO: Add draw function to the callback
        confirm_button = Button("Confirmar", lambda:  (WorldHandler
                                                        .getHandler()
                                                        .objectHandler
                                                        .addPoint(
                                                            Position3D(int(x_field.text()), int(y_field.text()), int(z_field.text()))
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
        
        # TODO: Add draw function to the callback
        confirm_button = Button("Confirmar", lambda: (WorldHandler
                                .getHandler()
                                .objectHandler
                                .addLine(
                                    Point(int(x1_field.text()), int(y1_field.text()), int(z1_field.text())),
                                    Point(int(x2_field.text()), int(y2_field.text()), int(z2_field.text()))
                                ),
                    window.close(), self.__parent.update()))
        layout.addWidget(confirm_button)
          
        window.show()
    
    def __createPolygonWindow(self):
        def addPointCallback(x, y, z):
            print(f"Adicionou ponto: ({x}, {y}, {z})")
            WorldHandler.getHandler().objectHandler.addPoint(Position3D(int(x), int(y), int(z)))
        
        window = QMainWindow(self.__parent)
        window.setWindowTitle("Criar Polígono")
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
        
        add_button = Button("Adicionar", lambda: (addPointCallback(x_field.text(), y_field.text(), z_field.text()), x_field.clear(), y_field.clear()))
        layout.addWidget(add_button)
        
        confirm_button = Button("Confirmar", lambda: (WorldHandler.getHandler().objectHandler.commitPolygon(), window.close(), self.__parent.update()))
        layout.addWidget(confirm_button)
            
        window.show()

class Window_Qt(QMainWindow):
    def __init__(self, w: int = 1280, h: int = 720):
        super().__init__()
        self.__widgets = {}
        self.__objWinFactory = ObjectWindowFactory(self)
        
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2
        self.setGeometry(x, y, w, h)
        self.setWindowTitle("MySGI")
        
        self.__sidebar = QWidget(self)
        self.__sidebar.setGeometry(0, 0, Constants.SIDEBAR_SIZE, Constants.SCREEN_HEIGHT)
        self.__sidebar.setStyleSheet("border: 1px solid black;")
        
        QVBoxLayout(self.__sidebar)
        
        # TODO: Change to Enum or Object after model is implemented
        self.__addSidebarObjBox("Objetos", ["Ponto", "Reta", "Polígono"])
        self.__addSidebarWindowBox()
                
        self.__console = Console(self)
        self.__console.setGeometry(Constants.SIDEBAR_SIZE, h - Constants.SIDEBAR_SIZE, w - Constants.SIDEBAR_SIZE, Constants.SIDEBAR_SIZE)
        
        self.__canvas = Canvas(self)
        self.__canvas.setStyleSheet("background-color: white; border: 1px solid black;")
        
        self.show()
    
    def update(self):
        print("Updating")
        
        obj_list = WorldHandler.getHandler().objectHandler.getObjectsViewport()
        self.__canvas.draw(obj_list)
    
    def __addSidebarWindowBox(self):
        window_box = QLabel("Window")
        window_box.setLayout(QVBoxLayout())
        window_box.setAlignment(Qt.AlignTop | Qt.AlignLeft)
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
        
        """ zoom_box = QGroupBox(window_box)
        zoom_box.setStyleSheet("border: transparent;")
        zoom_box.setGeometry(0, 100, 180, 100)
        zoom_box.setLayout(QHBoxLayout())
        
        zoom_box_label = QLabel("Zoom")
        zoom_box_label.setAlignment(Qt.AlignCenter)
        zoom_box.layout().addWidget(zoom_box_label)
        
        zoom_in_button = Button("+", lambda: print("Zoom in"))
        zoom_out_button = Button("-", lambda: print("Zoom out"))
        
        zoom_in_button.setFixedSize(25, 25)
        zoom_out_button.setFixedSize(25, 25)
        
        zoom_box.layout().addWidget(zoom_in_button)
        zoom_box.layout().addWidget(zoom_out_button) """
        
                
    def __addSidebarObjBox(self, title: str, items: list):
        box = QGroupBox(title)
        box.setGeometry(10, 60, 180, 100)
        self.__sidebar.layout().addWidget(box)
        
        layout = QVBoxLayout(box)
        
        for item in items:
            button = Button(item, lambda checked, item=item: self.__objWinFactory(item))
            layout.addWidget(button)
