# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
import mathutils
import libyafaray4_bindings
from ..util.math import multiply_matrix4x4_vector4


class Film:
    def __init__(self, film_yafaray, logger, is_preview):
        self.film_yafaray = film_yafaray
        self.logger = logger
        self.is_preview = is_preview

    def define_camera(self, camera, res_x, res_y, res_percentage, use_view_to_render, view_matrix):
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
            matrix = camera.matrix_world.copy()
            # matrix indexing (row, colums) changed in Blender rev.42816, for explanation see also:
            # http://wiki.blender.org/index.php/User:TrumanBlending/Matrix_Indexing
            pos = matrix.col[3]
            direction = matrix.col[2]
            up = pos + matrix.col[1]

        to = pos - direction

        x = int(res_x * res_percentage * 0.01)
        y = int(res_y * res_percentage * 0.01)

        param_map = libyafaray4_bindings.ParamMap()

        if use_view_to_render:
            param_map.set_string("type", "perspective")
            param_map.set_float("focal", 0.7)

        else:
            cam_type = camera.camera_type

            param_map.set_string("type", cam_type)

            if camera.use_clipping:
                param_map.set_float("nearClip", camera.clip_start)
                param_map.set_float("farClip", camera.clip_end)

            if cam_type == "orthographic":
                param_map.set_float("scale", camera.ortho_scale)

            elif cam_type in {"perspective", "architect"}:
                # Blenders GSOC 2011 project "tomato branch" merged into trunk.
                # Check for sensor settings and use them in yafaray exporter also.
                if camera.sensor_fit == 'AUTO':
                    horizontal_fit = (x > y)
                    sensor_size = camera.sensor_width
                elif camera.sensor_fit == 'HORIZONTAL':
                    horizontal_fit = True
                    sensor_size = camera.sensor_width
                else:
                    horizontal_fit = False
                    sensor_size = camera.sensor_height

                if horizontal_fit:
                    f_aspect = 1.0
                else:
                    f_aspect = x / y

                param_map.set_float("focal", camera.lens / (f_aspect * sensor_size))

                # DOF params, only valid for real camera
                # use DOF object distance if present or fixed DOF
                if bpy.app.version >= (2, 80, 0):
                    pass  # FIXME BLENDER >= v2.80
                else:
                    if camera.dof_object is not None:
                        # use DOF object distance
                        dist = (pos.xyz - camera.dof_object.location.xyz).length
                        dof_distance = dist
                    else:
                        # use fixed DOF distance
                        dof_distance = camera.dof_distance
                    param_map.set_float("dof_distance", dof_distance)

                param_map.set_float("aperture", camera.aperture)
                # bokeh params
                param_map.set_string("bokeh_type", camera.bokeh_type)
                param_map.set_float("bokeh_rotation", camera.bokeh_rotation)

            elif cam_type == "angular":
                param_map.set_bool("circular", camera.circular)
                param_map.set_bool("mirrored", camera.mirrored)
                param_map.set_string("projection", camera.angular_projection)
                param_map.set_float("max_angle", camera.max_angle)
                param_map.set_float("angle", camera.angular_angle)

        param_map.set_int("resx", x)
        param_map.set_int("resy", y)

        if self.is_preview and bpy.data.scenes[0].yafaray.preview.enable:

                #incl = bpy.data.scenes[0].yafaray.preview.camRotIncl
                #azi = bpy.data.scenes[0].yafaray.preview.camRotAzi
                rot = bpy.data.scenes[0].yafaray.preview.cam_rot
                dist = bpy.data.scenes[0].yafaray.preview.cam_dist

                #pos = (dist*math.sin(incl)*math.cos(azi), dist*math.sin(incl)*math.sin(azi), dist*math.cos(incl))
                #up = (math.sin(rotZ), 0, math.cos(rotZ))
                pos = (-dist*rot[0], -dist*rot[2], -dist*rot[1])
                up = (0,0,1)
                to = (0,0,0)

        param_map.set_vector("from", pos[0], pos[1], pos[2])
        param_map.set_vector("up", up[0], up[1], up[2])
        param_map.set_vector("to", to[0], to[1], to[2])
        self.film_yafaray.defineCamera(param_map)



def computeSceneSize(render):
    sizeX = int(render.resolution_x * render.resolution_percentage * 0.01)
    sizeY = int(render.resolution_y * render.resolution_percentage * 0.01)
    return [sizeX, sizeY]


