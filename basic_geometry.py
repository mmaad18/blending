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


def create_box(location, material, scale=(1, 1, 1)):
    """Create a single cube at a specified location, size, and assign a material to it."""
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.scale = scale
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


def create_array_of_cubes(dimension, spacing, pos_0=(0, 0, 0), alpha=1):
    """Create a row of boxes with specified spacing and material."""
    boxes = []
    for i in range(dimension[0]):
        for j in range(dimension[1]):
            color = (random.random(), random.random(), random.random())
            material = create_material("BoxMaterial", color, alpha)
            x_pos = i * (1 + spacing) + pos_0[0]
            y_pos = pos_0[1]
            z_pos = j * (1 + spacing) + pos_0[2]
            box = create_box((x_pos, y_pos, z_pos), material)
            boxes.append(box)
    return boxes