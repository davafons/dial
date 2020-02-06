# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
"""

from PySide2.QtCore import Qt
from PySide2.QtGui import QContextMenuEvent
from PySide2.QtWidgets import QAbstractItemView, QHeaderView, QMenu, QTableView


class ModelTableView(QTableView):
    """
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # How are headers going to stretch and resize?
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)

        # Columns can be rearranged in any order
        self.horizontalHeader().setSectionsMovable(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Is a context menu going to be called on right click?
        self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeader().customContextMenuRequested.connect(
            self.__show_header_context_menu
        )

        # Model cccepts drops
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

        # Model can be dragged
        self.setDragEnabled(True)

        self.__header_context_menu = None

    def setModel(self, model):
        # Assign model to view by calling the parent method
        super().setModel(model)

        # Additional: Create a context menu for showing/hiding the table headers
        # (columns)
        self.__header_context_menu = QMenu(self)
        header = self.horizontalHeader()

        # Iterate through each column
        for i in range(header.count()):
            column_label = model.headerData(
                section=i, orientation=Qt.Horizontal, role=Qt.DisplayRole
            )

            # Add a checkable action corresponding to each column
            action = self.__header_context_menu.addAction(column_label)
            action.setCheckable(True)
            action.setChecked(True)

            # Each action will show/hide the corresponding column referenced by its
            # index depending on if the action is checked or not (toggled)
            action.toggled.connect(
                lambda toggled, index=i: header.showSection(index)
                if toggled
                else header.hideSection(index)
            )

    def contextMenuEvent(self, event: QContextMenuEvent):
        menu = QMenu(self)

        menu.popup(event.globalPos())
        menu.addAction("Remove layer", lambda: self.deleteSelectedRows())

    def deleteSelectedRows(self):
        # When a row is deleted, the new row index is the last row index - 1
        # That's why we have an i variable on this loop, which represents the amount of
        # rows that have been deleted
        for i, row_index in enumerate(self.selectedIndexes()):
            self.model().removeRow(row_index.row() - i, row_index)

    def __show_header_context_menu(self, point):
        """
        Show a context menu for the horizontal header.
        """
        if not self.__header_context_menu:
            return

        self.__header_context_menu.popup(self.horizontalHeader().mapToGlobal(point))
