# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QAbstractTableModel, QModelIndex, QSize, Qt
from PySide2.QtGui import QPixmapCache

from dial.datasets import Dataset
from dial.misc import Dial
from dial.utils import log

LOGGER = log.get_logger(__name__)


class DatasetTableModel(QAbstractTableModel):
    """
    Model representing the rows/columns of a dataset.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__x = []
        self.__y = []
        self.__x_type = None
        self.__y_type = None

        self.__dataset = None

        self.__max_row_count = 100

        self.column_names = ("Input", "Output")

        self.__images_size = QSize(75, 75)

        self.__role_map = {
            Qt.DisplayRole: self.__display_role,
            Dial.TypeRole.value: self.__data_type_role,
        }

    def load_dataset(self, dataset: Dataset):
        """
        Load new Dataset data to the model.
        """

        LOGGER.debug("Loading new dataset to DatasetTableModel...")

        self.__dataset = dataset

        self.__x = []
        self.__y = []
        self.__x_type = dataset.x_type
        self.__y_type = dataset.y_type

        QPixmapCache.clear()

        # Model has been reset, redraw view
        self.modelReset.emit()

    def rowCount(self, parent=QModelIndex()):
        """
        Return the number of rows.
        """
        return len(self.__x)

    def columnCount(self, parent=QModelIndex()):
        """
        Return the number of columns.
        """
        return len(self.column_names)

    def headerData(self, section, orientation, role):
        """
        Return the name of the headers
        """

        if role != Qt.DisplayRole:
            return None

        # Column header must have their respective names
        if orientation == Qt.Horizontal:
            return self.column_names[section]

        # Row header will have the row number as name
        if orientation == Qt.Vertical:
            return f"{section}"

        return None

    def canFetchMore(self, parent: QModelIndex) -> bool:
        if parent.isValid():
            return False

        if not self.__dataset:
            return False

        return self.rowCount() < len(self.__dataset)

    def fetchMore(self, parent: QModelIndex):
        if parent.isValid():
            return False

        remainder = len(self.__dataset) - self.rowCount()
        items_to_fetch = min(remainder, self.__max_row_count)

        if items_to_fetch <= 0:
            return

        self.insertRows(self.rowCount(), items_to_fetch)

    def insertRows(self, row: int, count: int, parent=QModelIndex()) -> bool:
        self.beginInsertRows(parent, row, row + count - 1)

        x_set, y_set = self.__dataset.items(start=row, end=row + count, op="display")

        self.__x[row:row] = x_set
        self.__y[row:row] = y_set

        self.endInsertRows()

        return True

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        """
        Return the corresponding data depending on the specified role.
        """

        if not index.isValid():
            return None

        if role in self.__role_map:
            return self.__role_map[role](index.row(), index.column())

        return None

    def index(self, row, column, parent):
        if column == 0:
            return self.createIndex(row, column, self.__x[row])

        if column == 1:
            return self.createIndex(row, column, self.__y[row])

        return QModelIndex()

    def __display_role(self, row: int, column: int):
        """
        Return the text representation of the cell value.
        """
        if column == 0:
            return self.__x[row]

        if column == 1:
            return self.__y[row]

        return None

    def __data_type_role(self, row: int, column: int):
        """
        Return the type of the data on the cell.
        """
        if column == 0:
            return self.__x_type

        if column == 1:
            return self.__y_type

        return None