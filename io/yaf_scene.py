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
        bStartY = int(sizeY - maxY)
        bsizeX = int(maxX - minX)
        bsizeY = int(maxY - minY)

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
    yi.paramsSetFloat("AA_resampled_floor", scene.AA_resampled_floor)
    yi.paramsSetFloat("AA_sample_multiplier_factor", scene.AA_sample_multiplier_factor)
    yi.paramsSetFloat("AA_light_sample_multiplier_factor", scene.AA_light_sample_multiplier_factor)
    yi.paramsSetFloat("AA_indirect_sample_multiplier_factor", scene.AA_indirect_sample_multiplier_factor)
    yi.paramsSetBool("AA_detect_color_noise", scene.AA_detect_color_noise)
    yi.paramsSetFloat("AA_dark_threshold_factor", scene.AA_dark_threshold_factor)
    yi.paramsSetInt("AA_variance_edge_size", scene.AA_variance_edge_size)
    yi.paramsSetInt("AA_variance_pixels", scene.AA_variance_pixels)
    yi.paramsSetFloat("AA_clamp_samples", scene.AA_clamp_samples)
    yi.paramsSetFloat("AA_clamp_indirect", scene.AA_clamp_indirect)


def exportRenderSettings(yi, scene):
    yi.printInfo("Exporting Render Settings")

    render = scene.render

    [sizeX, sizeY, bStartX, bStartY, bsizeX, bsizeY, cam_data] = getRenderCoords(scene)

    yi.paramsSetString("camera_name", "cam")
    yi.paramsSetString("integrator_name", "default")
    yi.paramsSetString("volintegrator_name", "volintegr")

    output_device_color_space = "LinearRGB"
    output_device_gamma = 1.0

    if scene.gs_type_render == "file" or scene.gs_type_render == "xml":
        output_device_color_space = "sRGB"

        if scene.img_output == "OPEN_EXR" or scene.img_output == "HDR":  #If the output file is a HDR/EXR file, we force the render output to Linear
            output_device_color_space = "LinearRGB"
            
        elif scene.display_settings.display_device == "sRGB":
            output_device_color_space = "sRGB"
            
        elif scene.display_settings.display_device == "XYZ":
            output_device_color_space = "XYZ"
            
        elif scene.display_settings.display_device == "None":
            output_device_color_space = "Raw_Manual_Gamma"
            output_device_gamma = scene.gs_gamma  #We only use the selected gamma if the output device is set to "None"

    else:   #Render into Blender
        output_device_color_space = "LinearRGB"    #Blender expects a linear output from YafaRay

        if scene.display_settings.display_device == "sRGB" or scene.display_settings.display_device == "XYZ" or scene.display_settings.display_device == "Rec709":
            output_device_color_space = "LinearRGB"  #If we render into Blender, YafaRay generates linear output and Blender does the conversion to the color space
           
        elif scene.display_settings.display_device == "None":
            output_device_color_space = "Raw_Manual_Gamma"
            output_device_gamma = scene.gs_gamma  #We only use the selected gamma if the output device is set to "None"
        
    yi.paramsSetString("color_space", output_device_color_space)
    yi.paramsSetFloat("gamma", output_device_gamma)

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

    yi.paramsSetBool("clamp_rgb", scene.gs_clamp_rgb)
    yi.paramsSetBool("show_sam_pix", scene.gs_show_sam_pix)

    if scene.gs_type_render == "file" or scene.gs_type_render == "xml":
        yi.paramsSetBool("premult", scene.gs_premult)
    else:
        yi.paramsSetBool("premult", True)   #We force alpha premultiply when rendering into Blender as it expects premultiplied input

    yi.paramsSetInt("tile_size", scene.gs_tile_size)
    yi.paramsSetString("tiles_order", scene.gs_tile_order)

    yi.paramsSetBool("drawParams", scene.gs_draw_params)
    yi.paramsSetString("customString", scene.gs_custom_string)

    if scene.gs_auto_threads:
        yi.paramsSetInt("threads", -1)
    else:
        yi.paramsSetInt("threads", scene.gs_threads)

    yi.paramsSetString("background_name", "world_background")

    yi.paramsSetBool("adv_auto_shadow_bias_enabled", scene.adv_auto_shadow_bias_enabled)
    yi.paramsSetFloat("adv_shadow_bias_value", scene.adv_shadow_bias_value)
    yi.paramsSetBool("adv_auto_min_raydist_enabled", scene.adv_auto_min_raydist_enabled)
    yi.paramsSetFloat("adv_min_raydist_value", scene.adv_min_raydist_value)

    yi.paramsSetBool("pass_enable", scene.pass_enable)
    
    yi.paramsSetInt("pass_mask_obj_index", scene.pass_mask_obj_index)
    yi.paramsSetInt("pass_mask_mat_index", scene.pass_mask_mat_index)
    yi.paramsSetBool("pass_mask_invert", scene.pass_mask_invert)
    yi.paramsSetBool("pass_mask_only", scene.pass_mask_only)
    
    if scene.pass_enable and scene.render.layers[0].use_pass_z:
        yi.paramsSetString("pass_Depth", scene.pass_Depth)
    else:
        yi.paramsSetString("pass_Depth", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_vector:
        yi.paramsSetString("pass_Vector", scene.pass_Vector)
    else:
        yi.paramsSetString("pass_Vector", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_normal:
        yi.paramsSetString("pass_Normal", scene.pass_Normal)
    else:
        yi.paramsSetString("pass_Normal", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_uv:
        yi.paramsSetString("pass_UV", scene.pass_UV)
    else:
        yi.paramsSetString("pass_UV", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_color:
        yi.paramsSetString("pass_Color", scene.pass_Color)
    else:
        yi.paramsSetString("pass_Color", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_emit:
        yi.paramsSetString("pass_Emit", scene.pass_Emit)
    else:
        yi.paramsSetString("pass_Emit", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_mist:
        yi.paramsSetString("pass_Mist", scene.pass_Mist)
    else:
        yi.paramsSetString("pass_Mist", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_diffuse:
        yi.paramsSetString("pass_Diffuse", scene.pass_Diffuse)
    else:
        yi.paramsSetString("pass_Diffuse", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_specular:
        yi.paramsSetString("pass_Spec", scene.pass_Spec)
    else:
        yi.paramsSetString("pass_Spec", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_ambient_occlusion:
        yi.paramsSetString("pass_AO", scene.pass_AO)
    else:
        yi.paramsSetString("pass_AO", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_environment:
        yi.paramsSetString("pass_Env", scene.pass_Env)
    else:
        yi.paramsSetString("pass_Env", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_indirect:
        yi.paramsSetString("pass_Indirect", scene.pass_Indirect)
    else:
        yi.paramsSetString("pass_Indirect", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_shadow:
        yi.paramsSetString("pass_Shadow", scene.pass_Shadow)
    else:
        yi.paramsSetString("pass_Shadow", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_reflection:
        yi.paramsSetString("pass_Reflect", scene.pass_Reflect)
    else:
        yi.paramsSetString("pass_Reflect", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_refraction:
        yi.paramsSetString("pass_Refract", scene.pass_Refract)
    else:
        yi.paramsSetString("pass_Refract", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_object_index:
        yi.paramsSetString("pass_IndexOB", scene.pass_IndexOB)
    else:
        yi.paramsSetString("pass_IndexOB", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_material_index:
        yi.paramsSetString("pass_IndexMA", scene.pass_IndexMA)
    else:
        yi.paramsSetString("pass_IndexMA", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_diffuse_direct:
        yi.paramsSetString("pass_DiffDir", scene.pass_DiffDir)
    else:
        yi.paramsSetString("pass_DiffDir", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_diffuse_indirect:
        yi.paramsSetString("pass_DiffInd", scene.pass_DiffInd)
    else:
        yi.paramsSetString("pass_DiffInd", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_diffuse_color:
        yi.paramsSetString("pass_DiffCol", scene.pass_DiffCol)
    else:
        yi.paramsSetString("pass_DiffCol", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_glossy_direct:
        yi.paramsSetString("pass_GlossDir", scene.pass_GlossDir)
    else:
        yi.paramsSetString("pass_GlossDir", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_glossy_indirect:
        yi.paramsSetString("pass_GlossInd", scene.pass_GlossInd)
    else:
        yi.paramsSetString("pass_GlossInd", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_glossy_color:
        yi.paramsSetString("pass_GlossCol", scene.pass_GlossCol)
    else:
        yi.paramsSetString("pass_GlossCol", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_transmission_direct:
        yi.paramsSetString("pass_TransDir", scene.pass_TransDir)
    else:
        yi.paramsSetString("pass_TransDir", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_transmission_indirect:
        yi.paramsSetString("pass_TransInd", scene.pass_TransInd)
    else:
        yi.paramsSetString("pass_TransInd", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_transmission_color:
        yi.paramsSetString("pass_TransCol", scene.pass_TransCol)
    else:
        yi.paramsSetString("pass_TransCol", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_subsurface_direct:
        yi.paramsSetString("pass_SubsurfaceDir", scene.pass_SubsurfaceDir)
    else:
        yi.paramsSetString("pass_SubsurfaceDir", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_subsurface_indirect:
        yi.paramsSetString("pass_SubsurfaceInd", scene.pass_SubsurfaceInd)
    else:
        yi.paramsSetString("pass_SubsurfaceInd", "disabled")
        
    if scene.pass_enable and scene.render.layers[0].use_pass_subsurface_color:
        yi.paramsSetString("pass_SubsurfaceCol", scene.pass_SubsurfaceCol)
    else:
        yi.paramsSetString("pass_SubsurfaceCol", "disabled")
        
    
