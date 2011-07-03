#This file is part of Yafaray Exporter Integration for Blender 2.5

from yafaray.ui import properties_yaf_render
from yafaray.ui import properties_yaf_camera
from yafaray.ui import properties_yaf_material
from yafaray.ui import properties_yaf_mat_diffuse
from yafaray.ui import properties_yaf_mat_specular
from yafaray.ui import properties_yaf_texture
from yafaray.ui import properties_yaf_world
from yafaray.ui import properties_yaf_strand
from bl_ui import properties_object
from yafaray.ui import properties_yaf_object
from yafaray.ui import properties_yaf_light
from yafaray.ui import properties_yaf_convert
from bl_ui import properties_particle
for member in dir(properties_particle):  # add all particle panels from blender
    subclass = getattr(properties_particle, member)
    try:
        subclass.COMPAT_ENGINES.add('YAFA_RENDER')
    except:
        pass
del properties_particle
from bl_ui import properties_data_mesh
for member in dir(properties_data_mesh):  # add all object data panels from blender
    subclass = getattr(properties_data_mesh, member)
    try:
        subclass.COMPAT_ENGINES.add('YAFA_RENDER')
    except:
        pass
del properties_data_mesh
