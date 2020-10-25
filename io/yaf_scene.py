# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import bpy
import os
from collections import namedtuple

def computeSceneSize(render):
    sizeX = int(render.resolution_x * render.resolution_percentage * 0.01)
    sizeY = int(render.resolution_y * render.resolution_percentage * 0.01)
    return [sizeX, sizeY]


def getRenderCoords(scene):
    render = scene.render
    [sizeX, sizeY] = computeSceneSize(render)

    bStartX = 0
    bStartY = 0
    bsizeX = 0
    bsizeY = 0

    cam_data = None

    if scene.objects:
        for item in scene.objects:
            if item.type == 'CAMERA':
                cam_data = item.data
                break

    # Shift only available if camera is selected
    if not cam_data:
        shiftX = 0
        shiftY = 0

    else:
        # Sanne: get lens shift
        #camera = self.scene.objects.camera.getData()
        maxsize = max(sizeX, sizeY)
        shiftX = int(cam_data.shift_x * maxsize)
        shiftY = int(cam_data.shift_y * maxsize)

    # no border when rendering to view
    if render.use_border and  cam_data:
        minX = render.border_min_x * sizeX
        minY = render.border_min_y * sizeY
        maxX = render.border_max_x * sizeX
        maxY = render.border_max_y * sizeY
        bStartX = int(minX)
        bStartY = int(sizeY) - int(maxY)
        bsizeX = int(maxX) - int(minX)
        bsizeY = int(maxY) - int(minY)

    # Sanne: add lens shift
    bStartX += shiftX
    bStartY -= shiftY

    return [sizeX, sizeY, bStartX, bStartY, bsizeX, bsizeY, cam_data]


def exportAA(yi, scene):
    yi.paramsSetInt("AA_passes", scene.AA_passes)
    yi.paramsSetInt("AA_minsamples", scene.AA_min_samples)
    yi.paramsSetInt("AA_inc_samples", scene.AA_inc_samples)
    yi.paramsSetFloat("AA_pixelwidth", scene.AA_pixelwidth)
    yi.paramsSetFloat("AA_threshold", scene.AA_threshold)
    yi.paramsSetString("filter_type", scene.AA_filter_type)
    yi.paramsSetFloat("AA_resampled_floor", scene.yafaray.noise_control.resampled_floor)
    yi.paramsSetFloat("AA_sample_multiplier_factor", scene.yafaray.noise_control.sample_multiplier_factor)
    yi.paramsSetFloat("AA_light_sample_multiplier_factor", scene.yafaray.noise_control.light_sample_multiplier_factor)
    yi.paramsSetFloat("AA_indirect_sample_multiplier_factor", scene.yafaray.noise_control.indirect_sample_multiplier_factor)
    yi.paramsSetBool("AA_detect_color_noise", scene.yafaray.noise_control.detect_color_noise)
    yi.paramsSetString("AA_dark_detection_type", scene.yafaray.noise_control.dark_detection_type)
    yi.paramsSetFloat("AA_dark_threshold_factor", scene.yafaray.noise_control.dark_threshold_factor)
    yi.paramsSetInt("AA_variance_edge_size", scene.yafaray.noise_control.variance_edge_size)
    yi.paramsSetInt("AA_variance_pixels", scene.yafaray.noise_control.variance_pixels)
    yi.paramsSetFloat("AA_clamp_samples", scene.yafaray.noise_control.clamp_samples)
    yi.paramsSetFloat("AA_clamp_indirect", scene.yafaray.noise_control.clamp_indirect)
    yi.paramsSetBool("background_resampling", scene.yafaray.noise_control.background_resampling)

    if scene.name == "preview" and bpy.data.scenes[0].yafaray.preview.enable:
        yi.paramsSetInt("AA_passes", bpy.data.scenes[0].yafaray.preview.previewAApasses)
        yi.paramsSetFloat("AA_threshold", 0.01)


