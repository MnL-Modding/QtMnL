"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass

"""Module for handling template text."""

@dataclass(unsafe_hash=True, frozen=True)
class _Placeholder:
    match_text: str
    value: str | int | float
    filters: tuple[str]
    ...

class Template:
    """Class that handles template text like jinja2."""

    _PLACEHOLDER_RE = ...
    _STRING_RE = ...
    def __init__(self, text: str, filters: dict) -> None:
        """Initialize Template class."""
        ...

    def render(self, replacements: dict) -> str:
        """Render replacements."""
        ...
