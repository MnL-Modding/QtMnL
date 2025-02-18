import pathlib
import typing
from typing import override

from PySide6.QtCore import (
    QAbstractItemModel,
    QModelIndex,
    QObject,
    QPersistentModelIndex,
    Qt,
)
from PySide6.QtGui import QValidator
from PySide6.QtWidgets import (
    QDialog,
    QInputDialog,
    QLineEdit,
    QStyleOptionViewItem,
    QStyledItemDelegate,
    QWidget,
)


SCRIPT_DIR = pathlib.Path(__file__).parent


def fhex(num: int, width: int = 0) -> str:
    return f"{"-" if num < 0 else ""}0x{abs(num):0{width}X}"


class ValidatedItemDelegate(QStyledItemDelegate):
    validator: QValidator

    def __init__(self, validator: QValidator, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.validator = validator

    @override
    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> QWidget:
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            editor.setValidator(self.validator)
        return editor


class DialogItemDelegate(QStyledItemDelegate):
    @override
    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> QWidget:
        dialog = QInputDialog(parent)
        dialog.setModal(True)
        dialog.setOption(QInputDialog.InputDialogOption.UsePlainTextEditForTextInput)
        column_name = index.model().headerData(
            index.column(), Qt.Orientation.Horizontal
        )
        dialog.setWindowTitle(self.tr("Edit {0}").format(column_name))
        dialog.setLabelText(self.tr("{0}:").format(column_name))
        dialog.setTextValue(index.data())
        dialog.setFixedSize(600, 300)
        return dialog

    @override
    def setModelData(
        self,
        editor: QWidget,
        model: QAbstractItemModel,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        assert isinstance(editor, QInputDialog)

        if editor.result() != QDialog.DialogCode.Accepted:
            return
        model.setData(index, editor.textValue())
