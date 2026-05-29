"""
MATERIAL TAGS -> https://wiki.ros.org/urdf/XML/link

<material name="name">
    <color rgba="r g b a"/>
    <texture filename="path"/>
</material>
"""

class MaterialDescription:

    def __init__(self) -> None:
        # Color
        self.color: list[float] = [0.0, 0.0, 0.0, 0.0] # [r g b a]

        # Material
        self.material_path: str = ''