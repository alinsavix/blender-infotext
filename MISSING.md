# Missing Modifier Support

This document compares InfoText's modifier handlers with Blender 5.2.0 LTS. It
describes the information that a future handler should display; it is not a
proposal to duplicate every control in Blender's modifier panels.

InfoText currently has dedicated handlers for 33 of Blender's 83 modifier
types. There are 24 missing non-Grease-Pencil handlers. Grease Pencil accounts
for the remaining 26 types: the 25 `GREASE_PENCIL_*` identifiers plus
`LINEART`, whose RNA class is `GreasePencilLineartModifier`.

## Display conventions

All new handlers should follow the same basic rules:

- Always show the modifier name and the existing `Hidden` warning when
  `show_viewport` is disabled.
- Keep the first line useful when `detailed_modifiers` is disabled.
- In detailed mode, show values that explain the modifier's result rather than
  every advanced or UI-only property.
- Show missing required objects, node groups, caches, textures, UV maps, and
  vertex groups using the warning color.
- Show object and datablock names rather than Python representations.
- Format distances, angles, and percentages with the existing unit helpers.
- Only show conditional settings when their controlling option is active.
- Do not display panel-open state or other UI-only RNA properties.

## Non-Grease-Pencil modifiers

### `CLOTH` — Cloth

Compact line:

- Cache state (`Baked`, `Baking`, `Outdated`, or frame range).
- Simulation quality and time scale.

Detailed values:

- Mass, air damping, gravity, pin vertex group, and pin stiffness.
- Bending model plus bending, tension, compression, and shear stiffness.
- Enabled structural features: sewing, pressure, internal springs, and dynamic
  mesh.
- Object collision state, collision quality, minimum distance, and friction.
- Self-collision state, self distance, and self friction.
- Cache frame range, step, disk-cache state, and bake state.

Avoid dumping every solver stiffness maximum. The enabled features and their
primary values are more useful in an overlay.

### `COLLISION` — Collision

Compact line:

- Whether collision settings are enabled.
- Outer and inner thickness.

Detailed values:

- Damping and friction, including randomization only when nonzero.
- Permeability, stickiness, cloth friction, and absorption when nonzero.
- Particle-kill, culling, and normal-use flags when enabled.

### `DATA_TRANSFER` — Data Transfer

Compact line:

- Source object, or `No source` as a warning.
- Enabled data categories: vertex, edge, face-corner, and face.

Detailed values:

- Selected data types within each enabled category.
- Mapping mode for each enabled category.
- Object-transform usage.
- Maximum distance and ray radius when distance limiting is enabled.
- Mix mode and factor.
- Vertex group and inversion state.
- Source/destination layer selection for vertex groups, color attributes, and
  UVs, but only for data types that use those settings.

### `DYNAMIC_PAINT` — Dynamic Paint

Compact line:

- Mode: `Canvas` or `Brush`.
- For a canvas, surface count and bake/cache state.
- For a brush, paint source and primary color/wetness value.

Detailed canvas values:

- Each surface's name and surface type.
- Frame range, format, resolution, output layer, and baked state.
- Drying, dissolving, wave, or displacement options only when applicable to
  the surface type.

Detailed brush values:

- Paint source, color, alpha, wetness, erase state, and absolute-alpha state.
- Proximity distance/falloff or particle system, depending on source.
- Smudge and velocity effects when enabled.
- Wave type, factor, and clamp for wave brushes.

### `EXPLODE` — Explode

Compact line:

- Vertex group, protect factor, and edge-cut state.

Detailed values:

- Unborn/alive/dead visibility flags.
- Particle-size usage.
- Particle UV layer.
- Vertex-group inversion.

### `FLUID` — Fluid

Compact line:

- Fluid role: `Domain`, `Flow`, or `Effector`.
- The role-specific subtype and cache state.

Detailed domain values:

- Domain type, resolution, time scale, adaptive-domain state, and cache type.
- Cache directory, frame range, and data/noise/mesh/particle bake states.
- Gas: vorticity, dissolution, fire, and noise state.
- Liquid: FLIP ratio, mesh state, viscosity, diffusion, and secondary-particle
  types.
