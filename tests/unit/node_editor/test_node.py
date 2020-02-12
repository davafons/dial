# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest

from dial.node_editor import Node, Port


@pytest.fixture
def node_a():
    """Empty node a. Allows multiple connections to different ports. """
    return Node(title="a")


@pytest.fixture
def node_b():
    """Empty node b. Allows multiple connections to different ports. """
    return Node(title="b")


def test_title(node_a):
    assert node_a.title == "a"


def test_add_input_port(node_a):
    my_input_port = Port(port_type=int)
    node_a.add_input_port("port", my_input_port)

    assert node_a.inputs["port"] == my_input_port
    assert my_input_port not in node_a.outputs.values()

    assert my_input_port.node is node_a


def test_add_output_port(node_a):
    my_output_port = Port(port_type=int)
    node_a.add_output_port("port", my_output_port)

    assert node_a.outputs["port"] == my_output_port
    assert my_output_port not in node_a.inputs.values()

    assert my_output_port.node is node_a


def test_remove_input_port(node_a):
    my_input_port = Port(port_type=int)
    node_a.add_input_port("port", my_input_port)

    node_a.remove_input_port("port")
    assert my_input_port not in node_a.inputs

    assert my_input_port.node is None


def test_remove_output_port(node_a):
    my_output_port = Port(port_type=int)
    node_a.add_output_port("port", my_output_port)

    node_a.remove_output_port("port")
    assert my_output_port not in node_a.outputs

    assert my_output_port.node is None


def test_remove_connected_port(node_a):
    foo_port = Port(port_type=int)
    bar_port = Port(port_type=int)
    foo_port.connect_to(bar_port)

    node_a.add_input_port("foo", foo_port)

    assert foo_port in bar_port.connections
    assert bar_port in foo_port.connections

    node_a.remove_input_port("foo")

    assert foo_port not in bar_port.connections
    assert bar_port not in foo_port.connections


def test_node_connect_to_node(node_a, node_b):
    foo_port = Port(port_type=int)
    bar_port = Port(port_type=int)

    node_a.add_output_port("foo", foo_port)
    node_b.add_input_port("bar", bar_port)

    node_a.outputs["foo"].connect_to(node_b.inputs["bar"])

    # Assert the two ports are connected
    assert foo_port in bar_port.connections
    assert bar_port in foo_port.connections


def test_node_connect_to_inexistent(node_a, node_b):
    foo_port = Port(port_type=int)

    node_a.add_output_port("foo", foo_port)

    with pytest.raises(KeyError):
        node_a.outputs["foo"].connect_to(node_b.inputs["doesnt_exists"])