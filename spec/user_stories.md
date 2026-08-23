# User Stories

Terms below follow [glossary.md](glossary.md). Stories are grouped by epic and roughly ordered by workflow sequence (import -> author -> estimate physics -> validate -> export).

## Epic 1: FBX Import & Hierarchy

- **US-1**: As a user, I want to import a single FBX file containing my full robot assembly, so that I can start building a URDF without pre-splitting my model. ✅
- **US-2**: As a user, I want to see a visual tree of all meshes in the imported FBX, so that I understand the structure of my model before defining Links.
- **US-3**: As a user, I want to multi-select meshes and group them into a single Link, so that I can treat related sub-parts as one rigid body.
- **US-4**: As a user, I want to rename a Link after grouping, so that my URDF output has meaningful, readable names instead of default mesh names.
- **US-5**: As a user, I want to edit an existing Link's mesh membership or ungroup it, so that I can correct mistakes without restarting the import.

## Epic 2: Interactive Kinematic Authoring

- **US-6**: As a user, I want to select two Links and define a parent-child joint relationship between them, so that I can build the kinematic chain of my robot.
- **US-7**: As a user, I want to choose a joint type (Fixed, Revolute, Prismatic) when creating a joint, so that the URDF correctly represents my robot's degrees of freedom.
(Not for now) - **US-8**: As a user, I want to snap a joint's origin to a geometric center, edge, or custom coordinate, so that I can position joints precisely without manual math.
(Not for now) - **US-9**: As a user, I want to orient a joint's motion axis using a 3D gizmo, so that Revolute/Prismatic joints move in the correct direction.
- **US-10**: As a user, I want to edit or delete an existing joint, so that I can fix mistakes in my kinematic chain without rebuilding it from scratch.

## Epic 3: Physical Property Estimation

- **US-12**: As a user, I want to input a mass for each Link, so that the tool can estimate inertia from real physical values.
(Not for now) - **US-13**: As a user, I want the tool to automatically calculate the inertia matrix for a Link from its mesh volume and mass, so that I don't have to compute it manually.
(Not for now) - **US-14**: As a user, I want the tool to automatically calculate the center of mass for a Link's grouped meshes, so that the URDF's inertial origin is physically accurate.
- **US-15**: As a user, I want to generate simplified collision geometry (bounding box or cylinder) for a Link, so that my robot simulates efficiently without relying on the full-resolution visual mesh.
- **US-16**: As a user, I want to override auto-calculated physical properties (mass, center of mass, inertia) with custom values, so that I can correct estimates when I have more accurate real-world data.

## Epic 4: Kinematic Tree Validation & Feedback

- **US-17**: As a user, I want the tool to warn me in real time if any Link isn't connected to a single `base_link` root, so that I catch "floating" components before export.
- **US-18**: As a user, I want a visual indicator of the overall kinematic tree structure, so that I can verify my robot's hierarchy at a glance.

## Epic 5: Export

- **US-19**: As a user, I want to export a clean, valid URDF XML file, so that I can load my robot directly into ROS/robotics simulators without manual edits.
- **US-20**: As a user, I want the tool to automatically export/convert visual meshes into `.dae` or `.stl` with correct relative paths, so that the exported package works out of the box.
- **US-21**: As a user, I want the tool to validate the exported URDF against the schema before finalizing, so that I catch structural errors before using it in simulation.
