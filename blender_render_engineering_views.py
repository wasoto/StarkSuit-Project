#!/usr/bin/env python3
"""
Blender rendering script for outdoor calisthenics fortress engineering drawings.
Run this in Blender's Scripting tab (Shift+F11 → Open → Alt+P) or from terminal:
    blender --background --python render_engineering_views.py

Outputs 4 orthographic views to /workspace/blender_output/
"""

import bpy
import math
import os
import sys

# ── Paths ──
OUTPUT_DIR = '/workspace/blender_output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Clean scene
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj, do_unlink=True)
for coll in bpy.data.collections:
    bpy.data.collections.remove(coll)
for mat in bpy.data.materials:
    bpy.data.materials.remove(mat)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
scene.cycles.diffuse_bounces = 3
scene.cycles.glossy_bounces = 3
scene.cycles.transparent_min_bounces = 4
scene.render.film_transparent = False
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'

# ── Materials ──
def make_mat(name, color, roughness=0.7, metalness=0.0, alpha=1.0):
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = color + (alpha,)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metalness
    return m

WOOD = make_mat('Wood', (0.55, 0.35, 0.18), 0.75)
STEEL = make_mat('Steel', (0.25, 0.25, 0.25), 0.3, 0.9)
CONC = make_mat('Concrete', (0.45, 0.45, 0.45), 0.9)
GRASS = make_mat('Grass', (0.15, 0.35, 0.12), 0.95)
NET = make_mat('Netting', (0.1, 0.45, 0.1), 0.8, alpha=0.25)
DECK = make_mat('Deck', (0.5, 0.3, 0.15), 0.8)
ROPE = make_mat('Rope', (0.45, 0.35, 0.2), 0.9)
SHADE = make_mat('Shade', (0.85, 0.85, 0.8), 0.6, alpha=0.4)

# ── Helpers ──
def box(w, h, d, loc, mat, name):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (w/2, h/2, d/2)
    obj.data.materials.append(mat)
    return obj

def cyl_v2(r, h, loc, mat, name, segs=12):
    """Cylinder along Y axis"""
    bpy.ops.mesh.primitive_cylinder_add(vertices=segs, radius=r, depth=h, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    return obj

def cyl_v(r, h, loc, mat, name, segs=12):
    """Cylinder along Z axis"""
    bpy.ops.mesh.primitive_cylinder_add(vertices=segs, radius=r, depth=h, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    obj.rotation_euler = (math.pi/2, 0, 0)
    return obj

# ── Ground ──
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -0.02))
ground = bpy.context.active_object
ground.name = 'Ground'
ground.data.materials.append(GRASS)

# ═══════════════════════════════════════════
# ZONE A: Adventure Tower (12x12 ft, 14 ft tall)
# Deck at 13 ft, posts 14 ft tall
# ═══════════════════════════════════════════

# 6x6 posts (0.5 ft dia, 14 ft tall) at 4 corners
for i, (x, y) in enumerate([(-6, -6), (6, -6), (-6, 6), (6, 6)]):
    cyl_v2(0.25, 14, (x, y, 7), WOOD, f'ZA_P{i+1}')

# Top beams at 14 ft
box(12, 0.5, 0.5, (0, 0, 14), WOOD, 'ZA_B_Top_X')
box(0.5, 0.5, 12, (0, 0, 14), WOOD, 'ZA_B_Top_Y')

# Deck joists at 13 ft
for i in range(-5, 6):
    box(12, 0.25, 0.25, (0, i, 13), WOOD, f'ZA_J{i:+d}')

# Deck surface at 12.875 ft
box(12, 0.125, 12, (0, 0, 12.94), DECK, 'ZA_Deck')

# Mid frame at 10 ft (10x5 ft)
box(10, 0.5, 0.5, (0, 0, 10), WOOD, 'ZA_B_Mid_X')
box(0.5, 0.5, 10, (0, 0, 10), WOOD, 'ZA_B_Mid_Y')

# Cross braces (45°)
for side in [-1, 1]:
    box(0.25, 0.25, 6, (side*4, 0, 12), STEEL, f'ZA_CB{side:+d}')

# Safety netting around deck
box(12, 1, 0.02, (0, -6, 13.5), NET, 'ZA_N_Front')
box(12, 1, 0.02, (0, 6, 13.5), NET, 'ZA_N_Rear')
box(0.02, 1, 12, (-6, 0, 13.5), NET, 'ZA_N_Left')
box(0.02, 1, 12, (6, 0, 13.5), NET, 'ZA_N_Right')

# ═══════════════════════════════════════════
# ZONE B: Calisthenics Frame (10x5 ft, 12 ft tall)
# ═══════════════════════════════════════════

zb_x = 8  # center X

# 4x4 posts (0.35 ft dia, 12 ft tall)
for i, (x, y) in enumerate([(zb_x-5, -2.5), (zb_x+5, -2.5), (zb_x-5, 2.5), (zb_x+5, 2.5)]):
    cyl_v2(0.175, 12, (x, y, 6), WOOD, f'ZB_P{i+1}')

# Top beams at 12 ft
box(10, 0.4, 0.4, (zb_x, 0, 12), WOOD, 'ZB_B_Top_X')
box(0.4, 0.4, 5, (zb_x, 0, 12), WOOD, 'ZB_B_Top_Y')

# Mid beam at 9 ft
box(10, 0.3, 0.3, (zb_x, 0, 9), WOOD, 'ZB_B_Mid_X')

