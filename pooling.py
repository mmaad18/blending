import bpy

import sys
sys.path.append('C:\\Users\\mmbio\\Documents\\GitHub\\blending')

from basic_geometry import *


# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create arrays of boxes
first_array = create_array_of_rbg_cubes((4, 4), 0.15, alpha=0.6)
second_array = create_array_of_rbg_cubes((2, 2), 0.15, pos_0=(1.15, 4, 1.15), alpha=0.6)

# Create sets of pipes to emulate convolution
create_pooling_pipes(first_array, second_array, 4, 2)

# Create kernel
kernel_material = create_material("KernelMaterial", (0.6, 0, 0), 0.7)
create_box((2.875, 0.35, 2.875), kernel_material, (2.35, 1.2, 2.35))
create_box((2.3, 4.35, 2.3), kernel_material, (1.2, 1.2, 1.2))

# Create light
material_emitting = create_material("EmittingMaterial", (1, 1, 1), emission_strength=0.25)
create_sphere((0, 0, 0), 50, material_emitting)

# Create camera
rotation = (60, 0, 130)
location = (12, 10.5, 10)
create_camera(location, rotation, ortho=True, scale=7, resolution=(750, 750))

locationInverse = (-20, -20, -16)
material_white = create_material("WhiteMaterial", (0.5, 0.5, 0.5))
create_plane(locationInverse, material_white, (50, 50), rotation)



