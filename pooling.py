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
                    create_pipe(start_location, end_location, pipe_radius, material)


# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create arrays of boxes
first_array = create_array_of_cubes((4, 4), 0.05) # 5x5 array
second_array = create_array_of_cubes((2, 2), 0.05, pos_0=(1.05, 4, 1.05)) # 3x3 array

# Create sets of pipes to emulate convolution
create_set_of_pipes(first_array, second_array, 4, 2)

# Create kernel
kernel_material = create_material("KernelMaterial", (0.6, 0, 0), 0.8)
create_box((2.625, 0, 2.625), kernel_material, (2.15, 1.1, 2.15))
create_box((2.1, 4, 2.1), kernel_material, (1.1, 1.1, 1.1))
