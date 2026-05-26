import numpy as np
import trimesh

# trimesh.util.attach_to_log()

def scene_load(
    file_path: str
) -> trimesh.Scene:

    # Load scene
    scene = trimesh.load_scene(file_path)

    # Check is_valid
    if not scene.is_valid:
        scene = trimesh.Scene()

    ## DEBUG
    print("Loaded Scene!")
    scene_print_geometries_list(scene)
    
    return scene

def scene_print_geometries_list(
    scene: trimesh.Scene
) -> None:
    
    print("Scene geometry list:")
    for name, geo in scene.geometry.items():
        print(f"    {name}: {geo}")

def scene_add_geometry(
    scene: trimesh.Scene,
    file_path: str
) -> trimesh.Scene:
    
    scene.add_geometry(
        trimesh.load_mesh(file_path)
    )

    return scene

def scene_remove_geometry(
    scene: trimesh.Scene,
    name: str
) -> trimesh.Scene:
    
    # Check if geometry exists
    # and delete geometry if so
    if name in scene.geometry:
        scene.delete_geometry(
            name
        )
        print("Geometry was deleted from scene.")

    else:
        print("Geometry does not exist in scene.")

    return scene


if __name__ == "__main__":
    file_path: str = 'example/pile_of_cubes/pile_of_cubes.dae'
    scene = scene_load(file_path)

    scene_remove_geometry(scene, "Cube_004-mesh")
    scene_print_geometries_list(scene)

    scene_remove_geometry(scene, "Cube_004-mes")
    scene_print_geometries_list(scene)