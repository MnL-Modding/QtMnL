"""
This type stub file was generated by pyright.
"""

"""Module for color code."""

class _RGBA:
    """Class handling RGBA color code."""

    def __init__(self, r: int, g: int, b: int, a: float = ...) -> None:
        """Initialize rgba value.

        Args:
            r: Red(0~255).
            g: Green(0~255).
            b: Blue(0~255).
            a: Alpha(0~1). Defaults to 1.
        """
        ...

    def __str__(self) -> str:
        """Format RGBA class.

        e.g. rgba(100, 100, 100, 0.5).
        """
        ...

    def __getitem__(self, item: int) -> int | float:
        """Unpack to (r, g, b, a)."""
        ...

    def __eq__(self, other: _RGBA) -> bool:
        """Returns true if `r`, `g`, `b` and `a` are all the same."""
        ...

    @property
    def r(self) -> int: ...
    @property
    def g(self) -> int: ...
    @property
    def b(self) -> int: ...
    @property
    def a(self) -> float: ...

class _HSLA:
    def __init__(
        self, hue: int, sat: float, lum: float, alpha: float = ...
    ) -> None: ...
    def __eq__(self, other: _HSLA) -> bool:
        """Returns true if `hue`, `sat`, `lum` and `alpha` are all the same."""
        ...

    @property
    def hue(self) -> int: ...
    @property
    def sat(self) -> float: ...
    @property
    def lum(self) -> float: ...
    @property
    def alpha(self) -> float: ...
    @staticmethod
    def from_rgba(rgba: _RGBA) -> _HSLA: ...
    def to_rgba(self) -> _RGBA: ...

class Color:
    """Class handling color code(RGBA and HSLA)."""

    def __init__(self, color_code: _RGBA | _HSLA) -> None:
        """Initialize color code."""
        ...

    @property
    def rgba(self) -> _RGBA:
        """Return rgba."""
        ...

    @property
    def hsla(self) -> _HSLA:
        """Return hsla."""
        ...

    def __str__(self) -> str:
        """Format Color class.

        e.g. rgba(100, 100, 100, 0.5).
        """
        ...

    @staticmethod
    def from_rgba(r: int, g: int, b: int, a: int) -> Color:
        """Convert rgba to Color object."""
        ...

    @staticmethod
    def from_hex(hex: str) -> Color:
        """Convert hex string to Color object.

        Args:
            color_hex: Color hex string.

        Returns:
            Color: Color object converted from hex.
        """
        ...

    def to_hex_argb(self) -> str:
        """Convert Color object to hex(#AARRGGBB).

        Args:
            color: Color object.

        Returns:
            str: Hex converted from Color object.
        """
        ...

    def to_svg_tiny_color_format(self) -> str:
        """Convert Color object to string for svg.

        QtSvg does not support #RRGGBBAA format.
        Therefore, we need to set the alpha value to `fill-opacity` instead.

        Returns:
            str: RGBA format.
        """
        ...

    def lighten(self, factor: float) -> Color:
        """Lighten color."""
        ...

    def darken(self, factor: float) -> Color:
        """Darken color."""
        ...

    def transparent(self, factor: float) -> Color:
        """Make color transparent."""
        ...
