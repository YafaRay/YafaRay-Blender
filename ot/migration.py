# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.app.handlers import persistent
from bpy.props import PointerProperty
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
    if not bpy.context.blend_data.filepath:
        # If there is no blend file open, it might be the default "userpref.blend".
        # In that case, do not do any migration
        return

    scene = bpy.context.scene
    if scene.yafaray4.migrated_to_v4:
        if bpy.app.version >= (2, 80, 0):
            # Removing old scene yafaray property tree
            del scene["yafaray"]
        return
    else:
        scene.yafaray4.migrated_to_v4 = True

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

    if bpy.app.version >= (2, 80, 0):
        print("**Warning**: Migrating YafaRay v3 scenes to YafaRay v4 is not possible in Blender v2.80 or higher.")
        print("**Warning**: DO NOT SAVE the YafaRay v3 scene in Blender v2.80 or higher as some important scene data "
              "WILL BE PERMANENTLY LOST.")
        print("**Warning**: Open the YafaRay v3 Scene in Blender version v2.79b (exactly) so the migration from "
              "YafaRay v3 to v4 can take place.")
        print("**Warning**: Then save the migrated YafaRay v4 with Blender v2.79b. The migrated YafaRay v4 blend file "
              "can later be opened in any Blender version v2.79b, v2.80 or higher.")
        return

    print(bl_info["name"], "Handler: Initial 'one-off' migration from Yafaray v3 parameters")
    
    register_v3_yafaray_properties_needed = False

    if not hasattr(scene, "yafaray"):
        register_v3_yafaray_properties_needed = True
        from ..prop.scene_property_groups_v3 import (YafaRay3SceneProperties, YafaRay3MaterialPreviewControlProperties,
                                                     YafaRay3LayersProperties, YafaRay3LoggingProperties,
                                                     YafaRay3NoiseControlProperties,)

        bpy.utils.register_class(YafaRay3SceneProperties)
        bpy.types.Scene.yafaray = PointerProperty(type=YafaRay3SceneProperties)
    
        bpy.utils.register_class(YafaRay3LayersProperties)
        YafaRay3SceneProperties.passes = PointerProperty(type=YafaRay3LayersProperties)
    
        bpy.utils.register_class(YafaRay3NoiseControlProperties)
        YafaRay3SceneProperties.noise_control = PointerProperty(type=YafaRay3NoiseControlProperties)
    
        bpy.utils.register_class(YafaRay3LoggingProperties)
        YafaRay3SceneProperties.logging = PointerProperty(type=YafaRay3LoggingProperties)
    
        bpy.utils.register_class(YafaRay3MaterialPreviewControlProperties)
        YafaRay3SceneProperties.preview = PointerProperty(type=YafaRay3MaterialPreviewControlProperties)

    if hasattr(scene, "yafaray"):
        mapping_base = {
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

        mapping = {
            "output_node": None,
        }
        mapping.update(mapping_base)

        # convert old world texture slot to dedicated YafaRay world texture parameter
        scene.world.texture = scene.world.active_texture

        # convert old material texture slots to dedicated YafaRay material texture slots parameters
        for material in bpy.data.materials:
            for texture_slot_id in range(min(len(material.use_textures), len(material.yafaray4.use_textures))):
                material.yafaray4.use_textures[texture_slot_id] = material.use_textures[texture_slot_id]
            material.yafaray4.texture_slots.clear()
            for texture_slot in material.texture_slots:
                yaf4_texture_slot = material.yafaray4.texture_slots.add()
                copy_attributes(texture_slot, yaf4_texture_slot, mapping)

        if register_v3_yafaray_properties_needed:
            del YafaRay3SceneProperties.preview
            bpy.utils.unregister_class(YafaRay3MaterialPreviewControlProperties)
            del YafaRay3SceneProperties.logging
            bpy.utils.unregister_class(YafaRay3LoggingProperties)
            del YafaRay3SceneProperties.noise_control
            bpy.utils.unregister_class(YafaRay3NoiseControlProperties)
            del YafaRay3SceneProperties.passes
            bpy.utils.unregister_class(YafaRay3LayersProperties)
            del bpy.types.Scene.yafaray
            bpy.utils.unregister_class(YafaRay3SceneProperties)