def exportRenderSettings(yi, depsgraph):
    yi.printVerbose("Exporting Render Settings")
    scene = depsgraph.scene
    render = scene.render

    [sizeX, sizeY, bStartX, bStartY, bsizeX, bsizeY, cam_data] = getRenderCoords(scene)

    yi.paramsSetString("integrator_name", "default")
    yi.paramsSetString("volintegrator_name", "volintegr")

    exportAA(yi, scene)

    yi.paramsSetInt("xstart", bStartX)
    yi.paramsSetInt("ystart", bStartY)

    # no border when rendering to view
    if render.use_border and cam_data:
        yi.paramsSetInt("width", bsizeX)
        yi.paramsSetInt("height", bsizeY)
    else:
        yi.paramsSetInt("width", sizeX)
        yi.paramsSetInt("height", sizeY)

    yi.paramsSetBool("show_sam_pix", scene.gs_show_sam_pix)

    if scene.name == "preview" and bpy.data.scenes[0].yafaray.preview.enable:
        yi.paramsSetBool("show_sam_pix", False)

    yi.paramsSetInt("tile_size", scene.gs_tile_size)
    yi.paramsSetString("tiles_order", scene.gs_tile_order)

    if scene.gs_auto_threads:
        yi.paramsSetInt("threads", -1)
        yi.paramsSetInt("threads_photons", -1)
    else:
        yi.paramsSetInt("threads", scene.gs_threads)
        yi.paramsSetInt("threads_photons", scene.gs_threads)

    yi.paramsSetString("background_name", "world_background")
    
    yi.paramsSetString("images_autosave_interval_type", scene.gs_images_autosave_interval_type)
    yi.paramsSetInt("images_autosave_interval_passes", scene.gs_images_autosave_interval_passes)
    yi.paramsSetFloat("images_autosave_interval_seconds", scene.gs_images_autosave_interval_seconds)

    yi.paramsSetString("film_save_load", scene.gs_film_save_load)
    yi.paramsSetString("film_autosave_interval_type", scene.gs_film_autosave_interval_type)
    yi.paramsSetInt("film_autosave_interval_passes", scene.gs_film_autosave_interval_passes)
    yi.paramsSetFloat("film_autosave_interval_seconds", scene.gs_film_autosave_interval_seconds)

    yi.paramsSetBool("adv_auto_shadow_bias_enabled", scene.adv_auto_shadow_bias_enabled)
    yi.paramsSetFloat("adv_shadow_bias_value", scene.adv_shadow_bias_value)
    yi.paramsSetBool("adv_auto_min_raydist_enabled", scene.adv_auto_min_raydist_enabled)
    yi.paramsSetFloat("adv_min_raydist_value", scene.adv_min_raydist_value)
    yi.paramsSetFloat("adv_min_raydist_value", scene.adv_min_raydist_value)
    yi.paramsSetInt("adv_base_sampling_offset", scene.adv_base_sampling_offset)
    print(list(bpy.context.preferences.addons))
    yi.paramsSetInt("adv_computer_node", bpy.context.preferences.addons["yafaray4"].preferences.yafaray_computer_node)


def setLoggingAndBadgeSettings(yi, scene):
    yi.printVerbose("Exporting Logging and Badge settings")
    yi.paramsSetBool("badge_draw_render_settings", scene.yafaray.logging.drawRenderSettings)
    yi.paramsSetBool("badge_draw_aa_noise_settings", scene.yafaray.logging.drawAANoiseSettings)
    yi.paramsSetBool("logging_save_txt", scene.yafaray.logging.saveLog)
    yi.paramsSetBool("logging_save_html", scene.yafaray.logging.saveHTML)
    yi.paramsSetString("badge_position", scene.yafaray.logging.paramsBadgePosition)
    yi.paramsSetString("badge_title", scene.yafaray.logging.title)
    yi.paramsSetString("badge_author", scene.yafaray.logging.author)
    yi.paramsSetString("badge_contact", scene.yafaray.logging.contact)
    yi.paramsSetString("badge_comment", scene.yafaray.logging.comments)
    if scene.yafaray.logging.customIcon != "":
        yi.paramsSetString("badge_icon_path", os.path.abspath(bpy.path.abspath(scene.yafaray.logging.customIcon)))
    yi.paramsSetString("badge_font_path", scene.yafaray.logging.customFont)
    yi.paramsSetFloat("badge_font_size_factor", scene.yafaray.logging.fontScale)


def calcAlphaPremultiply(scene):
    alpha_premult = namedtuple("alpha_premult", ["blender", "secondary_output"])
    if scene.gs_premult == "auto":
        if scene.img_output == "PNG" or scene.img_output == "JPEG":
            enable_premult = False
        else:
            enable_premult = True
    elif scene.gs_premult == "yes":
        enable_premult = True
    else:
        enable_premult = False

    if scene.gs_type_render == "into_blender":
        # We force alpha premultiply when rendering into Blender as it expects premultiplied input
        # In case we use a secondary file output, we set the premultiply according to the Blender setting
        return alpha_premult(True, enable_premult)
    else:
        # In this case we use the calculated enable premult value, and leave the second value as False as there is no secondary output in this case
        return alpha_premult(enable_premult, False)


