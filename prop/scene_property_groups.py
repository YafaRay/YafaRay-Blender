import bpy
from .scene_property_groups_definitions import YafaRay4LoggingPropertiesDefinitions, \
    YafaRay4NoiseControlPropertiesDefinitions, YafaRay4MaterialPreviewControlPropertiesDefinitions, \
    YafaRay4LayersPropertiesDefinitions


class YafaRay4LoggingProperties(bpy.types.PropertyGroup):
    prop_defs = YafaRay4LoggingPropertiesDefinitions()
    paramsBadgePosition: prop_defs.paramsBadgePosition
    saveLog: prop_defs.saveLog
    saveHTML: prop_defs.saveHTML
    savePreset: prop_defs.savePreset
    logPrintDateTime: prop_defs.logPrintDateTime
    consoleVerbosity: prop_defs.consoleVerbosity
    logVerbosity: prop_defs.logVerbosity
    drawRenderSettings: prop_defs.drawRenderSettings
    drawAANoiseSettings: prop_defs.drawAANoiseSettings
    title: prop_defs.title
    author: prop_defs.author
    contact: prop_defs.contact
    comments: prop_defs.comments
    customIcon: prop_defs.customIcon
    customFont: prop_defs.customFont
    fontScale: prop_defs.fontScale


class YafaRay4NoiseControlProperties(bpy.types.PropertyGroup):
    prop_defs = YafaRay4NoiseControlPropertiesDefinitions()
    resampled_floor: prop_defs.resampled_floor
    sample_multiplier_factor: prop_defs.sample_multiplier_factor
    light_sample_multiplier_factor: prop_defs.light_sample_multiplier_factor
    indirect_sample_multiplier_factor: prop_defs.indirect_sample_multiplier_factor
    detect_color_noise: prop_defs.detect_color_noise
    dark_detection_type: prop_defs.dark_detection_type
    dark_threshold_factor: prop_defs.dark_threshold_factor
    variance_edge_size: prop_defs.variance_edge_size
    variance_pixels: prop_defs.variance_pixels
    clamp_samples: prop_defs.clamp_samples
    clamp_indirect: prop_defs.clamp_indirect
    background_resampling: prop_defs.background_resampling


class YafaRay4LayersProperties(bpy.types.PropertyGroup):
    prop_defs = YafaRay4LayersPropertiesDefinitions()
    pass_enable: prop_defs.pass_enable
    pass_mask_obj_index: prop_defs.pass_mask_obj_index
    pass_mask_mat_index: prop_defs.pass_mask_mat_index
    pass_mask_invert: prop_defs.pass_mask_invert
    pass_mask_only: prop_defs.pass_mask_only
    objectEdgeThickness: prop_defs.objectEdgeThickness
    facesEdgeThickness: prop_defs.facesEdgeThickness
    objectEdgeThreshold: prop_defs.objectEdgeThreshold
    facesEdgeThreshold: prop_defs.facesEdgeThreshold
    objectEdgeSmoothness: prop_defs.objectEdgeSmoothness
    facesEdgeSmoothness: prop_defs.facesEdgeSmoothness
    toonEdgeColor: prop_defs.toonEdgeColor
    toonPreSmooth: prop_defs.toonPreSmooth
    toonPostSmooth: prop_defs.toonPostSmooth
    toonQuantization: prop_defs.toonQuantization
    pass_Combined: prop_defs.pass_Combined
    pass_Depth: prop_defs.pass_Depth
    pass_Vector: prop_defs.pass_Vector
    pass_Normal: prop_defs.pass_Normal
    pass_UV: prop_defs.pass_UV
    pass_Color: prop_defs.pass_Color
    pass_Emit: prop_defs.pass_Emit
    pass_Mist: prop_defs.pass_Mist
    pass_Diffuse: prop_defs.pass_Diffuse
    pass_Spec: prop_defs.pass_Spec
    pass_AO: prop_defs.pass_AO
    pass_Env: prop_defs.pass_Env
    pass_Indirect: prop_defs.pass_Indirect
    pass_Shadow: prop_defs.pass_Shadow
    pass_Reflect: prop_defs.pass_Reflect
    pass_Refract: prop_defs.pass_Refract
    pass_IndexOB: prop_defs.pass_IndexOB
    pass_IndexMA: prop_defs.pass_IndexMA
    pass_DiffDir: prop_defs.pass_DiffDir
    pass_DiffInd: prop_defs.pass_DiffInd
    pass_DiffCol: prop_defs.pass_DiffCol
    pass_GlossDir: prop_defs.pass_GlossDir
    pass_GlossInd: prop_defs.pass_GlossInd
    pass_GlossCol: prop_defs.pass_GlossCol
    pass_TransDir: prop_defs.pass_TransDir
    pass_TransInd: prop_defs.pass_TransInd
    pass_TransCol: prop_defs.pass_TransCol
    pass_SubsurfaceDir: prop_defs.pass_SubsurfaceDir
    pass_SubsurfaceInd: prop_defs.pass_SubsurfaceInd
    pass_SubsurfaceCol: prop_defs.pass_SubsurfaceCol


class YafaRay4MaterialPreviewControlProperties(bpy.types.PropertyGroup):
    prop_defs = YafaRay4MaterialPreviewControlPropertiesDefinitions()
    enable: prop_defs.enable
    objScale: prop_defs.objScale
    rotZ: prop_defs.rotZ
    lightRotZ: prop_defs.lightRotZ
    keyLightPowerFactor: prop_defs.keyLightPowerFactor
    fillLightPowerFactor: prop_defs.fillLightPowerFactor
    keyLightColor: prop_defs.keyLightColor
    fillLightColor: prop_defs.fillLightColor
    previewRayDepth: prop_defs.previewRayDepth
    previewAApasses: prop_defs.previewAApasses
    previewBackground: prop_defs.previewBackground
    previewObject: prop_defs.previewObject
    camDist: prop_defs.camDist
    camRot: prop_defs.camRot

    class PreviewCamRotReset(bpy.types.Operator):
        """ Reset camera rotation/zoom to initial values. """
        bl_idname = "yafaray4.preview_camera_rotation_reset"
        bl_label = "reset camera rotation/distance values to defaults"
        country = bpy.props.StringProperty()

        # noinspection PyMethodMayBeStatic,PyUnusedLocal
        def execute(self, context):
            bpy.data.scenes[0].yafaray.is_preview.camRot = (0, 0, 1)
            bpy.data.scenes[0].yafaray.is_preview.camDist = 12
            return {'FINISHED'}

    class PreviewCamZoomIn(bpy.types.Operator):
        """ Camera zoom in (reduces distance between camera and object) """
        bl_idname = "yafaray4.preview_camera_zoom_in"
        bl_label = "reset camera rotation/distance values to defaults"
        country = bpy.props.StringProperty()

        # noinspection PyMethodMayBeStatic,PyUnusedLocal
        def execute(self, context):
            bpy.data.scenes[0].yafaray.is_preview.camDist -= 0.5
            return {'FINISHED'}

    class PreviewCamZoomOut(bpy.types.Operator):
        """ Camera zoom out (increases distance between camera and object) """
        bl_idname = "yafaray4.preview_camera_zoom_out"
        bl_label = "reset camera rotation/distance values to defaults"
        country = bpy.props.StringProperty()

        # noinspection PyMethodMayBeStatic,PyUnusedLocal
        def execute(self, context):
            bpy.data.scenes[0].yafaray.is_preview.camDist += 0.5
            return {'FINISHED'}
