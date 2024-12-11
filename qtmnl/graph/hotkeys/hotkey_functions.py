# pyright: standard

# Taken from https://github.com/jchanvfx/NodeGraphQt/blob/main/examples/hotkeys/hotkey_functions.py  # noqa: E501

# ------------------------------------------------------------------------------
# menu command functions
# ------------------------------------------------------------------------------


import NodeGraphQt


def zoom_in(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Set the node graph to zoom in by 0.1
    """
    zoom = graph.get_zoom() + 0.1
    graph.set_zoom(zoom)


def zoom_out(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Set the node graph to zoom in by 0.1
    """
    zoom = graph.get_zoom() - 0.2
    graph.set_zoom(zoom)


def reset_zoom(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Reset zoom level.
    """
    graph.reset_zoom()


def layout_h_mode(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Set node graph layout direction to horizontal.
    """
    graph.set_layout_direction(0)


def layout_v_mode(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Set node graph layout direction to vertical.
    """
    graph.set_layout_direction(1)


def open_session(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Prompts a file open dialog to load a session.
    """
    current = graph.current_session()
    file_path = graph.load_dialog(current)
    if file_path:
        graph.load_session(file_path)


def import_session(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Prompts a file open dialog to load a session.
    """
    current = graph.current_session()
    file_path = graph.load_dialog(current)
    if file_path:
        graph.import_session(file_path)


def save_session(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Prompts a file save dialog to serialize a session if required.
    """
    current = graph.current_session()
    if current:
        graph.save_session(current)
        msg = "Session layout saved:\n{}".format(current)
        viewer = graph.viewer()
        viewer.message_dialog(msg, title="Session Saved")
    else:
        save_session_as(graph)


def save_session_as(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Prompts a file save dialog to serialize a session.
    """
    current = graph.current_session()
    file_path = graph.save_dialog(current)
    if file_path:
        graph.save_session(file_path)


def clear_session(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Prompts a warning dialog to new a node graph session.
    """
    if graph.question_dialog("Clear Current Session?", "Clear Session"):
        graph.clear_session()


def clear_undo(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Prompts a warning dialog to clear undo.
    """
    viewer = graph.viewer()
    msg = "Clear all undo history, Are you sure?"
    if viewer.question_dialog("Clear Undo History", msg):
        graph.clear_undo_stack()


def copy_nodes(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Copy nodes to the clipboard.
    """
    graph.copy_nodes()


def cut_nodes(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Cut nodes to the clip board.
    """
    graph.cut_nodes()


def paste_nodes(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Pastes nodes copied from the clipboard.
    """
    graph.paste_nodes()


def delete_nodes(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Delete selected node.
    """
    graph.delete_nodes(graph.selected_nodes())


def extract_nodes(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Extract selected nodes.
    """
    graph.extract_nodes(graph.selected_nodes())


def clear_node_connections(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Clear port connection on selected nodes.
    """
    graph.undo_stack().beginMacro("clear selected node connections")
    for node in graph.selected_nodes():
        for port in node.input_ports() + node.output_ports():
            port.clear_connections()
    graph.undo_stack().endMacro()


def select_all_nodes(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Select all nodes.
    """
    graph.select_all()


def clear_node_selection(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Clear node selection.
    """
    graph.clear_selection()


def invert_node_selection(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Invert node selection.
    """
    graph.invert_selection()


def disable_nodes(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Toggle disable on selected nodes.
    """
    graph.disable_nodes(graph.selected_nodes())


def duplicate_nodes(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Duplicated selected nodes.
    """
    graph.duplicate_nodes(graph.selected_nodes())


def expand_group_node(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Expand selected group node.
    """
    selected_nodes = graph.selected_nodes()
    if not selected_nodes:
        graph.message_dialog('Please select a "GroupNode" to expand.')
        return
    graph.expand_group_node(selected_nodes[0])


def fit_to_selection(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Sets the zoom level to fit selected nodes.
    """
    graph.fit_to_selection()


def show_undo_view(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Show the undo list widget.
    """
    graph.undo_view.show()


def curved_pipe(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Set node graph pipes layout as curved.
    """
    from NodeGraphQt.constants import PipeLayoutEnum

    graph.set_pipe_style(PipeLayoutEnum.CURVED.value)


def straight_pipe(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Set node graph pipes layout as straight.
    """
    from NodeGraphQt.constants import PipeLayoutEnum

    graph.set_pipe_style(PipeLayoutEnum.STRAIGHT.value)


def angle_pipe(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Set node graph pipes layout as angled.
    """
    from NodeGraphQt.constants import PipeLayoutEnum

    graph.set_pipe_style(PipeLayoutEnum.ANGLE.value)


def bg_grid_none(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Turn off the background patterns.
    """
    from NodeGraphQt.constants import ViewerEnum

    graph.set_grid_mode(ViewerEnum.GRID_DISPLAY_NONE.value)


def bg_grid_dots(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Set background node graph background with grid dots.
    """
    from NodeGraphQt.constants import ViewerEnum

    graph.set_grid_mode(ViewerEnum.GRID_DISPLAY_DOTS.value)


def bg_grid_lines(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Set background node graph background with grid lines.
    """
    from NodeGraphQt.constants import ViewerEnum

    graph.set_grid_mode(ViewerEnum.GRID_DISPLAY_LINES.value)


def layout_graph_down(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Auto layout the nodes down stream.
    """
    nodes = graph.selected_nodes() or graph.all_nodes()
    graph.auto_layout_nodes(nodes=nodes, down_stream=True)


def layout_graph_up(graph: NodeGraphQt.NodeGraph) -> None:
    """
    Auto layout the nodes up stream.
    """
    nodes = graph.selected_nodes() or graph.all_nodes()
    graph.auto_layout_nodes(nodes=nodes, down_stream=False)


def toggle_node_search(graph: NodeGraphQt.NodeGraph) -> None:
    """
    show/hide the node search widget.
    """
    graph.toggle_node_search()
