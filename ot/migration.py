# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.app.handlers import persistent

from .. import bl_info


def copy_attributes(source, destination, mapping):
    print("Copying attributes from", source, "to", destination)
    attributes = [a for a in dir(source) if not a.startswith("__")]
    for attr in attributes:
        if attr in mapping:
            if mapping[attr] is None:
                continue
            else:
                attr_v4 = mapping[attr]
        else:
            attr_v4 = attr
        if hasattr(source, attr):
            attr_value = getattr(source, attr)
            print("  Copying attribute:", attr, "with value:", attr_value, "to attribute v4:", attr_v4)
            setattr(destination, attr_v4, attr_value)


@persistent
def migration(_dummy):
    scene = bpy.context.scene
    print("scene.world.texture", scene.world.texture, "scene.world.texture", scene.world.texture)
    for tex in bpy.data.textures:
        if tex is not None:
            # set the correct texture type on file load....
            # converts old files, where property yaf_tex_type wasn't defined
            print(bl_info["name"], "Handler: Convert Yafaray texture \"{0}\" with texture type: \"{1}\" to \"{2}\""
                  .format(tex.name, tex.yaf_tex_type, tex.type))
            tex.yaf_tex_type = tex.type
    for mat in bpy.data.materials:
        if mat is not None:
            # from old scenes, convert old blend material Enum properties into the new string properties
            if mat.mat_type == "blend":
                if not mat.is_property_set("material1name") or not mat.material1name:
                    mat.material1name = mat.material1
                if not mat.is_property_set("material2name") or not mat.material2name:
                    mat.material2name = mat.material2
    # convert image output file type setting from blender to YafaRay's file type setting on file load, so that both
    # are the same...
    if scene.render.image_settings.file_format is not scene.img_output:
        scene.img_output = scene.render.image_settings.file_format

    # convert old world texture slot to dedicated YafaRay world texture parameter
    if (bpy.app.version < (2, 80, 0)
            and not scene.yafaray4.migration.migrated_to_v4
            and scene.world.active_texture is not None):
        print(bl_info["name"], "Handler: Initial 'one-off' migration from Yafaray v3 parameters")
        scene.world.texture = scene.world.active_texture
        scene.yafaray4.migration.migrated_to_v4 = True
        if hasattr(scene, "yafaray"):
            mapping_base = {
                #"name": None,
                "bl_rna": None,
                "rna_type": None,
            }
            mapping = {
                "verbosityLevels": None,
                "paramsBadgePosition": "params_badge_position",
                "saveLog": "save_log",
                "saveHTML": "save_html",
                "savePreset": "save_preset",
                "logPrintDateTime": "log_print_date_time",
                "consoleVerbosity": "console_verbosity",
                "logVerbosity": "log_verbosity",
                "drawRenderSettings": "draw_render_settings",
                "drawAANoiseSettings": "draw_aa_noise_settings",
                "customIcon": "custom_icon",
                "customFont": "custom_font",
                "fontScale": "font_scale",
            }
            mapping.update(mapping_base)
            copy_attributes(scene.yafaray.logging, scene.yafaray4.logging, mapping)
            mapping = mapping_base
            copy_attributes(scene.yafaray.noise_control, scene.yafaray4.noise_control, mapping)
            mapping = {
                "OBJECT_OT_CamRotReset": None,
                "OBJECT_OT_CamZoomIn": None,
                "OBJECT_OT_CamZoomOut": None,
                "objScale": "obj_scale",
                "rotZ": "rot_z",
                "lightRotZ": "light_rot_z",
                "keyLightPowerFactor": "key_light_power_factor",
                "fillLightPowerFactor": "fill_light_power_factor",
                "keyLightColor": "key_light_color",
                "fillLightColor": "fill_light_color",
                "previewRayDepth": "preview_ray_depth",
                "previewAApasses": "preview_aa_passes",
                "previewBackground": "preview_background",
                "previewObject": "preview_object",
                "camDist": "cam_dist",
                "camRot": "cam_rot",
            }
            mapping.update(mapping_base)
            copy_attributes(scene.yafaray.preview, scene.yafaray4.preview, mapping)
            mapping = {
                "renderPassItemsBasic": None,
                "renderInternalPassAdvanced": None,
                "renderPassAllItems": None,
                "renderPassItemsAO": None,
                "renderPassItemsDisabled": None,
                "renderPassItemsIndex": None,
                "renderPassItemsDebug": None,
                "renderPassItemsDepth": None,
                "objectEdgeThickness": "object_edge_thickness",
                "facesEdgeThickness": "faces_edge_thickness",
                "objectEdgeThreshold": "object_edge_threshold",
                "facesEdgeThreshold": "faces_edge_threshold",
                "objectEdgeSmoothness": "object_edge_smoothness",
                "facesEdgeSmoothness": "faces_edge_smoothness",
                "toonEdgeColor": "toon_edge_color",
                "toonPreSmooth": "toon_pre_smooth",
                "toonPostSmooth": "toon_post_smooth",
                "toonQuantization": "toon_quantization",
                "pass_Combined": "pass_Combined",
                "pass_Depth": "pass_depth",
                "pass_Vector": "pass_vector",
                "pass_Normal": "pass_normal",
                "pass_UV": "pass_uv",
                "pass_Color": "pass_color",
                "pass_Emit": "pass_emit",
                "pass_Mist": "pass_mist",
                "pass_Diffuse": "pass_diffuse",
                "pass_Spec": "pass_spec",
                "pass_AO": "pass_ao",
                "pass_Env": "pass_env",
                "pass_Indirect": "pass_indirect",
                "pass_Shadow": "pass_shadow",
                "pass_Reflect": "pass_reflect",
                "pass_Refract": "pass_refract",
                "pass_IndexOB": "pass_index_ob",
                "pass_IndexMA": "pass_index_ma",
                "pass_DiffDir": "pass_diff_dir",
                "pass_DiffInd": "pass_diff_ind",
                "pass_DiffCol": "pass_diff_col",
                "pass_GlossDir": "pass_gloss_dir",
                "pass_GlossInd": "pass_gloss_ind",
                "pass_GlossCol": "pass_gloss_col",
                "pass_TransDir": "pass_trans_dir",
                "pass_TransInd": "pass_trans_ind",
                "pass_TransCol": "pass_trans_col",
                "pass_SubsurfaceDir": "pass_subsurface_dir",
                "pass_SubsurfaceInd": "pass_subsurface_ind",
                "pass_SubsurfaceCol": "pass_subsurface_col",
            }
            mapping.update(mapping_base)
            copy_attributes(scene.yafaray.passes, scene.yafaray4.passes, mapping)

            # for material in bpy.data.materials:
            #     print(material, material.name)
            #     material.use_nodes = True
            #     for texture_slot in material.texture_slots:
            #         if texture_slot is not None:
            #             #print(texture_slot, dir(texture_slot))
            #             for attr in dir(texture_slot):
            #                 print(attr, getattr(texture_slot, attr))
            #             node_created = material.node_tree.nodes.new(type="YafaRay4TextureNode1")
            #             node_created.name = "test"

            mapping = {
                "output_node": None,
            }
            mapping.update(mapping_base)
            for material in bpy.data.materials:
                for texture_slot_id in range(min(len(material.use_textures), len(material.yafaray4.use_textures))):
                    material.yafaray4.use_textures[texture_slot_id] = material.use_textures[texture_slot_id]
                material.yafaray4.texture_slots.clear()
                for texture_slot in material.texture_slots:
                    yaf4_texture_slot = material.yafaray4.texture_slots.add()
                    copy_attributes(texture_slot, yaf4_texture_slot, mapping)


