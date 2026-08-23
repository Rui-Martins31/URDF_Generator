#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct MeshId(pub usize);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct LinkId(pub usize);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum JointType {
    Fixed,
    Revolute,
    Prismatic,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MaterialType {
    Diffuse,
}

// PLACEHOLDER
#[derive(Debug, Clone, Copy, PartialEq, Default)]
pub struct Transform {
    pub translation: [f32; 3],  // vector
    pub rotation: [f32; 4],     // quaternion
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Axis(pub [f32; 3]);  // vector