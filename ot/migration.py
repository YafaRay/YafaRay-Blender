# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.app.handlers import persistent
from .. import bl_info


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
            scene.yafaray4.passes.pass_enable = scene.yafaray.passes.pass_enable
            scene.yafaray4.passes.pass_mask_obj_index = scene.yafaray.passes.pass_mask_obj_index
            scene.yafaray4.passes.pass_mask_mat_index = scene.yafaray.passes.pass_mask_mat_index
            scene.yafaray4.passes.pass_mask_invert = scene.yafaray.passes.pass_mask_invert
            scene.yafaray4.passes.pass_mask_only = scene.yafaray.passes.pass_mask_only
            scene.yafaray4.passes.objectEdgeThickness = scene.yafaray.passes.objectEdgeThickness
            scene.yafaray4.passes.facesEdgeThickness = scene.yafaray.passes.facesEdgeThickness
            scene.yafaray4.passes.objectEdgeThreshold = scene.yafaray.passes.objectEdgeThreshold
            scene.yafaray4.passes.facesEdgeThreshold = scene.yafaray.passes.facesEdgeThreshold
            scene.yafaray4.passes.objectEdgeSmoothness = scene.yafaray.passes.objectEdgeSmoothness
            scene.yafaray4.passes.facesEdgeSmoothness = scene.yafaray.passes.facesEdgeSmoothness
            scene.yafaray4.passes.toonEdgeColor = scene.yafaray.passes.toonEdgeColor
            scene.yafaray4.passes.toonPreSmooth = scene.yafaray.passes.toonPreSmooth
            scene.yafaray4.passes.toonPostSmooth = scene.yafaray.passes.toonPostSmooth
            scene.yafaray4.passes.toonQuantization = scene.yafaray.passes.toonQuantization
            scene.yafaray4.passes.pass_Combined = scene.yafaray.passes.pass_Combined
            scene.yafaray4.passes.pass_Depth = scene.yafaray.passes.pass_Depth
            scene.yafaray4.passes.pass_Vector = scene.yafaray.passes.pass_Vector
            scene.yafaray4.passes.pass_Normal = scene.yafaray.passes.pass_Normal
            scene.yafaray4.passes.pass_UV = scene.yafaray.passes.pass_UV
            scene.yafaray4.passes.pass_Color = scene.yafaray.passes.pass_Color
            scene.yafaray4.passes.pass_Emit = scene.yafaray.passes.pass_Emit
            scene.yafaray4.passes.pass_Mist = scene.yafaray.passes.pass_Mist
            scene.yafaray4.passes.pass_Diffuse = scene.yafaray.passes.pass_Diffuse
            scene.yafaray4.passes.pass_Spec = scene.yafaray.passes.pass_Spec
            scene.yafaray4.passes.pass_AO = scene.yafaray.passes.pass_AO
            scene.yafaray4.passes.pass_Env = scene.yafaray.passes.pass_Env
            scene.yafaray4.passes.pass_Indirect = scene.yafaray.passes.pass_Indirect
            scene.yafaray4.passes.pass_Shadow = scene.yafaray.passes.pass_Shadow
            scene.yafaray4.passes.pass_Reflect = scene.yafaray.passes.pass_Reflect
            scene.yafaray4.passes.pass_Refract = scene.yafaray.passes.pass_Refract
            scene.yafaray4.passes.pass_IndexOB = scene.yafaray.passes.pass_IndexOB
            scene.yafaray4.passes.pass_IndexMA = scene.yafaray.passes.pass_IndexMA
            scene.yafaray4.passes.pass_DiffDir = scene.yafaray.passes.pass_DiffDir
            scene.yafaray4.passes.pass_DiffInd = scene.yafaray.passes.pass_DiffInd
            scene.yafaray4.passes.pass_DiffCol = scene.yafaray.passes.pass_DiffCol
            scene.yafaray4.passes.pass_GlossDir = scene.yafaray.passes.pass_GlossDir
            scene.yafaray4.passes.pass_GlossInd = scene.yafaray.passes.pass_GlossInd
            scene.yafaray4.passes.pass_GlossCol = scene.yafaray.passes.pass_GlossCol
            scene.yafaray4.passes.pass_TransDir = scene.yafaray.passes.pass_TransDir
            scene.yafaray4.passes.pass_TransInd = scene.yafaray.passes.pass_TransInd
            scene.yafaray4.passes.pass_TransCol = scene.yafaray.passes.pass_TransCol
            scene.yafaray4.passes.pass_SubsurfaceDir = scene.yafaray.passes.pass_SubsurfaceDir
            scene.yafaray4.passes.pass_SubsurfaceInd = scene.yafaray.passes.pass_SubsurfaceInd
            scene.yafaray4.passes.pass_SubsurfaceCol = scene.yafaray.passes.pass_SubsurfaceCol

            scene.yafaray4.noise_control.resampled_floor = scene.yafaray.noise_control.resampled_floor
            scene.yafaray4.noise_control.sample_multiplier_factor = scene.yafaray.noise_control.sample_multiplier_factor
            scene.yafaray4.noise_control.light_sample_multiplier_factor = scene.yafaray.noise_control.light_sample_multiplier_factor
            scene.yafaray4.noise_control.indirect_sample_multiplier_factor = scene.yafaray.noise_control.indirect_sample_multiplier_factor
            scene.yafaray4.noise_control.detect_color_noise = scene.yafaray.noise_control.detect_color_noise
            scene.yafaray4.noise_control.dark_detection_type = scene.yafaray.noise_control.dark_detection_type
            scene.yafaray4.noise_control.dark_threshold_factor = scene.yafaray.noise_control.dark_threshold_factor
            scene.yafaray4.noise_control.variance_edge_size = scene.yafaray.noise_control.variance_edge_size
            scene.yafaray4.noise_control.variance_pixels = scene.yafaray.noise_control.variance_pixels
            scene.yafaray4.noise_control.clamp_samples = scene.yafaray.noise_control.clamp_samples
            scene.yafaray4.noise_control.clamp_indirect = scene.yafaray.noise_control.clamp_indirect
            scene.yafaray4.noise_control.background_resampling = scene.yafaray.noise_control.background_resampling

            scene.yafaray4.logging.paramsBadgePosition = scene.yafaray.logging.paramsBadgePosition
            scene.yafaray4.logging.saveLog = scene.yafaray.logging.saveLog
            scene.yafaray4.logging.saveHTML = scene.yafaray.logging.saveHTML
            scene.yafaray4.logging.savePreset = scene.yafaray.logging.savePreset
            scene.yafaray4.logging.logPrintDateTime = scene.yafaray.logging.logPrintDateTime
            scene.yafaray4.logging.consoleVerbosity = scene.yafaray.logging.consoleVerbosity
            scene.yafaray4.logging.logVerbosity = scene.yafaray.logging.logVerbosity
            scene.yafaray4.logging.drawRenderSettings = scene.yafaray.logging.drawRenderSettings
            scene.yafaray4.logging.drawAANoiseSettings = scene.yafaray.logging.drawAANoiseSettings
            scene.yafaray4.logging.title = scene.yafaray.logging.title
            scene.yafaray4.logging.author = scene.yafaray.logging.author
            scene.yafaray4.logging.contact = scene.yafaray.logging.contact
            scene.yafaray4.logging.comments = scene.yafaray.logging.comments
            scene.yafaray4.logging.customIcon = scene.yafaray.logging.customIcon
            scene.yafaray4.logging.customFont = scene.yafaray.logging.customFont
            scene.yafaray4.logging.fontScale = scene.yafaray.logging.fontScale

            scene.yafaray4.preview.enable = scene.yafaray.preview.enable
            scene.yafaray4.preview.objScale = scene.yafaray.preview.objScale
            scene.yafaray4.preview.rotZ = scene.yafaray.preview.rotZ
            scene.yafaray4.preview.lightRotZ = scene.yafaray.preview.lightRotZ
            scene.yafaray4.preview.keyLightPowerFactor = scene.yafaray.preview.keyLightPowerFactor
            scene.yafaray4.preview.fillLightPowerFactor = scene.yafaray.preview.fillLightPowerFactor
            scene.yafaray4.preview.keyLightColor = scene.yafaray.preview.keyLightColor
            scene.yafaray4.preview.fillLightColor = scene.yafaray.preview.fillLightColor
            scene.yafaray4.preview.previewRayDepth = scene.yafaray.preview.previewRayDepth
            scene.yafaray4.preview.previewAApasses = scene.yafaray.preview.previewAApasses
            scene.yafaray4.preview.previewBackground = scene.yafaray.preview.previewBackground
            scene.yafaray4.preview.previewObject = scene.yafaray.preview.previewObject
            scene.yafaray4.preview.camDist = scene.yafaray.preview.camDist
            scene.yafaray4.preview.camRot = scene.yafaray.preview.camRot
