import bpy
import random
import math


def create_material(name, color, alpha):
    """Create a new material with specified color and alpha."""
    material = bpy.data.materials.new(name=name)
    material.diffuse_color = (*color, alpha)  # RGBA
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Alpha"].default_value = alpha
    return material


def create_box(location, material, size=1):
    """Create a single cube at a specified location, size, and assign a material to it."""
    bpy.ops.mesh.primitive_cube_add(size=size, enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.data.materials.append(material)
    return obj


def create_pipe(start_location, end_location, radius, material):
    """Create a pipe (cylinder) between two points with a specified material."""
    # Calculate the distance and midpoint between the start and end locations
    midpoint = [(s + e) / 2 for s, e in zip(start_location, end_location)]
    distance = math.sqrt(sum([(s - e) ** 2 for s, e in zip(start_location, end_location)]))

    # Create the cylinder at the midpoint
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=distance, location=midpoint)

    # Rotate the cylinder to align with the start and end points
    dx, dy, dz = [e - s for s, e in zip(start_location, end_location)]
    phi = math.atan2(dy, dx)
    theta = math.acos(dz / distance)
    bpy.context.object.rotation_euler[1] = theta
    bpy.context.object.rotation_euler[2] = phi

    # Assign material to the cylinder
    pipe = bpy.context.active_object
    pipe.data.materials.append(material)


def create_array_of_boxes(size, spacing, pos_0=(0, 0, 0), alpha=1):
    """Create a row of boxes with specified spacing and material."""
    boxes = []
    for i in range(size):
        for j in range(size):
            color = (random.random(), random.random(), random.random())
            material = create_material("BoxMaterial", color, alpha)
            x_pos = i * (1 + spacing) + pos_0[0]
            y_pos = pos_0[1]
            z_pos = j * (1 + spacing) + pos_0[2]
            box = create_box((x_pos, y_pos, z_pos), material)
            boxes.append(box)
    return boxes


def create_set_of_pipes(start_array, end_array, rows, cols, pipe_radius, box_size=1):
    """Create pipes to emulate convolution from a 3x3 segment of start_array to blocks in end_array."""
    kernel_size = 3  # Assuming a kernel_size of 3 for simplicity
    half_box_size = box_size / 2  # Half the size of the box to calculate face centers

    for row in range(0, rows - 2, kernel_size):
        for col in range(0, cols - 2, kernel_size):
            start_idx = row * cols + col
            end_idx = (row // kernel_size) * (cols // kernel_size) + (col // kernel_size)

            if end_idx < len(end_array):
                for i in range(kernel_size):
                    for j in range(kernel_size):
                        idx = start_idx + i * cols + j
                        if idx < len(start_array):
                            start_box = start_array[idx]
                            end_box = end_array[end_idx]

                            # Adjust start and end locations to the centers of the front and back faces of the boxes
                            start_location = (start_box.location[0], start_box.location[1] + half_box_size, start_box.location[2])
                            end_location = (end_box.location[0], end_box.location[1] - half_box_size, end_box.location[2])

                            material = end_box.data.materials[0]
                            create_pipe(start_location, end_location, pipe_radius, material)


# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create arrays of boxes
first_array = create_array_of_boxes(5, 0.05) # 5x5 array
second_array = create_array_of_boxes(3, 0.05, pos_0=(1.05, 4, 1.05)) # 3x3 array

# Pipe parameters
pipe_radius = 0.02
pipe_material = create_material("PipeMaterial", (0, 0, 1), 1)  # Blue color

# Create sets of pipes to emulate convolution
create_set_of_pipes(first_array, second_array, 5, 5, pipe_radius)
