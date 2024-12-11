"""
This type stub file was generated by pyright.
"""

class NodePropertyWidgetFactory:
    """
    Node property widget factory for mapping the corresponding property widget
    to the Properties bin.
    """

    def __init__(self) -> None: ...
    def get_widget(
        self, widget_type=...
    ):  # -> FloatValueEdit | IntValueEdit | PropCheckBox | PropColorPickerRGB | PropColorPickerRGBA | PropComboBox | PropDoubleSlider | PropDoubleSpinBox | PropFilePath | PropFileSavePath | PropLabel | PropLineEdit | PropSlider | PropSpinBox | PropTextEdit | PropVector2 | PropVector3 | PropVector4 | None:
        """
        Return a new instance of a node property widget.

        Args:
            widget_type (int): widget type index.

        Returns:
            BaseProperty: node property widget.
        """
        ...
