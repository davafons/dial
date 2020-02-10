# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import QBrush, QColor, QFont, QPainter, QPainterPath, QPen
from PySide2.QtWidgets import QGraphicsItem, QGraphicsTextItem


class GraphicsNode(QGraphicsItem):
    def __init__(self, scene, title="Node Graphics Item", parent=None):
        super().__init__(parent)

        self._title_color = Qt.white

        self._title_font = QFont("Ubuntu", 10)

        self.width = 180
        self.height = 180
        self.edge_size = 10

        self.title_height = 24
        self._padding = 10.0

        self._title = ""

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))
        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self.initTitle()
        self.title = title

        self.__setup_ui()

    def __setup_ui(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self,)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)

        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(self.width - self._padding * 2)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def boundingRect(self):
        return QRectF(
            0, 0, 2 * self.edge_size + self.width, 2 * self.edge_size + self.height
        ).normalized()

    def paint(self, painter: QPainter, option, widget=None):
        # Title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(
            0, 0, self.width, self.title_height, self.edge_size, self.edge_size
        )
        path_title.addRect(
            0, self.title_height - self.edge_size, self.edge_size, self.edge_size
        )

        path_title.addRect(
            self.width - self.edge_size,
            self.title_height - self.edge_size,
            self.edge_size,
            self.edge_size,
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # Content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(
            0,
            self.title_height,
            self.width,
            self.height - self.title_height,
            self.edge_size,
            self.edge_size,
        )

        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(
            self.width - self.edge_size,
            self.title_height,
            self.edge_size,
            self.edge_size,
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # Outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(
            0, 0, self.width, self.height, self.edge_size, self.edge_size
        )

        painter.setPen(
            self._pen_default if not self.isSelected() else self._pen_selected
        )

        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())