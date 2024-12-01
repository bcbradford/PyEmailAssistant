''' Module containing the main window class '''

import sys
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QMenu, QPushButton, QWidget, QSizePolicy
from PyQt6.QtWidgets import QRadioButton, QLineEdit, QLabel, QTextEdit
from PyQt6.QtGui import QScreen, QAction

from .dialog_window import init_dialog_window
from pyemailassistant.errors import *
from pyemailassistant.models import init_model


class MainWindow(QMainWindow):

    def __init__(self, config: dict, logger: "logger"):
        super().__init__()
        self._window_config = config["MAIN_WINDOW"]
        self._model_config = config["MODEL"]
        self._logger = logger

        self._init_window()
        self._model = self._load_model(config, logger)

    def _init_window(self):
        self.setWindowTitle(self._window_config.get("TITLE", "App"))
        self._set_size()
        self._create_menubar()
        self._create_widgets()

    def _load_model(self, config, logger):
        try: return init_model(config["MODEL"], logger)
        except AppError as e: self._display_error(e)
        except Exception as e:
            desc = "An unhandled error ocurred while loading the model."
            error = AppError(desc, str(e))
            self._display_error(error)

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
                "Close": (QAction("Close", self), self._close_clicked, False)
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

    def _close_clicked(self):
        self._logger.info("Close Triggered")
        self.close()

    def _submit_clicked(self):
        try: self._validate_inputs()
        except AppError as e: 
            self._display_error(e)
            return

        data = {
            "domain": [self.domain_textbox.text()],
            "subject": [self.subject_textbox.text()],
            "body": [self.body_textbox.toPlainText()],
            "urls": ["1"] if self.url_radio.isChecked() else ["0"]
        }

        df = pd.DataFrame(data)

        try: self._display_model_prediction(df)
        except AppError as e: self._display_error(e)
        except Exception as e:
            desc = "An unhandled exception occured while getting model predictions."
            error = AppError(desc, str(e))
            self._display_error(error)

    def _validate_inputs(self):
        self._logger.info("Validating inputs.")

        if self.subject_textbox.text() == "":
            desc = "The subject can't be empty. Please type unknown if there is no subject."
            raise InputValidationError(desc, "Empty subject field during validation.")

        if self.domain_textbox.text() == "":
            desc = "The domain can't be empty. Please type unkown if there is no domain."
            raise InputValidationError(desc, "Empty domain field during validation.")

        if self.body_textbox.toPlainText() == "":
            desc = "The body can't be empty. Please type unkown if there is no body."
            raise InputValidationError(desc, "Empty body field during validation.")

        self._logger.info("Finished validating inputs.")

    def _display_model_prediction(self, df):
        try:
            y_pred = self._model.predict(df)
            text = ""
            for i, y in enumerate(y_pred): text += self._get_model_result_text(i, y)
            self._display_prediction(text)
        except AppError as e:
            self._display_error(e)

    def _get_model_result_text(self, index, y):
        self._logger.info(f"Getting prediction {index}: {y}")
        text = f"Prediction: {y}\n\n"
        
        if y == 0:
            msg = (
                f"The {self._model.get_model_type()} model classified this email as **not a phishing attempt**.\n\n"
                "However, please note that machine learning models can make mistakes. To stay safe:\n"
                "- Avoid clicking on any links or downloading attachments unless you're certain of the sender.\n"
                "- If you're unsure, contact the sender (e.g., your financial institution or the business)\n"
                "using their official website or phone number to verify the email.\n\n"
            )
        else:
            msg = (
                f"The {self._model.get_model_type()} model classified this email as a **phishing attempt**.\n\n"
                "We strongly recommend:\n"
                "- Avoid clicking any links or downloading attachments in this email.\n"
                "- Delete the email immediately if it seems suspicious.\n"
                "- Report it to your email provider or the appropriate authority.\n\n"
            )

        self._logger.info("Finished getting prediction text.")
        return text + msg

    def _display_error(self, error):
        self._logger.error(error.get_logger_output())
        error_dialog = init_dialog_window("Error", error.to_string())
        error_dialog.exec()

    def _display_prediction(self, text):
        prediction_dialog = init_dialog_window("Prediction Result", text)
        prediction_dialog.exec()

def init_main_window(app: "QApplication", config: dict, logger: "logger") -> MainWindow:
    
    try:
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
    except Exception as e:
        desc = "An error ocurred while loading the main window."
        error = AppLoadError(desc, str(e))
        logger.error(str(e))
        raise error
