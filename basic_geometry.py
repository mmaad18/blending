import bpy
import random
import math


def create_material(name, color, alpha=1):
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color, alpha)  # RGBA
    material.use_nodes = True

    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Alpha"].default_value = alpha
    bsdf.inputs["Base Color"].default_value = [*color, alpha]

    return material


def create_plane(location, material, scale=(1, 1), rotation=(0, 0, 0)):
    # Create a new plane
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=location)
    plane = bpy.context.active_object

    # Apply scaling
    plane.scale = (scale[0], scale[1], 1)

    # Apply rotation (Blender uses radians, not degrees)
    plane.rotation_euler = (math.radians(rotation[0]), math.radians(rotation[1]), math.radians(rotation[2]))

    plane.data.materials.append(material)


def create_box(location, material, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=location)
    box = bpy.context.active_object
    box.scale = scale
    box.data.materials.append(material)
    return box


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


def create_array_of_cubes(dimension, spacing, pos_0=(0, 0, 0), alpha=1):
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


def create_camera(name, location, rotation):
    # Create a new camera data block
    cam_data = bpy.data.cameras.new(name)

    # Create a new object with the camera data
    cam_object = bpy.data.objects.new(name, cam_data)

    # Set camera location and rotation
    cam_object.location = location
    cam_object.rotation_euler = (math.radians(rotation[0]), math.radians(rotation[1]), math.radians(rotation[2]))

    # Link the camera object to the scene
    bpy.context.collection.objects.link(cam_object)

    # Set the active camera (optional, if you want this to be the active scene camera)
    bpy.context.scene.camera = cam_object


def create_point_light(name, location, color=(1, 1, 1), energy=100):
    # Create a new light data block
    light_data = bpy.data.lights.new(name=name, type='POINT')

    # Set light color and energy
    light_data.color = color
    light_data.energy = energy

    # Create a new object with the light data
    light_object = bpy.data.objects.new(name=name, object_data=light_data)

    # Set light object location
    light_object.location = location

    # Link the light object to the scene
    bpy.context.collection.objects.link(light_object)

    return light_object





