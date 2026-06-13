from PyQt5.QtCore import pyqtSignal, QLocale
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from backend.link_description import LinkDescription, VisualDescription


class PropertiesPanel(QWidget):
    origin_changed = pyqtSignal(list)   # [x, y, z, r, p, yaw]
    color_changed  = pyqtSignal(list)   # [r, g, b, a]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumWidth(280)

        self._current_link:   LinkDescription   | None = None
        self._current_visual: VisualDescription | None = None

        self._build_ui()
        self.hide()

    # Build
    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)
        outer.setSpacing(6)

        self._name_label = QLabel()
        self._name_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        outer.addWidget(self._name_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.addWidget(self._build_inertial_group())
        layout.addWidget(self._build_material_group())
        layout.addStretch()

        scroll.setWidget(container)
        outer.addWidget(scroll)

    def _build_inertial_group(self) -> QGroupBox:
        group = QGroupBox("Inertial")
        form  = QFormLayout(group)
        form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self._ori_x   = self._make_spinbox()
        self._ori_y   = self._make_spinbox()
        self._ori_z   = self._make_spinbox()
        self._ori_r   = self._make_spinbox()
        self._ori_p   = self._make_spinbox()
        self._ori_yaw = self._make_spinbox()
        self._mass    = self._make_spinbox(minimum=0.0)
        self._ixx     = self._make_spinbox()
        self._ixy     = self._make_spinbox()
        self._ixz     = self._make_spinbox()
        self._iyy     = self._make_spinbox()
        self._iyz     = self._make_spinbox()
        self._izz     = self._make_spinbox()

        form.addRow("Origin X:",   self._ori_x)
        form.addRow("Origin Y:",   self._ori_y)
        form.addRow("Origin Z:",   self._ori_z)
        form.addRow("Origin R:",   self._ori_r)
        form.addRow("Origin P:",   self._ori_p)
        form.addRow("Origin Yaw:", self._ori_yaw)
        form.addRow("Mass:",       self._mass)
        form.addRow("Ixx:",        self._ixx)
        form.addRow("Ixy:",        self._ixy)
        form.addRow("Ixz:",        self._ixz)
        form.addRow("Iyy:",        self._iyy)
        form.addRow("Iyz:",        self._iyz)
        form.addRow("Izz:",        self._izz)

        self._ori_x.valueChanged.connect(  lambda v: self._write_origin(0, v))
        self._ori_y.valueChanged.connect(  lambda v: self._write_origin(1, v))
        self._ori_z.valueChanged.connect(  lambda v: self._write_origin(2, v))
        self._ori_r.valueChanged.connect(  lambda v: self._write_origin(3, v))
        self._ori_p.valueChanged.connect(  lambda v: self._write_origin(4, v))
        self._ori_yaw.valueChanged.connect(lambda v: self._write_origin(5, v))
        self._mass.valueChanged.connect( lambda v: self._write_mass(v))
        self._ixx.valueChanged.connect(  lambda v: self._write_inertia(0, v))
        self._ixy.valueChanged.connect(  lambda v: self._write_inertia(1, v))
        self._ixz.valueChanged.connect(  lambda v: self._write_inertia(2, v))
        self._iyy.valueChanged.connect(  lambda v: self._write_inertia(3, v))
        self._iyz.valueChanged.connect(  lambda v: self._write_inertia(4, v))
        self._izz.valueChanged.connect(  lambda v: self._write_inertia(5, v))

        return group

    def _build_material_group(self) -> QGroupBox:
        group = QGroupBox("Material")
        form  = QFormLayout(group)
        form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self._mat_r = self._make_spinbox(minimum=0.0, maximum=1.0, step=0.01, decimals=3)
        self._mat_g = self._make_spinbox(minimum=0.0, maximum=1.0, step=0.01, decimals=3)
        self._mat_b = self._make_spinbox(minimum=0.0, maximum=1.0, step=0.01, decimals=3)
        self._mat_a = self._make_spinbox(minimum=0.0, maximum=1.0, step=0.01, decimals=3)
        self._mat_a.setValue(1.0)

        self._color_swatch = QLabel()
        self._color_swatch.setFixedSize(20, 20)

        self._texture = QLineEdit()

        form.addRow("R:", self._mat_r)
        form.addRow("G:", self._mat_g)
        form.addRow("B:", self._mat_b)
        form.addRow("A:", self._mat_a)
        form.addRow("Color:", self._color_swatch)
        form.addRow("Texture:", self._texture)

        self._mat_r.valueChanged.connect(lambda v: self._write_color(0, v))
        self._mat_g.valueChanged.connect(lambda v: self._write_color(1, v))
        self._mat_b.valueChanged.connect(lambda v: self._write_color(2, v))
        self._mat_a.valueChanged.connect(lambda v: self._write_color(3, v))
        self._texture.textChanged.connect(self._write_texture)

        return group

    # Public
    def show_link(self, link: LinkDescription) -> None:
        self._current_link = link

        if not link.visual:
            link.visual.append(VisualDescription())
        self._current_visual = link.visual[0]

        self._set_signals_blocked(True)

        self._name_label.setText(link.name)

        ori = link.inertial.origin
        self._ori_x.setValue(ori[0])
        self._ori_y.setValue(ori[1])
        self._ori_z.setValue(ori[2])
        self._ori_r.setValue(ori[3])
        self._ori_p.setValue(ori[4])
        self._ori_yaw.setValue(ori[5])
        self._mass.setValue(link.inertial.mass)

        inertia = link.inertial.inertia
        self._ixx.setValue(inertia[0])
        self._ixy.setValue(inertia[1])
        self._ixz.setValue(inertia[2])
        self._iyy.setValue(inertia[3])
        self._iyz.setValue(inertia[4])
        self._izz.setValue(inertia[5])

        color = self._current_visual.material.color
        self._mat_r.setValue(color[0])
        self._mat_g.setValue(color[1])
        self._mat_b.setValue(color[2])
        self._mat_a.setValue(color[3] if len(color) > 3 else 1.0)
        self._texture.setText(self._current_visual.material.texture_path)
        self._refresh_swatch()

        self._set_signals_blocked(False)
        self.show()

    def clear(self) -> None:
        self._current_link   = None
        self._current_visual = None
        self.hide()

    # Writers
    def _write_origin(self, idx: int, val: float) -> None:
        if self._current_link:
            self._current_link.inertial.origin[idx] = val
            self.origin_changed.emit(list(self._current_link.inertial.origin))

    def _write_mass(self, val: float) -> None:
        if self._current_link:
            self._current_link.inertial.mass = val

    def _write_inertia(self, idx: int, val: float) -> None:
        if self._current_link:
            self._current_link.inertial.inertia[idx] = val

    def _write_color(self, idx: int, val: float) -> None:
        if self._current_visual:
            color = self._current_visual.material.color
            if len(color) <= idx:
                color.extend([0.0] * (idx + 1 - len(color)))
            color[idx] = val
            self._refresh_swatch()
            self.color_changed.emit(list(color))

    def _write_texture(self, val: str) -> None:
        if self._current_visual:
            self._current_visual.material.texture_path = val

    # Helpers
    def _set_signals_blocked(self, blocked: bool) -> None:
        for w in (
            self._ori_x, self._ori_y, self._ori_z,
            self._ori_r, self._ori_p, self._ori_yaw,
            self._mass,
            self._ixx, self._ixy, self._ixz,
            self._iyy, self._iyz, self._izz,
            self._mat_r, self._mat_g, self._mat_b, self._mat_a,
            self._texture,
        ):
            w.blockSignals(blocked)

    def _refresh_swatch(self) -> None:
        if self._current_visual:
            c = self._current_visual.material.color
            r, g, b = (int(c[i] * 255) for i in range(3))
            self._color_swatch.setStyleSheet(
                f"background-color: rgb({r},{g},{b}); border: 1px solid #555;"
            )

    @staticmethod
    def _make_spinbox(
        minimum: float = -1e9,
        maximum: float =  1e9,
        step:    float =  0.001,
        decimals: int  =  6,
    ) -> QDoubleSpinBox:
        sb = QDoubleSpinBox()
        sb.setLocale(QLocale(QLocale.C))
        sb.setRange(minimum, maximum)
        sb.setSingleStep(step)
        sb.setDecimals(decimals)
        return sb