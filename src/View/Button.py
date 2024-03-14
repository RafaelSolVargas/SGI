from PyQt5.QtWidgets import QPushButton, QWidget

class Button(QPushButton):
    def __init__(self, text: str, parent: QWidget, onClick: callable = None):
        super().__init__(text, parent)
        self.__onClick = onClick
        # Register onClick event
        self.clicked.connect(self.__onClick)
        
    def setOnClick(self, onClick: callable):
        self.__onClick = onClick
        self.clicked.connect(self.__onClick)
    