# Pull-up bar (6 ft steel pipe at 12 ft)
cyl_v2(0.0625, 6, (zb_x, 0, 12), STEEL, 'ZB_PullUp')

# Monkey bar rungs at 9 ft (8 rungs, 1 ft spacing)
for i in range(-3.5, 4):
    cyl_v2(0.025, 0.25, (zb_x + i, 0, 9.15), STEEL, f'ZB_Monkey{i:.1f}')

# Dip station
cyl_v2(0.05, 0.4, (zb_x-2, -2.5, 2.33), STEEL, 'ZB_Dip_Low')
cyl_v2(0.05, 0.4, (zb_x-2, 2.5, 2.67), STEEL, 'ZB_Dip_High')
cyl_v2(0.05, 4, (zb_x-2, -2.5, 2), STEEL, 'ZB_Dip_P_L')
cyl_v2(0.05, 4, (zb_x-2, 2.5, 2), STEEL, 'ZB_Dip_P_R')

# ═══════════════════════════════════════════
# ACCESSORIES
# ═══════════════════════════════════════════

# Rope tower
for rx in [-3, 0, 3]:
    cyl_v2(0.02, 13, (rx, 4.5, 6.5), ROPE, f'ZA_Rope_{rx}')

# Disc obstacles
for rz in [3, 5, 7]:
    cyl_v2(0.3, 0.08, (0, rz, 10), STEEL, f'ZA_Disc{rz}')

# Swings
cyl_v2(0.015, 7, (-4, -5, 9.5), STEEL, 'ZA_Swing_L')
cyl_v2(0.015, 7, (4, -5, 9.5), STEEL, 'ZA_Swing_R')

# Tire swing
bpy.ops.mesh.primitive_torus_add(major_radius=0.4, minor_radius=0.08, location=(0, -5, 6.5))
bpy.context.active_object.name = 'ZA_Tire'
bpy.context.active_object.data.materials.append(WOOD)

# Shade sails
for sign in [-1, 1]:
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=1, y_subdivisions=1, size=1, location=(sign*6, 0, 13))
    sail = bpy.context.active_object
    sail.name = f'ZA_Shade{sign:+d}'
    sail.data.materials.append(SHADE)

# Hammock
cyl_v2(0.03, 2, (6.5, 6, 12), STEEL, 'ZA_Hammock')
cyl_v2(0.02, 3, (6.5, 6, 10.5), ROPE, 'ZA_Hammock_Rope')

# ═══════════════════════════════════════════
# FOUNDATION FOOTINGS
# ═══════════════════════════════════════════

for x, y in [(-6, -6), (6, -6), (-6, 6), (6, 6)]:
    cyl_v2(0.7, 0.3, (x, y, -0.15), CONC, f'F{len(os.listdir(OUTPUT_DIR))}')

for x, y in [(zb_x-5, -2.5), (zb_x+5, -2.5), (zb_x-5, 2.5), (zb_x+5, 2.5)]:
    cyl_v2(0.5, 0.3, (x, y, -0.15), CONC, f'Fb{len(os.listdir(OUTPUT_DIR))}')

# ═══════════════════════════════════════════
# LIGHTING
# ═══════════════════════════════════════════

for obj in bpy.data.objects:
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

bpy.ops.object.light_add(type='SUN', location=(5, -8, 12))
k = bpy.context.active_object; k.name = 'Key'; k.data.energy = 8; k.data.angle = 0.5

bpy.ops.object.light_add(type='SUN', location=(-5, 5, 8))
f = bpy.context.active_object; f.name = 'Fill'; f.data.energy = 3; f.data.angle = 0.7

bpy.ops.object.light_add(type='SUN', location=(0, -10, 3))
r = bpy.context.active_object; r.name = 'Rim'; r.data.energy = 2; r.data.angle = 0.5

# ═══════════════════════════════════════════
# RENDER 4 VIEWS
# ═══════════════════════════════════════════

views = [
    ('front',    (0, -15, 0), (0, 0, 0)),           # Front elevation
    ('top',      (0, 0, 20),  (math.radians(90), 0, 0)),  # Top/Plan view
    ('right',    (20, 0, 0),  (0, 0, math.radians(90))),  # Right elevation
    ('iso',      (18, 18, 20), (math.radians(35), 0, math.radians(45))),  # Isometric
]

for name, loc, rot in views:
    cam_data = bpy.data.cameras.new(f'Cam_{name}')
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = 25
    cam_data.clip_start = 0.5
    cam_data.clip_end = 60
    
    cam_obj = bpy.data.objects.new(f'Camera_{name}', cam_data)
    cam_obj.location = loc
    cam_obj.rotation_euler = rot
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # Tracking
    empty = bpy.data.objects.new('Empty', None)
    empty.location = (2, 0, 7)
    scene.collection.objects.link(empty)
    
    track = cam_obj.constraints.new('TRACK_TO')
    track.target = empty
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    filepath = os.path.join(OUTPUT_DIR, f'{name}_elevation.png')
    scene.render.filepath = filepath
    
    print(f'Rendering {name.upper()} elevation...')
    bpy.ops.render.render(write_st=True)
    print(f'  → {filepath} ({os.path.getsize(filepath):,} bytes)')

print(f'\nAll views rendered to: {OUTPUT_DIR}')
for f in sorted(os.listdir(OUTPUT_DIR)):
    fpath = os.path.join(OUTPUT_DIR, f)
    print(f'  {f} ({os.path.getsize(fpath):,} bytes)')
