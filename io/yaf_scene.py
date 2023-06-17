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
from ..util.io_utils import scene_from_depsgraph

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
    if render.use_border and cam_data:
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
    yaf_param_map.setInt("AA_passes", scene.AA_passes)
    yaf_param_map.setInt("AA_minsamples", scene.AA_min_samples)
    yaf_param_map.setInt("AA_inc_samples", scene.AA_inc_samples)
    yaf_param_map.setFloat("AA_pixelwidth", scene.AA_pixelwidth)
    yaf_param_map.setFloat("AA_threshold", scene.AA_threshold)
    yaf_param_map.setString("filter_type", scene.AA_filter_type)
    yaf_param_map.setFloat("AA_resampled_floor", scene.yafaray.noise_control.resampled_floor)
    yaf_param_map.setFloat("AA_sample_multiplier_factor", scene.yafaray.noise_control.sample_multiplier_factor)
    yaf_param_map.setFloat("AA_light_sample_multiplier_factor", scene.yafaray.noise_control.light_sample_multiplier_factor)
    yaf_param_map.setFloat("AA_indirect_sample_multiplier_factor", scene.yafaray.noise_control.indirect_sample_multiplier_factor)
    yaf_param_map.setBool("AA_detect_color_noise", scene.yafaray.noise_control.detect_color_noise)
    yaf_param_map.setString("AA_dark_detection_type", scene.yafaray.noise_control.dark_detection_type)
    yaf_param_map.setFloat("AA_dark_threshold_factor", scene.yafaray.noise_control.dark_threshold_factor)
    yaf_param_map.setInt("AA_variance_edge_size", scene.yafaray.noise_control.variance_edge_size)
    yaf_param_map.setInt("AA_variance_pixels", scene.yafaray.noise_control.variance_pixels)
    yaf_param_map.setFloat("AA_clamp_samples", scene.yafaray.noise_control.clamp_samples)
    yaf_param_map.setFloat("AA_clamp_indirect", scene.yafaray.noise_control.clamp_indirect)
    yaf_param_map.setBool("background_resampling", scene.yafaray.noise_control.background_resampling)

    if scene.name == "preview" and bpy.data.scenes[0].yafaray.preview.enable:
        yaf_param_map.setInt("AA_passes", bpy.data.scenes[0].yafaray.preview.previewAApasses)
        yaf_param_map.setFloat("AA_threshold", 0.01)


