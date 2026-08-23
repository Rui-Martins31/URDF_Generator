use crate::backend::joint::MeshDescription;
use crate::backend::types::{MeshId, Transform};

use super::types::LinkId;
use super::link::Link;
use super::joint::Joint;

use super::scene_loader::SceneDescriptor;

pub struct RobotModel {
    base_link: LinkId,
    links: Vec<Link>,
    joints: Vec<Joint>,
    meshes: Vec<MeshDescription>,
}

impl RobotModel {
    pub fn new(path: &str) -> RobotModel {
        // Load scene
        let scene_desc      = SceneDescriptor::new(path);

        // Initialization vars
        let mut meshes = Vec::new();
        let mut links             = Vec::new();

        // Parse meshes/links
        let raw_meshes = scene_desc.get_meshes();

        for (idx, msh) in raw_meshes.into_iter().enumerate() {
            let mesh_id = MeshId(idx);
            let link_id = LinkId(idx);
            let name    = msh.name.clone();

            meshes.push(MeshDescription::new(mesh_id, msh));

            // Link
            let link = Link::new(
                link_id,
                name,
                vec![mesh_id],
                Option::None,         // TO BE CHANGED. THESE ARE JUST DEFAULT VALUES.
                Transform::default(),   // TO BE CHANGED. THESE ARE JUST DEFAULT VALUES.
                0.0 as f32,               // TO BE CHANGED. THESE ARE JUST DEFAULT VALUES.
            );
            links.push(link);
        }

        // Return
        RobotModel {
            base_link: LinkId(0),
            links,
            joints: Vec::new(),
            meshes,
        }
    }
}