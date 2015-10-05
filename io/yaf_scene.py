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
    yi.paramsSetBool("premult", scene.gs_premult)

    yi.paramsSetInt("tile_size", scene.gs_tile_size)
    yi.paramsSetString("tiles_order", scene.gs_tile_order)

    yi.paramsSetBool("z_channel", scene.gs_z_channel)

    if scene.gs_type_render == "into_blender":
        yi.paramsSetBool("normalize_z_channel", False)

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
