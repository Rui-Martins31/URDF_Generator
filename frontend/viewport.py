import numpy as np
import pyvista as pv
import trimesh
import vtk
from pyvistaqt import QtInteractor
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout


_HIGHLIGHT_COLOR = (1.0, 0.75, 0.0)  # gold highlight for selected mesh


def trimesh_to_pyvista(mesh: trimesh.Trimesh) -> pv.PolyData:
    vertices   = np.array(mesh.vertices)
    faces      = np.array(mesh.faces)
    face_count = np.full((len(faces), 1), 3, dtype=faces.dtype)
    pv_faces   = np.hstack([face_count, faces]).ravel()

    return pv.PolyData(vertices, pv_faces)


class Viewport(QWidget):
    geometry_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.plotter = QtInteractor(self)
        self.plotter.set_background("dimgray")
        self.plotter.add_axes()
        layout.addWidget(self.plotter)

        self._actors:   dict[str, pv.Actor]        = {}
        self._colors:   dict[str, tuple[float, float, float]] = {}
        self._selected: str | None                 = None

        vtk_iren = getattr(self.plotter.iren, 'interactor', self.plotter.iren)
        vtk_iren.AddObserver("LeftButtonPressEvent", self._on_pick)

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

    def set_selected(self, name: str | None) -> None:
        if self._selected and self._selected in self._actors:
            orig = self._colors.get(self._selected, (0.678, 0.847, 0.902))
            self._actors[self._selected].GetProperty().SetColor(*orig)

        self._selected = name

        if name and name in self._actors:
            self._actors[name].GetProperty().SetColor(*_HIGHLIGHT_COLOR)

        self.plotter.render()

    def clear(self) -> None:
        for actor in self._actors.values():
            self.plotter.remove_actor(actor)
        self._actors.clear()
        self._colors.clear()
        self._selected = None

    # ---------------------------------------------------------------- private

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
        self._colors[name] = actor.GetProperty().GetColor()

    def _on_pick(self, obj, event) -> None:
        x, y = obj.GetEventPosition()
        picker = vtk.vtkPropPicker()
        picker.Pick(x, y, 0, self.plotter.renderer)
        actor = picker.GetActor()
        if actor is not None:
            for name, a in self._actors.items():
                if a == actor:
                    self.geometry_selected.emit(name)
                    break

    def closeEvent(self, event):
        self.plotter.close()
        super().closeEvent(event)