def get_render_coords(scene_blender):
    render = scene_blender.render
    [sizeX, sizeY] = computeSceneSize(render)

    bStartX = 0
    bStartY = 0
    bsizeX = 0
    bsizeY = 0

    cam_data = None

    if scene_blender.objects:
        for item in scene_blender.objects:
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


def exportAA(yi, scene_blender, param_map):
    param_map.set_int("AA_passes", scene_blender.AA_passes)
    param_map.set_int("AA_minsamples", scene_blender.AA_min_samples)
    param_map.set_int("AA_inc_samples", scene_blender.AA_inc_samples)
    param_map.set_float("AA_pixelwidth", scene_blender.AA_pixelwidth)
    param_map.set_float("AA_threshold", scene_blender.AA_threshold)
    param_map.set_string("filter_type", scene_blender.AA_filter_type)
    param_map.set_float("AA_resampled_floor", scene_blender.yafaray4.noise_control.resampled_floor)
    param_map.set_float("AA_sample_multiplier_factor", scene_blender.yafaray4.noise_control.sample_multiplier_factor)
    param_map.set_float("AA_light_sample_multiplier_factor", scene_blender.yafaray4.noise_control.light_sample_multiplier_factor)
    param_map.set_float("AA_indirect_sample_multiplier_factor", scene_blender.yafaray4.noise_control.indirect_sample_multiplier_factor)
    param_map.set_bool("AA_detect_color_noise", scene_blender.yafaray4.noise_control.detect_color_noise)
    param_map.set_string("AA_dark_detection_type", scene_blender.yafaray4.noise_control.dark_detection_type)
    param_map.set_float("AA_dark_threshold_factor", scene_blender.yafaray4.noise_control.dark_threshold_factor)
    param_map.set_int("AA_variance_edge_size", scene_blender.yafaray4.noise_control.variance_edge_size)
    param_map.set_int("AA_variance_pixels", scene_blender.yafaray4.noise_control.variance_pixels)
    param_map.set_float("AA_clamp_samples", scene_blender.yafaray4.noise_control.clamp_samples)
    param_map.set_float("AA_clamp_indirect", scene_blender.yafaray4.noise_control.clamp_indirect)
    param_map.set_bool("background_resampling", scene_blender.yafaray4.noise_control.background_resampling)

    if scene_blender.name == "preview" and bpy.data.scenes[0].yafaray.preview.enable:
        param_map.set_int("AA_passes", bpy.data.scenes[0].yafaray.preview.preview_aa_passes)
        param_map.set_float("AA_threshold", 0.01)


