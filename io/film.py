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
import mathutils
import libyafaray4_bindings
from ..util.math import multiply_matrix4x4_vector4


class Film:
    def __init__(self, yaf_film, yaf_logger, is_preview):
        self.yaf_film = yaf_film
        self.yaf_logger = yaf_logger
        self.is_preview = is_preview

    def define_camera(self, bl_camera, res_x, res_y, res_percentage, use_view_to_render, view_matrix):
        if use_view_to_render and view_matrix:
            # use the view matrix to calculate the inverted transformed
            # points cam pos (0,0,0), front (0,0,1) and up (0,1,0)
            # view matrix works like the opengl view part of the
            # projection matrix, i.e. transforms everything so camera is
            # at 0,0,0 looking towards 0,0,1 (y axis being up)
            inv = view_matrix.inverted()

            pos = multiply_matrix4x4_vector4(inv, mathutils.Vector((0, 0, 0, 1)))
            above_cam = multiply_matrix4x4_vector4(inv, mathutils.Vector((0, 1, 0, 1)))
            front_cam = multiply_matrix4x4_vector4(inv, mathutils.Vector((0, 0, 1, 1)))

            direction = front_cam - pos
            up = above_cam

        else:
            # get cam worldspace transformation matrix, e.g. if cam is parented matrix_local does not work
            matrix = bl_camera.matrix_world.copy()
            # matrix indexing (row, colums) changed in Blender rev.42816, for explanation see also:
            # http://wiki.blender.org/index.php/User:TrumanBlending/Matrix_Indexing
            pos = matrix.col[3]
            direction = matrix.col[2]
            up = pos + matrix.col[1]

        to = pos - direction

        x = int(res_x * res_percentage * 0.01)
        y = int(res_y * res_percentage * 0.01)

        yaf_param_map = libyafaray4_bindings.ParamMap()

        if use_view_to_render:
            yaf_param_map.setString("type", "perspective")
            yaf_param_map.setFloat("focal", 0.7)

        else:
            cam_type = bl_camera.camera_type

            yaf_param_map.setString("type", cam_type)

            if bl_camera.use_clipping:
                yaf_param_map.setFloat("nearClip", bl_camera.clip_start)
                yaf_param_map.setFloat("farClip", bl_camera.clip_end)

            if cam_type == "orthographic":
                yaf_param_map.setFloat("scale", bl_camera.ortho_scale)

            elif cam_type in {"perspective", "architect"}:
                # Blenders GSOC 2011 project "tomato branch" merged into trunk.
                # Check for sensor settings and use them in yafaray exporter also.
                if bl_camera.sensor_fit == 'AUTO':
                    horizontal_fit = (x > y)
                    sensor_size = bl_camera.sensor_width
                elif bl_camera.sensor_fit == 'HORIZONTAL':
                    horizontal_fit = True
                    sensor_size = bl_camera.sensor_width
                else:
                    horizontal_fit = False
                    sensor_size = bl_camera.sensor_height

                if horizontal_fit:
                    f_aspect = 1.0
                else:
                    f_aspect = x / y

                yaf_param_map.setFloat("focal", bl_camera.lens / (f_aspect * sensor_size))

                # DOF params, only valid for real camera
                # use DOF object distance if present or fixed DOF
                if bpy.app.version >= (2, 80, 0):
                    pass  # FIXME BLENDER 2.80-3.00
                else:
                    if bl_camera.dof_object is not None:
                        # use DOF object distance
                        dist = (pos.xyz - bl_camera.dof_object.location.xyz).length
                        dof_distance = dist
                    else:
                        # use fixed DOF distance
                        dof_distance = bl_camera.dof_distance
                    yaf_param_map.setFloat("dof_distance", dof_distance)

                yaf_param_map.setFloat("aperture", bl_camera.aperture)
                # bokeh params
                yaf_param_map.setString("bokeh_type", bl_camera.bokeh_type)
                yaf_param_map.setFloat("bokeh_rotation", bl_camera.bokeh_rotation)

            elif cam_type == "angular":
                yaf_param_map.setBool("circular", bl_camera.circular)
                yaf_param_map.setBool("mirrored", bl_camera.mirrored)
                yaf_param_map.setString("projection", bl_camera.angular_projection)
                yaf_param_map.setFloat("max_angle", bl_camera.max_angle)
                yaf_param_map.setFloat("angle", bl_camera.angular_angle)

        yaf_param_map.setInt("resx", x)
        yaf_param_map.setInt("resy", y)

        if self.is_preview and bpy.data.scenes[0].yafaray.is_preview.enable:

                #incl = bpy.data.scenes[0].yafaray.preview.camRotIncl
                #azi = bpy.data.scenes[0].yafaray.preview.camRotAzi
                rot = bpy.data.scenes[0].yafaray.is_preview.camRot
                dist = bpy.data.scenes[0].yafaray.is_preview.camDist

                #pos = (dist*math.sin(incl)*math.cos(azi), dist*math.sin(incl)*math.sin(azi), dist*math.cos(incl))
                #up = (math.sin(rotZ), 0, math.cos(rotZ))
                pos = (-dist*rot[0], -dist*rot[2], -dist*rot[1])
                up = (0,0,1)
                to = (0,0,0)

        yaf_param_map.setVector("from", pos[0], pos[1], pos[2])
        yaf_param_map.setVector("up", up[0], up[1], up[2])
        yaf_param_map.setVector("to", to[0], to[1], to[2])
        self.yaf_film.defineCamera(yaf_param_map)



