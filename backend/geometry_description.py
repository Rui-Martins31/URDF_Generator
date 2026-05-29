"""
GEOMETRY TAGS -> https://wiki.ros.org/urdf/XML/link

<geometry>
    <cylinder radius="r" length="l"/>
    <mesh filename="path" scale="s"/>   ## package://<packagename>/<path>
    <box size="s">
    <sphere radius="r">
</geometry>
"""

from dataclasses import dataclass


@dataclass
class BoxGeometry:
    size: float = 0.0


@dataclass
class CylinderGeometry:
    radius: float = 0.0
    length: float = 0.0


@dataclass
class SphereGeometry:
    radius: float = 0.0


@dataclass
class MeshGeometry:
    filename: str = ''
    scale: float = 1.0


GeometryDescription = BoxGeometry | CylinderGeometry | SphereGeometry | MeshGeometry
