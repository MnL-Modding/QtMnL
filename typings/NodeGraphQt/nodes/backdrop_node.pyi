"""
This type stub file was generated by pyright.
"""

from NodeGraphQt.base.node import NodeObject

class BackdropNode(NodeObject):
    """
    The ``NodeGraphQt.BackdropNode`` class allows other node object to be
    nested inside, it's mainly good for grouping nodes together.

    .. inheritance-diagram:: NodeGraphQt.BackdropNode

    .. image:: ../_images/backdrop.png
        :width: 250px

    -
    """

    NODE_NAME = ...
    def __init__(self, qgraphics_views=...) -> None: ...
    def on_backdrop_updated(self, update_prop, value=...):  # -> None:
        """
        Slot triggered by the "on_backdrop_updated" signal from
        the node graph.

        Args:
            update_prop (str): update property type.
            value (object): update value (optional)
        """
        ...

    def auto_size(self):  # -> None:
        """
        Auto resize the backdrop node to fit around the intersecting nodes.
        """
        ...

    def wrap_nodes(self, nodes):  # -> None:
        """
        Set the backdrop size to fit around specified nodes.

        Args:
            nodes (list[NodeGraphQt.NodeObject]): list of nodes.
        """
        ...

    def nodes(self):  # -> list[Any]:
        """
        Returns nodes wrapped within the backdrop node.

        Returns:
            list[NodeGraphQt.BaseNode]: list of node under the backdrop.
        """
        ...

    def set_text(self, text=...):  # -> None:
        """
        Sets the text to be displayed in the backdrop node.

        Args:
            text (str): text string.
        """
        ...

    def text(self):  # -> Any | None:
        """
        Returns the text on the backdrop node.

        Returns:
            str: text string.
        """
        ...

    def set_size(self, width, height):  # -> None:
        """
        Sets the backdrop size.

        Args:
            width (float): backdrop width size.
            height (float): backdrop height size.
        """
        ...

    def size(self):  # -> tuple[Any, Any]:
        """
        Returns the current size of the node.

        Returns:
            tuple: node width, height
        """
        ...

    def inputs(self):  # -> None:
        ...

    def outputs(self):  # -> None:
        ...
