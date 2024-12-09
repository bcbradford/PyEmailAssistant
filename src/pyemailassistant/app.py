''' Main script used as app entry point '''

import sys
import os
import warnings
from pyemailassistant.errors import AppLoadError
from pyemailassistant.config import init_config
from pyemailassistant.logger import init_logger
from pyemailassistant.gui.main_window import init_main_window
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QScreen

def run():
    warnings.filterwarnings("ignore", category=UserWarning)

    config = init_config()
    logger = init_logger(config["LOGGER"], config["DEBUG"])
    app = QApplication(sys.argv)
    
    try: main_window = init_main_window(app, config, logger)
    except AppLoadError as e:
        print(e.to_string())
        return

    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run()
