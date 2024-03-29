from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from View.Button import Button
from Handlers.WorldHandler import WorldHandler

# TODO: Add a way to pass the callback to the buttons
class ArrowButtonWidget(QWidget):
    def __init__(self, update_function: callable, text: str = "", parent=None):
        super().__init__(parent)

        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)

        # Create buttons
        self.up_button = Button("^", lambda: (WorldHandler.getHandler().window.moveUp(), update_function()))
        self.down_button = Button("v", lambda: (WorldHandler.getHandler().window.moveDown(), update_function()))
        self.left_button = Button("<", lambda: (WorldHandler.getHandler().window.moveLeft(), update_function()))
        self.right_button = Button(">", lambda: (WorldHandler.getHandler().window.moveRight(), update_function()))

        # Set button sizes
        button_width = 25
        button_height = 25
        self.up_button.setFixedSize(button_width, button_height)
        self.down_button.setFixedSize(button_width, button_height)
        self.left_button.setFixedSize(button_width, button_height)
        self.right_button.setFixedSize(button_width, button_height)

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.left_button)
        button_layout.addWidget(self.up_button)
        button_layout.addWidget(self.right_button)

        # Layout for the label and buttons
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(button_layout)
        layout.addWidget(self.down_button, alignment=Qt.AlignCenter)


        self.setLayout(layout)