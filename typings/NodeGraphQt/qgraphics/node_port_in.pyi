"""
This type stub file was generated by pyright.
"""

from NodeGraphQt.qgraphics.node_base import NodeItem

class PortInputNodeItem(NodeItem):
    """
    Input Port Node item.

    Args:
        name (str): name displayed on the node.
        parent (QtWidgets.QGraphicsItem): parent item.
    """

    def __init__(self, name=..., parent=...) -> None: ...
    def set_proxy_mode(self, mode):  # -> None:
        """
        Set whether to draw the node with proxy mode.
        (proxy mode toggles visibility for some qgraphic items in the node.)

        Args:
            mode (bool): true to enable proxy mode.
        """
        ...