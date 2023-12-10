import bpy

def create_material(name, color, alpha):
    """Create a new material with specified color and alpha."""
    material = bpy.data.materials.new(name=name)
    material.diffuse_color = (*color, alpha)  # RGBA
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Alpha"].default_value = alpha
    return material

def create_box(location, material):
    """Create a single cube at a specified location and assign a material to it."""
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.data.materials.append(material)

def create_row_of_boxes(number_of_boxes, spacing, color, alpha):
    """Create a row of boxes with specified spacing and material."""
    material = create_material("BoxMaterial", color, alpha)
    for i in range(number_of_boxes):
        for j in range(number_of_boxes):
            x_location = i * (1 + spacing)
            z_location = j * (1 + spacing)
            create_box((x_location, 0, z_location), material)


# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a row of 5 boxes with a spacing of 0.1 units and 50% opacity
create_row_of_boxes(5, 0.1, (1, 0, 0), 0.5)  # Red color, 50% opacity


