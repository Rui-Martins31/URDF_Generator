use super::material::Material;
use super::types::{LinkId, MeshId, Transform};

pub struct Link {
    id: LinkId,
    name: String,
    meshes: Vec<MeshId>,
    material: Option<Material>,
    origin: Transform,
    mass: f32,
    // TODO: inertia, center_of_mass, collision_geometry 
}

impl Link {
    pub fn new(
        id: LinkId,
        name: String,
        meshes: Vec<MeshId>,
        material: Option<Material>,
        origin: Transform,
        mass: f32,
    ) -> Link {
        Link {
            id,
            name,
            meshes,
            material,
            origin,
            mass,
        }
    }
}