mod backend;

use backend::scene_loader;

fn main() {
    let scene_desc = scene_loader::SceneDescriptor::new("example/pile_of_cubes/pile_of_cubes.dae");
    scene_desc.print_content();
}