def exportRenderSettings(yi, depsgraph, render_path, render_filename):
    self.logger.printVerbose("Exporting Render Settings")
    scene = scene_from_depsgraph(depsgraph)
    render = scene.render

    [sizeX, sizeY, bStartX, bStartY, bsizeX, bsizeY, cam_data] = get_render_coords(scene)

    param_map.set_string("scene_accelerator", scene.gs_accelerator)

    exportAA(yi, scene)

    param_map.set_int("xstart", bStartX)
    param_map.set_int("ystart", bStartY)

    # no border when rendering to view
    if render.use_border and cam_data:
        param_map.set_int("width", bsizeX)
        param_map.set_int("height", bsizeY)
    else:
        param_map.set_int("width", sizeX)
        param_map.set_int("height", sizeY)

    param_map.set_bool("show_sam_pix", scene.gs_show_sam_pix)

    if scene.name == "preview" and bpy.data.scenes[0].yafaray.preview.enable:
        param_map.set_bool("show_sam_pix", False)

    param_map.set_int("tile_size", scene.gs_tile_size)
    param_map.set_string("tiles_order", scene.gs_tile_order)

    if scene.gs_auto_threads:
        param_map.set_int("threads", -1)
        param_map.set_int("threads_photons", -1)
    else:
        param_map.set_int("threads", scene.gs_threads)
        param_map.set_int("threads_photons", scene.gs_threads)

    param_map.set_string("images_autosave_interval_type", scene.gs_images_autosave_interval_type)
    param_map.set_int("images_autosave_interval_passes", scene.gs_images_autosave_interval_passes)
    param_map.set_float("images_autosave_interval_seconds", scene.gs_images_autosave_interval_seconds)

    param_map.set_string("film_load_save_mode", scene.gs_film_save_load)
    param_map.set_string("film_load_save_path", render_path + "/" + render_filename)
    param_map.set_string("film_autosave_interval_type", scene.gs_film_autosave_interval_type)
    param_map.set_int("film_autosave_interval_passes", scene.gs_film_autosave_interval_passes)
    param_map.set_float("film_autosave_interval_seconds", scene.gs_film_autosave_interval_seconds)

    param_map.set_bool("adv_auto_shadow_bias_enabled", scene.adv_auto_shadow_bias_enabled)
    param_map.set_float("adv_shadow_bias_value", scene.adv_shadow_bias_value)
    param_map.set_bool("adv_auto_min_raydist_enabled", scene.adv_auto_min_raydist_enabled)
    param_map.set_float("adv_min_raydist_value", scene.adv_min_raydist_value)
    param_map.set_float("adv_min_raydist_value", scene.adv_min_raydist_value)
    param_map.set_int("adv_base_sampling_offset", scene.adv_base_sampling_offset)
    if bpy.app.version >= (2, 80, 0):
        pass   # FIXME BLENDER >= v2.80
    else:
        param_map.set_int("adv_computer_node", bpy.context.user_preferences.addons["yafaray4"].preferences.yafaray_computer_node)

    param_map.set_int("layer_mask_obj_index", scene.yafaray4.passes.pass_mask_obj_index)
    param_map.set_int("layer_mask_mat_index", scene.yafaray4.passes.pass_mask_mat_index)
    param_map.set_bool("layer_mask_invert", scene.yafaray4.passes.pass_mask_invert)
    param_map.set_bool("layer_mask_only", scene.yafaray4.passes.pass_mask_only)

    param_map.set_int("layer_object_edge_thickness", scene.yafaray4.passes.object_edge_thickness)
    param_map.set_int("layer_faces_edge_thickness", scene.yafaray4.passes.faces_edge_thickness)
    param_map.set_float("layer_object_edge_threshold", scene.yafaray4.passes.object_edge_threshold)
    param_map.set_float("layer_faces_edge_threshold", scene.yafaray4.passes.faces_edge_threshold)
    param_map.set_float("layer_object_edge_smoothness", scene.yafaray4.passes.object_edge_smoothness)
    param_map.set_float("layer_faces_edge_smoothness", scene.yafaray4.passes.faces_edge_smoothness)
    param_map.set_color("layer_toon_edge_color", scene.yafaray4.passes.toon_edge_color[0],
                            scene.yafaray4.passes.toon_edge_color[1], scene.yafaray4.passes.toon_edge_color[2])
    param_map.set_float("layer_toon_pre_smooth", scene.yafaray4.passes.toon_pre_smooth)
    param_map.set_float("layer_toon_post_smooth", scene.yafaray4.passes.toon_post_smooth)
    param_map.set_float("layer_toon_quantization", scene.yafaray4.passes.toon_quantization)


def setLoggingAndBadgeSettings(yi, scene):
    self.logger.printVerbose("Exporting Logging and Badge settings")
    param_map.set_bool("badge_draw_render_settings", scene.yafaray4.logging.draw_render_settings)
    param_map.set_bool("badge_draw_aa_noise_settings", scene.yafaray4.logging.draw_aa_noise_settings)
    param_map.set_bool("logging_save_txt", scene.yafaray4.logging.save_log)
    param_map.set_bool("logging_save_html", scene.yafaray4.logging.save_html)
    param_map.set_string("badge_position", scene.yafaray4.logging.params_badge_position)
    param_map.set_string("badge_title", scene.yafaray4.logging.title)
    param_map.set_string("badge_author", scene.yafaray4.logging.author)
    param_map.set_string("badge_contact", scene.yafaray4.logging.contact)
    param_map.set_string("badge_comment", scene.yafaray4.logging.comments)
    if scene.yafaray4.logging.custom_icon != "":
        param_map.set_string("badge_icon_path", os.path.abspath(bpy.path.abspath(scene.yafaray4.logging.custom_icon)))
    param_map.set_string("badge_font_path", scene.yafaray4.logging.custom_font)
    param_map.set_float("badge_font_size_factor", scene.yafaray4.logging.font_scale)


def calc_alpha_premultiply(scene_blender):
    alpha_premult = namedtuple("alpha_premult", ["blender", "secondary_output"])
    if scene_blender.gs_premult == "auto":
        if scene_blender.img_output == "PNG" or scene_blender.img_output == "JPEG":
            enable_premult = False
        else:
            enable_premult = True
    elif scene_blender.gs_premult == "yes":
        enable_premult = True
    else:
        enable_premult = False

    if scene_blender.gs_type_render == "into_blender":
        # We force alpha premultiply when rendering into Blender as it expects premultiplied input
        # In case we use a secondary file output, we set the premultiply according to the Blender setting
        return alpha_premult(True, enable_premult)
    else:
        # In this case we use the calculated enable premult value, and leave the second value as False as there is no secondary output in this case
        return alpha_premult(enable_premult, False)