def calcGamma(scene):
    gamma = namedtuple("gamma", ["blender", "secondary_output"])
    gamma_1 = 1.0
    gamma_2 = 1.0
    if scene.gs_type_render == "into_blender" and scene.display_settings.display_device == "None":
        gamma_1 = scene.gs_gamma  # We only use the selected gamma if the output device is set to "None"
        if scene.display_settings.display_device == "None":
            gamma_2 = scene.gs_gamma  #We only use the selected gamma if the output device is set to "None"
    elif scene.display_settings.display_device == "None":
        gamma_1 = scene.gs_gamma  # We only use the selected gamma if the output device is set to "None"

    return gamma(gamma_1, gamma_2)


def calcColorSpace(scene):
    color_space = namedtuple("color_space", ["blender", "secondary_output"])
    color_space_2 = "sRGB"

    if scene.gs_type_render == "into_blender":
        if scene.display_settings.display_device == "None":
            color_space_1 = "Raw_Manual_Gamma"
        else:
            color_space_1 = "LinearRGB"  #For all other Blender display devices, it expects a linear output from YafaRay
        #Optional Secondary file output color space
        if scene.img_output == "OPEN_EXR" or scene.img_output == "HDR":  #If the output file is a HDR/EXR file, we force the render output to Linear
            color_space_2 = "LinearRGB"
        elif scene.display_settings.display_device == "sRGB":
            color_space_2 = "sRGB"
        elif scene.display_settings.display_device == "XYZ":
            color_space_2 = "XYZ"
        elif scene.display_settings.display_device == "None":
            color_space_2 = "Raw_Manual_Gamma"
    else:
        if scene.img_output == "OPEN_EXR" or scene.img_output == "HDR":  # If the output file is a HDR/EXR file, we force the render output to Linear
            color_space_1 = "LinearRGB"
        elif scene.display_settings.display_device == "sRGB":
            color_space_1 = "sRGB"
        elif scene.display_settings.display_device == "XYZ":
            color_space_1 = "XYZ"
        elif scene.display_settings.display_device == "None":
            color_space_1 = "Raw_Manual_Gamma"
        else:
            color_space_1 = "sRGB"

    return color_space(color_space_1, color_space_2)


