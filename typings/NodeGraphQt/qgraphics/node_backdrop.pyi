"""
This type stub file was generated by pyright.
"""

from qtpy import QtWidgets
from NodeGraphQt.qgraphics.node_abstract import AbstractNodeItem

class BackdropSizer(QtWidgets.QGraphicsItem):
    """
    Sizer item for resizing a backdrop item.

    Args:
        parent (BackdropNodeItem): the parent node item.
        size (float): sizer size.
    """

    def __init__(self, parent=..., size=...) -> None: ...
    @property
    def size(self):  # -> float:
        ...

    def set_pos(self, x, y):  # -> None:
        ...

    def boundingRect(self):  # -> QRectF:
        ...

    def itemChange(self, change, value):  # -> QPointF | Any:
        ...

    def mouseDoubleClickEvent(self, event):  # -> None:
        ...

    def mousePressEvent(self, event):  # -> None:
        ...

    def mouseReleaseEvent(self, event):  # -> None:
        ...

    def paint(self, painter, option, widget):  # -> None:
        """
        Draws the backdrop sizer in the bottom right corner.

        Args:
            painter (QtGui.QPainter): painter used for drawing the item.
            option (QtGui.QStyleOptionGraphicsItem):
                used to describe the parameters needed to draw.
            widget (QtWidgets.QWidget): not used.
        """
        ...

class BackdropNodeItem(AbstractNodeItem):
    """
    Base Backdrop item.

    Args:
        name (str): name displayed on the node.
        text (str): backdrop text.
        parent (QtWidgets.QGraphicsItem): parent item.
    """

    def __init__(self, name=..., text=..., parent=...) -> None: ...
    def mouseDoubleClickEvent(self, event):  # -> None:
        ...

    def mousePressEvent(self, event):  # -> None:
        ...

    def mouseReleaseEvent(self, event):  # -> None:
        ...

    def on_sizer_pos_changed(self, pos):  # -> None:
        ...

    def on_sizer_pos_mouse_release(self):  # -> None:
        ...

    def on_sizer_double_clicked(self):  # -> None:
        ...

    def paint(self, painter, option, widget):  # -> None:
        """
        Draws the backdrop rect.

        Args:
            painter (QtGui.QPainter): painter used for drawing the item.
            option (QtGui.QStyleOptionGraphicsItem):
                used to describe the parameters needed to draw.
            widget (QtWidgets.QWidget): not used.
        """
        ...

    def get_nodes(self, inc_intersects=...):  # -> list[Any]:
        ...

    def calc_backdrop_size(self, nodes=...):  # -> dict[str, list[float] | float]:
        ...

    @property
    def minimum_size(self):  # -> tuple[Literal[80], Literal[80]]:
        ...

    @minimum_size.setter
    def minimum_size(self, size=...):  # -> None:
        ...

    @property
    def backdrop_text(self):  # -> str | tuple[int, int, int, int] | bool | int | None:
        ...

    @backdrop_text.setter
    def backdrop_text(self, text):  # -> None:
        ...

    @AbstractNodeItem.width.setter
    def width(self, width=...):  # -> None:
        ...

    @AbstractNodeItem.height.setter
    def height(self, height=...):  # -> None:
        ...

    def from_dict(self, node_dict):  # -> None:
        ...
