from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from io import StringIO
import sys

class StdoutRedirector(QThread):
    messageWritten = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.output = StringIO()

    def write(self, message):
        self.output.write(message)
        self.messageWritten.emit(message)

    def flush(self):
        sys.stdout.flush()

    def run(self):
        sys.stdout = self
        
class Console(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.stdout_redirector = StdoutRedirector(self)
        self.stdout_redirector.messageWritten.connect(self.append_text)

        sys.stdout = self.stdout_redirector
        self.setStyleSheet("background-color: white; border: 1px solid black;")
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def append_text(self, text):
        cursor = self.text_edit.textCursor()
        cursor.insertText(text)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()