def calc_gamma(scene_blender):
    gamma = namedtuple("gamma", ["blender", "secondary_output"])
    gamma_1 = 1.0
    gamma_2 = 1.0
    if scene_blender.gs_type_render == "into_blender" and scene_blender.display_settings.display_device == "None":
        gamma_1 = scene_blender.gs_gamma  # We only use the selected gamma if the output device is set to "None"
        if scene_blender.display_settings.display_device == "None":
            gamma_2 = scene_blender.gs_gamma  #We only use the selected gamma if the output device is set to "None"
    elif scene_blender.display_settings.display_device == "None":
        gamma_1 = scene_blender.gs_gamma  # We only use the selected gamma if the output device is set to "None"

    return gamma(gamma_1, gamma_2)


def calc_color_space(scene_blender):
    color_space = namedtuple("color_space", ["blender", "secondary_output"])
    color_space_2 = "sRGB"

    if scene_blender.gs_type_render == "into_blender":
        if scene_blender.display_settings.display_device == "None":
            color_space_1 = "Raw_Manual_Gamma"
        else:
            color_space_1 = "LinearRGB"  #For all other Blender display devices, it expects a linear output from YafaRay
        #Optional Secondary file output color space
        if scene_blender.img_output == "OPEN_EXR" or scene_blender.img_output == "HDR":  #If the output file is a HDR/EXR file, we force the render output to Linear
            color_space_2 = "LinearRGB"
        elif scene_blender.display_settings.display_device == "sRGB":
            color_space_2 = "sRGB"
        elif scene_blender.display_settings.display_device == "XYZ":
            color_space_2 = "XYZ"
        elif scene_blender.display_settings.display_device == "None":
            color_space_2 = "Raw_Manual_Gamma"
    else:
        if scene_blender.img_output == "OPEN_EXR" or scene_blender.img_output == "HDR":  # If the output file is a HDR/EXR file, we force the render output to Linear
            color_space_1 = "LinearRGB"
        elif scene_blender.display_settings.display_device == "sRGB":
            color_space_1 = "sRGB"
        elif scene_blender.display_settings.display_device == "XYZ":
            color_space_1 = "XYZ"
        elif scene_blender.display_settings.display_device == "None":
            color_space_1 = "Raw_Manual_Gamma"
        else:
            color_space_1 = "sRGB"

    return color_space(color_space_1, color_space_2)