def computeSceneSize(render):
    sizeX = int(render.resolution_x * render.resolution_percentage * 0.01)
    sizeY = int(render.resolution_y * render.resolution_percentage * 0.01)
    return [sizeX, sizeY]


def get_render_coords(bl_scene):
    render = bl_scene.render
    [sizeX, sizeY] = computeSceneSize(render)

    bStartX = 0
    bStartY = 0
    bsizeX = 0
    bsizeY = 0

    cam_data = None

    if bl_scene.objects:
        for item in bl_scene.objects:
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


def exportAA(yi, bl_scene, yaf_param_map):
    yaf_param_map.setInt("AA_passes", bl_scene.AA_passes)
    yaf_param_map.setInt("AA_minsamples", bl_scene.AA_min_samples)
    yaf_param_map.setInt("AA_inc_samples", bl_scene.AA_inc_samples)
    yaf_param_map.setFloat("AA_pixelwidth", bl_scene.AA_pixelwidth)
    yaf_param_map.setFloat("AA_threshold", bl_scene.AA_threshold)
    yaf_param_map.setString("filter_type", bl_scene.AA_filter_type)
    yaf_param_map.setFloat("AA_resampled_floor", bl_scene.yafaray.noise_control.resampled_floor)
    yaf_param_map.setFloat("AA_sample_multiplier_factor", bl_scene.yafaray.noise_control.sample_multiplier_factor)
    yaf_param_map.setFloat("AA_light_sample_multiplier_factor", bl_scene.yafaray.noise_control.light_sample_multiplier_factor)
    yaf_param_map.setFloat("AA_indirect_sample_multiplier_factor", bl_scene.yafaray.noise_control.indirect_sample_multiplier_factor)
    yaf_param_map.setBool("AA_detect_color_noise", bl_scene.yafaray.noise_control.detect_color_noise)
    yaf_param_map.setString("AA_dark_detection_type", bl_scene.yafaray.noise_control.dark_detection_type)
    yaf_param_map.setFloat("AA_dark_threshold_factor", bl_scene.yafaray.noise_control.dark_threshold_factor)
    yaf_param_map.setInt("AA_variance_edge_size", bl_scene.yafaray.noise_control.variance_edge_size)
    yaf_param_map.setInt("AA_variance_pixels", bl_scene.yafaray.noise_control.variance_pixels)
    yaf_param_map.setFloat("AA_clamp_samples", bl_scene.yafaray.noise_control.clamp_samples)
    yaf_param_map.setFloat("AA_clamp_indirect", bl_scene.yafaray.noise_control.clamp_indirect)
    yaf_param_map.setBool("background_resampling", bl_scene.yafaray.noise_control.background_resampling)

    if bl_scene.name == "preview" and bpy.data.scenes[0].yafaray.is_preview.enable:
        yaf_param_map.setInt("AA_passes", bpy.data.scenes[0].yafaray.is_preview.previewAApasses)
        yaf_param_map.setFloat("AA_threshold", 0.01)


def exportRenderSettings(yi, depsgraph, render_path, render_filename):
    self.yaf_logger.printVerbose("Exporting Render Settings")
    scene = scene_from_depsgraph(depsgraph)
    render = scene.render

    [sizeX, sizeY, bStartX, bStartY, bsizeX, bsizeY, cam_data] = get_render_coords(scene)

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

    if scene.name == "preview" and bpy.data.scenes[0].yafaray.is_preview.enable:
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


def calc_alpha_premultiply(bl_scene):
    alpha_premult = namedtuple("alpha_premult", ["blender", "secondary_output"])
    if bl_scene.gs_premult == "auto":
        if bl_scene.img_output == "PNG" or bl_scene.img_output == "JPEG":
            enable_premult = False
        else:
            enable_premult = True
    elif bl_scene.gs_premult == "yes":
        enable_premult = True
    else:
        enable_premult = False

    if bl_scene.gs_type_render == "into_blender":
        # We force alpha premultiply when rendering into Blender as it expects premultiplied input
        # In case we use a secondary file output, we set the premultiply according to the Blender setting
        return alpha_premult(True, enable_premult)
    else:
        # In this case we use the calculated enable premult value, and leave the second value as False as there is no secondary output in this case
        return alpha_premult(enable_premult, False)


