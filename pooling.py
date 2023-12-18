import bpy
import random
import math

import sys
sys.path.append('C:\\Users\\mmbio\\Documents\\GitHub\\blending')

from basic_geometry import *


def create_set_of_pipes(start_array, end_array, start_cols, kernel_size, pipe_radius=0.02, box_size=1):
    half_box_size = box_size / 2  # Half the size of the box

    # Iterate over each box in the end_array
    for end_idx, end_box in enumerate(end_array):
        # Calculate the corresponding top-left corner in the start_array for this end_box
        start_row = (end_idx // (start_cols // kernel_size)) * kernel_size
        start_col = (end_idx % (start_cols // kernel_size)) * kernel_size

        # Create pipes from the kernel_size x kernel_size segment starting at (start_row, start_col)
        for i in range(kernel_size):
            for j in range(kernel_size):
                idx = (start_row + i) * start_cols + (start_col + j)
                if idx < len(start_array):
                    start_box = start_array[idx]

                    # For pooling, connect the center of each start box to the center of the end box
                    start_location = (start_box.location[0], start_box.location[1] + half_box_size, start_box.location[2])
                    end_location = (end_box.location[0], end_box.location[1] - half_box_size, end_box.location[2])

                    material = end_box.data.materials[0]  # Use the material of the end_box
                    set_material_alpha(material, 1.0)
                    create_pipe(start_location, end_location, pipe_radius, material)


# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create arrays of boxes
first_array = create_array_of_rbg_cubes((4, 4), 0.15, alpha=0.6)
second_array = create_array_of_rbg_cubes((2, 2), 0.15, pos_0=(1.15, 4, 1.15), alpha=0.6)

# Create sets of pipes to emulate convolution
create_set_of_pipes(first_array, second_array, 4, 2)

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