def defineLayers(yi, depsgraph):
    self.logger.printVerbose("Exporting Render Passes settings")
    scene = scene_from_depsgraph(depsgraph)

    def defineLayer(layer_type, exported_image_type, exported_image_name):
        param_map.set_string("type", layer_type)
        param_map.set_string("image_type", exported_image_type)
        param_map.set_string("exported_image_name", exported_image_name)
        param_map.set_string("exported_image_type", exported_image_type)
        yi.defineLayer()
        param_map = libyafaray4_bindings.ParamMap()

    defineLayer("combined", "ColorAlpha", "Combined")

    if scene.yafaray4.passes.pass_enable:
        if scene.render.layers[0].use_pass_z:
            defineLayer(scene.yafaray4.passes.pass_depth, "Gray", "Depth")

        if scene.render.layers[0].use_pass_vector:
            defineLayer(scene.yafaray4.passes.pass_vector, "ColorAlpha", "Vector")

        if scene.render.layers[0].use_pass_normal:
            defineLayer(scene.yafaray4.passes.pass_normal, "Color", "Normal")

        if scene.render.layers[0].use_pass_uv:
            defineLayer(scene.yafaray4.passes.pass_uv, "Color", "UV")

        if scene.render.layers[0].use_pass_color:
            defineLayer(scene.yafaray4.passes.pass_color, "ColorAlpha", "Color")

        if scene.render.layers[0].use_pass_emit:
            defineLayer(scene.yafaray4.passes.pass_emit, "Color", "Emit")

        if scene.render.layers[0].use_pass_mist:
            defineLayer(scene.yafaray4.passes.pass_mist, "Gray", "Mist")

        if scene.render.layers[0].use_pass_diffuse:
            defineLayer(scene.yafaray4.passes.pass_diffuse, "Color", "Diffuse")

        if scene.render.layers[0].use_pass_specular:
            defineLayer(scene.yafaray4.passes.pass_spec, "Color", "Spec")

        if scene.render.layers[0].use_pass_ambient_occlusion:
            defineLayer(scene.yafaray4.passes.pass_ao, "Color", "AO")

        if scene.render.layers[0].use_pass_environment:
            defineLayer(scene.yafaray4.passes.pass_env, "Color", "Env")

        if scene.render.layers[0].use_pass_indirect:
            defineLayer(scene.yafaray4.passes.pass_indirect, "Color", "Indirect")

        if scene.render.layers[0].use_pass_shadow:
            defineLayer(scene.yafaray4.passes.pass_shadow, "Color", "Shadow")

        if scene.render.layers[0].use_pass_reflection:
            defineLayer(scene.yafaray4.passes.pass_reflect, "Color", "Reflect")

        if scene.render.layers[0].use_pass_refraction:
            defineLayer(scene.yafaray4.passes.pass_refract, "Color", "Refract")

        if scene.render.layers[0].use_pass_object_index:
            defineLayer(scene.yafaray4.passes.pass_index_ob, "Gray", "IndexOB")

        if scene.render.layers[0].use_pass_material_index:
            defineLayer(scene.yafaray4.passes.pass_index_ma, "Gray", "IndexMA")

        if scene.render.layers[0].use_pass_diffuse_direct:
            defineLayer(scene.yafaray4.passes.pass_depth, "pass_DiffDir", "DiffDir")

        if scene.render.layers[0].use_pass_diffuse_indirect:
            defineLayer(scene.yafaray4.passes.pass_diff_ind, "Color", "DiffInd")

        if scene.render.layers[0].use_pass_diffuse_color:
            defineLayer(scene.yafaray4.passes.pass_diff_col, "Color", "DiffCol")

        if scene.render.layers[0].use_pass_glossy_direct:
            defineLayer(scene.yafaray4.passes.pass_gloss_dir, "Color", "GlossDir")

        if scene.render.layers[0].use_pass_glossy_indirect:
            defineLayer(scene.yafaray4.passes.pass_gloss_ind, "Color", "GlossInd")

        if scene.render.layers[0].use_pass_glossy_color:
            defineLayer(scene.yafaray4.passes.pass_gloss_col, "Color", "GlossCol")

        if scene.render.layers[0].use_pass_transmission_direct:
            defineLayer(scene.yafaray4.passes.pass_trans_dir, "Color", "TransDir")

        if scene.render.layers[0].use_pass_transmission_indirect:
            defineLayer(scene.yafaray4.passes.pass_trans_ind, "Color", "TransInd")

        if scene.render.layers[0].use_pass_transmission_color:
            defineLayer(scene.yafaray4.passes.pass_trans_col, "Color", "TransCol")

        if scene.render.layers[0].use_pass_subsurface_direct:
            defineLayer(scene.yafaray4.passes.pass_subsurface_dir, "Color", "SubsurfaceDir")

        if scene.render.layers[0].use_pass_subsurface_indirect:
            defineLayer(scene.yafaray4.passes.pass_subsurface_ind, "Color", "SubsurfaceInd")

        if scene.render.layers[0].use_pass_subsurface_color:
            defineLayer(scene.yafaray4.passes.pass_subsurface_col, "Color", "SubsurfaceCol")



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
        frame_numb_str = "{:0" + str(len(str(self.scene_blender.frame_end))) + "d}"

        filebasename = ""
        if self.scene_blender.img_add_blend_name:
            if bpy.data.filepath == "":
                filebasename += "temp"
            filebasename += os.path.splitext(os.path.basename(bpy.data.filepath))[0] + " - "

        filebasename += frame_numb_str.format(self.scene_blender.frame_current)

        if self.scene_blender.img_add_datetime:
            filebasename += " (" + datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S") + ")"

        output = os.path.join(output_path, filebasename)
        # try to create dir if it not exists...
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
            except Exception:
                print("Unable to create directory...")
                import traceback
                traceback.print_exc()
                output = ""
        outputFile = output + "." + filetype

        return outputFile, output, filetype

    def define_image_output(self, output_name, fp, scene_blender, bl_render, color_space, gamma, alpha_premultiply):
        self.output_file, self.output, self.file_type = self.decide_output_file_name(fp, scene_blender.img_output)
        param_map = libyafaray4_bindings.ParamMap()
        param_map.set_string("image_path", str(self.output_file))
        param_map.set_string("color_space", color_space)
        param_map.set_float("gamma", gamma)
        param_map.set_bool("alpha_premultiply", alpha_premultiply)
        param_map.set_bool("multi_layer", scene_blender.img_multilayer)
        param_map.set_bool("denoise_enabled", scene_blender.img_denoise)
        param_map.set_int("denoise_h_lum", scene_blender.img_denoiseHLum)
        param_map.set_int("denoise_h_col", scene_blender.img_denoiseHCol)
        param_map.set_float("denoise_mix", scene_blender.img_denoiseMix)
        print(bl_render.image_settings.color_mode)
        param_map.set_bool("alpha_channel", bl_render.image_settings.color_mode == "RGBA")
        # self.film_yafaray.setLoggingAndBadgeSettings(self.scene_yafaray, self.scene)
        self.co = self.film.film_yafaray.createOutput(output_name, param_map)


        def update_blender_result(x, y, w, h, view_name, tiles, callback_name):
            # print(x, y, w, h, view_name, tiles, callback_name, scene.render.use_multiview)
            if self.scene_blender.render.use_multiview:
                blender_result_buffers = self.begin_result(x, y, w, h, "", view_name)
            else:
                blender_result_buffers = self.begin_result(x, y, w, h)
            for tile in tiles:
                tile_name, tile_bitmap = tile
                print("tile_name:", tile_name, " tile_bitmap:", tile_bitmap, " blender_result_buffers:",
                      blender_result_buffers)
                try:
                    blender_result_buffers.layers[0].passes[0].rect = tile_bitmap
                except Exception:
                    print("Exporter: Exception while rendering in " + callback_name + " function:")
                    traceback.print_exc()
            self.end_result(blender_result_buffers)

        def highlight_callback(*args):
            view_name, area_id, x_0, y_0, x_1, y_1, tiles = args
            w = x_1 - x_0
            h = y_1 - y_0
            if view_name == "":  # In case we use Render 3D viewport with Views enabled, it will copy the result to all views
                for view in self.scene_blender.render.views:
                    update_blender_result(x_0, y_0, w, h, view.name, tiles, "highlightCallback")
            else:  # Normal rendering
                update_blender_result(x_0, y_0, w, h, view_name, tiles, "highlightCallback")

        def flush_area_callback(*args):
            # view_name, area_id, x_0, y_0, x_1, y_1, tiles = args
            area_id, x_0, y_0, x_1, y_1, tiles = args
            view_name = "test"
            w = x_1 - x_0
            h = y_1 - y_0
            if view_name == "":  # In case we use Render 3D viewport with Views enabled, it will copy the result to all views
                for view in self.scene_blender.render.views:
                    update_blender_result(x_0, y_0, w, h, view.name, tiles, "flushAreaCallback")
            else:  # Normal rendering
                update_blender_result(x_0, y_0, w, h, view_name, tiles, "flushAreaCallback")

        def flush_callback(*args):
            w, h, tiles = args
            view_name = "test"
            if view_name == "":  # In case we use Render 3D viewport with Views enabled, it will copy the result to all views
                for view in self.scene_blender.render.views:
                    update_blender_result(0, 0, w, h, view.name, tiles, "flushCallback")
            else:  # Normal rendering
                update_blender_result(0, 0, w, h, view_name, tiles, "flushCallback")

    def render(self):
        self.film.film_yafaray.setFlushAreaCallback(flush_area_callback)
        self.film.film_yafaray.setFlushCallback(flush_callback)
        self.film.film_yafaray.setHighlightAreaCallback(highlight_callback)
        # Creating RenderControl #
        render_control = libyafaray4_bindings.RenderControl()
        # Creating RenderMonitor #
        render_monitor = libyafaray4_bindings.RenderMonitor(progress_callback)
        render_control.setForNormalStart()
        scene_modified_flags = self.scene_yafaray.checkAndClearModifiedFlags()
        self.scene_yafaray.preprocess(render_control, scene_modified_flags)
        self.integrator.yaf_integrator.preprocess(render_monitor, render_control, self.scene_yafaray)
        self.integrator.yaf_integrator.render(render_control, render_monitor, self.film.film_yafaray)
        return  # FIXME!!!
        t = threading.Thread(target=self.yaf_integrator, args=(self.scene_yafaray, progressCallback,))
        t.start()

        while t.is_alive() and not self.test_break():
            time.sleep(0.2)

        if t.is_alive():
            self.update_stats("",
                              "Aborting, please wait for all pending tasks to complete (progress in console log)...")
            self.scene_yafaray.cancelRendering()
            t.join()
