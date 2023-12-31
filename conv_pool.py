import bpy

import sys
sys.path.append('C:\\Users\\mmbio\\Documents\\GitHub\\blending')

from basic_geometry import *


# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create arrays of boxes
first_array = create_array_of_rbg_cubes((6, 6), 0.15, alpha=0.5)
second_array = create_array_of_rbg_cubes((4, 4), 0.15, pos_0=(1.15, 4, 1.15), alpha=0.6)
third_array = create_array_of_rbg_cubes((2, 2), 0.15, pos_0=(2.3, 8, 2.3), alpha=0.6)

# Create sets of pipes to emulate convolution
create_convolution_pipes(first_array, second_array, 6, 3)
create_pooling_pipes(second_array, third_array, 4, 2)

# Create kernel
kernel_material_red = create_material("KernelMaterial", (0.6, 0, 0), 0.7)
kernel_material_blue = create_material("KernelMaterial", (0, 0, 0.6), 0.7)
create_box((4.6, 0.35, 4.6), kernel_material_red, (3.5, 1.2, 3.5))
create_box((4.6, 4.35, 4.6), kernel_material_red, (1.2, 1.2, 1.2))
create_box((1.725, 4.35, 4.025), kernel_material_blue, (2.35, 1.2, 2.35))
create_box((2.3, 8.35, 3.45), kernel_material_blue, (1.2, 1.2, 1.2))

# Create light
material_emitting = create_material("EmittingMaterial", (1, 1, 1), emission_strength=0.25)
create_sphere((0, 0, 0), 50, material_emitting)

# Create camera
rotation = (60, 0, 130)
location = (12, 10.5, 10)
create_camera(location, rotation, ortho=True, scale=11, resolution=(750, 750))

locationInverse = (-20, -20, -16)
material_white = create_material("WhiteMaterial", (0.5, 0.5, 0.5))
create_plane(locationInverse, material_white, (50, 50), rotation)

