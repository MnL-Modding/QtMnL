"""
This type stub file was generated by pyright.
"""

from qtpy import QtWidgets

class PortItem(QtWidgets.QGraphicsItem):
    """
    Base Port Item.
    """

    def __init__(self, parent=...) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self):  # -> str:
        ...

    def boundingRect(self):  # -> QRectF:
        ...

    def paint(self, painter, option, widget):  # -> None:
        """
        Draws the circular port.

        Args:
            painter (QtGui.QPainter): painter used for drawing the item.
            option (QtGui.QStyleOptionGraphicsItem):
                used to describe the parameters needed to draw.
            widget (QtWidgets.QWidget): not used.
        """
        ...

    def itemChange(self, change, value):  # -> Any:
        ...

    def mousePressEvent(self, event):  # -> None:
        ...

    def mouseReleaseEvent(self, event):  # -> None:
        ...

    def hoverEnterEvent(self, event):  # -> None:
        ...

    def hoverLeaveEvent(self, event):  # -> None:
        ...

    def viewer_start_connection(self):  # -> None:
        ...

    def redraw_connected_pipes(self):  # -> None:
        ...

    def add_pipe(self, pipe):  # -> None:
        ...

    def remove_pipe(self, pipe):  # -> None:
        ...

    @property
    def connected_pipes(self):  # -> list[Any]:
        ...

    @property
    def connected_ports(self):  # -> list[Any]:
        ...

    @property
    def hovered(self):  # -> bool:
        ...

    @hovered.setter
    def hovered(self, value=...):  # -> None:
        ...

    @property
    def node(self):  # -> QGraphicsItem:
        ...

    @property
    def name(self):  # -> str:
        ...

    @name.setter
    def name(self, name=...):  # -> None:
        ...

    @property
    def display_name(self):  # -> bool:
        ...

    @display_name.setter
    def display_name(self, display=...):  # -> None:
        ...

    @property
    def color(self):  # -> tuple[Literal[49], Literal[115], Literal[100], Literal[255]]:
        ...

    @color.setter
    def color(self, color=...):  # -> None:
        ...

    @property
    def border_color(
        self,
    ):  # -> tuple[Literal[29], Literal[202], Literal[151], Literal[255]]:
        ...

    @border_color.setter
    def border_color(self, color=...):  # -> None:
        ...

    @property
    def border_size(self):  # -> int:
        ...

    @border_size.setter
    def border_size(self, size=...):  # -> None:
        ...

    @property
    def locked(self):  # -> bool:
        ...

    @locked.setter
    def locked(self, value=...):  # -> None:
        ...

    @property
    def multi_connection(self):  # -> bool:
        ...

    @multi_connection.setter
    def multi_connection(self, mode=...):  # -> None:
        ...

    @property
    def port_type(self):  # -> None:
        ...

    @port_type.setter
    def port_type(self, port_type):  # -> None:
        ...

    def connect_to(self, port):  # -> None:
        ...

    def disconnect_from(self, port):  # -> None:
        ...

class CustomPortItem(PortItem):
    """
    Custom port item for drawing custom shape port.
    """

    def __init__(self, parent=..., paint_func=...) -> None: ...
    def set_painter(self, func=...):  # -> None:
        """
        Set custom paint function for drawing.

        Args:
            func (function): paint function.
        """
        ...

    def paint(self, painter, option, widget):  # -> None:
        """
        Draws the port item.

        Args:
            painter (QtGui.QPainter): painter used for drawing the item.
            option (QtGui.QStyleOptionGraphicsItem):
                used to describe the parameters needed to draw.
            widget (QtWidgets.QWidget): not used.
        """
        ...
