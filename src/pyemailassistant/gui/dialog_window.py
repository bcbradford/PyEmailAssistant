''' Module used to display text with a dialog window '''

from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton

class DialogWindow(QDialog):
    def __init__(self, title, text):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(300, 200)

        layout = QVBoxLayout()
        label = QLabel(text)
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        
        layout.addWidget(label)
        layout.addWidget(close_button)
        self.setLayout(layout)

def init_dialog_window(title, text):
    return DialogWindow(title, text)
