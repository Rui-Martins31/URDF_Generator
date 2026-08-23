use russimp::scene::{PostProcess, Scene};
use russimp::mesh::Mesh;

// Struct Scene
pub struct SceneDescriptor {
    scene_content: Scene,
}

impl SceneDescriptor {

    pub fn new(path: &str) -> Self {
        // Load scene
        let scene = Scene::from_file(
            path,
            vec![PostProcess::Triangulate, PostProcess::ValidateDataStructure],
        )
        .expect("Failed to load scene"); // FIX THIS TO HANDLE ERRORS PROPERLY 
        
        // Return
        return SceneDescriptor {
            scene_content: scene
        };
    }

    pub fn get_meshes(self) -> Vec<Mesh> {
        self.scene_content.meshes
    }

    pub fn print_content(&self) {
        // Materials
        println!("MATERIALS");
        for mat in &self.scene_content.materials {
            println!("{:#?}", mat);
        }

        // Meshes
        println!("\nMESHES");
        for msh in &self.scene_content.meshes {
            println!("{:#?}", msh.name);
        }
    }

} // impl SceneDescriptor