import numpy as np
import trimesh
from enum import Enum

from link_description import LinkDescription

# Constants
class UpdateMode(Enum):
    ## Update Mode
    # 0 -> add
    # 1 -> remove

    ADD    = 0
    REMOVE = 1


# Utils
def scene_print_geometries_list(
    scene: trimesh.Scene
) -> None:
    
    print("Scene geometry list:")
    for name, geo in scene.geometry.items():
        print(f"    {name}: {geo}")


# Class SceneDescription
class SceneDescription:

    def __init__(
        self,
        file_path: str
    ) -> None:
        
        # File
        self.file_path: str = file_path

        # Scene
        self.scene: trimesh.Scene = trimesh.Scene()
        self.load_scene(self.file_path)

        # Links
        self.links: list[LinkDescription] = []
        self.update_link_info()
    
    def load_scene(
        self,
        file_path: str
    ) -> None:

        # Load scene
        scene = trimesh.load_scene(file_path)

        # Check is_valid
        if not scene.is_valid:
            scene = trimesh.Scene()

        self.scene = scene

        ## DEBUG
        print("Loaded Scene!")
        scene_print_geometries_list(scene)
        
        return
    
    def add_geometry(
        self,
        scene: trimesh.Scene,
        file_path: str
    ) -> trimesh.Scene:
        
        scene.add_geometry(
            trimesh.load_mesh(file_path)
        )
        self.update_link_info(name)
        print("Geometry was added to scene.")

        return scene

    def remove_geometry(
        self,
        scene: trimesh.Scene,
        name: str
    ) -> trimesh.Scene:
        
        # Check if geometry exists
        # and delete geometry if so
        if name in scene.geometry:
            scene.delete_geometry(
                name
            )
            self.update_link_info(name)
            print("Geometry was deleted from scene.")

        else:
            print("Geometry does not exist in scene.")

        return scene

    def update_link_info(
        self,
        link_name:   str        = '',
        update_mode: UpdateMode = UpdateMode.ADD
    ) -> None:

        # Check if it's first call
        if not self.links:
            for name in self.scene.geometry:
                self.links.append(self._make_link(name))
            print(f"Populated the links list for the first time!")

        # Add/Remove geometry
        elif link_name != '':

            match update_mode:
                case UpdateMode.ADD:
                    self.links.append(self._make_link(link_name))
                    print(f"Added new link: {link_name}")

                case UpdateMode.REMOVE:
                    _link_tmp = None
                    for _link in self.links:
                        if _link.name == link_name:
                            _link_tmp = _link
                    
                    if _link_tmp: 
                        self.links.remove(_link_tmp)
                        print(f"Removed new link: {link_name}")

        # Throw warning
        else:
            print(f"Invalid link name: {link_name}")


    # Helpers
    def _make_link(self, name: str) -> LinkDescription:
        link    = LinkDescription(name)
        geo     = self.scene.geometry.get(name)
        
        if isinstance(geo, trimesh.Trimesh) and len(geo.vertices):
            xyz                  = geo.vertices.mean(axis=0).tolist()
            roll, pitch, yaw     = 0.0, 0.0, 0.0
            link.inertial.origin = xyz + [roll, pitch, yaw]

        return link