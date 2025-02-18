import copy
import gc
import io
import itertools
import pathlib
import sys
import traceback
import typing
from typing import override

from NodeGraphQt.constants import LayoutDirectionEnum
from NodeGraphQt.custom_widgets.nodes_palette import (
    _NodesGridProxyModel,  # pyright: ignore[reportPrivateUsage]
    NodesGridView,
)
from NodeGraphQt.nodes.base_node import BaseNode
import cached_path
import mnllib
import ndspy.code
import ndspy.rom
import NodeGraphQt
from PySide6.QtCore import (
    QObject,
    QSignalBlocker,
    QSize,
    QStandardPaths,
    QThread,
    QTimer,
    Qt,
    Signal,
    Slot,
)
from PySide6.QtGui import (
    QAction,
    QCloseEvent,
    QFont,
    QFontDatabase,
    QIntValidator,
    QKeySequence,
    QStandardItemModel,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QDockWidget,
    QFileDialog,
    QHeaderView,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressDialog,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
import qdarktheme
import yaml

from qtmnl.consts import (
    APP_DISPLAY_NAME,
    APP_NAME,
    NDS_ROM_FILENAME_FILTER,
    NODE_IDENTIFIER,
    NODE_IDENTIFIER_GENERAL,
    SCRIPT_DOC_URLS,
    ScriptType,
)
from qtmnl.misc import compile_text, decompile_text
from qtmnl.scriptdoc import ScriptDoc
from qtmnl.utils import SCRIPT_DIR, DialogItemDelegate, ValidatedItemDelegate, fhex


fixed_font: QFont

script_docs: dict[ScriptType, ScriptDoc] = {}


class DocsDownloaderWorker(QObject):
    progress_updated = Signal(int)
    errored = Signal(str)
    canceled = Signal()
    finished = Signal()

    current_index: int

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.current_index = 0

    def process_items_from(self, start: int) -> None:
        for i, (script_type, url) in enumerate(SCRIPT_DOC_URLS.items()):
            if i < start:
                continue
            if QThread.currentThread().isInterruptionRequested():
                self.canceled.emit()
                return
            self.current_index = i
            try:
                path = cached_path.cached_path(url)
                with path.open("r") as f:
                    script_docs[script_type] = yaml.safe_load(f)
            except Exception:
                if QThread.currentThread().isInterruptionRequested():
                    self.canceled.emit()
                    return
                self.errored.emit(traceback.format_exc())
                return
            self.progress_updated.emit(i + 1)
        if QThread.currentThread().isInterruptionRequested():
            self.canceled.emit()
            return
        print("Script documentation files downloaded and loaded successfully.")
        self.finished.emit()

    @Slot()
    def run(self) -> None:
        self.process_items_from(self.current_index)


class DocsDownloader(QObject):
    finished = Signal()

    worker_thread: QThread
    worker: DocsDownloaderWorker
    progress: QProgressDialog

    @Slot()
    def download_docs(self) -> None:
        print("Downloading the script documentation files...")
        self.progress = QProgressDialog(
            self.tr("Downloading the script documentation files..."),
            self.tr("Cancel"),
            0,
            len(SCRIPT_DOC_URLS),
        )
        self.progress.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.progress.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose)
        self.progress.setMinimumDuration(500)
        self.progress.setValue(0)

        self.worker_thread = QThread(self)
        self.worker = DocsDownloaderWorker()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker_thread.finished.connect(self.worker.deleteLater)
        self.progress.canceled.connect(self.worker_thread.requestInterruption)
        self.worker.progress_updated.connect(self.progress.setValue)
        self.worker.errored.connect(self.on_error)
        self.worker.canceled.connect(self.on_canceled)
        self.worker.finished.connect(self.on_finished)
        self.worker_thread.start()

    @Slot(str)
    def on_error(self, formatted_exception: str) -> None:
        print(
            "Error downloading or loading script documentation files:\n"
            + formatted_exception
        )
        if (
            QMessageBox.critical(
                self.progress,
                self.tr(
                    "Error downloading or loading script documentation files!",
                ),
                self.tr(
                    "Error downloading or loading the script documentation files! "
                    "The program cannot operate without them.\n\n{0}",
                ).format(formatted_exception),
                QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Cancel,
            )
            == QMessageBox.StandardButton.Cancel
        ):
            self.worker_thread.quit()
            QApplication.quit()
            return
        self.worker.run()

    @Slot()
    def on_canceled(self) -> None:
        self.worker_thread.quit()
        QApplication.quit()

    @Slot()
    def on_finished(self) -> None:
        self.worker_thread.quit()
        self.finished.emit()


