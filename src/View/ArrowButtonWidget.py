from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class ArrowButtonWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        # Create buttons
        self.up_button = QPushButton("^")
        self.down_button = QPushButton("v")
        self.left_button = QPushButton("<")
        self.right_button = QPushButton(">")

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