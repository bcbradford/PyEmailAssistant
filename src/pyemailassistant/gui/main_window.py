import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QMenu, QPushButton, QWidget, QSizePolicy
from PyQt6.QtWidgets import QRadioButton, QLineEdit, QLabel, QTextEdit
from PyQt6.QtGui import QScreen, QAction

class MainWindow(QMainWindow):

    def __init__(self, config: dict, logger: "logger"):
        super().__init__()
        self._window_config = config["MAIN_WINDOW"]
        self._model_config = config["MODEL"]
        self._logger = logger

        self._init_window()

    def _init_window(self):
        self.setWindowTitle(self._window_config.get("TITLE", "App"))
        self._set_size()
        self._create_menubar()
        self._create_widgets()

    def _set_size(self):
        x = self._window_config.get("X", 1024)
        y = self._window_config.get("Y", 768)
        self.setFixedSize(x, y)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def _create_menubar(self):
        menubar = self.menuBar()
        
        # Dictionary: { "Menu_Name": {"Action_Name": (Action, Event, LineSeparator)} }
        menus = {
            "File": { 
                "Open": (QAction("Open", self), self._open_clicked, False),
                "Exit": (QAction("Exit", self), self._close_clicked, False)
                },
            "Model": {
                "Train": (QAction("Train", self), self._train_model_clicked, True)
                },
            "Settings": {
                "Display": (QAction("Display", self), self._show_display_settings_clicked, True)
                }
        }

        for menu_name, actions in menus.items():
            self._create_menu(menubar, menu_name, actions)
            

    def _create_menu(self, menubar, menu_name: str, actions: dict):
        # actions: {"Action_Name": (Action, Event, LineSeparator)}
        menu = menubar.addMenu(menu_name)

        for action_name, (action, event, separator) in actions.items():
            menu.addAction(action)
            action.triggered.connect(event)
            if separator: menu.addSeparator()
    
    def _create_widgets(self):
        self._create_submit_button()
        self._create_url_radio_button()
        self._create_subject_textbox()
        self._create_domain_textbox()
        self._create_body_textbox()

    def _create_submit_button(self):
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setGeometry(914, 30, 100, 30)
        self.submit_button.setStyleSheet("font-size: 18px;")
        self.submit_button.clicked.connect(self._submit_clicked)

    def _create_url_radio_button(self):
        self.url_radio = QRadioButton("Email Contains Url", self)
        self.url_radio.setGeometry(704, 35, 200, 20)
        self.url_radio.setStyleSheet("font-size: 18px;")

    def _create_subject_textbox(self):
        self.subject_label = QLabel("Subject:", self)
        self.subject_label.setGeometry(10, 30, 75, 30)
        self.subject_label.setStyleSheet("font-size: 18px;")

        self.subject_textbox = QLineEdit(self)
        self.subject_textbox.setGeometry(90, 30, 250, 30)
        self.subject_textbox.setStyleSheet("font-size: 18px;")

    def _create_domain_textbox(self):
        self.domain_label = QLabel("Domain:", self)
        self.domain_label.setGeometry(350, 30, 75, 30)
        self.domain_label.setStyleSheet("font-size: 18px;")

        self.domain_textbox = QLineEdit(self)
        self.domain_textbox.setGeometry(430, 30, 250, 30)
        self.domain_textbox.setStyleSheet("font-size: 18px;")

    def _create_body_textbox(self):
        self.body_label = QLabel("Body:", self)
        self.body_label.setGeometry(10, 70, 75, 30)
        self.body_label.setStyleSheet("font-size: 18px;")

        self.body_textbox = QTextEdit(self)
        self.body_textbox.setGeometry(90, 70, 924, 688)
        self.body_textbox.setStyleSheet("font-size: 18px;")

    def _open_clicked(self):
        self._logger.info("Open Triggered")

    def _close_clicked(self):
        self._logger.info("Close Triggered")
        self.close()

    def _train_model_clicked(self):
        self._logger.info("Train Model Triggered")

    def _show_display_settings_clicked(self):
        self._logger.info("Show Display Settings Triggered")

    def _submit_clicked(self):
        print("Submit Clicked")
        print(f"Subject: {self.subject_textbox.text()}")
        print(f"Domain: {self.domain_textbox.text()}")
        print(f"Body: {self.body_textbox.toPlainText()}")
        if self.url_radio.isChecked():
            print("URL Radio Button Checked.")
        self.subject_textbox.clear()
        self.domain_textbox.clear()
        self.body_textbox.clear()

def init_main_window(app: "QApplication", config: dict, logger: "logger") -> MainWindow:
    logger.info("Creating Main Window")
    window = MainWindow(config, logger)
    
    # center window
    screen = QScreen.availableGeometry(app.primaryScreen())
    screen_center = screen.center()
    window_frame = window.frameGeometry()
    window_frame.moveCenter(screen_center)

    window.move(window_frame.topLeft())

    logger.info("Main Window Created")
    return window