- Guide state and guide source when enabled.

Detailed flow values:

- Flow type, behavior, and source.
- Density, fuel, temperature, initial velocity, and subframes when relevant.
- Particle system or texture/UV settings when used.

Detailed effector values:

- Effector type, surface distance, velocity factor, guide mode, and subframes.

The full fluid RNA surface is too large for an overlay. Prefer state, cache,
resolution, and the few values that materially define the simulation.

### `MESH_CACHE` — Mesh Cache

Compact line:

- Cache filename, format, deform mode, and factor.

Detailed values:

- Interpolation, time mode, and play mode.
- The active evaluation value: frame, time, or factor.
- Frame start and scale where applicable.
- Forward/up axes and axis-flip state.
- Vertex group and inversion state.
- Missing or empty filepath as a warning.

### `MESH_SEQUENCE_CACHE` — Mesh Sequence Cache

Compact line:

- Cache-file datablock and object path.

Detailed values:

- Data being read.
- Vertex interpolation state.
- Velocity scale.
- Missing cache file or object path as a warning.

### `MESH_TO_VOLUME` — Mesh to Volume

Compact line:

- Source object and density.

Detailed values:

- Resolution mode.
- Voxel size or voxel amount, according to the selected mode.
- Interior band width.
- Missing source object as a warning.

### `NODES` — Geometry Nodes

Compact line:

- Node-group name, or `No node group` as a warning.
- Warning count and bake status summary when present.

Detailed values:

- Exposed group inputs, using interface socket names rather than internal ID
  property identifiers.
- Object, collection, material, image, and texture inputs by datablock name.
- Values that use attributes should show the attribute name and make the mode
  clear.
- Bake target, bake directory when relevant, and per-item baked/baking state.
- The first node warning, followed by a count if more warnings exist.

Geometry Nodes inputs are dynamic. This handler should iterate the node-group
interface and match sockets to the modifier's ID properties instead of
hard-coding property names. Inputs hidden by panels or unavailable sockets
should be skipped. Long interfaces need a configurable limit or compact wrap.

### `NORMAL_EDIT` — Normal Edit

Compact line:

- Mode, target object, and mix factor.

Detailed values:

- Direction-parallel state for directional mode.
- Offset.
- Mix mode, factor, and limit.
- Vertex group and inversion state.
- Polygon-normal fix state.
- Missing target as a warning when the selected mode requires one.

### `OCEAN` — Ocean

Compact line:

- Geometry mode, spectrum, viewport resolution, and cached state.

Detailed values:

- Render resolution, spatial size, X/Y repeats, time, and random seed.
- Wind velocity, wave scale, smallest wave, choppiness, damping, depth,
  direction, and alignment.
- Foam and spray state plus their layer names and coverage where relevant.
- Normals state.
- Bake frame range, filepath, and cache state.

### `PARTICLE_INSTANCE` — Particle Instance

Compact line:

- Source object and particle system.
- Axis and coordinate space.

Detailed values:

- Children, path, normal, preserve-shape, and particle-size flags.
- Unborn/alive/dead visibility.
- Position and random position.
- Rotation and random rotation.
- Particle amount and offset.
- Index/value color-attribute layer names when set.
- Missing source object or particle system as a warning.

### `PARTICLE_SYSTEM` — Particle System

Compact line:

- Particle-system and settings names.
- Emitter/hair type and particle count.

Detailed values:

- Emission frame range and lifetime.
- Viewport display and render modes.
- Seed and child-particle state when available.
- Point-cache frame range and bake state.
- Missing particle-system pointer as a warning.

The modifier itself exposes only a particle-system pointer, so the useful
values must be read from the linked `ParticleSystem`, `ParticleSettings`, and
point cache.

### `SOFT_BODY` — Soft Body

Compact line:

- Cache state, mass, and goal/spring state.

Detailed values:

- Friction, speed, gravity, and mass vertex group.
- Goal state, goal vertex group, default/min/max weights, spring, and friction.
- Edge-spring state with pull, push, damping, bend, shear, and spring vertex
  group.
