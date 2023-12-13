import bpy
import random
import math

import sys
sys.path.append('C:\\Users\\mmbio\\Documents\\GitHub\\blending')

from basic_geometry import *


def create_set_of_pipes(start_array, end_array, start_cols, kernel_size, pipe_radius=0.03, box_size=1):
    half_box_size = box_size / 2  # Half the size of the box

    # Iterate over each box in the end_array
    for end_idx, end_box in enumerate(end_array):
        # Calculate the corresponding top-left corner in the start_array for this end_box
        start_row = end_idx // (start_cols - kernel_size + 1)
        start_col = end_idx % (start_cols - kernel_size + 1)

        # Create pipes from the 3x3 segment starting at (start_row, start_col)
        for i in range(kernel_size):
            for j in range(kernel_size):
                idx = (start_row + i) * start_cols + (start_col + j)
                if idx < len(start_array):
                    start_box = start_array[idx]

                    start_location = (start_box.location[0], start_box.location[1] + half_box_size, start_box.location[2])
                    end_location = (end_box.location[0], end_box.location[1] - half_box_size, end_box.location[2])

                    material = end_box.data.materials[0]
                    create_pipe(start_location, end_location, pipe_radius, material)


# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create arrays of boxes
first_array = create_array_of_cubes((5, 5), 0.05) # 5x5 array
second_array = create_array_of_cubes((3, 3), 0.05, pos_0=(1.05, 4, 1.05)) # 3x3 array

# Create sets of pipes to emulate convolution
create_set_of_pipes(first_array, second_array, 5, 3)

# Create kernel
kernel_material = create_material("KernelMaterial", (0.6, 0, 0), 0.8)
create_box((3.15, 0, 3.15), kernel_material, (3.15, 1.1, 3.15))
create_box((3.15, 4, 3.15), kernel_material, (1.1, 1.1, 1.1))