def calc_gamma(bl_scene):
    gamma = namedtuple("gamma", ["blender", "secondary_output"])
    gamma_1 = 1.0
    gamma_2 = 1.0
    if bl_scene.gs_type_render == "into_blender" and bl_scene.display_settings.display_device == "None":
        gamma_1 = bl_scene.gs_gamma  # We only use the selected gamma if the output device is set to "None"
        if bl_scene.display_settings.display_device == "None":
            gamma_2 = bl_scene.gs_gamma  #We only use the selected gamma if the output device is set to "None"
    elif bl_scene.display_settings.display_device == "None":
        gamma_1 = bl_scene.gs_gamma  # We only use the selected gamma if the output device is set to "None"

    return gamma(gamma_1, gamma_2)


def calc_color_space(bl_scene):
    color_space = namedtuple("color_space", ["blender", "secondary_output"])
    color_space_2 = "sRGB"

    if bl_scene.gs_type_render == "into_blender":
        if bl_scene.display_settings.display_device == "None":
            color_space_1 = "Raw_Manual_Gamma"
        else:
            color_space_1 = "LinearRGB"  #For all other Blender display devices, it expects a linear output from YafaRay
        #Optional Secondary file output color space
        if bl_scene.img_output == "OPEN_EXR" or bl_scene.img_output == "HDR":  #If the output file is a HDR/EXR file, we force the render output to Linear
            color_space_2 = "LinearRGB"
        elif bl_scene.display_settings.display_device == "sRGB":
            color_space_2 = "sRGB"
        elif bl_scene.display_settings.display_device == "XYZ":
            color_space_2 = "XYZ"
        elif bl_scene.display_settings.display_device == "None":
            color_space_2 = "Raw_Manual_Gamma"
    else:
        if bl_scene.img_output == "OPEN_EXR" or bl_scene.img_output == "HDR":  # If the output file is a HDR/EXR file, we force the render output to Linear
            color_space_1 = "LinearRGB"
        elif bl_scene.display_settings.display_device == "sRGB":
            color_space_1 = "sRGB"
        elif bl_scene.display_settings.display_device == "XYZ":
            color_space_1 = "XYZ"
        elif bl_scene.display_settings.display_device == "None":
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



    def decide_output_file_name(self, output_path, filetype):

        switch_file_type = {
            'PNG': 'png',
            'TARGA': 'tga',
            'TIFF': 'tif',
            'JPEG': 'jpg',
            'HDR': 'hdr',
            'OPEN_EXR': 'exr',
            'xml': 'xml',
            'c': 'c',
            'python': 'py',
        }
        filetype = switch_file_type.get(filetype, 'png')
        # write image or XML-File with filename from framenumber
        frame_numb_str = "{:0" + str(len(str(self.bl_scene.frame_end))) + "d}"

        filebasename = ""
        if self.bl_scene.img_add_blend_name:
            if bpy.data.filepath == "":
                filebasename += "temp"
            filebasename += os.path.splitext(os.path.basename(bpy.data.filepath))[0] + " - "

        filebasename += frame_numb_str.format(self.bl_scene.frame_current)

        if self.bl_scene.img_add_datetime:
            filebasename += " (" + datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S") + ")"

        output = os.path.join(output_path, filebasename)
        # try to create dir if it not exists...
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
            except:
                print("Unable to create directory...")
                import traceback
                traceback.print_exc()
                output = ""
        outputFile = output + "." + filetype

        return outputFile, output, filetype

    def define_image_output(self, output_name, fp, bl_scene, bl_render, color_space, gamma, alpha_premultiply):
        self.output_file, self.output, self.file_type = self.decide_output_file_name(fp, bl_scene.img_output)
        yaf_param_map = libyafaray4_bindings.ParamMap()
        yaf_param_map.setString("image_path", str(self.output_file))
        yaf_param_map.setString("color_space", color_space)
        yaf_param_map.setFloat("gamma", gamma)
        yaf_param_map.setBool("alpha_premultiply", alpha_premultiply)
        yaf_param_map.setBool("multi_layer", bl_scene.img_multilayer)
        yaf_param_map.setBool("denoise_enabled", bl_scene.img_denoise)
        yaf_param_map.setInt("denoise_h_lum", bl_scene.img_denoiseHLum)
        yaf_param_map.setInt("denoise_h_col", bl_scene.img_denoiseHCol)
        yaf_param_map.setFloat("denoise_mix", bl_scene.img_denoiseMix)
        print(bl_render.image_settings.color_mode)
        yaf_param_map.setBool("alpha_channel", bl_render.image_settings.color_mode == "RGBA")
        # self.yaf_film.setLoggingAndBadgeSettings(self.yaf_scene, self.scene)
        self.co = self.film.yaf_film.createOutput(output_name, yaf_param_map)
