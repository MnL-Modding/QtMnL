"""
This type stub file was generated by pyright.
"""

from qtpy import QtWidgets

class BaseProperty(QtWidgets.QWidget):
    """
    Base class for a custom node property widget to be displayed in the
    PropertiesBin widget.

    Inherits from: :class:`PySide2.QtWidgets.QWidget`
    """

    value_changed = ...
    def __init__(self, parent=...) -> None: ...
    def __repr__(self):  # -> str:
        ...

    def get_name(self):  # -> None:
        """
        Returns:
            str: property name matching the node property.
        """
        ...

    def set_name(self, name):  # -> None:
        """
        Args:
            name (str): property name matching the node property.
        """
        ...

    def get_value(self):
        """
        Returns:
            object: widgets current value.
        """
        ...

    def set_value(self, value):
        """
        Args:
            value (object): property value to update the widget.
        """
        ...