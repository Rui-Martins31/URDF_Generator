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

from geometry_description import GeometryDescription
from material_description import MaterialDescription

class LinkDescription:

    def __init__(
        self,
        link_name: str
    ) -> None:
        
        # Name
        self.name: str = link_name
        
        # Inertial
        self.inertial: dict = {
            "origin":  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # [x y z r p y]
            "mass":    0.0,
            "inertia": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # [ixx  ixy  ixz iyy iyz izz]
        }

        # Visual
        self.visual: dict = {
            "origin":   [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # [x y z r p y]
            "geometry": [], # GeometryDescription
            "material": [], # MaterialDescription
        }

        # Collision
        self.collision: dict = {
            "origin":   [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # [x y z r p y]
            "geometry": [], # GeometryDescription
        }