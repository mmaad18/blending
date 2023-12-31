import bpy
import random
import math


def create_material(name, color, alpha=1.0, emission_strength=0.0):
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color, alpha)  # RGBA
    material.use_nodes = True

    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Alpha"].default_value = alpha
    bsdf.inputs["Base Color"].default_value = [*color, alpha]
    bsdf.inputs["Emission Strength"].default_value = emission_strength

    return material


def set_material_alpha(material, alpha):
    if material and material.use_nodes:
        # Assuming the use of a Principled BSDF shader
        for node in material.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                # Set the alpha value
                node.inputs['Alpha'].default_value = alpha

    return material


def create_plane(location, material, scale=(1.0, 1.0), rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=location)
    plane = bpy.context.active_object
    plane.scale = (scale[0], scale[1], 1)
    plane.rotation_euler = (math.radians(rotation[0]), math.radians(rotation[1]), math.radians(rotation[2]))
    plane.data.materials.append(material)

    return plane


def create_box(location, material, scale=(1.0, 1.0, 1.0)):
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=location)
    box = bpy.context.active_object
    box.scale = scale
    box.data.materials.append(material)

    return box


def create_sphere(location, radius, material):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, enter_editmode=False, align='WORLD', location=location)
    sphere = bpy.context.active_object
    sphere.data.materials.append(material)

    return sphere


def create_pipe(start_location, end_location, radius, material):
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


def create_array_of_cubes(dimension, spacing, pos_0=(0.0, 0.0, 0.0), alpha=1.0):
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


def create_rbg_cube(location, color=(1.0, 1.0, 1.0), alpha=0.75, sliced=False):
    R = color[0]
    G = color[1]
    B = color[2]

    single_material_red = create_material("SingleMaterialRed", (R, 0, 0))
    single_material_green = create_material("SingleMaterialGreen", (0, G, 0))
    single_material_blue = create_material("SingleMaterialBlue", (0, 0, B))
    combined_material = create_material("CombinedMaterial", (R, G, B), alpha)
    scale = (1, 0.3, 1)

    create_box(location, single_material_red, scale)
    create_box((location[0], 0.35 + location[1], location[2]), single_material_green, scale)
    create_box((location[0], 0.7 + location[1], location[2]), single_material_blue, scale)

    if sliced:
        return create_box((-0.05 + location[0], 0.35 + location[1], location[2]), combined_material, (1, 1.1, 1.1))
    else:
        return create_box((location[0], 0.35 + location[1], location[2]), combined_material, (1.1, 1.1, 1.1))


def create_array_of_rbg_cubes(dimension, spacing, pos_0=(0.0, 0.0, 0.0), alpha=0.75, sliced=False):
    cubes = []

    for i in range(dimension[0]):
        for j in range(dimension[1]):
            color = (random.random(), random.random(), random.random())
            x_pos = i * (1 + spacing) + pos_0[0]
            y_pos = pos_0[1]
            z_pos = j * (1 + spacing) + pos_0[2]
            cube = create_rbg_cube((x_pos, y_pos, z_pos), color, alpha, sliced)
            cubes.append(cube)

    return cubes


def create_camera(location, rotation, resolution=(1000, 1000), samples=1000, ortho=False, scale=5.0, lens=50.0, name="Camera"):
    cam_data = bpy.data.cameras.new(name)
    cam_object = bpy.data.objects.new(name, cam_data)

    # Set camera type
    if ortho:
        cam_object.data.type = 'ORTHO'
        cam_object.data.ortho_scale = scale
    else:
        cam_object.data.type = 'PERSP'
        cam_object.data.lens = lens

    # Set camera location and rotation
    cam_object.location = location
    cam_object.rotation_euler = (math.radians(rotation[0]), math.radians(rotation[1]), math.radians(rotation[2]))

    # Link the camera object to the scene
    bpy.context.collection.objects.link(cam_object)

    # Set to active camera
    bpy.context.scene.camera = cam_object

    # Set render settings
    bpy.context.scene.render.resolution_x = resolution[0]
    bpy.context.scene.render.resolution_y = resolution[1]
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = samples


def create_point_light(location, color=(1.0, 1.0, 1.0), energy=100, name="PointLight"):
    light_data = bpy.data.lights.new(name=name, type='POINT')
    light_data.color = color
    light_data.energy = energy

    # Create a new object with the light data
    light_object = bpy.data.objects.new(name=name, object_data=light_data)

    # Set light object location
    light_object.location = (location[0] + 1, location[1] + 1, location[2])

    # Link the light object to the scene
    bpy.context.collection.objects.link(light_object)

    return light_object


def create_spot_light(location, rotation, color=(1.0, 1.0, 1.0), energy=100, spot_size=100, blend=0, name="SpotLight"):
    light_data = bpy.data.lights.new(name=name, type='SPOT')
    light_data.color = color
    light_data.energy = energy
    light_data.spot_size = math.radians(spot_size)
    light_data.spot_blend = blend

    # Create a new object with the light data
    light_object = bpy.data.objects.new(name=name, object_data=light_data)

    # Set light object location and rotation
    light_object.location = location
    light_object.rotation_euler = (math.radians(rotation[0]), math.radians(rotation[1]), math.radians(rotation[2]))

    # Link the light object to the scene
    bpy.context.collection.objects.link(light_object)

    return light_object


def create_box_of_point_lights(xy=2, z=2, r=2, energy=100):
    create_point_light((-r, 0, 0), energy=energy)
    create_point_light((r, 0, 0), energy=energy)
    create_point_light((0, -r, 0), energy=energy)
    create_point_light((0, r, 0), energy=energy)
    create_point_light((0, 0, -r), energy=energy)
    create_point_light((0, 0, r), energy=energy)

    for x in (xy, -xy):
        for y in (xy, -xy):
            for z_sign in (1, -1):
                create_point_light((x, y, z * z_sign), energy=energy)


def create_convolution_pipes(start_array, end_array, start_cols, kernel_size, pipe_radius=0.02, box_size=1):
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
                    set_material_alpha(material, 1.0)
                    create_pipe(start_location, end_location, pipe_radius, material)


def create_pooling_pipes(start_array, end_array, start_cols, kernel_size, pipe_radius=0.02, box_size=1):
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

