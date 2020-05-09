# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import json
import os
from typing import Optional

import numpy as np

from dial_core.datasets import Dataset
from dial_core.datasets.datatype import DataTypeContainer
from dial_core.utils import log

LOGGER = log.get_logger(__name__)


class TTVSetsIOFormat:
    """The TTVSetsIOFormat provides an interface for defining different formats in which
    a dataset could be stored on the file system."""

    @classmethod
    def save(
        self, identifier: str, description_file_path: str, dataset: "Dataset",
    ) -> dict:
        """Writes the passed dataset to the file system.

        Args:
            root_path: Root directory where the dataset should be written to.
            name: Name of the output file/folder.
            dataset_desc: dataset_description dictionary (Data types, relative path...)
            dataset: Dataset to save.
        """
        parent_dir = os.path.dirname(description_file_path)

        dataset_description = self.save_to_description(parent_dir, dataset)

        with open(description_file_path, "w") as desc_file:
            json.dump(desc_file, dataset_description, indent=4)

        return dataset_description

    @classmethod
    def save_to_description(
        self, identifier: str, parent_dir: str, dataset: "Dataset"
    ) -> dict:
        dataset_description = {}
        dataset_description["x_type"] = dataset.x_type.to_dict()
        dataset_description["y_type"] = dataset.y_type.to_dict()

        return dataset_description

    @classmethod
    def load(self, description_file_path: str) -> Optional["Dataset"]:
        """Loads the dataset from the file system.

        Args:
            root_path: Path to the directory where the dataset file/dir is contained.
            dataset_desc: dataset_description dictionary (Data types, relative path...)

        Returns:
            The loaded dataset.
        """
        with open(description_file_path, "r") as desc_file:
            dataset_description = json.load(desc_file)

        parent_dir = os.path.dirname(description_file_path)

        return self.load_from_description(parent_dir, dataset_description)

    @classmethod
    def load_from_description(
        self, parent_dir: str, dataset_description: dict
    ) -> "Dataset":
        """Loads the dataset from the specified `dataset_description` object. A
        `parent_dir` must be passed to resolve relative paths on the
        `dataset_description`.

        Returns:
            The loaded dataset.
        """
        x_type = getattr(
            DataTypeContainer, dataset_description["x_type"]["type"]
        )().from_dict(dataset_description["x_type"])

        y_type = getattr(
            DataTypeContainer, dataset_description["y_type"]["type"]
        )().from_dict(dataset_description["y_type"])

        # Dataset data (x, y) must be filled by subclasses overriding this method
        return Dataset(x_type=x_type, y_type=y_type)

    def __str__(self):
        return type(self).__name__


class NpzFormat(TTVSetsIOFormat):
    """The NpzFormat class stores datasets using Numpy's .npz files. See `np.savez` for
    more details."""

    @classmethod
    def save_to_description(
        self, identifier: str, parent_dir: str, dataset: "Dataset",
    ):
        """Writes the passed dataset to the file system.

        Args:
            root_path: Root directory where the dataset should be written to.
            name: Name of the output file/folder.
            dataset_desc: dataset_description dictionary (Data types, relative path...)
            dataset: Dataset to save.
        """
        dataset_description = super().save_to_description(
            identifier, parent_dir, dataset
        )

        dataset_description["filename"] = f"{identifier}.npz"

        np.savez(
            parent_dir + os.path.sep + dataset_description["filename"],
            x=dataset.x,
            y=dataset.y,
        )

        return dataset_description

    @classmethod
    def load_from_description(
        self, parent_dir: str, dataset_description: dict
    ) -> Optional["Dataset"]:
        """Loads the dataset from the file system.
        Args:
            root_path: Path to the directory where the dataset file/dir is contained.
            dataset_desc: dataset_desc dictionary (Data types, relative path...)
        """
        dataset = super().load_from_description(parent_dir, dataset_description)

        data = np.load(parent_dir + os.path.sep + dataset_description["filename"])

        dataset.x = data["x"]
        dataset.y = data["y"]

        return dataset


class TxtFormat(TTVSetsIOFormat):
    """The TxtFormat class stores datasets on plain readable .txt files."""

    @classmethod
    def save_to_description(
        self, identifier: str, parent_dir: str, dataset: "Dataset",
    ):
        """Writes the passed dataset to the file system.

        Args:
            root_path: Root directory where the dataset should be written to.
            name: Name of the output file/folder.
            dataset_desc: dataset_description dictionary (Data types, relative path...)
            dataset: Dataset to save.
        """
        dataset_description = super().save_to_description(
            identifier, parent_dir, dataset
        )

        dataset_description["x_filename"] = f"x_{identifier}.txt"
        dataset_description["y_filename"] = f"y_{identifier}.txt"

        np.savetxt(
            parent_dir + os.path.sep + dataset_description["x_filename"], dataset.x,
        )
        np.savetxt(
            parent_dir + os.path.sep + dataset_description["y_filename"], dataset.y,
        )

        return dataset_description

    @classmethod
    def load_from_description(
        self, parent_dir: str, dataset_description: dict
    ) -> "Dataset":
        """"""
        dataset = super().load_from_description(parent_dir, dataset_description)

        dataset.x = np.loadtxt(
            parent_dir + os.path.sep + dataset_description["x_filename"]
        )

        dataset.y = np.loadtxt(
            parent_dir + os.path.sep + dataset_description["y_filename"]
        )

        return dataset


class CategoryImagesFormat(TTVSetsIOFormat):
    @classmethod
    def save_from_description(
        self, identifier: str, parent_dir: str, dataset: "Dataset"
    ):
        print("save")

    @classmethod
    def load_from_description(
        self, parent_dir: str, dataset_description: dict
    ) -> Optional["Dataset"]:
        print("load")