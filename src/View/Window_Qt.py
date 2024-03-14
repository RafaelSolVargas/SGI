from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget, QMainWindow, QVBoxLayout, QGroupBox, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt
from View.Button import Button
from View.Console import Console
from View.ArrowButtonWidget import ArrowButtonWidget

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
        layout.addWidget(z_field)
        
        # TODO: Add draw function to the callback
        confirm_button = Button("Confirmar", lambda: (print(f"Criou ponto: ({x_field.text()}, {y_field.text()}, {z_field.text()})"), window.close()))
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
        layout.addWidget(z2_field)
        
        # TODO: Add draw function to the callback
        confirm_button = Button("Confirmar", lambda: (print(f"Criou reta: ({x1_field.text()}, {y1_field.text()}, {z1_field.text()}), ({x2_field.text()}, {y2_field.text()}, {z2_field.text()})"), window.close()))
        layout.addWidget(confirm_button)
          
        window.show()
    
    def __createPolygonWindow(self):
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
        layout.addWidget(z_field)
        
        add_button = Button("Adicionar", lambda: (print(f"Adicionou ponto: ({x_field.text()}, {y_field.text()}, {z_field.text()})")))
        layout.addWidget(add_button)
        
        confirm_button = Button("Confirmar", lambda: (print("Confirmou pontos"), window.close()))
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
        self.__sidebar.setGeometry(0, 0, 200, h)
        self.__sidebar.setStyleSheet("border: 1px solid black;")
        
        QVBoxLayout(self.__sidebar)
        
        # TODO: Change to Enum or Object after model is implemented
        self.__addSidebarBox("Objetos", ["Ponto", "Reta", "Polígono"])
        
        self.__addSidebarLabel("Window")
                
        self.__console = Console(self)
        self.__console.setGeometry(200, h - 200, w - 200, 200)
        
        self.__canvas = QLabel(self)
        self.__canvas.setStyleSheet("background-color: white; border: 1px solid black;")
        self.__canvas.setGeometry(200, 0, w - 200, h - 200)
        
        self.__widgets["sidebar"] = self.__sidebar
        self.__widgets["console"] = self.__console
        self.__widgets["canvas"] = self.__canvas
        
        self.show()
        
    def __addSidebarLabel(self, text: str):
        label = QLabel(text)
        label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.__sidebar.layout().addWidget(label)
                
    def __addSidebarBox(self, title: str, items: list):
        box = QGroupBox(title)
        box.setGeometry(10, 60, 180, 150)
        self.__sidebar.layout().addWidget(box)
        
        layout = QVBoxLayout(box)
        
        for item in items:
            button = Button(item, lambda checked, item=item: self.__objWinFactory(item))
            layout.addWidget(button)
        
    def __addButtonToWidget(self, widget: QWidget, text: str, callback):
        button = Button(text, callback)
        widget.layout().addWidget(button)
        return button