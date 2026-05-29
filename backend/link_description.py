"""
LINK TAGS -> https://wiki.ros.org/urdf/XML/link

<inertial>
    <origin xyz="x y z" rpy="r p y"/>
    <mass value="m"/>
    <inertia ixx="ixx"  ixy="ixy"  ixz="ixz" iyy="iyy" iyz="iyz" izz="izz" />
</inertial>

<visual name="name">
    <origin xyz="x y z" rpy="r p y" />
    <geometry>
        <cylinder radius="r" length="l"/>
        <mesh filename="path" scale="s"/>   ## package://<packagename>/<path>
        <box size="s">
        <sphere radius="r">
    </geometry>
    <material name="name">
        <color rgba="r g b a"/>
        <texture filename="path"/>
    </material>
</visual>

<collision name="name">
    <origin xyz="x y z" rpy="r p y"/>
    <geometry>
        <cylinder radius="r" length="l"/>
        <mesh filename="path" scale="s"/>   ## package://<packagename>/<path>
        <box size="s">
        <sphere radius="r">
    </geometry>
</collision>
"""

from dataclasses import dataclass, field
from geometry_description import GeometryDescription, BoxGeometry
from material_description import MaterialDescription


@dataclass
class InertialDescription:
    origin:  list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])  # [x y z r p y]
    mass:    float       = 0.0
    inertia: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])  # [ixx ixy ixz iyy iyz izz]


@dataclass
class VisualDescription:
    origin:   list[float]         = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])  # [x y z r p y]
    geometry: GeometryDescription = field(default_factory=BoxGeometry)
    material: MaterialDescription = field(default_factory=MaterialDescription)


@dataclass
class CollisionDescription:
    origin:   list[float]         = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])  # [x y z r p y]
    geometry: GeometryDescription = field(default_factory=BoxGeometry)


class LinkDescription:

    def __init__(
        self,
        link_name: str
    ) -> None:

        # Tags
        self.name:      str                        = link_name
        self.inertial:  InertialDescription        = InertialDescription()
        self.visual:    list[VisualDescription]    = []
        self.collision: list[CollisionDescription] = []
