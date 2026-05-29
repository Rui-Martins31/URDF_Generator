from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAction,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QSplitter,
    QStatusBar,
    QWidget,
)

from backend.scene_description import SceneDescription
from frontend.viewport import Viewport
from frontend.properties_panel import PropertiesPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("URDF Generator")
        self.resize(1200, 800)

        self._scene_desc: SceneDescription | None = None

        self._build_top_menu()
        self._build_central()
        self._build_status_bar()

    # UI Layout
    def _build_top_menu(self) -> None:
        # Menu bar
        menu_bar    = self.menuBar()

        # Components of menu bar
        file_menu   = menu_bar.addMenu("File")

        # Actions
        open_action = QAction("Open…", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_file)

        # Connect actions to components
        file_menu.addAction(open_action)

    def _build_central(self) -> None:
        self._splitter = QSplitter(Qt.Horizontal)

        # Left panel: geometry list
        left        = QWidget()
        left_layout = QHBoxLayout(left)
        left_layout.setContentsMargins(4, 4, 4, 4)

        self._geo_list = QListWidget()
        self._geo_list.setMaximumWidth(240)
        self._geo_list.itemChanged.connect(self._on_item_changed)
        self._geo_list.itemClicked.connect(self._on_item_clicked)
        left_layout.addWidget(self._geo_list)

        self._splitter.addWidget(left)

        # Centre panel: 3D viewport
        self._viewport = Viewport()
        self._viewport.geometry_selected.connect(self._select_geometry)
        self._splitter.addWidget(self._viewport)

        # Right panel: properties
        self._props_panel = PropertiesPanel()
        self._splitter.addWidget(self._props_panel)

        self._splitter.setStretchFactor(0, 0)
        self._splitter.setStretchFactor(1, 1)
        self._splitter.setStretchFactor(2, 0)

        self.setCentralWidget(self._splitter)

    def _build_status_bar(self) -> None:
        self._status       = QStatusBar()
        self._status_label = QLabel("No scene loaded")
        self._status.addWidget(self._status_label)
        self.setStatusBar(self._status)


    # Auxiliary Methods
    def _open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open 3D Scene/Model",
            "",
            "3D Files (*.dae);;All Files (*)",
        )
        if not path:
            return
        self._load(path)

    def _load(self, path: str) -> None:
        self._scene_desc = SceneDescription(path)
        self._props_panel.clear()
        self._populate_geo_list(self._scene_desc.scene.geometry)
        self._viewport.load_scene(self._scene_desc.scene)
        count = len(self._scene_desc.scene.geometry)
        self._status_label.setText(
            f"Loaded: {path}  |  {count} geometr{'y' if count == 1 else 'ies'}"
        )

    def _populate_geo_list(self, scene_geometry: dict) -> None:
        self._geo_list.blockSignals(True)
        self._geo_list.clear()
        for name in scene_geometry:
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            self._geo_list.addItem(item)
        self._geo_list.blockSignals(False)

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        self._select_geometry(item.text())

    def _select_geometry(self, name: str) -> None:
        if self._scene_desc is None:
            return

        link = next(
            (l for l in self._scene_desc.links if l.name == name), None
        )
        if link:
            self._props_panel.show_link(link)
        else:
            self._props_panel.clear()

        self._viewport.set_selected(name)

        # Sync list highlight without re-triggering itemChanged
        self._geo_list.blockSignals(True)
        for i in range(self._geo_list.count()):
            item = self._geo_list.item(i)
            if item is not None:
                item.setSelected(item.text() == name)
        self._geo_list.blockSignals(False)

    def _on_item_changed(self, item: QListWidgetItem) -> None:
        if self._scene_desc is None:
            return
        name = item.text()
        if item.checkState() == Qt.Checked:
            self._viewport.show_geometry(name)
        else:
            self._viewport.hide_geometry(name)

    def closeEvent(self, event):
        self._viewport.plotter.close()
        super().closeEvent(event)
