# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Menu bar for the main window.
"""

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QAction, QMenuBar, QWidget


class MainMenuBar(QMenuBar):
    """
    Top menu bar for the main window.
    """

    open_project = Signal()
    save_project = Signal()
    save_project_as = Signal()
    open_predefined_dataset = Signal()
    quit = Signal()

    toggle_log_window = Signal()

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.__create_actions()
        self.__create_menus()

    def __create_actions(self):
        self._open_project_act = QAction("Open project", self)
        self._open_project_act.triggered.connect(self.open_project)

        self._save_project_act = QAction("Save project", self)
        self._save_project_act.triggered.connect(self.save_project)

        self._save_project_as_act = QAction("Save project as...", self)
        self._save_project_as_act.triggered.connect(self.save_project_as)

        self._open_predefined_dataset_act = QAction("Open predefined dataset...", self)
        self._open_predefined_dataset_act.triggered.connect(
            self.open_predefined_dataset
        )

        self._quit_act = QAction("Quit", self)
        self._quit_act.triggered.connect(self.quit)

        # Show log window act
        self._show_log_act = QAction("Show log", self)
        self._show_log_act.triggered.connect(self.toggle_log_window)

    def __create_menus(self):
        # File menu
        self._file_menu = self.addMenu("&File")
        self._file_menu.addAction(self._open_project_act)
        self._file_menu.addAction(self._save_project_act)
        self._file_menu.addAction(self._save_project_as_act)
        self._file_menu.addSeparator()
        self._file_menu.addAction(self._open_predefined_dataset_act)
        self._file_menu.addSeparator()
        self._file_menu.addAction(self._quit_act)

        # Windows menu
        self._windows_menu = self.addMenu("Windows")
        self._windows_menu.addAction(self._show_log_act)