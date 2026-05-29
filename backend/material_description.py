"""
MATERIAL TAGS -> https://wiki.ros.org/urdf/XML/link

<material name="name">
    <color rgba="r g b a"/>
    <texture filename="path"/>
</material>
"""

from dataclasses import dataclass, field


@dataclass
class MaterialDescription:
    color: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 1.0])  # [r g b a]
    texture_path: str = ''
