"""
This type stub file was generated by pyright.
"""

from qtpy import QtWidgets

class AbstractNodeItem(QtWidgets.QGraphicsItem):
    """
    The base class of all node qgraphics item.
    """

    def __init__(self, name=..., parent=...) -> None: ...
    def __repr__(self):  # -> str:
        ...

    def boundingRect(self):  # -> QRectF:
        ...

    def mousePressEvent(self, event):  # -> None:
        """
        Re-implemented to update "self._properties['selected']" attribute.

        Args:
            event (QtWidgets.QGraphicsSceneMouseEvent): mouse event.
        """
        ...

    def setSelected(self, selected):  # -> None:
        ...

    def draw_node(self):  # -> None:
        """
        Re-draw the node item in the scene with proper
        calculated size and widgets aligned.

        (this is called from the builtin custom widgets.)
        """
        ...

    def pre_init(self, viewer, pos=...):  # -> None:
        """
        Called before node has been added into the scene.

        Args:
            viewer (NodeGraphQt.widgets.viewer.NodeViewer): main viewer.
            pos (tuple): the cursor pos if node is called with tab search.
        """
        ...

    def post_init(self, viewer, pos=...):  # -> None:
        """
        Called after node has been added into the scene.

        Args:
            viewer (NodeGraphQt.widgets.viewer.NodeViewer): main viewer
            pos (tuple): the cursor pos if node is called with tab search.
        """
        ...

    @property
    def id(self):  # -> str | tuple[int, int, int, int] | bool | int | None:
        ...

    @id.setter
    def id(self, unique_id=...):  # -> None:
        ...

    @property
    def type_(self):  # -> str | tuple[int, int, int, int] | bool | int | None:
        ...

    @type_.setter
    def type_(self, node_type=...):  # -> None:
        ...

    @property
    def layout_direction(
        self,
    ):  # -> str | tuple[int, int, int, int] | bool | int | None:
        ...

    @layout_direction.setter
    def layout_direction(self, value=...):  # -> None:
        ...

    @property
    def size(self):  # -> tuple[int | float, int | float]:
        ...

    @property
    def width(self) -> int | float: ...
    @width.setter
    def width(self, width: int | float = ...) -> None: ...
    @property
    def height(self) -> int | float: ...
    @height.setter
    def height(self, height: int | float = ...) -> None: ...
    @property
    def color(self):  # -> str | tuple[int, int, int, int] | bool | int | None:
        ...

    @color.setter
    def color(self, color=...):  # -> None:
        ...

    @property
    def text_color(self):  # -> str | tuple[int, int, int, int] | bool | int | None:
        ...

    @text_color.setter
    def text_color(self, color=...):  # -> None:
        ...

    @property
    def border_color(self):  # -> str | tuple[int, int, int, int] | bool | int | None:
        ...

    @border_color.setter
    def border_color(self, color=...):  # -> None:
        ...

    @property
    def disabled(self):  # -> str | tuple[int, int, int, int] | bool | int | None:
        ...

    @disabled.setter
    def disabled(self, state=...):  # -> None:
        ...

    @property
    def selected(self):  # -> bool | str | tuple[int, int, int, int] | int | None:
        ...

    @selected.setter
    def selected(self, selected=...):  # -> None:
        ...

    @property
    def visible(self):  # -> str | tuple[int, int, int, int] | bool | int | None:
        ...

    @visible.setter
    def visible(self, visible=...):  # -> None:
        ...

    @property
    def xy_pos(self):  # -> list[float]:
        """
        return the item scene postion.
        ("node.pos" conflicted with "QGraphicsItem.pos()"
        so it was refactored to "xy_pos".)

        Returns:
            list[float]: x, y scene position.
        """
        ...

    @xy_pos.setter
    def xy_pos(self, pos=...):  # -> None:
        """
        set the item scene postion.
        ("node.pos" conflicted with "QGraphicsItem.pos()"
        so it was refactored to "xy_pos".)

        Args:
            pos (list[float]): x, y scene position.
        """
        ...

    @property
    def name(self):  # -> str | tuple[int, int, int, int] | bool | int | None:
        ...

    @name.setter
    def name(self, name=...):  # -> None:
        ...

    @property
    def properties(self):  # -> dict[str, int | float | list[float]]:
        """
        return the node view attributes.

        Returns:
            dict: {property_name: property_value}
        """
        ...

    def viewer(self):  # -> None:
        """
        return the main viewer.

        Returns:
            NodeGraphQt.widgets.viewer.NodeViewer: viewer object.
        """
        ...

    def delete(self):  # -> None:
        """
        remove node view from the scene.
        """
        ...

    def from_dict(self, node_dict):  # -> None:
        """
        set the node view attributes from the dictionary.

        Args:
            node_dict (dict): serialized node dict.
        """
        ...