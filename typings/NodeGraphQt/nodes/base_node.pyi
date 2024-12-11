"""
This type stub file was generated by pyright.
"""

from typing import Any, Callable
from NodeGraphQt.base.node import NodeObject
from NodeGraphQt.base.port import Port
from NodeGraphQt.widgets.node_widgets import NodeBaseWidget
from PySide6.QtCore import QRectF
from PySide6.QtGui import QPainter

class BaseNode(NodeObject):
    """
    The ``NodeGraphQt.BaseNode`` class is the base class for nodes that allows
    port connections from one node to another.

    .. inheritance-diagram:: NodeGraphQt.BaseNode

    .. image:: ../_images/node.png
        :width: 250px

    example snippet:

    .. code-block:: python
        :linenos:

        from NodeGraphQt import BaseNode

        class ExampleNode(BaseNode):

            # unique node identifier domain.
            __identifier__ = 'io.jchanvfx.github'

            # initial default node name.
            NODE_NAME = 'My Node'

            def __init__(self):
                super(ExampleNode, self).__init__()

                # create an input port.
                self.add_input('in')

                # create an output port.
                self.add_output('out')
    """

    NODE_NAME: str = ...
    def __init__(self, qgraphics_item=...) -> None: ...
    def update_model(self):  # -> None:
        """
        Update the node model from view.
        """
        ...

    def set_property(self, name: str, value: object, push_undo: bool = ...) -> None:
        """
        Set the value on the node custom property.

        Args:
            name (str): name of the property.
            value (object): property data (python built in types).
            push_undo (bool): register the command to the undo stack. (default: True)
        """
        ...

    def set_layout_direction(self, value=...):  # -> None:
        """
        Sets the node layout direction to either horizontal or vertical on
        the current node only.

        `Implemented in` ``v0.3.0``

        See Also:
            :meth:`NodeGraph.set_layout_direction`,
            :meth:`NodeObject.layout_direction`


        Warnings:
            This function does not register to the undo stack.

        Args:
            value (int): layout direction mode.
        """
        ...

    def set_icon(self, icon=...):  # -> None:
        """
        Set the node icon.

        Args:
            icon (str): path to the icon image.
        """
        ...

    def icon(self):  # -> None:
        """
        Node icon path.

        Returns:
            str: icon image file path.
        """
        ...

    def widgets(self):
        """
        Returns all embedded widgets from this node.

        See Also:
            :meth:`BaseNode.get_widget`

        Returns:
            dict: embedded node widgets. {``property_name``: ``node_widget``}
        """
        ...

    def get_widget(self, name: str) -> NodeBaseWidget:
        """
        Returns the embedded widget associated with the property name.

        See Also:
            :meth:`BaseNode.add_combo_menu`,
            :meth:`BaseNode.add_text_input`,
            :meth:`BaseNode.add_checkbox`,

        Args:
            name (str): node property name.

        Returns:
            NodeBaseWidget: embedded node widget.
        """
        ...

    def add_custom_widget(self, widget, widget_type=..., tab=...):  # -> None:
        """
        Add a custom node widget into the node.

        see example :ref:`Embedding Custom Widgets`.

        Note:
            The ``value_changed`` signal from the added node widget is wired
            up to the :meth:`NodeObject.set_property` function.

        Args:
            widget (NodeBaseWidget): node widget class object.
            widget_type: widget flag to display in the
                :class:`NodeGraphQt.PropertiesBinWidget`
                (default: :attr:`NodeGraphQt.constants.NodePropWidgetEnum.HIDDEN`).
            tab (str): name of the widget tab to display in.
        """
        ...

    def add_combo_menu(
        self,
        name: str,
        label: str = ...,
        items: list[str] = ...,
        tooltip: str = ...,
        tab: str = ...,
    ) -> None:
        """
        Creates a custom property with the :meth:`NodeObject.create_property`
        function and embeds a :class:`PySide2.QtWidgets.QComboBox` widget
        into the node.

        Note:
            The ``value_changed`` signal from the added node widget is wired
            up to the :meth:`NodeObject.set_property` function.

        Args:
            name (str): name for the custom property.
            label (str): label to be displayed.
            items (list[str]): items to be added into the menu.
            tooltip (str): widget tooltip.
            tab (str): name of the widget tab to display in.
        """
        ...

    def add_text_input(
        self,
        name: str,
        label: str = ...,
        text: str = ...,
        placeholder_text: str = ...,
        tooltip: str = ...,
        tab: str = ...,
    ) -> None:
        """
        Creates a custom property with the :meth:`NodeObject.create_property`
        function and embeds a :class:`PySide2.QtWidgets.QLineEdit` widget
        into the node.

        Note:
            The ``value_changed`` signal from the added node widget is wired
            up to the :meth:`NodeObject.set_property` function.

        Args:
            name (str): name for the custom property.
            label (str): label to be displayed.
            text (str): pre-filled text.
            placeholder_text (str): placeholder text.
            tooltip (str): widget tooltip.
            tab (str): name of the widget tab to display in.
        """
        ...

    def add_checkbox(
        self,
        name: str,
        label: str = ...,
        text: str = ...,
        state: bool = ...,
        tooltip: str = ...,
        tab: str = ...,
    ) -> None:
        """
        Creates a custom property with the :meth:`NodeObject.create_property`
        function and embeds a :class:`PySide2.QtWidgets.QCheckBox` widget
        into the node.

        Note:
            The ``value_changed`` signal from the added node widget is wired
            up to the :meth:`NodeObject.set_property` function.

        Args:
            name (str): name for the custom property.
            label (str): label to be displayed.
            text (str): checkbox text.
            state (bool): pre-check.
            tooltip (str): widget tooltip.
            tab (str): name of the widget tab to display in.
        """
        ...

    def hide_widget(self, name, push_undo=...):  # -> None:
        """
        Hide an embedded node widget.

        Args:
            name (str): node property name for the widget.
            push_undo (bool): register the command to the undo stack. (default: True)

        See Also:
            :meth:`BaseNode.add_custom_widget`,
            :meth:`BaseNode.show_widget`,
            :meth:`BaseNode.get_widget`
        """
        ...

    def show_widget(self, name, push_undo=...):  # -> None:
        """
        Show an embedded node widget.

        Args:
            name (str): node property name for the widget.
            push_undo (bool): register the command to the undo stack. (default: True)

        See Also:
            :meth:`BaseNode.add_custom_widget`,
            :meth:`BaseNode.hide_widget`,
            :meth:`BaseNode.get_widget`
        """
        ...

    def add_input(
        self,
        name: str = ...,
        multi_input: bool = ...,
        display_name: bool = ...,
        color: tuple[int, int, int] = ...,
        locked: bool = ...,
        painter_func: Callable[[QPainter, QRectF, dict[str, Any]], None] | None = ...,
    ) -> Port:
        """
        Add input :class:`Port` to node.

        Warnings:
            Undo is NOT supported for this function.

        Args:
            name (str): name for the input port.
            multi_input (bool): allow port to have more than one connection.
            display_name (bool): display the port name on the node.
            color (tuple): initial port color (r, g, b) ``0-255``.
            locked (bool): locked state see :meth:`Port.set_locked`
            painter_func (function or None): custom function to override the drawing
                of the port shape see example: :ref:`Creating Custom Shapes`

        Returns:
            NodeGraphQt.Port: the created port object.
        """
        ...

    def add_output(
        self,
        name: str = ...,
        multi_output: bool = ...,
        display_name: bool = ...,
        color: tuple[int, int, int] = ...,
        locked: bool = ...,
        painter_func: Callable[[QPainter, QRectF, dict[str, Any]], None] | None = ...,
    ) -> Port:
        """
        Add output :class:`Port` to node.

        Warnings:
            Undo is NOT supported for this function.

        Args:
            name (str): name for the output port.
            multi_output (bool): allow port to have more than one connection.
            display_name (bool): display the port name on the node.
            color (tuple): initial port color (r, g, b) ``0-255``.
            locked (bool): locked state see :meth:`Port.set_locked`
            painter_func (function or None): custom function to override the drawing
                of the port shape see example: :ref:`Creating Custom Shapes`

        Returns:
            NodeGraphQt.Port: the created port object.
        """
        ...

    def get_input(self, port: str | int) -> Port:
        """
        Get input port by the name or index.

        Args:
            port (str or int): port name or index.

        Returns:
            NodeGraphQt.Port: node port.
        """
        ...

    def get_output(self, port: str | int) -> Port:
        """
        Get output port by the name or index.

        Args:
            port (str or int): port name or index.

        Returns:
            NodeGraphQt.Port: node port.
        """
        ...

    def delete_input(self, port: str | int) -> None:
        """
        Delete input port.

        Warnings:
            Undo is NOT supported for this function.

            You can only delete ports if :meth:`BaseNode.port_deletion_allowed`
            returns ``True`` otherwise a port error is raised see also
            :meth:`BaseNode.set_port_deletion_allowed`.

        Args:
            port (str or int): port name or index.
        """
        ...

    def delete_output(self, port: str | int) -> None:
        """
        Delete output port.

        Warnings:
            Undo is NOT supported for this function.

            You can only delete ports if :meth:`BaseNode.port_deletion_allowed`
            returns ``True`` otherwise a port error is raised see also
            :meth:`BaseNode.set_port_deletion_allowed`.

        Args:
            port (str or int): port name or index.
        """
        ...

    def set_port_deletion_allowed(self, mode=...):  # -> None:
        """
        Allow ports to be removable on this node.

        See Also:
            :meth:`BaseNode.port_deletion_allowed` and
            :meth:`BaseNode.set_ports`

        Args:
            mode (bool): true to allow.
        """
        ...

    def port_deletion_allowed(self):  # -> bool:
        """
        Return true if ports can be deleted on this node.

        See Also:
            :meth:`BaseNode.set_port_deletion_allowed`

        Returns:
            bool: true if ports can be deleted.
        """
        ...

    def set_ports(self, port_data):  # -> None:
        """
        Create node input and output ports from serialized port data.

        Warnings:
            You can only use this function if the node has
            :meth:`BaseNode.port_deletion_allowed` is `True`
            see :meth:`BaseNode.set_port_deletion_allowed`

        Hint:
            example snippet of port data.

            .. highlight:: python
            .. code-block:: python

                {
                    'input_ports':
                        [{
                            'name': 'input',
                            'multi_connection': True,
                            'display_name': 'Input',
                            'locked': False
                        }],
                    'output_ports':
                        [{
                            'name': 'output',
                            'multi_connection': True,
                            'display_name': 'Output',
                            'locked': False
                        }]
                }

        Args:
            port_data(dict): port data.
        """
        ...

    def inputs(self):  # -> dict[Any, Any]:
        """
        Returns all the input ports from the node.

        Returns:
            dict: {<port_name>: <port_object>}
        """
        ...

    def input_ports(self):  # -> list[Any]:
        """
        Return all input ports.

        Returns:
            list[NodeGraphQt.Port]: node input ports.
        """
        ...

    def outputs(self):  # -> dict[Any, Any]:
        """
        Returns all the output ports from the node.

        Returns:
            dict: {<port_name>: <port_object>}
        """
        ...

    def output_ports(self):  # -> list[Any]:
        """
        Return all output ports.

        Returns:
            list[NodeGraphQt.Port]: node output ports.
        """
        ...

    def input(self, index: int) -> Port:
        """
        Return the input port with the matching index.

        Args:
            index (int): index of the input port.

        Returns:
            NodeGraphQt.Port: port object.
        """
        ...

    def set_input(self, index: int, port: Port) -> None:
        """
        Creates a connection pipe to the targeted output :class:`Port`.

        Args:
            index (int): index of the port.
            port (NodeGraphQt.Port): port object.
        """
        ...

    def output(self, index: int) -> Port:
        """
        Return the output port with the matching index.

        Args:
            index (int): index of the output port.

        Returns:
            NodeGraphQt.Port: port object.
        """
        ...

    def set_output(self, index: int, port: Port) -> None:
        """
        Creates a connection pipe to the targeted input :class:`Port`.

        Args:
            index (int): index of the port.
            port (NodeGraphQt.Port): port object.
        """
        ...

    def connected_input_nodes(self):  # -> OrderedDict[Any, Any]:
        """
        Returns all nodes connected from the input ports.

        Returns:
            dict: {<input_port>: <node_list>}
        """
        ...

    def connected_output_nodes(self):  # -> OrderedDict[Any, Any]:
        """
        Returns all nodes connected from the output ports.

        Returns:
            dict: {<output_port>: <node_list>}
        """
        ...

    def add_accept_port_type(self, port, port_type_data):  # -> None:
        """
        Add an accept constrain to a specified node port.

        Once a constraint has been added only ports of that type specified will
        be allowed a pipe connection.

        port type data example

        .. highlight:: python
        .. code-block:: python

            {
                'port_name': 'foo'
                'port_type': PortTypeEnum.IN.value
                'node_type': 'io.github.jchanvfx.NodeClass'
            }

        See Also:
            :meth:`NodeGraphQt.BaseNode.accepted_port_types`

        Args:
            port (NodeGraphQt.Port): port to assign constrain to.
            port_type_data (dict): port type data to accept a connection
        """
        ...

    def accepted_port_types(self, port):
        """
        Returns a dictionary of connection constrains of the port types
        that allow for a pipe connection to this node.

        Args:
            port (NodeGraphQt.Port): port object.

        Returns:
            dict: {<node_type>: {<port_type>: [<port_name>]}}
        """
        ...

    def add_reject_port_type(self, port, port_type_data):  # -> None:
        """
        Add a reject constrain to a specified node port.

        Once a constraint has been added only ports of that type specified will
        NOT be allowed a pipe connection.

        port type data example

        .. highlight:: python
        .. code-block:: python

            {
                'port_name': 'foo'
                'port_type': PortTypeEnum.IN.value
                'node_type': 'io.github.jchanvfx.NodeClass'
            }

        See Also:
            :meth:`NodeGraphQt.Port.rejected_port_types`

        Args:
            port (NodeGraphQt.Port): port to assign constrain to.
            port_type_data (dict): port type data to reject a connection
        """
        ...

    def rejected_port_types(self, port):
        """
        Returns a dictionary of connection constrains of the port types
        that are NOT allowed for a pipe connection to this node.

        Args:
            port (NodeGraphQt.Port): port object.

        Returns:
            dict: {<node_type>: {<port_type>: [<port_name>]}}
        """
        ...

    def on_input_connected(self, in_port, out_port):  # -> None:
        """
        Callback triggered when a new pipe connection is made.

        *The default of this function does nothing re-implement if you require
        logic to run for this event.*

        Note:
            to work with undo & redo for this method re-implement
            :meth:`BaseNode.on_input_disconnected` with the reverse logic.

        Args:
            in_port (NodeGraphQt.Port): source input port from this node.
            out_port (NodeGraphQt.Port): output port that connected to this node.
        """
        ...

    def on_input_disconnected(self, in_port, out_port):  # -> None:
        """
        Callback triggered when a pipe connection has been disconnected
        from a INPUT port.

        *The default of this function does nothing re-implement if you require
        logic to run for this event.*

        Note:
            to work with undo & redo for this method re-implement
            :meth:`BaseNode.on_input_connected` with the reverse logic.

        Args:
            in_port (NodeGraphQt.Port): source input port from this node.
            out_port (NodeGraphQt.Port): output port that was disconnected.
        """
        ...