class MainWindow(QMainWindow):
    rom_path: pathlib.Path | None
    is_directory: bool | None
    rom: ndspy.rom.NintendoDSRom | None
    fevent_manager: mnllib.FEventScriptManager | None
    graph: NodeGraphQt.NodeGraph | None
    room_id: int | None
    triple_index: int | None

    save_action: QAction
    save_as_rom_action: QAction
    save_as_dir_action: QAction
    room_id_list_widget: QListWidget | None
    room_id_list_widget_dock: QDockWidget | None
    script_properties_widget: QWidget | None
    script_header_field: QPlainTextEdit | None
    language_tables_layout: QVBoxLayout | None
    language_table_widgets: dict[int, QTableWidget] | None
    script_properties_dock: QDockWidget | None
    nodes_palette: NodeGraphQt.NodesPaletteWidget | None
    nodes_palette_dock: QDockWidget | None

    def __init__(self) -> None:
        super().__init__()

        self.rom_path = None
        self.is_directory = None
        self.rom = None
        self.fevent_manager = None
        self.graph = None
        self.room_id = None
        self.triple_index = None

        self.room_id_list_widget = None
        self.room_id_list_widget_dock = None
        self.script_properties_widget = None
        self.script_header_field = None
        self.language_tables_layout = None
        self.language_table_widgets = None
        self.script_properties_dock = None
        self.nodes_palette = None
        self.nodes_palette_dock = None

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu(self.tr("&File"))
        file_menu.addAction(
            self.tr("&Open ROM..."),
            QKeySequence.StandardKey.Open,
            self.open_rom,
        )
        file_menu.addAction(
            self.tr("Open Extracted ROM &Folder..."),
            QKeySequence(self.tr("Ctrl+Shift+O")),
            self.open_rom_directory,
        )
        file_menu.addSeparator()
        self.save_action = typing.cast(
            QAction,
            file_menu.addAction(
                self.tr("&Save"), QKeySequence.StandardKey.Save, self.save_rom
            ),
        )
        self.save_action.setDisabled(True)
        self.save_as_rom_action = typing.cast(
            QAction,
            file_menu.addAction(
                self.tr("Save &As ROM..."),
                QKeySequence.StandardKey.SaveAs,
                self.save_rom_as,
            ),
        )
        self.save_as_rom_action.setDisabled(True)
        self.save_as_dir_action = typing.cast(
            QAction,
            file_menu.addAction(
                self.tr("Save As Extracted ROM Fo&lder..."),
                QKeySequence(self.tr("Ctrl+Alt+Shift+S")),
                self.save_rom_as_dir,
            ),
        )
        self.save_as_dir_action.setDisabled(True)
        file_menu.addSeparator()
        file_menu.addAction(
            self.tr("&Quit"),
            QKeySequence.StandardKey.Quit,
            QApplication.quit,
        )

        help_menu = menu_bar.addMenu(self.tr("&Help"))
        help_menu.addAction(self.tr("About Qt"), QApplication.aboutQt)

        no_rom_label = QLabel(self.tr("No ROM is currently loaded."))
        no_rom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(no_rom_label)

    @Slot()
    def open_rom(self) -> None:
        (path, _selected_filter) = QFileDialog.getOpenFileName(
            parent=self,
            caption=self.tr("Open ROM"),
            filter=NDS_ROM_FILENAME_FILTER,
        )
        if path == "":
            return

        self.setCursor(Qt.CursorShape.WaitCursor)
        try:
            rom_path = pathlib.Path(path)
            rom = ndspy.rom.NintendoDSRom.fromFile(  # pyright: ignore[reportUnknownMemberType] # noqa: E501
                path
            )
            overlays = rom.loadArm9Overlays([3, 6])
            fevent_manager = mnllib.FEventScriptManager(load=False)
            fevent_manager.load_overlay3(io.BytesIO(overlays[3].data))
            fevent_manager.load_overlay6(io.BytesIO(overlays[6].data))
            fevent_manager.load_fevent(
                io.BytesIO(rom.getFileByName(mnllib.FEVENT_FILE_NAME))
            )

            self.rom_path = rom_path
            self.is_directory = False
            self.rom = rom
            self.fevent_manager = fevent_manager

            self.load_rom()
        except Exception:
            QMessageBox.critical(
                self,
                self.tr("Error opening ROM!"),
                self.tr("Error opening ROM:\n{0}").format(traceback.format_exc()),
            )
        self.unsetCursor()

    @Slot()
    def open_rom_directory(self) -> None:
        path = QFileDialog.getExistingDirectory(
            parent=self, caption=self.tr("Open Extracted ROM Folder")
        )
        if path == "":
            return

        self.setCursor(Qt.CursorShape.WaitCursor)
        try:
            rom_path = pathlib.Path(path)
            fevent_manager = mnllib.FEventScriptManager(load=False)
            fevent_manager.load_overlay3(rom_path / "overlay.dec/overlay_0003.dec.bin")
            fevent_manager.load_overlay6(rom_path / "overlay.dec/overlay_0006.dec.bin")
            fevent_manager.load_fevent(rom_path / "data" / mnllib.FEVENT_FILE_NAME)

            self.rom_path = rom_path
            self.is_directory = True
            self.rom = None
            self.fevent_manager = fevent_manager

            self.load_rom()
        except Exception:
            QMessageBox.critical(
                self,
                self.tr("Error opening extracted ROM folder!"),
                self.tr("Error opening extracted ROM folder:\n{0}").format(
                    traceback.format_exc()
                ),
            )
        self.unsetCursor()

    def load_rom(self) -> None:
        assert self.fevent_manager is not None

        self.room_id = None
        self.triple_index = None

        if self.graph is not None:
            self.graph.deleteLater()
        self.graph = NodeGraphQt.NodeGraph(
            self, layout_direction=LayoutDirectionEnum.VERTICAL.value
        )
        self.graph.node_factory.clear_registered_nodes()
        self.graph.set_context_menu_from_file(
            SCRIPT_DIR / "graph/hotkeys/hotkeys.json", "graph"
        )
        main_window_self = self

        class SubroutineNode(NodeGraphQt.BaseNode):
            __identifier__ = NODE_IDENTIFIER_GENERAL
            NODE_NAME = main_window_self.tr("Subroutine")

            def __init__(self) -> None:
                super().__init__()

                self.add_output(multi_output=False, display_name=False)

                self.add_text_input("index", main_window_self.tr("Index"))
                self.get_widget("index").widget().setFixedWidth(600)
                self.add_text_input("footer", main_window_self.tr("Footer"))
                self.get_widget("footer").widget().setFixedWidth(600)

        self.graph.register_node(SubroutineNode)
        for command_id in range(mnllib.FEVENT_NUMBER_OF_COMMANDS):
            command_doc = script_docs["fevent"]["commands"].get(command_id)
            if command_doc is not None and "name" in command_doc:
                node_name = self.tr("{0} (FE_{1:04X})").format(
                    command_doc["name"], command_id, 4
                )
            else:
                node_name = self.tr("Command FE_{0:04X}").format(command_id, 4)

            class CommandNode(NodeGraphQt.BaseNode):
                __identifier__ = f"{NODE_IDENTIFIER}.fevent"
                NODE_NAME = node_name

                cmd_id = command_id
                cmd_doc = command_doc

                def __init__(self) -> None:
                    assert main_window_self.fevent_manager is not None

                    super().__init__()

                    self.view.width = 600

                    self.add_input(multi_input=True, display_name=False)
                    self.add_output(multi_output=False, display_name=False)

                    # fmt: off
                    param_metadata = (
                        main_window_self.fevent_manager
                        .command_parameter_metadata_table[
                            self.cmd_id
                        ]
                    )
                    # fmt: on
                    for i in range(len(param_metadata.parameter_types)):
                        if (
                            self.cmd_doc is not None
                            and "parameters" in self.cmd_doc
                            and len(self.cmd_doc["parameters"]) > i
                        ):
                            param = self.cmd_doc["parameters"][i] or "???"
                        else:
                            param = "???"
                        property_name = f"param_{i}"
                        param_label, sep, _ = param.partition("\n")
                        if sep != "":
                            param_label += "..."
                        self.add_text_input(
                            property_name,
                            main_window_self.tr("Parameter {0}: {1}").format(
                                i + 1, param_label
                            ),
                            tooltip=param,
                        )
                        self.get_widget(property_name).widget().setFixedWidth(600)
                    if param_metadata.has_return_value:
                        if self.cmd_doc is not None:
                            returns = self.cmd_doc.get("returns") or "???"
                        else:
                            returns = "???"
                        returns_label, sep, _ = returns.partition("\n")
                        if sep != "":
                            returns_label += "..."
                        self.add_text_input(
                            "return",
                            main_window_self.tr("Result variable: {0}").format(
                                returns_label
                            ),
                            tooltip=returns,
                        )
                        self.get_widget("return").widget().setFixedWidth(600)

            CommandNode.__name__ = f"Command{command_id:04X}"
            self.graph.register_node(CommandNode)
        self.setCentralWidget(self.graph.widget)

        if self.room_id_list_widget_dock is None:
            self.room_id_list_widget_dock = QDockWidget(
                self.tr("Room and Chunk ID"), self
            )
            self.addDockWidget(
                Qt.DockWidgetArea.LeftDockWidgetArea, self.room_id_list_widget_dock
            )
        if self.room_id_list_widget is not None:
            self.room_id_list_widget.deleteLater()
        self.room_id_list_widget = QListWidget(self.room_id_list_widget_dock)
        self.room_id_list_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.room_id_list_widget.setFont(fixed_font)
        self.room_id_list_widget.currentItemChanged.connect(
            self.selected_room_id_changed
        )
        self.room_id_list_widget.addItems(
            [
                f"{fhex(room_id, 4)}{f"-{triple_index}" if triple_index != 0 else ""}"
                for room_id, chunk_triple in enumerate(
                    self.fevent_manager.fevent_chunks
                )
                for triple_index, chunk in enumerate(chunk_triple)
                if isinstance(chunk, mnllib.FEventScript)
            ],
        )
        self.room_id_list_widget_dock.setWidget(self.room_id_list_widget)

        if self.script_properties_dock is None:
            self.script_properties_dock = QDockWidget(
                self.tr("Script Properties"), self
            )
            self.addDockWidget(
                Qt.DockWidgetArea.LeftDockWidgetArea, self.script_properties_dock
            )
        if self.script_properties_widget is not None:
            self.script_properties_widget.deleteLater()
        self.script_properties_widget = QWidget(self.script_properties_dock)
        script_properties = QVBoxLayout(self.script_properties_widget)
        script_properties.addWidget(QLabel(self.tr("Header")))
        self.script_header_field = QPlainTextEdit()
        self.script_header_field.setFont(fixed_font)
        script_properties.addWidget(self.script_header_field)
        self.language_tables_layout = QVBoxLayout()
        script_properties.addLayout(self.language_tables_layout)
        self.script_properties_dock.setWidget(self.script_properties_widget)

        if self.nodes_palette_dock is None:
            self.nodes_palette_dock = QDockWidget(self.tr("Nodes Palette"), self)
            self.addDockWidget(
                Qt.DockWidgetArea.BottomDockWidgetArea, self.nodes_palette_dock
            )
        if self.nodes_palette is not None:
            self.nodes_palette.deleteLater()
        self.nodes_palette = NodeGraphQt.NodesPaletteWidget(
            self.nodes_palette_dock, self.graph
        )
        self.nodes_palette.set_category_label(
            NODE_IDENTIFIER_GENERAL, self.tr("General")
        )
        self.nodes_palette.set_category_label(
            f"{NODE_IDENTIFIER}.fevent", self.tr("FEvent")
        )
        nodes_palette_tab_widget = self.nodes_palette.tab_widget()
        for i in range(nodes_palette_tab_widget.count()):
            model = typing.cast(
                QStandardItemModel,
                typing.cast(
                    _NodesGridProxyModel,
                    typing.cast(
                        NodesGridView, nodes_palette_tab_widget.widget(i)
                    ).model(),
                ).sourceModel(),
            )
            for j in range(model.rowCount()):
                model.item(j).setSizeHint(QSize(300, 40))
        self.nodes_palette_dock.setWidget(self.nodes_palette)

        self.room_id_list_widget.setCurrentRow(0)

        self.save_action.setDisabled(False)
        self.save_as_rom_action.setDisabled(False)
        self.save_as_dir_action.setDisabled(False)

    @Slot(QListWidgetItem, QListWidgetItem)
    def selected_room_id_changed(
        self, current: QListWidgetItem, previous: QListWidgetItem
    ) -> None:
        if self.prompt_dirty():
            QTimer.singleShot(  # pyright: ignore[reportUnknownMemberType]
                0, lambda: self.restore_room_id_selection(previous)
            )
            return

        room_id, _, triple_index = current.text().partition("-")
        self.load_script(int(room_id, base=0), int(triple_index or 0))

    def restore_room_id_selection(self, item: QListWidgetItem) -> None:
        assert self.room_id_list_widget is not None

        with QSignalBlocker(self.room_id_list_widget):
            self.room_id_list_widget.setCurrentItem(item)

    def load_script(self, room_id: int, triple_index: int) -> None:
        assert self.fevent_manager is not None
        assert self.graph is not None
        assert self.script_header_field is not None
        assert self.language_tables_layout is not None

        self.room_id = room_id
        self.triple_index = triple_index

        script = typing.cast(
            mnllib.FEventScript,
            self.fevent_manager.fevent_chunks[room_id][triple_index],
        )
        progress = QProgressDialog(
            self.tr("Loading room..."),
            typing.cast(str, None),
            0,
            len(script.subroutines),
            self,
        )
        progress.setWindowModality(Qt.WindowModality.ApplicationModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)

        self.script_header_field.setPlainText(
            script.header.to_bytes(self.fevent_manager).hex().upper()
        )
        self.language_table_widgets = {}
        for i in reversed(range(self.language_tables_layout.count())):
            self.language_tables_layout.takeAt(i).widget().deleteLater()
        language_table = self.fevent_manager.fevent_chunks[room_id][2]
        if isinstance(language_table, mnllib.LanguageTable):
            for language_id, text_table in enumerate(language_table.text_tables):
                if not isinstance(text_table, mnllib.TextTable):
                    continue
                self.language_tables_layout.addWidget(
                    QLabel(self.tr("Text Table {0}").format(fhex(language_id, 2)))
                )
                table_widget = QTableWidget(len(text_table.entries), 3)
                table_widget.setItemDelegateForColumn(
                    0, DialogItemDelegate(table_widget)
                )
                size_delegate = ValidatedItemDelegate(
                    QIntValidator(0, 0xFF, table_widget)
                )
                table_widget.setItemDelegateForColumn(1, size_delegate)
                table_widget.setItemDelegateForColumn(2, size_delegate)
                table_widget.setHorizontalHeaderLabels(
                    [self.tr("Text"), self.tr("Wd."), self.tr("Ht.")]
                )
                table_widget.setVerticalHeaderLabels(
                    [str(i) for i in range(len(text_table.entries))]
                )
                table_widget.horizontalHeader().setSectionResizeMode(
                    QHeaderView.ResizeMode.ResizeToContents
                )
                table_widget.horizontalHeader().setSectionResizeMode(
                    0, QHeaderView.ResizeMode.Stretch
                )
                for i, text_entry in enumerate(text_table.entries):
                    table_widget.setItem(
                        i, 0, QTableWidgetItem(decompile_text(text_entry))
                    )
                    textbox_sizes = typing.cast(
                        list[tuple[int, int]], text_table.textbox_sizes
                    )
                    table_widget.setItem(
                        i, 1, QTableWidgetItem(str(textbox_sizes[i][0]))
                    )
                    table_widget.setItem(
                        i, 2, QTableWidgetItem(str(textbox_sizes[i][1]))
                    )
                self.language_table_widgets[language_id] = table_widget
                self.language_tables_layout.addWidget(table_widget)

        for node in self.graph.all_nodes():
            for port in itertools.chain(node.input_ports(), node.output_ports()):
                port.clear_connections(push_undo=False)
                port.model.node = None
            self.graph.model.nodes.pop(node.id)  # type: ignore[attr-defined]
            node.view.delete()
            for referrer in gc.get_referrers(node):  # FIXME: Ugly and slow hack!
                try:
                    del referrer.cell_contents
                except AttributeError:
                    pass
        self.graph.clear_session()
        gc.collect()
        for subroutine_index, subroutine in enumerate(script.subroutines):
            x = subroutine_index * 1000
            subroutine_node = self.graph.create_node(
                f"{NODE_IDENTIFIER_GENERAL}.SubroutineNode",
                pos=(x + (1000 - 600) / 2, 0),
                push_undo=False,
            )
            subroutine_node.set_property(
                "index", str(subroutine_index), push_undo=False
            )
            subroutine_node.set_property(
                "footer", subroutine.footer.hex().upper(), push_undo=False
            )
            last_node = subroutine_node
            y = subroutine_node.view.height + 40
            for command in subroutine.commands:
                command_node = self.graph.create_node(
                    f"{NODE_IDENTIFIER}.fevent.Command{command.command_id:04X}",
                    pos=(x, round(y)),
                    push_undo=False,
                )
                # command_node.set_pos(x + (1000 - command_node.view.width) / 2, y)
                command_node.set_property(
                    "pos",
                    [x + (1000 - command_node.view.width) / 2, float(y)],
                    push_undo=False,
                )
                for i, argument in enumerate(command.arguments):
                    if isinstance(argument, mnllib.Variable):
                        formatted_argument = f"VAR({fhex(argument.number, 4)})"
                    else:
                        formatted_argument = fhex(
                            argument,
                            mnllib.COMMAND_PARAMETER_STRUCT_MAP[
                                self.fevent_manager.command_parameter_metadata_table[
                                    command.command_id
                                ].parameter_types[i]
                            ].size
                            * 2,
                        )
                    command_node.set_property(
                        f"param_{i}", formatted_argument, push_undo=False
                    )
                if command.result_variable is not None:
                    command_node.set_property(
                        "return",
                        fhex(command.result_variable.number, 4),
                        push_undo=False,
                    )
                command_node.set_input(0, last_node.output(0))
                y += command_node.view.height + 40
                last_node = command_node
            progress.setValue(subroutine_index + 1)
        self.graph.clear_selection()
        self.graph.clear_undo_stack()

    def build_script(self) -> tuple[mnllib.FEventScript, mnllib.FEventChunk | None]:
        assert self.fevent_manager is not None
        assert self.graph is not None
        assert self.room_id is not None
        assert self.triple_index is not None
        assert self.script_header_field is not None
        assert self.language_table_widgets is not None

        language_table = copy.deepcopy(
            self.fevent_manager.fevent_chunks[self.room_id][2]
        )
        if isinstance(language_table, mnllib.LanguageTable):
            for language_id, text_table_widget in self.language_table_widgets.items():
                entries: list[bytes] = []
                textbox_sizes: list[tuple[int, int]] = []
                for i in range(text_table_widget.rowCount()):
                    entries.append(compile_text(text_table_widget.item(i, 0).text()))
                    textbox_sizes.append(
                        (
                            int(text_table_widget.item(i, 1).text()),
                            int(text_table_widget.item(i, 2).text()),
                        )
                    )
                language_table.text_tables[language_id] = mnllib.TextTable(
                    entries, is_dialog=True, textbox_sizes=textbox_sizes
                )
            language_table.text_tables[mnllib.FEVENT_PADDING_TEXT_TABLE_ID] = b""
            language_table_size = len(language_table.to_bytes(self.fevent_manager))
            language_table.text_tables[mnllib.FEVENT_PADDING_TEXT_TABLE_ID] = (
                b"\x00"
                * (
                    (
                        -(language_table_size + 1)
                        % mnllib.FEVENT_LANGUAGE_TABLE_ALIGNMENT
                    )
                    + 1
                )
            )

        index = self.room_id * 3 + self.triple_index
        header = mnllib.FEventScriptHeader.from_stream(
            self.fevent_manager,
            io.BytesIO(bytes.fromhex(self.script_header_field.toPlainText())),
            index=index,
        )

        subroutines: dict[int, mnllib.Subroutine] = {}
        for subroutine_node in self.graph.get_nodes_by_type(
            f"{NODE_IDENTIFIER_GENERAL}.SubroutineNode"
        ):
            commands: list[mnllib.Command] = []
            command_node = typing.cast(BaseNode, subroutine_node)
            while True:
                connected_ports = command_node.get_output(0).connected_ports()
                if len(connected_ports) <= 0:
                    break
                command_node = connected_ports[0].node()
                command_id = int(type(command_node).__name__[7:], base=16)
                param_metadata = self.fevent_manager.command_parameter_metadata_table[
                    command_id
                ]
                arguments: list[int | mnllib.Variable] = []
                for i in range(len(param_metadata.parameter_types)):
                    property = typing.cast(str, command_node.get_property(f"param_{i}"))
                    if property.startswith("VAR(") and property.endswith(")"):
                        arguments.append(mnllib.Variable(int(property[4:-1], base=0)))
                    else:
                        arguments.append(int(property, base=0))
                commands.append(
                    mnllib.Command(
                        command_id,
                        arguments,
                        (
                            mnllib.Variable(
                                int(
                                    typing.cast(
                                        str, command_node.get_property("return")
                                    ),
                                    base=0,
                                )
                            )
                            if param_metadata.has_return_value
                            else None
                        ),
                    )
                )
            subroutines[
                int(typing.cast(str, subroutine_node.get_property("index")), base=0)
            ] = mnllib.Subroutine(
                commands,
                footer=bytes.fromhex(
                    typing.cast(str, subroutine_node.get_property("footer"))
                ),
            )
        subroutines_list: list[mnllib.Subroutine] = []
        for i in range(len(subroutines)):
            subroutine = subroutines.get(i)
            if subroutine is None:
                raise ValueError(
                    f"subroutine indexes are not in order (missing index {i})"
                )
            subroutines_list.append(subroutine)

        return (
            mnllib.FEventScript(header, subroutines_list, index=index),
            language_table,
        )

    @Slot()
    def save_rom(self) -> None:
        self.setCursor(Qt.CursorShape.WaitCursor)

        try:
            assert self.rom_path is not None
            assert self.fevent_manager is not None
            assert self.room_id is not None
            assert self.triple_index is not None

            chunk_triple = list(self.fevent_manager.fevent_chunks[self.room_id])
            chunk_triple[self.triple_index], chunk_triple[2] = self.build_script()
            self.fevent_manager.fevent_chunks[self.room_id] = typing.cast(
                tuple[
                    mnllib.FEventScript | None,
                    mnllib.FEventChunk | None,
                    mnllib.FEventChunk | None,
                ],
                tuple(chunk_triple),
            )

            if self.is_directory:
                self.fevent_manager.save_fevent(
                    self.rom_path / "data" / mnllib.FEVENT_FILE_NAME
                )
                self.fevent_manager.save_overlay6(
                    self.rom_path / "overlay.dec/overlay_0006.dec.bin"
                )
                self.fevent_manager.save_overlay3(
                    self.rom_path / "overlay.dec/overlay_0003.dec.bin"
                )
            else:
                assert self.rom is not None

                data = io.BytesIO()
                self.fevent_manager.save_fevent(data)
                self.rom.setFileByName(mnllib.FEVENT_FILE_NAME, data.getvalue())
                overlays = self.rom.loadArm9Overlays()
                data = io.BytesIO(overlays[6].data)
                self.fevent_manager.save_overlay6(data)
                overlays[6].data = data.getvalue()
                self.rom.files[overlays[6].fileID] = overlays[6].save(compress=True)
                data = io.BytesIO(overlays[3].data)
                self.fevent_manager.save_overlay3(data)
                overlays[3].data = data.getvalue()
                self.rom.files[overlays[3].fileID] = overlays[3].save(compress=True)
                self.rom.arm9OverlayTable = ndspy.code.saveOverlayTable(overlays)

                self.rom.saveToFile(  # pyright: ignore[reportUnknownMemberType]
                    self.rom_path
                )
        except Exception:
            QMessageBox.critical(
                self,
                self.tr("Error saving ROM!"),
                self.tr("Error saving ROM:\n{0}").format(traceback.format_exc()),
            )

        self.unsetCursor()

    @Slot()
    def save_rom_as(self) -> None:
        assert self.rom_path is not None

        path, _selected_filter = QFileDialog.getSaveFileName(
            parent=self,
            caption=self.tr("Save ROM As"),
            dir=str(self.rom_path.parent),
            filter=NDS_ROM_FILENAME_FILTER,
        )
        if path == "":
            return
        self.rom_path = pathlib.Path(path)
        self.is_directory = False
        if self.rom is None:
            self.rom = ndspy.rom.NintendoDSRom.fromFile(  # pyright: ignore[reportUnknownMemberType] # noqa: E501
                path
            )

        self.save_rom()

    @Slot()
    def save_rom_as_dir(self) -> None:
        assert self.rom_path is not None

        path = QFileDialog.getExistingDirectory(
            parent=self,
            caption=self.tr("Save Extracted ROM Folder As"),
            dir=str(self.rom_path),
        )
        if path == "":
            return
        self.rom_path = pathlib.Path(path)
        self.is_directory = True
        self.rom = None

        self.save_rom()

    def is_dirty(self) -> bool:
        if (
            self.fevent_manager is None
            or self.room_id is None
            or self.triple_index is None
        ):
            return False

        original_script = self.fevent_manager.fevent_chunks[self.room_id][
            self.triple_index
        ]
        original_script_bytes = (
            original_script.to_bytes(self.fevent_manager)
            if original_script is not None
            else None
        )
        original_third_chunk = self.fevent_manager.fevent_chunks[self.room_id][2]
        original_third_chunk_bytes = (
            original_third_chunk.to_bytes(self.fevent_manager)
            if original_third_chunk is not None
            else None
        )
        script, third_chunk = self.build_script()
        script_bytes = script.to_bytes(self.fevent_manager)
        third_chunk_bytes = (
            third_chunk.to_bytes(self.fevent_manager)
            if third_chunk is not None
            else None
        )

        return (
            original_script_bytes != script_bytes
            or original_third_chunk_bytes != third_chunk_bytes
        )

    def prompt_dirty(self) -> bool:
        try:
            if not self.is_dirty():
                return False
        except Exception:
            assert self.room_id is not None
            return (
                QMessageBox.critical(
                    self,
                    self.tr("Error compiling room!"),
                    self.tr(
                        "You have unsaved changes to room {0}, "
                        "but it failed to compile and cannot be saved. "
                        "Would you like to try to fix it or "
                        "discard your changes?\n\n{1}"
                    ).format(fhex(self.room_id, 4), traceback.format_exc()),
                    QMessageBox.StandardButton.Discard
                    | QMessageBox.StandardButton.Cancel,
                    defaultButton=QMessageBox.StandardButton.Cancel,
                )
                == QMessageBox.StandardButton.Cancel
            )
        assert self.room_id is not None

        match QMessageBox.warning(
            self,
            self.tr("Unsaved changes"),
            self.tr(
                "You have unsaved changes to room {0}. Do you want to save them?"
            ).format(fhex(self.room_id, 4)),
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
        ):
            case QMessageBox.StandardButton.Save:
                self.save_rom()
                return False
            case QMessageBox.StandardButton.Discard:
                return False
            case _:
                return True

    @override
    def closeEvent(self, event: QCloseEvent) -> None:
        if self.prompt_dirty():
            event.ignore()
        else:
            event.accept()


def main() -> None:
    global fixed_font

    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_DISPLAY_NAME)
    fixed_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
    cached_path.set_cache_dir(
        QStandardPaths.writableLocation(QStandardPaths.StandardLocation.CacheLocation)
    )
    docs_downloader = DocsDownloader()
    main_window = MainWindow()
    docs_downloader.finished.connect(main_window.show)
    QTimer.singleShot(  # pyright: ignore[reportUnknownMemberType]
        0, docs_downloader.download_docs
    )
    sys.exit(app.exec())
