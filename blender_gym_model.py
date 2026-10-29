"""
Blender script to create and render outdoor calisthenics fortress
Generates: front, top, side, isometric views as PNG images
Run in Blender Text Editor: Shift+F11, then run script
"""

import bpy
import math
from mathutils import Vector, Matrix

# ── Cleanup ──
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for collection in bpy.data.collections:
    bpy.data.collections.remove(collection)

# Remove default cube and lamp
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj, do_unlink=True)

# ── Scene setup ──
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64  # Fast preview
scene.cycles.diffuse_bounces = 2
scene.cycles.glossy_bounces = 2
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.film_transparent = False

# Materials
def mat(color, roughness=0.7, metalness=0.0):
    m = bpy.data.materials.new(name=f'mat_{color}')
    m.use_nodes = True
    bsdf = m.node_tree.nodes['BSDF']
    bsdf.inputs['Base Color'].default_value = color + (1.0,)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metalness
    return m

mat_wood = mat((0.6, 0.4, 0.2, 1.0), roughness=0.8)
mat_steel = mat((0.3, 0.3, 0.3, 1.0), roughness=0.3, metalness=0.8)
mat_concrete = mat((0.5, 0.5, 0.5, 1.0), roughness=0.9)
mat_net = mat((0.1, 0.5, 0.1, 1.0), roughness=0.9, alpha=0.3)

# ── Helper: create beam ──
def add_beam(x, y, z, w, h, d, material, name='beam'):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (w/2, h/2, d/2)
    obj.data.materials.append(material)
    return obj

# ── Helper: create cylinder (post) ──
def add_cylinder(x, y, z, r, h, material, name='post'):
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=r, depth=h, location=(x, y, z))
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(material)
    return obj

# ═══════════════════════════════════════
# ZONE A: Adventure Tower (12x12 ft deck at 13 ft, 14 ft total)
# 1 ft = 1 Blender unit
# ═══════════════════════════════════════

# Posts (4 at corners) — 6x6 actual = 0.5 ft diameter cylinder
post_positions = [(-6, -6, 0), (6, -6, 0), (-6, 6, 0), (6, 6, 0)]
for i, (px, py, pz) in enumerate(post_positions):
    add_cylinder(px, py, pz + 7, 0.25, 14, mat_wood, name=f'ZA_Post_{i+1}')

# Top beam at 14 ft elevation (y-level = 14)
# 6x6 beams along perimeter
add_beam(0, 0, 14, 12, 0.5, 0.5, mat_wood, 'ZA_Beam_Top_X')
add_beam(0, 0, 14, 0.5, 0.5, 12, mat_wood, 'ZA_Beam_Top_Y')

# Deck joists at 13 ft
for i in range(-5, 6):
    add_beam(0, i, 13, 12, 0.25, 0.25, mat_wood, f'ZA_Joist_{i}')

# Deck surface at 12.875 ft
add_beam(0, 0, 12.875, 12, 0.125, 12, mat_wood, 'ZA_Deck')

# Main frame at 10 ft
add_beam(0, 0, 10, 10, 0.5, 0.5, mat_wood, 'ZA_Beam_Mid_X')
add_beam(0, 0, 10, 0.5, 0.5, 10, mat_wood, 'ZA_Beam_Mid_Y')

# Cross braces (diagonal from top to mid frame)
for side in [-1, 1]:
    add_beam(3*side, 5, 12, 0.25, 0.25, 5.5, mat_steel, f'ZA_Brace_{side:+d}')

# ═══════════════════════════════════════
# ZONE B: Calisthenics Frame (10x5 ft, 12 ft tall)
# ═══════════════════════════════════════

# Posts (4 at corners) — 4x4 actual = 0.35 ft diameter cylinder
zb_x = 8  # 10 ft from Zone A center
post_b = [
    (zb_x - 5, -2.5, 0), (zb_x + 5, -2.5, 0),
    (zb_x - 5, 2.5, 0), (zb_x + 5, 2.5, 0)
]
for i, (px, py, pz) in enumerate(post_b):
    add_cylinder(px, py, pz + 6, 0.175, 12, mat_wood, name=f'ZB_Post_{i+1}')

# Top beam at 12 ft
add_beam(zb_x, 0, 12, 10, 0.4, 0.4, mat_wood, 'ZB_Beam_Top_X')
add_beam(zb_x, 0, 12, 0.4, 0.4, 5, mat_wood, 'ZB_Beam_Top_Y')

# Mid beam at 9 ft (monkey bar level)
add_beam(zb_x, 0, 9, 10, 0.3, 0.3, mat_wood, 'ZB_Beam_Mid_X')

# Pull-up bar (steel pipe at 12 ft, centered)
add_cylinder(zb_x, 0, 11.5, 0.06, 6, mat_steel, name='ZB_PullUp_Bar')

# Monkey bar rungs (horizontal bars at 9 ft)
for i in range(-4, 5):
    add_cylinder(zb_x + i*0.75, 0, 9.3, 0.03, 0.3, mat_steel, name=f'ZB_Monkey_Rung_{i}')

# Dip station (2 bars at different heights)
add_cylinder(zb_x - 2, -2, 3, 0.05, 4, mat_steel, name='ZB_Dip_Low')
add_cylinder(zb_x - 2, 2, 3.3, 0.05, 4, mat_steel, name='ZB_Dip_High')

# ═══════════════════════════════════════
# GROUND PLANE
# ═══════════════════════════════════════
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -0.01))
ground = bpy.context.active_object
ground.name = 'Ground'
ground.data.materials.append(mat_concrete)

# ═══════════════════════════════════════
# CAMERA SETUP FOR ORTHOGRAPHIC VIEWS
# ═══════════════════════════════════════

def setup_camera(location, target, name='camera', angle=45):
    cam = bpy.data.cameras.new(name=name)
    cam.type = 'ORTHO'
    cam.ortho_scale = 20
    cam.clip_start = 0.1
    cam.clip_end = 100
    
    cam_obj = bpy.data.objects.new(name, cam)
    cam_obj.location = location
    cam_obj.rotation_euler = (math.radians(angle), 0, 0)
    scene.collection.objects.link(cam_obj)
    
    # Track target
    track = cam_obj.constraints.new('TRACK_TO')
    track.target = bpy.data.objects.new('empty_target', None)
    track.target.location = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    return cam_obj

# ── Front view (looking from -Z) ──
setup_camera(
    location=(0, 0, 30),
    target=(0, 0, 7),
    name='Cam_Front',
    angle=0
)

# ── Top view (looking from +Y) ──
setup_camera(
    location=(0, 25, 0),
    target=(0, 0, 7),
    name='Cam_Top',
    angle=90
)

# ── Side view (looking from +X) ──
setup_camera(
    location=(20, 0, 0),
    target=(0, 0, 7),
    name='Cam_Side',
    angle=0
)

# ── Isometric view ──
setup_camera(
    location=(15, 15, 20),
    target=(0, 0, 7),
    name='Cam_Iso',
    angle=30
)

print("Scene ready. Cameras created.")
print("Run render: bpy.ops.render.render(write_st=True)")
