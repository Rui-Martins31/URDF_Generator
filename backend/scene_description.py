import numpy as np
import trimesh

from link_description import LinkDescription

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
        self.scene: trimesh.Scene = self.load_scene(self.file_path)

        # Links
        self.links: list[LinkDescription] = []
    
    def load_scene(
        self,
        file_path: str
    ) -> trimesh.Scene:

        # Load scene
        scene = trimesh.load_scene(file_path)

        # Check is_valid
        if not scene.is_valid:
            scene = trimesh.Scene()

        # Update geometry list
        self.update_link_info()

        ## DEBUG
        print("Loaded Scene!")
        scene_print_geometries_list(scene)
        
        return scene
    
    def add_geometry(
        self,
        scene: trimesh.Scene,
        file_path: str
    ) -> trimesh.Scene:
        
        scene.add_geometry(
            trimesh.load_mesh(file_path)
        )
        self.update_link_info()
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
            self.update_link_info()
            print("Geometry was deleted from scene.")

        else:
            print("Geometry does not exist in scene.")

        return scene
    
    def update_link_info(self):
        pass