#This file is part of Yafaray Exporter Integration for Blender 2.5

from yafaray.ui import properties_yaf_render

from yafaray.ui import properties_yaf_camera
from yafaray.ui import properties_yaf_material
from yafaray.ui import properties_yaf_texture
from yafaray.ui import properties_yaf_world
import bl_ui.properties_object as properties_object
#properties_object.unregister()
from yafaray.ui import properties_yaf_object
#properties_object.register()
from yafaray.ui import properties_yaf_light
from yafaray.ui import properties_yaf_convert

import bl_ui.properties_particle
import bl_ui.properties_data_mesh

panelSet = [
bl_ui.properties_particle.PARTICLE_PT_context_particles,
bl_ui.properties_particle.PARTICLE_PT_emission,
bl_ui.properties_particle.PARTICLE_PT_hair_dynamics,
bl_ui.properties_particle.PARTICLE_PT_velocity,
bl_ui.properties_particle.PARTICLE_PT_rotation,
bl_ui.properties_particle.PARTICLE_PT_physics,
bl_ui.properties_particle.PARTICLE_PT_boidbrain,
bl_ui.properties_particle.PARTICLE_PT_render,
bl_ui.properties_particle.PARTICLE_PT_draw,
bl_ui.properties_particle.PARTICLE_PT_force_fields,
bl_ui.properties_data_mesh.DATA_PT_context_mesh,
bl_ui.properties_data_mesh.DATA_PT_custom_props_mesh,
bl_ui.properties_data_mesh.DATA_PT_normals,
bl_ui.properties_data_mesh.DATA_PT_settings,
bl_ui.properties_data_mesh.DATA_PT_shape_keys,
bl_ui.properties_data_mesh.DATA_PT_texface,
bl_ui.properties_data_mesh.DATA_PT_uv_texture,
bl_ui.properties_data_mesh.DATA_PT_vertex_colors,
bl_ui.properties_data_mesh.DATA_PT_vertex_groups,
bl_ui.properties_data_mesh.MESH_MT_shape_key_specials,
bl_ui.properties_data_mesh.MESH_MT_vertex_group_specials
]

for panel in panelSet:
    panel.COMPAT_ENGINES.add('YAFA_RENDER')

del bl_ui.properties_particle, bl_ui.properties_data_mesh