- Edge, face, and self-collision states plus collision type.
- Aerodynamics type and factor.
- Solver step range and error threshold.
- Point-cache frame range and bake state.

### `SURFACE` — Surface

Blender 5.1 exposes no specialized RNA properties on `SurfaceModifier` beyond
the common modifier fields. Display the modifier name and viewport/render
state only. Do not invent configuration values; this is primarily an internal
physics modifier.

### `UV_PROJECT` — UV Project

Compact line:

- UV layer and projector count.

Detailed values:

- Projector object names, warning about empty slots.
- Aspect X/Y.
- Scale X/Y.
- Missing UV layer or zero projectors as warnings.

### `UV_WARP` — UV Warp

Compact line:

- UV layer and From/To objects.

Detailed values:

- From/To bones when the corresponding object is an armature.
- U/V axes.
- Center, offset, scale, and rotation.
- Vertex group and inversion state.
- Missing UV layer or transform objects as warnings.

### `VERTEX_WEIGHT_EDIT` — Vertex Weight Edit

Compact line:

- Target vertex group, falloff type, and default weight.

Detailed values:

- Add/remove states and their thresholds.
- Normalize and inverted-falloff states.
- Mask factor and, when used, mask vertex group or texture.
- Texture channel and mapping source, with UV layer or object/bone as needed.
- Missing target group or required mask source as a warning.

### `VERTEX_WEIGHT_MIX` — Vertex Weight Mix

Compact line:

- Vertex groups A/B, mix mode, and mix set.

Detailed values:

- Default weights and inversion state for each group.
- Normalize state.
- Mask factor and mask vertex group or texture.
- Texture channel and mapping source, with UV layer or object/bone as needed.
- Missing group A as a warning; group B may be optional depending on the mix
  configuration.

### `VERTEX_WEIGHT_PROXIMITY` — Vertex Weight Proximity

Compact line:

- Target vertex group, target object, and proximity mode.

Detailed values:

- Geometry elements used by geometry proximity.
- Minimum and maximum distance.
- Falloff type, inverted-falloff state, and normalization.
- Mask factor and mask vertex group or texture.
- Texture mapping details when a texture mask is active.
- Missing target object or vertex group as a warning.

### `VOLUME_DISPLACE` — Volume Displace

Compact line:

- Texture and strength.

Detailed values:

- Texture midpoint.
- Mapping mode and mapping object when used.
- Texture sample radius.
- Missing texture or mapping object as a warning.

### `VOLUME_TO_MESH` — Volume to Mesh

Compact line:

- Source volume object and grid name.

Detailed values:

- Threshold and adaptivity.
- Resolution mode.
- Voxel size or voxel amount, according to the selected mode.
- Smooth-shading state.
- Missing source or grid name as a warning.

### `WELD` — Weld

Compact line:

- Mode and merge distance.

Detailed values:

- Vertex group and inversion state.
- Loose-edge state.
- Empty vertex group is valid and should mean the entire mesh, not a warning.

## Grease Pencil design

Grease Pencil should use shared formatting infrastructure rather than 26
independent copies of the same influence-filter code.

### Shared layout

Each Grease Pencil modifier should render in this order:

1. **Header:** modifier name, hidden warning, and a short effect summary.
2. **Primary settings:** two to six values that most strongly define the
   effect.
3. **Influence:** one compact line emitted only when at least one filter or
   vertex-group restriction is active.
4. **Secondary settings:** randomization, fading, curves, masks, or advanced
   options, shown only in detailed mode and only when active.

The shared influence formatter should support:

- Layer or layer-group filter and inversion.
- Layer-pass filter and inversion.
- Material filter and inversion.
- Material-pass filter and inversion.
- Vertex group and inversion.
- Custom influence curve when enabled.

Filters should read like `Influence: Layer Ink (invert), Material Lines,
VGroup Mask`, rather than exposing raw property names. Unset filters should
not consume space.

### Effect-specific values

