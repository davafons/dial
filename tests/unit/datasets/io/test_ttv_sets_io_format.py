# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os
from unittest.mock import patch

from dial_core.datasets.io import NpzFormat, TxtFormat


@patch("dial_core.datasets.io.ttv_sets_io_format.np")
def test_npz_save_to_description(mock_np, train_dataset):
    identifier = "train"
    parent_dir = "foo"

    dataset_description = NpzFormat.save_to_description(
        identifier, parent_dir, train_dataset
    )

    assert dataset_description["filename"] == f"{identifier}.npz"
    assert dataset_description["x_type"] == train_dataset.x_type.to_dict()
    assert dataset_description["y_type"] == train_dataset.y_type.to_dict()

    mock_np.savez.assert_called_once_with(
        parent_dir + os.path.sep + f"{identifier}.npz",
        x=train_dataset.x,
        y=train_dataset.y,
    )


@patch("dial_core.datasets.io.ttv_sets_io_format.np")
def test_npz_load_from_description(mock_np, train_dataset):
    identifier = "train"
    parent_dir = "foo"

    dataset_description = {
        "filename": f"{identifier}.npz",
        "x_type": train_dataset.x_type.to_dict(),
        "y_type": train_dataset.y_type.to_dict(),
    }

    mock_np.load.side_effect = [{"x": train_dataset.x, "y": train_dataset.y}]

    loaded_dataset = NpzFormat.load_from_description(parent_dir, dataset_description)

    mock_np.load.assert_called_once_with(
        parent_dir + os.path.sep + dataset_description["filename"]
    )

    assert loaded_dataset.x.tolist() == train_dataset.x.tolist()
    assert loaded_dataset.y.tolist() == train_dataset.y.tolist()


@patch("dial_core.datasets.io.ttv_sets_io_format.np")
def test_txt_save_to_description(mock_np, train_dataset):
    identifier = "train"
    parent_dir = "foo"

    dataset_description = TxtFormat.save_to_description(
        identifier, parent_dir, train_dataset
    )

    calls_list = mock_np.savetxt.call_args_list
    assert calls_list[0][0] == (
        parent_dir + os.path.sep + dataset_description["x_filename"],
        train_dataset.x,
    )
    assert calls_list[1][0] == (
        parent_dir + os.path.sep + dataset_description["y_filename"],
        train_dataset.y,
    )

    assert dataset_description["x_filename"] == f"x_{identifier}.txt"
    assert dataset_description["y_filename"] == f"y_{identifier}.txt"
    assert dataset_description["x_type"] == train_dataset.x_type.to_dict()
    assert dataset_description["y_type"] == train_dataset.y_type.to_dict()


@patch("dial_core.datasets.io.ttv_sets_io_format.np")
def test_txt_load_from_description(mock_np, train_dataset):
    identifier = "train"
    parent_dir = "foo"

    dataset_description = {
        "x_filename": f"x_{identifier}.txt",
        "y_filename": f"y_{identifier}.txt",
        "x_type": train_dataset.x_type.to_dict(),
        "y_type": train_dataset.y_type.to_dict(),
    }

    mock_np.loadtxt.side_effect = [train_dataset.x, train_dataset.y]

    loaded_dataset = TxtFormat.load_from_description(parent_dir, dataset_description)

    calls_list = mock_np.loadtxt.call_args_list
    assert calls_list[0][0] == (
        parent_dir + os.path.sep + dataset_description["x_filename"],
    )
    assert calls_list[1][0] == (
        parent_dir + os.path.sep + dataset_description["y_filename"],
    )

    assert loaded_dataset.x.tolist() == train_dataset.x.tolist()
    assert loaded_dataset.y.tolist() == train_dataset.y.tolist()
