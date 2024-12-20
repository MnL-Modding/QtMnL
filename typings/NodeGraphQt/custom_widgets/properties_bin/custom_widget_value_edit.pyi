"""
This type stub file was generated by pyright.
"""

from qtpy import QtWidgets

_NUMB_REGEX = ...

class _NumberValueMenu(QtWidgets.QMenu):
    mouseMove = ...
    mouseRelease = ...
    stepChange = ...
    def __init__(self, parent=...) -> None: ...
    def __repr__(self):  # -> str:
        ...

    def mousePressEvent(self, event):  # -> None:
        """
        Disabling the mouse press event.
        """
        ...

    def mouseReleaseEvent(self, event):  # -> None:
        """
        Additional functionality to emit signal.
        """
        ...

    def mouseMoveEvent(self, event):  # -> None:
        """
        Additional functionality to emit step changed signal.
        """
        ...

    def set_steps(self, steps):  # -> None:
        ...

    def set_data_type(self, data_type):  # -> None:
        ...

class _NumberValueEdit(QtWidgets.QLineEdit):
    value_changed = ...
    def __init__(self, parent=..., data_type=...) -> None: ...
    def __repr__(self):  # -> str:
        ...

    def mouseMoveEvent(self, event):  # -> None:
        ...

    def mousePressEvent(self, event):  # -> None:
        ...

    def mouseReleaseEvent(self, event):  # -> None:
        ...

    def keyPressEvent(self, event):  # -> None:
        ...

    def set_data_type(self, data_type):  # -> None:
        """
        Sets the line edit to either display value in float or int.

        Args:
            data_type(int or float): int or float data type object.
        """
        ...

    def set_steps(self, steps=...):  # -> None:
        """
        Sets the step items in the MMB context menu.

        Args:
            steps (list[int] or list[float]): list of ints or floats.
        """
        ...

    def set_min(self, value=...):  # -> None:
        """
        Set the minimum range for the input field.

        Args:
            value (int or float): minimum range value.
        """
        ...

    def set_max(self, value=...):  # -> None:
        """
        Set the maximum range for the input field.

        Args:
            value (int or float): maximum range value.
        """
        ...

    def get_value(self):  # -> int | float:
        ...

    def set_value(self, value):  # -> None:
        ...

class IntValueEdit(_NumberValueEdit):
    def __init__(self, parent=...) -> None: ...

class FloatValueEdit(_NumberValueEdit):
    def __init__(self, parent=...) -> None: ...

if __name__ == "__main__":
    app = ...
    int_edit = ...
    float_edit = ...
    widget = ...
    layout = ...