| Modifier | Primary values to display |
| --- | --- |
| `GREASE_PENCIL_ARMATURE` | Armature object, vertex groups, bone envelopes, preserve volume, influence vertex group |
| `GREASE_PENCIL_ARRAY` | Count; enabled constant, relative, and object offsets; offset object; random offset/rotation/scale and seed |
| `GREASE_PENCIL_BUILD` | Mode, transition, timing mode, delay and length or speed/percentage; restricted frame range and fading when enabled |
| `GREASE_PENCIL_COLOR` | Color mode, hue, saturation, value, custom-curve state |
| `GREASE_PENCIL_DASH` | Dash offset and a compact summary of each segment's dash, gap, radius, and opacity values |
| `GREASE_PENCIL_ENVELOPE` | Mode, spread, thickness, strength, skip, material index |
| `GREASE_PENCIL_HOOK` | Target object/bone, strength, falloff type/radius, uniform-falloff state, influence vertex group |
| `GREASE_PENCIL_LATTICE` | Lattice object, strength, influence vertex group |
| `GREASE_PENCIL_LENGTH` | Mode; start/end factors or lengths; overshoot; randomization and seed; curvature controls when enabled |
| `GREASE_PENCIL_MIRROR` | Mirror object and enabled X/Y/Z axes |
| `GREASE_PENCIL_MULTIPLY` | Duplicate count, distance, offset, and fading thickness/opacity/center when enabled |
| `GREASE_PENCIL_NOISE` | Position/strength/thickness/UV factors, noise scale/offset, random mode, step, and seed |
| `GREASE_PENCIL_OFFSET` | Offset mode; object or stroke location/rotation/scale; random seed, step, and start offset |
| `GREASE_PENCIL_OPACITY` | Color mode, opacity/color factor, hardness factor, uniform-opacity state, weight-as-factor state |
| `GREASE_PENCIL_OUTLINE` | Target object, outline material, thickness, sample length, subdivision, keep-shape state |
| `GREASE_PENCIL_SHRINKWRAP` | Target and auxiliary target, method/mode, offset, project axes/directions/limit, culling, subdivision, smoothing |
| `GREASE_PENCIL_SIMPLIFY` | Mode and its relevant value: factor, step, length, sharp threshold, or distance |
| `GREASE_PENCIL_SMOOTH` | Factor, repeat steps, affected channels (position/strength/thickness/UV), keep-shape and smooth-ends states |
| `GREASE_PENCIL_SUBDIV` | Subdivision type and level |
| `GREASE_PENCIL_TEXTURE` | Mode, UV offset/scale, alignment rotation, fill offset/scale/rotation, fit method |
| `GREASE_PENCIL_THICKNESS` | Uniform thickness or thickness factor, weight-factor state, custom-curve state |
| `GREASE_PENCIL_TIME` | Mode, offset, frame scale, custom frame range, keep-loop state; segment summary for chain mode |
| `GREASE_PENCIL_TINT` | Color mode, tint mode, factor, color or gradient object/radius, weight-as-factor state |
| `GREASE_PENCIL_VERTEX_WEIGHT_ANGLE` | Target vertex group, angle, axis, space, minimum weight, multiply/invert-output states |
| `GREASE_PENCIL_VERTEX_WEIGHT_PROXIMITY` | Target vertex group/object, start/end distances, minimum weight, multiply/invert-output states |
| `LINEART` | Source type and object/collection, camera, target layer/material, enabled edge types, crease threshold, level range, masks, cache/bake state |

### Grease Pencil implementation structure

Use a shared helper module such as `_grease_pencil.py` for:

- Influence-filter formatting.
- Object/material/layer target formatting and missing-target warnings.
- Axis, channel, and inversion summaries.
- Conditional curve, randomization, and fading summaries.
- Segment collection formatting for Dash and Time.

Keep one discovered public module per modifier type, or group closely related
effects into a module whose `MODIFIER_HANDLERS` mapping contains multiple
entries. Helper modules must start with `_` so automatic discovery ignores
them.

Grease Pencil output should default to one effect line plus an optional
influence line. Detailed mode may expand to secondary settings, but should not
reproduce all of Blender's modifier panels.