def exportRenderSettings(yi, depsgraph, render_path, render_filename):
    self.yaf_logger.printVerbose("Exporting Render Settings")
    scene = scene_from_depsgraph(depsgraph)
    render = scene.render

    [sizeX, sizeY, bStartX, bStartY, bsizeX, bsizeY, cam_data] = getRenderCoords(scene)

    yaf_param_map.setString("scene_accelerator", scene.gs_accelerator)

    exportAA(yi, scene)

    yaf_param_map.setInt("xstart", bStartX)
    yaf_param_map.setInt("ystart", bStartY)

    # no border when rendering to view
    if render.use_border and cam_data:
        yaf_param_map.setInt("width", bsizeX)
        yaf_param_map.setInt("height", bsizeY)
    else:
        yaf_param_map.setInt("width", sizeX)
        yaf_param_map.setInt("height", sizeY)

    yaf_param_map.setBool("show_sam_pix", scene.gs_show_sam_pix)

    if scene.name == "preview" and bpy.data.scenes[0].yafaray.preview.enable:
        yaf_param_map.setBool("show_sam_pix", False)

    yaf_param_map.setInt("tile_size", scene.gs_tile_size)
    yaf_param_map.setString("tiles_order", scene.gs_tile_order)

    if scene.gs_auto_threads:
        yaf_param_map.setInt("threads", -1)
        yaf_param_map.setInt("threads_photons", -1)
    else:
        yaf_param_map.setInt("threads", scene.gs_threads)
        yaf_param_map.setInt("threads_photons", scene.gs_threads)

    yaf_param_map.setString("images_autosave_interval_type", scene.gs_images_autosave_interval_type)
    yaf_param_map.setInt("images_autosave_interval_passes", scene.gs_images_autosave_interval_passes)
    yaf_param_map.setFloat("images_autosave_interval_seconds", scene.gs_images_autosave_interval_seconds)

    yaf_param_map.setString("film_load_save_mode", scene.gs_film_save_load)
    yaf_param_map.setString("film_load_save_path", render_path + "/" + render_filename)
    yaf_param_map.setString("film_autosave_interval_type", scene.gs_film_autosave_interval_type)
    yaf_param_map.setInt("film_autosave_interval_passes", scene.gs_film_autosave_interval_passes)
    yaf_param_map.setFloat("film_autosave_interval_seconds", scene.gs_film_autosave_interval_seconds)

    yaf_param_map.setBool("adv_auto_shadow_bias_enabled", scene.adv_auto_shadow_bias_enabled)
    yaf_param_map.setFloat("adv_shadow_bias_value", scene.adv_shadow_bias_value)
    yaf_param_map.setBool("adv_auto_min_raydist_enabled", scene.adv_auto_min_raydist_enabled)
    yaf_param_map.setFloat("adv_min_raydist_value", scene.adv_min_raydist_value)
    yaf_param_map.setFloat("adv_min_raydist_value", scene.adv_min_raydist_value)
    yaf_param_map.setInt("adv_base_sampling_offset", scene.adv_base_sampling_offset)
    if bpy.app.version >= (2, 80, 0):
        pass   # FIXME BLENDER 2.80-3.00
    else:
        yaf_param_map.setInt("adv_computer_node", bpy.context.user_preferences.addons["yafaray4"].preferences.yafaray_computer_node)

    yaf_param_map.setInt("layer_mask_obj_index", scene.yafaray.passes.pass_mask_obj_index)
    yaf_param_map.setInt("layer_mask_mat_index", scene.yafaray.passes.pass_mask_mat_index)
    yaf_param_map.setBool("layer_mask_invert", scene.yafaray.passes.pass_mask_invert)
    yaf_param_map.setBool("layer_mask_only", scene.yafaray.passes.pass_mask_only)

    yaf_param_map.setInt("layer_object_edge_thickness", scene.yafaray.passes.objectEdgeThickness)
    yaf_param_map.setInt("layer_faces_edge_thickness", scene.yafaray.passes.facesEdgeThickness)
    yaf_param_map.setFloat("layer_object_edge_threshold", scene.yafaray.passes.objectEdgeThreshold)
    yaf_param_map.setFloat("layer_faces_edge_threshold", scene.yafaray.passes.facesEdgeThreshold)
    yaf_param_map.setFloat("layer_object_edge_smoothness", scene.yafaray.passes.objectEdgeSmoothness)
    yaf_param_map.setFloat("layer_faces_edge_smoothness", scene.yafaray.passes.facesEdgeSmoothness)
    yaf_param_map.setColor("layer_toon_edge_color", scene.yafaray.passes.toonEdgeColor[0],
                      scene.yafaray.passes.toonEdgeColor[1], scene.yafaray.passes.toonEdgeColor[2])
    yaf_param_map.setFloat("layer_toon_pre_smooth", scene.yafaray.passes.toonPreSmooth)
    yaf_param_map.setFloat("layer_toon_post_smooth", scene.yafaray.passes.toonPostSmooth)
    yaf_param_map.setFloat("layer_toon_quantization", scene.yafaray.passes.toonQuantization)


def setLoggingAndBadgeSettings(yi, scene):
    self.yaf_logger.printVerbose("Exporting Logging and Badge settings")
    yaf_param_map.setBool("badge_draw_render_settings", scene.yafaray.logging.drawRenderSettings)
    yaf_param_map.setBool("badge_draw_aa_noise_settings", scene.yafaray.logging.drawAANoiseSettings)
    yaf_param_map.setBool("logging_save_txt", scene.yafaray.logging.saveLog)
    yaf_param_map.setBool("logging_save_html", scene.yafaray.logging.saveHTML)
    yaf_param_map.setString("badge_position", scene.yafaray.logging.paramsBadgePosition)
    yaf_param_map.setString("badge_title", scene.yafaray.logging.title)
    yaf_param_map.setString("badge_author", scene.yafaray.logging.author)
    yaf_param_map.setString("badge_contact", scene.yafaray.logging.contact)
    yaf_param_map.setString("badge_comment", scene.yafaray.logging.comments)
    if scene.yafaray.logging.customIcon != "":
        yaf_param_map.setString("badge_icon_path", os.path.abspath(bpy.path.abspath(scene.yafaray.logging.customIcon)))
    yaf_param_map.setString("badge_font_path", scene.yafaray.logging.customFont)
    yaf_param_map.setFloat("badge_font_size_factor", scene.yafaray.logging.fontScale)


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

