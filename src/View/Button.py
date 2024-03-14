from PyQt5.QtWidgets import QPushButton, QWidget

class Button(QPushButton):
    def __init__(self, text: str, onClick: callable = lambda: None):
        super().__init__(text)
        self.__onClick = onClick
        # Register onClick event
        self.clicked.connect(self.__onClick)
        
        self.setStyleSheet("QPushButton { background-color: #f0f0f0; border: 1px solid #999999; }"
                                 "QPushButton:hover { background-color: #e0e0e0; }"
                                 "QPushButton:pressed { background-color: #d0d0d0; }")
        
    def setOnClick(self, onClick: callable):
        self.__onClick = onClick
        self.clicked.connect(self.__onClick)
    