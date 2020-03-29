# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial_core.node_editor import Node


class ValueNode(Node):
    def __init__(self, value=0):
        super().__init__("Value Node")

        # Port configuration
        self.add_output_port(name="value", port_type=int)
        self.outputs["value"].set_generator_function(self.__generate_value)

        # Attributes
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

        self.outputs["value"].send()

    def __generate_value(self):
        return self.__value


class ReceiveValueNode(Node):
    def __init__(self):
        super().__init__("Receive Value Node")

        self.add_input_port(name="value", port_type=int)
        self.inputs["value"].set_processor_function(self.__set_value)

        self.value = None

    def __set_value(self, value):
        self.value = value


def test_automatic_propagation():
    value_node = ValueNode(10)
    receive_value_node = ReceiveValueNode()

    value_node.outputs["value"].connect_to(receive_value_node.inputs["value"])

    assert value_node.value == 10
    assert receive_value_node.value == 10

    value_node.value = 20
    assert value_node.value == 20
    assert receive_value_node.value == 20

    # But if we activate propagation
    receive_value_node.inputs["value"].toggle_receives_input(False)

    value_node.value = 5
    assert value_node.value == 5
    assert receive_value_node.value == 20

    value_node.value = 8
    assert value_node.value == 8
    assert receive_value_node.value == 20
