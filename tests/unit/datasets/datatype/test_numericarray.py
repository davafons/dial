# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import numpy as np
import pytest

from dial_core.datasets.datatype import NumericArray


@pytest.fixture
def numericarray_obj():
    """
    Returns an instance of NumericArray.
    """
    return NumericArray()


@pytest.mark.parametrize(
    "test_input, expected", [(np.array([1, 2, 3]), np.array([1, 2, 3]))]
)
def test_process(numericarray_obj, test_input, expected):
    assert np.alltrue(numericarray_obj.process(test_input) == expected)


@pytest.mark.parametrize("test_input, expected", [(np.array([1, 2]), "[1, 2]")])
def test_display(numericarray_obj, test_input, expected):
    assert numericarray_obj.display(test_input) == expected


def test_convert_to_expected_format(numericarray_obj):
    assert numericarray_obj.convert_to_expected_format([1, 2]).tolist() == [1, 2]
