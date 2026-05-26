import trimesh
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

from backend.load_model import scene_load
from frontend.viewport import Viewport


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("URDF Generator")
        self.resize(1200, 800)

        self._scene: trimesh.Scene | None = None

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
        splitter = QSplitter(Qt.Horizontal)

        # Left panel: geometry list
        left        = QWidget()
        left_layout = QHBoxLayout(left)
        left_layout.setContentsMargins(4, 4, 4, 4)

        self._geo_list = QListWidget()
        self._geo_list.setMaximumWidth(240)
        self._geo_list.itemChanged.connect(self._on_item_changed)
        left_layout.addWidget(self._geo_list)

        splitter.addWidget(left)

        # Right panel: 3D viewport
        self._viewport = Viewport()
        splitter.addWidget(self._viewport)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)

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
        scene       = scene_load(path)
        self._scene = scene
        self._populate_geo_list(scene)
        self._viewport.load_scene(scene)
        count       = len(scene.geometry)
        self._status_label.setText(f"Loaded: {path}  |  {count} geometr{'y' if count == 1 else 'ies'}")

    def _populate_geo_list(self, scene: trimesh.Scene) -> None:
        self._geo_list.blockSignals(True)
        self._geo_list.clear()
        for name in scene.geometry:
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            self._geo_list.addItem(item)
        self._geo_list.blockSignals(False)

    def _on_item_changed(self, item: QListWidgetItem) -> None:
        if self._scene is None:
            return
        name = item.text()
        if item.checkState() == Qt.Checked:
            self._viewport.show_geometry(name)
        else:
            self._viewport.hide_geometry(name)

    def closeEvent(self, event):
        self._viewport.plotter.close()
        super().closeEvent(event)
