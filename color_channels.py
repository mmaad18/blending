import bpy
import random
import math

import sys
sys.path.append('C:\\Users\\mmbio\\Documents\\GitHub\\blending')

from basic_geometry import *

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

R = 30/255
G = 230/255
B = 200/255

single_material_red = create_material("SingleMaterialRed", (R, 0, 0), 1)
single_material_green = create_material("SingleMaterialGreen", (0, G, 0), 1)
single_material_blue = create_material("SingleMaterialBlue", (0, 0, B), 1)
combined_material = create_material("CombinedMaterial", (R, G, B), 0.75)
scale = (1, 0.3, 1)

create_box((0, 0, 0), single_material_red, scale)
create_box((0, 0.35, 0), single_material_green, scale)
create_box((0, 0.7, 0), single_material_blue, scale)
create_box((-0.15, 0.35, 0), combined_material, (0.8, 1.1, 1.1))


