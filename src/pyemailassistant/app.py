''' Main script used as app entry point '''

import sys
import os
from pyemailassistant.config import init_config
from pyemailassistant.logger import init_logger
from pyemailassistant.gui.main_window import init_main_window
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QScreen

def run():
    config = init_config()
    logger = init_logger(config["LOGGER"])
    app = QApplication(sys.argv)
    main_window = init_main_window(config["MAIN_WINDOW"], logger)
    
    screen = QScreen.availableGeometry(QApplication.primaryScreen())
    main_window.center(screen)
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    run()
