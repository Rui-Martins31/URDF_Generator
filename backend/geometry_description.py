"""
GEOMETRY TAGS -> https://wiki.ros.org/urdf/XML/link

<geometry>
    <cylinder radius="r" length="l"/>
    <mesh filename="path" scale="s"/>   ## package://<packagename>/<path> 
    <box size="s">
    <sphere radius="r">
</geometry>
"""

class GeometryDescription:

    def __init__(
        self,
        geometry_type: str = "box"
    ) -> None:
        
        match geometry_type:
            case "box":
                pass

            case "cylinder":
                pass

            case "sphere":
                pass

            case "mesh":
                pass