#This file is part of Yafaray Exporter Integration for Blender 2.5
from . import properties_yaf_render
from . import properties_yaf_camera
from . import properties_yaf_material
from . import properties_yaf_texture
from . import properties_yaf_world
from . import properties_yaf_strand
from . import properties_yaf_object
from . import properties_yaf_light

from bl_ui import properties_object as properties_object
for member in dir(properties_object):  # add all "object" panels from blender
    subclass = getattr(properties_object, member)
    try:
        subclass.COMPAT_ENGINES.add('YAFA_RENDER')
    except:
        pass
del properties_object

from bl_ui import properties_particle as properties_particle
for member in dir(properties_particle):  # add all "particle" panels from blender
    subclass = getattr(properties_particle, member)
    try:
        subclass.COMPAT_ENGINES.add('YAFA_RENDER')
    except:
        pass
del properties_particle

from bl_ui import properties_data_mesh as properties_data_mesh
for member in dir(properties_data_mesh):  # add all "object data" panels from blender
    subclass = getattr(properties_data_mesh, member)
    try:
        subclass.COMPAT_ENGINES.add('YAFA_RENDER')
    except:
        pass
del properties_data_mesh

from bl_ui import properties_data_speaker as properties_data_speaker
for member in dir(properties_data_speaker):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_data_speaker, member)
    try:
        subclass.COMPAT_ENGINES.add('YAFA_RENDER')
    except:
        pass
del properties_data_speaker
