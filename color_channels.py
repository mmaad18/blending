import bpy

import sys
sys.path.append('C:\\Users\\mmbio\\Documents\\GitHub\\blending')

from basic_geometry import *

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

create_rbg_cube((0, 0, 0), (30 / 255, 230 / 255, 200 / 255), sliced=True)

# Create light sphere
material_emitting = create_material("EmittingMaterial", (1, 1, 1), emission_strength=0.25)
create_sphere((0, 0, 0), 40, material_emitting)

# Create camera
rotation = (60, 0, 130)
location = (4, 3.75, 3.05)
create_camera(location, rotation, ortho=True, scale=2, resolution=(750, 750))

locationInverse = (-8, -8, -6)
material_white = create_material("WhiteMaterial", (0.5, 0.5, 0.5))
create_plane(locationInverse, material_white, (20, 20), rotation)


