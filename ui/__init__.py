#This file is part of Yafaray Exporter Integration for Blender 2.5

from yafaray.ui import properties_yaf_render
from yafaray.ui import properties_yaf_camera
from yafaray.ui import properties_yaf_material
from yafaray.ui import properties_yaf_texture
from yafaray.ui import properties_yaf_world

try:
    import properties_object
    properties_object.unregister()
    from yafaray.ui import properties_yaf_object
    properties_object.register()
    bl_ui = False

except ImportError:  # API changes since rev. 35667
    import bl_ui.properties_object
    from yafaray.ui import properties_yaf_object
    bl_ui = True

from yafaray.ui import properties_yaf_light
from yafaray.ui import properties_yaf_convert

if bl_ui:  # API changes since rev. 35667
    import bl_ui.properties_particle
    import bl_ui.properties_data_mesh
    print("Blender Revision >= 35667")
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

else:
    import properties_particle
    import properties_data_mesh
    print("Blender Revision < 35667")
    panelSet = [
    properties_particle.PARTICLE_PT_context_particles,
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
    properties_data_mesh.MESH_MT_vertex_group_specials
    ]

    for panel in panelSet:
        panel.COMPAT_ENGINES.add('YAFA_RENDER')

    del properties_particle, properties_data_mesh
