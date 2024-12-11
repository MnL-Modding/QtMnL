import typing

from PySide6.QtCore import QCoreApplication


APP_NAME = "qtmnl"
APP_DISPLAY_NAME = QCoreApplication.translate("Global", "QtMnL")

NDS_ROM_FILENAME_FILTER = QCoreApplication.translate(
    "Global", "NDS ROMs (*.nds);;All Files (*)"
)

ScriptType: typing.TypeAlias = typing.Literal["fevent", "battle", "menu", "shop"]

NODE_IDENTIFIER = "io.github.mnl_modding"
NODE_IDENTIFIER_GENERAL = f"{NODE_IDENTIFIER}.general"

SCRIPT_DOC_URLS: dict[ScriptType, str] = {
    "fevent": "https://raw.githubusercontent.com/MnL-Modding/BIS-docs/refs/heads/main/cutscene_code/bis_docs_commands.yml",  # noqa: E501
    # "battle": "https://raw.githubusercontent.com/MnL-Modding/BIS-docs/refs/heads/main/cutscene_code/bis_docs_commands.yml",  # noqa: E501 # TODO
}
