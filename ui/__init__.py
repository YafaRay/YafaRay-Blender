#This file is part of Yafaray Exporter Integration for Blender 2.5

from yafaray.ui import properties_yaf_render_control
from yafaray.ui import properties_yaf_general_settings
from yafaray.ui import properties_yaf_integrator
from yafaray.ui import properties_yaf_AA_settings
from yafaray.ui import properties_yaf_render_output

from yafaray.ui import properties_yaf_camera
from yafaray.ui import properties_yaf_material
from yafaray.ui import properties_yaf_texture
from yafaray.ui import properties_yaf_volume_integrator
from yafaray.ui import properties_yaf_world
from yafaray.ui import properties_yaf_object_light
from yafaray.ui import properties_yaf_light
from yafaray.ui import properties_yaf_convert

import properties_particle, properties_data_mesh

for panel in [properties_particle.PARTICLE_PT_context_particles,
              properties_particle.PARTICLE_PT_emission,
              properties_particle.PARTICLE_PT_hair_dynamics,
              properties_particle.PARTICLE_PT_velocity,
              properties_particle.PARTICLE_PT_rotation,
              properties_particle.PARTICLE_PT_physics,
              properties_particle.PARTICLE_PT_boidbrain,
              properties_particle.PARTICLE_PT_render,
              properties_particle.PARTICLE_PT_draw,
              properties_particle.PARTICLE_PT_force_fields,
              properties_data_mesh.DATA_PT_context_mesh,
              properties_data_mesh.DATA_PT_custom_props_mesh,
              properties_data_mesh.DATA_PT_normals,
              properties_data_mesh.DATA_PT_settings,
              properties_data_mesh.DATA_PT_shape_keys,
              properties_data_mesh.DATA_PT_texface,
              properties_data_mesh.DATA_PT_uv_texture,
              properties_data_mesh.DATA_PT_vertex_colors,
              properties_data_mesh.DATA_PT_vertex_groups,
              properties_data_mesh.MESH_MT_shape_key_specials,
              properties_data_mesh.MESH_MT_vertex_group_specials]:
    panel.COMPAT_ENGINES.add('YAFA_RENDER')

del properties_particle, properties_data_mesh

