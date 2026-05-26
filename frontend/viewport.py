import numpy as np
import pyvista as pv
import trimesh
from pyvistaqt import QtInteractor
from PyQt5.QtWidgets import QWidget, QVBoxLayout


def trimesh_to_pyvista(mesh: trimesh.Trimesh) -> pv.PolyData:
    vertices   = np.array(mesh.vertices)
    faces      = np.array(mesh.faces)
    face_count = np.full((len(faces), 1), 3, dtype=faces.dtype)
    pv_faces   = np.hstack([face_count, faces]).ravel()
    
    return pv.PolyData(vertices, pv_faces)


class Viewport(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.plotter = QtInteractor(self)
        self.plotter.set_background("dimgray")
        self.plotter.add_axes()
        layout.addWidget(self.plotter)

        self._actors: dict[str, pv.Actor] = {}

    def load_scene(self, scene: trimesh.Scene) -> None:
        self.clear()
        for name, geo in scene.geometry.items():
            if isinstance(geo, trimesh.Trimesh):
                self._add_mesh(name, geo)
        self.plotter.reset_camera()

    def show_geometry(self, name: str) -> None:
        actor = self._actors.get(name)
        if actor is not None:
            actor.SetVisibility(True)

    def hide_geometry(self, name: str) -> None:
        actor = self._actors.get(name)
        if actor is not None:
            actor.SetVisibility(False)

    def clear(self) -> None:
        for actor in self._actors.values():
            self.plotter.remove_actor(actor)
        self._actors.clear()

    # Auxiliary Methods
    def _add_mesh(self, name: str, geo: trimesh.Trimesh) -> None:
        pv_mesh = trimesh_to_pyvista(geo)
        color = (
            [c / 255.0 for c in geo.visual.main_color[:3]]
            if hasattr(geo.visual, "main_color")
            else "lightblue"
        )
        actor = self.plotter.add_mesh(
            pv_mesh,
            color=color,
            show_edges=True,
            edge_color="black",
            opacity=1.0,
            name=name,
        )
        self._actors[name] = actor

    def closeEvent(self, event):
        self.plotter.close()
        super().closeEvent(event)
