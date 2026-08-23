use russimp::mesh::Mesh;

use crate::backend::types::MeshId;

use super::types::{Axis, JointType, LinkId, Transform};

// Joint
pub struct Joint {
    parent: LinkId,
    child: LinkId,
    joint_type: JointType,
    origin: Transform,
    axis: Option<Axis>,
}

impl Joint {
    pub fn new(
        parent:     LinkId,
        child:      LinkId,
        joint_type: &str,
        origin:     Transform,
        axis:       Option<Axis>
    ) -> Joint {
        let j_type = match joint_type {
            "revolute"  => JointType::Revolute,
            "prismatic" => JointType::Prismatic,
            _           => JointType::Fixed,
        };

        Joint {
            parent,
            child,
            joint_type: j_type,
            origin,
            axis,
        }
    }
}


// Mesh Description
pub struct MeshDescription {
    id: MeshId,
    mesh: Mesh,
}

impl MeshDescription {
    pub fn new(
        id: MeshId,
        mesh: Mesh,       
    ) -> MeshDescription {
        MeshDescription {
            id,
            mesh
        }
    }
}