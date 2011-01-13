#This file is part of Yafaray Exporter Integration for Blender 2.5

from yafaray.ui import properties_yaf_camera
from yafaray.ui import properties_yaf_general_settings
from yafaray.ui import properties_yaf_integrator
from yafaray.ui import properties_yaf_material
from yafaray.ui import properties_yaf_object_light
from yafaray.ui import properties_yaf_texture
from yafaray.ui import properties_yaf_volume_integrator
from yafaray.ui import properties_yaf_world
from yafaray.ui import properties_yaf_AA_settings
from yafaray.ui import properties_yaf_object_light
#from yafaray.ui import properties_yaf_data_lamp
from yafaray.ui import yaf_light

# import properties_data_mesh from Blender, "as is"
# TODO: select only necessary elements

import properties_data_mesh
for member in dir(properties_data_mesh):
    subclass = getattr(properties_data_mesh, member)
    try:
        subclass.COMPAT_ENGINES.add('YAFA_RENDER')
    except:
        pass
del properties_data_mesh

# moved from yaf_export

import properties_render, properties_particle

for panel in [properties_render.RENDER_PT_render,
              properties_render.RENDER_PT_dimensions,
              properties_render.RENDER_PT_output,
              properties_particle.PARTICLE_PT_context_particles,
              properties_particle.PARTICLE_PT_emission,
              properties_particle.PARTICLE_PT_hair_dynamics,
              properties_particle.PARTICLE_PT_velocity,
              properties_particle.PARTICLE_PT_rotation,
              properties_particle.PARTICLE_PT_physics,
              properties_particle.PARTICLE_PT_boidbrain,
              properties_particle.PARTICLE_PT_render,
              properties_particle.PARTICLE_PT_draw,
              properties_particle.PARTICLE_PT_force_fields]:
    panel.COMPAT_ENGINES.add('YAFA_RENDER')

del properties_render, properties_particle