def defineLayers(yi, depsgraph):
    self.yaf_logger.printVerbose("Exporting Render Passes settings")
    scene = scene_from_depsgraph(depsgraph)

    def defineLayer(layer_type, exported_image_type, exported_image_name):
        yaf_param_map.setString("type", layer_type)
        yaf_param_map.setString("image_type", exported_image_type)
        yaf_param_map.setString("exported_image_name", exported_image_name)
        yaf_param_map.setString("exported_image_type", exported_image_type)
        yi.defineLayer()
        yaf_param_map = libyafaray4_bindings.ParamMap()

    defineLayer("combined", "ColorAlpha", "Combined")

    if scene.yafaray.passes.pass_enable:
        if scene.render.layers[0].use_pass_z:
            defineLayer(scene.yafaray.passes.pass_Depth, "Gray", "Depth")
            
        if scene.render.layers[0].use_pass_vector:
            defineLayer(scene.yafaray.passes.pass_Vector, "ColorAlpha", "Vector")
            
        if scene.render.layers[0].use_pass_normal:
            defineLayer(scene.yafaray.passes.pass_Normal, "Color", "Normal")
            
        if scene.render.layers[0].use_pass_uv:
            defineLayer(scene.yafaray.passes.pass_UV, "Color", "UV")
            
        if scene.render.layers[0].use_pass_color:
            defineLayer(scene.yafaray.passes.pass_Color, "ColorAlpha", "Color")
            
        if scene.render.layers[0].use_pass_emit:
            defineLayer(scene.yafaray.passes.pass_Emit, "Color", "Emit")
            
        if scene.render.layers[0].use_pass_mist:
            defineLayer(scene.yafaray.passes.pass_Mist, "Gray", "Mist")
            
        if scene.render.layers[0].use_pass_diffuse:
            defineLayer(scene.yafaray.passes.pass_Diffuse, "Color", "Diffuse")
            
        if scene.render.layers[0].use_pass_specular:
            defineLayer(scene.yafaray.passes.pass_Spec, "Color", "Spec")
            
        if scene.render.layers[0].use_pass_ambient_occlusion:
            defineLayer(scene.yafaray.passes.pass_AO, "Color", "AO")
            
        if scene.render.layers[0].use_pass_environment:
            defineLayer(scene.yafaray.passes.pass_Env, "Color", "Env")
            
        if scene.render.layers[0].use_pass_indirect:
            defineLayer(scene.yafaray.passes.pass_Indirect, "Color", "Indirect")
            
        if scene.render.layers[0].use_pass_shadow:
            defineLayer(scene.yafaray.passes.pass_Shadow, "Color", "Shadow")
            
        if scene.render.layers[0].use_pass_reflection:
            defineLayer(scene.yafaray.passes.pass_Reflect, "Color", "Reflect")
            
        if scene.render.layers[0].use_pass_refraction:
            defineLayer(scene.yafaray.passes.pass_Refract, "Color", "Refract")
            
        if scene.render.layers[0].use_pass_object_index:
            defineLayer(scene.yafaray.passes.pass_IndexOB, "Gray", "IndexOB")
            
        if scene.render.layers[0].use_pass_material_index:
            defineLayer(scene.yafaray.passes.pass_IndexMA, "Gray", "IndexMA")
            
        if scene.render.layers[0].use_pass_diffuse_direct:
            defineLayer(scene.yafaray.passes.pass_Depth, "pass_DiffDir", "DiffDir")
            
        if scene.render.layers[0].use_pass_diffuse_indirect:
            defineLayer(scene.yafaray.passes.pass_DiffInd, "Color", "DiffInd")
            
        if scene.render.layers[0].use_pass_diffuse_color:
            defineLayer(scene.yafaray.passes.pass_DiffCol, "Color", "DiffCol")
            
        if scene.render.layers[0].use_pass_glossy_direct:
            defineLayer(scene.yafaray.passes.pass_GlossDir, "Color", "GlossDir")
            
        if scene.render.layers[0].use_pass_glossy_indirect:
            defineLayer(scene.yafaray.passes.pass_GlossInd, "Color", "GlossInd")
            
        if scene.render.layers[0].use_pass_glossy_color:
            defineLayer(scene.yafaray.passes.pass_GlossCol, "Color", "GlossCol")
            
        if scene.render.layers[0].use_pass_transmission_direct:
            defineLayer(scene.yafaray.passes.pass_TransDir, "Color", "TransDir")
            
        if scene.render.layers[0].use_pass_transmission_indirect:
            defineLayer(scene.yafaray.passes.pass_TransInd, "Color", "TransInd")
            
        if scene.render.layers[0].use_pass_transmission_color:
            defineLayer(scene.yafaray.passes.pass_TransCol, "Color", "TransCol")
            
        if scene.render.layers[0].use_pass_subsurface_direct:
            defineLayer(scene.yafaray.passes.pass_SubsurfaceDir, "Color", "SubsurfaceDir")
            
        if scene.render.layers[0].use_pass_subsurface_indirect:
            defineLayer(scene.yafaray.passes.pass_SubsurfaceInd, "Color", "SubsurfaceInd")
            
        if scene.render.layers[0].use_pass_subsurface_color:
            defineLayer(scene.yafaray.passes.pass_SubsurfaceCol, "Color", "SubsurfaceCol")

    