def exportRenderPassesSettings(yi, depsgraph):
    yi.printVerbose("Exporting Render Passes settings")
    scene = depsgraph.scene

    yi.paramsSetInt("layer_mask_obj_index", scene.yafaray.passes.pass_mask_obj_index)
    yi.paramsSetInt("layer_mask_mat_index", scene.yafaray.passes.pass_mask_mat_index)
    yi.paramsSetBool("layer_mask_invert", scene.yafaray.passes.pass_mask_invert)
    yi.paramsSetBool("layer_mask_only", scene.yafaray.passes.pass_mask_only)
    
    yi.paramsSetInt("layer_object_edge_thickness", scene.yafaray.passes.objectEdgeThickness)
    yi.paramsSetInt("layer_faces_edge_thickness", scene.yafaray.passes.facesEdgeThickness)
    yi.paramsSetFloat("layer_object_edge_threshold", scene.yafaray.passes.objectEdgeThreshold)
    yi.paramsSetFloat("layer_faces_edge_threshold", scene.yafaray.passes.facesEdgeThreshold)
    yi.paramsSetFloat("layer_object_edge_smoothness", scene.yafaray.passes.objectEdgeSmoothness)
    yi.paramsSetFloat("layer_faces_edge_smoothness", scene.yafaray.passes.facesEdgeSmoothness)
    yi.paramsSetColor("layer_toon_edge_color", scene.yafaray.passes.toonEdgeColor[0], scene.yafaray.passes.toonEdgeColor[1], scene.yafaray.passes.toonEdgeColor[2])
    yi.paramsSetFloat("layer_toon_pre_smooth", scene.yafaray.passes.toonPreSmooth)
    yi.paramsSetFloat("layer_toon_post_smooth", scene.yafaray.passes.toonPostSmooth)
    yi.paramsSetFloat("layer_toon_quantization", scene.yafaray.passes.toonQuantization)


    # Possible image type names: "Gray", "GrayAlpha", "Color", "ColorAlpha"
    yi.defineLayer("combined", "ColorAlpha", "Combined") #Must always be defined!
    if scene.yafaray.passes.pass_enable:
        if depsgraph.view_layer.use_pass_z:
            yi.defineLayer(scene.yafaray.passes.pass_Depth, "Gray", "Depth")
            
        if depsgraph.view_layer.use_pass_vector:
            yi.defineLayer(scene.yafaray.passes.pass_Vector, "ColorAlpha", "Vector")
            
        if depsgraph.view_layer.use_pass_normal:
            yi.defineLayer(scene.yafaray.passes.pass_Normal, "Color", "Normal")
            
        if depsgraph.view_layer.use_pass_uv:
            yi.defineLayer(scene.yafaray.passes.pass_UV, "Color", "UV")
            
        if depsgraph.view_layer.use_pass_color:
            yi.defineLayer(scene.yafaray.passes.pass_Color, "ColorAlpha", "Color")
            
        if depsgraph.view_layer.use_pass_emit:
            yi.defineLayer(scene.yafaray.passes.pass_Emit, "Color", "Emit")
            
        if depsgraph.view_layer.use_pass_mist:
            yi.defineLayer(scene.yafaray.passes.pass_Mist, "Gray", "Mist")
            
        if depsgraph.view_layer.use_pass_diffuse:
            yi.defineLayer(scene.yafaray.passes.pass_Diffuse, "Color", "Diffuse")
            
        if depsgraph.view_layer.use_pass_specular:
            yi.defineLayer(scene.yafaray.passes.pass_Spec, "Color", "Spec")
            
        if depsgraph.view_layer.use_pass_ambient_occlusion:
            yi.defineLayer(scene.yafaray.passes.pass_AO, "Color", "AO")
            
        if depsgraph.view_layer.use_pass_environment:
            yi.defineLayer(scene.yafaray.passes.pass_Env, "Color", "Env")
            
        if depsgraph.view_layer.use_pass_indirect:
            yi.defineLayer(scene.yafaray.passes.pass_Indirect, "Color", "Indirect")
            
        if depsgraph.view_layer.use_pass_shadow:
            yi.defineLayer(scene.yafaray.passes.pass_Shadow, "Color", "Shadow")
            
        if depsgraph.view_layer.use_pass_reflection:
            yi.defineLayer(scene.yafaray.passes.pass_Reflect, "Color", "Reflect")
            
        if depsgraph.view_layer.use_pass_refraction:
            yi.defineLayer(scene.yafaray.passes.pass_Refract, "Color", "Refract")
            
        if depsgraph.view_layer.use_pass_object_index:
            yi.defineLayer(scene.yafaray.passes.pass_IndexOB, "Gray", "IndexOB")
            
        if depsgraph.view_layer.use_pass_material_index:
            yi.defineLayer(scene.yafaray.passes.pass_IndexMA, "Gray", "IndexMA")
            
        if depsgraph.view_layer.use_pass_diffuse_direct:
            yi.defineLayer(scene.yafaray.passes.pass_Depth, "pass_DiffDir", "DiffDir")
            
        if depsgraph.view_layer.use_pass_diffuse_indirect:
            yi.defineLayer(scene.yafaray.passes.pass_DiffInd, "Color", "DiffInd")
            
        if depsgraph.view_layer.use_pass_diffuse_color:
            yi.defineLayer(scene.yafaray.passes.pass_DiffCol, "Color", "DiffCol")
            
        if depsgraph.view_layer.use_pass_glossy_direct:
            yi.defineLayer(scene.yafaray.passes.pass_GlossDir, "Color", "GlossDir")
            
        if depsgraph.view_layer.use_pass_glossy_indirect:
            yi.defineLayer(scene.yafaray.passes.pass_GlossInd, "Color", "GlossInd")
            
        if depsgraph.view_layer.use_pass_glossy_color:
            yi.defineLayer(scene.yafaray.passes.pass_GlossCol, "Color", "GlossCol")
            
        if depsgraph.view_layer.use_pass_transmission_direct:
            yi.defineLayer(scene.yafaray.passes.pass_TransDir, "Color", "TransDir")
            
        if depsgraph.view_layer.use_pass_transmission_indirect:
            yi.defineLayer(scene.yafaray.passes.pass_TransInd, "Color", "TransInd")
            
        if depsgraph.view_layer.use_pass_transmission_color:
            yi.defineLayer(scene.yafaray.passes.pass_TransCol, "Color", "TransCol")
            
        if depsgraph.view_layer.use_pass_subsurface_direct:
            yi.defineLayer(scene.yafaray.passes.pass_SubsurfaceDir, "Color", "SubsurfaceDir")
            
        if depsgraph.view_layer.use_pass_subsurface_indirect:
            yi.defineLayer(scene.yafaray.passes.pass_SubsurfaceInd, "Color", "SubsurfaceInd")
            
        if depsgraph.view_layer.use_pass_subsurface_color:
            yi.defineLayer(scene.yafaray.passes.pass_SubsurfaceCol, "Color", "SubsurfaceCol")

    
