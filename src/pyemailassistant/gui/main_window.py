import sys
from PyQt6.QtWidgets import QMainWindow, QMenu
from PyQt6.QtGui import QScreen, QAction

class MainWindow(QMainWindow):

    def __init__(self, config: dict, logger: "logger"):
        super().__init__()
        self.config = config
        self.logger = logger
        self._set_properties()
        self._set_size()
        self._create_menubar()

    def _set_properties(self):
        self.setWindowTitle(self.config.get("TITLE", "App"))

    def _set_size(self):
        x = self.config.get("X", 1024)
        y = self.config.get("Y", 768)
        self.resize(x, y)

    def _create_menubar(self):
        menubar = self.menuBar()
        
        # Dictionary: { "Menu_Name": {"Action_Name": (Action, Event, LineSeparator)} }
        menus = {
            "File": { 
                "Open": (QAction("Open", self), self._open, False),
                "Exit": (QAction("Exit", self), self._close, False)
                },
            "Model": {
                "Train": (QAction("Train", self), self._train_model, True)
                },
            "Settings": {
                "Display": (QAction("Display", self), self._show_display_settings, True)
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


    def center(self, screen: "QRect"):
        window = self.frameGeometry()
        window.moveCenter(screen.center())
        self.move(window.topLeft())

    def _open(self):
        print("Open Triggered")

    def _close(self):
        print("Close Triggered")
        self.close()

    def _train_model(self):
        print("Train Model Triggered")

    def _show_display_settings(self):
        print("Show Display Settings Triggered")

def init_main_window(config: dict, logger: "logger") -> MainWindow:
    return MainWindow(config, logger)

