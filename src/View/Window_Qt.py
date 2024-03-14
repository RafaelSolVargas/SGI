from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget
from View.Button import Button

class Window_Qt(QWidget):
    def __init__(self, w: int = 1280, h: int = 720):
        super().__init__()
        self.__widgets = {}
        self.__initUI(w, h)
        
    def __initUI(self, w: int, h: int):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2
        self.setGeometry(x, y, w, h)
        self.setWindowTitle("MySGI")
        
        button = Button("Quit", self, self.close)
        button.move(50, 50)
        
        self.show()
        
    def loadCallbacks(self, callbacks: dict):
        pass