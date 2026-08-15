# Glossary

Domain terms used throughout the spec:

- **FBX** — Autodesk's 3D interchange format.
- **URDF (Unified Robot Description Format)** — XML schema used by ROS/robotics simulators to describe a robot's links, joints and physical properties.
- **Link** — A single rigid body in the robot model. Created by grouping one or more meshes into one logical unit.
- **Joint** — The connection between two Links (a parent and a child) that defines how they move relative to each other.
- **Joint type**
  - **Fixed** — No relative motion between parent and child.
  - **Revolute** — Rotation around a single axis, with motion limits.
  - **Prismatic** — Translation along a single axis, with motion limits.
- **base_link** — The single root Link of the kinematic tree. Every other Link must connect back to it through a chain of joints.
- **Kinematic chain / tree** — The full graph of Links connected by Joints, rooted at `base_link`.
- **Joint origin** — The position and orientation of a joint relative to its parent Link's frame.
- **Axis of motion** — The direction (x, y or z) a Revolute or Prismatic joint rotates or translates along.
- **Center of Mass** — The point at which a Link's mass is considered to be concentrated. Required for the URDF `<inertial>` element.
- **Inertia matrix** — The 3x3 matrix describing how a Link's mass is distributed in space.
- **Collision geometry** — A simplified shape (for example, bounding box or cylinder) used for physics/collision checks in place of the full-resolution visual mesh, for simulation performance.
- **Visual mesh** — The full-resolution geometry shown for rendering, as opposed to the simplified collision geometry.
- **Coordinate transformation** — Conversion from FBX's global/world coordinates to URDF's parent-relative coordinate system.
