"""
This type stub file was generated by pyright.
"""

from qdarktheme.qtpy.qt_compat import QT_API

"""Module for detecting Qt version."""
__version__: str | None = ...
if QT_API == "PySide6":
    __version__ = ...
else:
    __version__ = ...
