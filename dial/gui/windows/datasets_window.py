# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Window for all the dataset related operations (Visualization, loading...)
"""

from PySide2.QtWidgets import (
    QFormLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QWidget,
)

from dial.gui.widgets import PredefinedDatasetsList, TrainTestTabs
from dial.project import ProjectInstance
from dial.utils import log

LOGGER = log.get_logger(__name__)


class DatasetsWindow(QWidget):
    """
    Window for all the dataset related operations (Visualization, loading...)
    """

    def __init__(self, dataset_table_widget: TrainTestTabs, parent=None):
        super().__init__(parent)

        # Initialize widgets
        self.__main_layout = QGridLayout()
        self.__options_layout = QFormLayout()

        self.__train_test_tabs = dataset_table_widget
        self.__train_test_tabs.setParent(self)

        self.__dataset_name_label = QLabel("")
        self.__dataset_loader_button = QPushButton("More...")

        self.__train_len_label = QLabel("")
        self.__test_len_label = QLabel("")

        # Configure interface
        self.__setup_ui()

        # Connect signals
        self.__dataset_loader_button.clicked.connect(self.load_predefined_dataset)

    def __setup_ui(self):
        splitter = QSplitter()

        self.__options_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.__options_layout.addRow("Dataset name", self.__dataset_name_label)
        self.__options_layout.addRow("Total items (train)", self.__train_len_label)
        self.__options_layout.addRow("Total items (test)", self.__test_len_label)
        self.__options_layout.addRow(
            "Load predefined dataset", self.__dataset_loader_button
        )

        options_widget = QWidget()
        options_widget.setLayout(self.__options_layout)

        splitter.addWidget(options_widget)
        splitter.addWidget(self.__train_test_tabs)

        self.__main_layout.addWidget(splitter, 0, 0)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def load_predefined_dataset(self):
        """
        Select and load a predefined dataset from a Dialog list.
        """
        dataset_loader_dialog = PredefinedDatasetsList.Dialog(parent=self)

        LOGGER.debug("Opening dialog to select a predefined dataset...")

        accepted = dataset_loader_dialog.exec_()

        if accepted:
            LOGGER.debug("Dataset selected")

            # Get the selected loader
            dataset_loader = dataset_loader_dialog.selected_loader()

            # Add the new dataset to the project
            ProjectInstance().load_dataset(dataset_loader)

            # Update models to reflect the new dataset
            self.__train_test_tabs.set_train_dataset(ProjectInstance().train_dataset)
            self.__train_test_tabs.set_test_dataset(ProjectInstance().test_dataset)

            # Update texts and label to match the new dataset
            self.__update_dataset_text(ProjectInstance())

        else:
            LOGGER.debug("Operation cancelled")

    def __update_dataset_text(self, project):
        """
        Update the texts and labels according to the new project dataset.
        """

        self.__dataset_name_label.setText(str(project.dataset_name))
        self.__train_len_label.setText(str(len(project.train_dataset)))
        self.__test_len_label.setText(str(len(project.test_dataset)))

        # Logging
        LOGGER.info("Dataset loaded: %s", project.dataset_name)
        LOGGER.info(
            "Data types: Input -> %s | Output -> %s",
            str(project.dataset_x_type),
            str(project.dataset_y_type),
        )
        LOGGER.info("Train instances: %d", len(project.train_dataset))
        LOGGER.info("Test instances: %d", len(project.test_dataset))
