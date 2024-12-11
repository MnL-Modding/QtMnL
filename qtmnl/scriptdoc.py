from __future__ import annotations

import typing


class ScriptDoc(typing.TypedDict):
    commands: dict[int, CommandDoc]


class CommandDoc(typing.TypedDict, total=False):
    name: str
    description: str
    returns: str
    parameters: list[str | None]
