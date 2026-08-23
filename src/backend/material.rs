use super::types::MaterialType;

pub struct Material {
    name: String,
    material_type: MaterialType,
    color: Option<[f32; 4]>,        // RGBA
    texture: Option<String>,        // path to texture file
}

impl Material {
    pub fn new(
        name: String,
        material_type: MaterialType,
        color: Option<[f32; 4]>,
        texture: Option<String>,
    ) -> Material {
        Material {
            name,
            material_type,
            color,
            texture,
        }
    }
}