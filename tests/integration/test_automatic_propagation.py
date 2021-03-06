# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial_core.node_editor import Node


class ValueNode(Node):
    def __init__(self, value=0):
        super().__init__("Value Node")

        # Port configuration
        self.add_output_port(name="value", port_type=int)
        self.outputs["value"].set_generator_function(self._generate_value)

        # Attributes
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

        self.outputs["value"].send()

    def _generate_value(self):
        return self._value


class ReceiveValueNode(Node):
    def __init__(self):
        super().__init__("Receive Value Node")

        self.add_input_port(name="value", port_type=int)
        self.inputs["value"].set_processor_function(self._set_value)

        self.value = None

    def _set_value(self, value):
        self.value = value

        return self.value


def test_automatic_propagation():
    value_node = ValueNode(10)
    receive_value_node = ReceiveValueNode()

    value_node.outputs["value"].connect_to(receive_value_node.inputs["value"])

    assert value_node.value == 10
    assert receive_value_node.value == 10

    value_node.value = 20
    assert value_node.value == 20
    assert receive_value_node.value == 20


class AddTwoValues(Node):
    def __init__(self):
        super().__init__("Receive Value Node")

        self.add_input_port(name="value1", port_type=int)
        self.add_input_port(name="value2", port_type=int)
        self.inputs["value1"].set_processor_function(self._add_values)
        self.inputs["value2"].set_processor_function(self._add_values)

        self.result = 0

    def _add_values(self, _):
        value1 = self.inputs["value1"].receive()
        value2 = self.inputs["value2"].receive()

        self.result = value1 + value2

        return self.result


def test_incomplete_propagation():
    value_node_1 = ValueNode(10)
    value_node_2 = ValueNode(20)

    add_node = AddTwoValues()

    # When connecting, the node will try to add the two values, but is still missing a
    # connection. Shouldn't throw any exception, but don't modify the node state either
    add_node.inputs["value1"].connect_to(value_node_1.outputs["value"])

    assert add_node.result == 0

    # Once we connect the second one, the node will be able to perform the operation
    add_node.inputs["value2"].connect_to(value_node_2.outputs["value"])

    assert add_node.result == 30
