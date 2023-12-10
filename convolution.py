import bpy
import random


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


def create_array_of_boxes(number_of_boxes, spacing, pos_0=(0,0,0), alpha=1):
    """Create a row of boxes with specified spacing and material."""
    for i in range(number_of_boxes):
        for j in range(number_of_boxes):
            color = (random.random(), random.random(), random.random())
            material = create_material("BoxMaterial", color, alpha)
            x_pos = i * (1 + spacing) + pos_0[0]
            y_pos = pos_0[1]
            z_pos = j * (1 + spacing) + pos_0[2]
            create_box((x_pos, y_pos, z_pos), material)


# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

create_array_of_boxes(5, 0.05)
create_array_of_boxes(3, 0.05, pos_0=(1,4,1))



