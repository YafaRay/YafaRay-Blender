# SPDX-License-Identifier: GPL-2.0-or-later

import datetime
import os
import traceback
from collections import namedtuple

import bpy
import libyafaray4_bindings
import mathutils

from ..util.io import scene_from_depsgraph
from ..util.math import multiply_matrix4x4_vector4


def compute_scene_size(render):
    size_x = int(render.resolution_x * render.resolution_percentage * 0.01)
    size_y = int(render.resolution_y * render.resolution_percentage * 0.01)
    return [size_x, size_y]


def decide_output_file_name(scene_blender, output_path, file_type):
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
    file_type = switch_file_type.get(file_type, 'png')
    # write image or XML-File with filename from frame number
    frame_numb_str = "{:0" + str(len(str(scene_blender.frame_end))) + "d}"

    file_base_name = ""
    if scene_blender.img_add_blend_name:
        if bpy.data.filepath == "":
            file_base_name += "temp"
        file_base_name += os.path.splitext(os.path.basename(bpy.data.filepath))[0] + " - "

    file_base_name += frame_numb_str.format(scene_blender.frame_current)

    if scene_blender.img_add_datetime:
        file_base_name += " (" + datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S") + ")"

    output = os.path.join(output_path, file_base_name)
    # try to create dir if it not exists...
    if not os.path.exists(output_path):
        try:
            os.makedirs(output_path)
        except Exception:
            print("Unable to create directory...")
            import traceback
            traceback.print_exc()
            output = ""
    output_file = output + "." + file_type
    return output_file, output, file_type


def get_render_coords(scene_blender):
    render = scene_blender.render
    [size_x, size_y] = compute_scene_size(render)

    b_start_x = 0
    b_start_y = 0
    b_size_x = 0
    b_size_y = 0

    cam_data = None

    if scene_blender.objects:
        for item in scene_blender.objects:
            if item.type == 'CAMERA':
                cam_data = item.data
                break

    # Shift only available if camera is selected
    if not cam_data:
        shift_x = 0
        shift_y = 0

    else:
        # Sanne: get lens shift
        # camera = self.scene_blender.objects.camera.getData()
        max_size = max(size_x, size_y)
        shift_x = int(cam_data.shift_x * max_size)
        shift_y = int(cam_data.shift_y * max_size)

    # no border when rendering to view
    if render.use_border and cam_data:
        min_x = render.border_min_x * size_x
        min_y = render.border_min_y * size_y
        max_x = render.border_max_x * size_x
        max_y = render.border_max_y * size_y
        b_start_x = int(min_x)
        b_start_y = int(size_y) - int(max_y)
        b_size_x = int(max_x) - int(min_x)
        b_size_y = int(max_y) - int(min_y)

    # Sanne: add lens shift
    b_start_x += shift_x
    b_start_y -= shift_y

    return [size_x, size_y, b_start_x, b_start_y, b_size_x, b_size_y, cam_data]


class FilmExporter:
    def __init__(self, film_name, scene_blender, surface_integrator_yafaray, logger, is_preview):
        self.scene_blender = scene_blender
        self.logger = logger
        self.is_preview = is_preview
        self.film_name = film_name
        self.surface_integrator_yafaray = surface_integrator_yafaray
        self.film_yafaray = None

    def define_camera(self, camera_blender, res_x, res_y, res_percentage, use_view_to_render, view_matrix):
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
            matrix = camera_blender.matrix_world.copy()
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
            cam_type = camera_blender.data.camera_type

            param_map.set_string("type", cam_type)

            if camera_blender.data.use_clipping:
                param_map.set_float("nearClip", camera_blender.data.clip_start)
                param_map.set_float("farClip", camera_blender.data.clip_end)

            if cam_type == "orthographic":
                param_map.set_float("scale", camera_blender.data.ortho_scale)

            elif cam_type in {"perspective", "architect"}:
                # Blenders GSOC 2011 project "tomato branch" merged into trunk.
                # Check for sensor settings and use them in yafaray exporter also.
                if camera_blender.data.sensor_fit == 'AUTO':
                    horizontal_fit = (x > y)
                    sensor_size = camera_blender.data.sensor_width
                elif camera_blender.data.sensor_fit == 'HORIZONTAL':
                    horizontal_fit = True
                    sensor_size = camera_blender.data.sensor_width
                else:
                    horizontal_fit = False
                    sensor_size = camera_blender.data.sensor_height

                if horizontal_fit:
                    f_aspect = 1.0
                else:
                    f_aspect = x / y

                param_map.set_float("focal", camera_blender.data.lens / (f_aspect * sensor_size))

                # DOF params, only valid for real camera
                # use DOF object distance if present or fixed DOF
                if bpy.app.version >= (2, 80, 0):
                    pass  # FIXME BLENDER >= v2.80
                else:
                    if camera_blender.data.dof_object is not None:
                        # use DOF object distance
                        dist = (pos.xyz - camera_blender.data.dof_object.location.xyz).length
                        dof_distance = dist
                    else:
                        # use fixed DOF distance
                        dof_distance = camera_blender.data.dof_distance
                    param_map.set_float("dof_distance", dof_distance)

                param_map.set_float("aperture", camera_blender.data.aperture)
                # bokeh params
                param_map.set_string("bokeh_type", camera_blender.data.bokeh_type)
                param_map.set_float("bokeh_rotation", camera_blender.data.bokeh_rotation)

            elif cam_type == "angular":
                param_map.set_bool("circular", camera_blender.data.circular)
                param_map.set_bool("mirrored", camera_blender.data.mirrored)
                param_map.set_string("projection", camera_blender.data.angular_projection)
                param_map.set_float("max_angle", camera_blender.data.max_angle)
                param_map.set_float("angle", camera_blender.data.angular_angle)

        param_map.set_int("resx", x)
        param_map.set_int("resy", y)

        if self.is_preview and bpy.data.scenes[0].yafaray.preview.enable:
            # incl = bpy.data.scenes[0].yafaray.preview.camRotIncl
            # azi = bpy.data.scenes[0].yafaray.preview.camRotAzi
            rot = bpy.data.scenes[0].yafaray.preview.cam_rot
            dist = bpy.data.scenes[0].yafaray.preview.cam_dist

            # pos = (dist*math.sin(incl)*math.cos(azi), dist*math.sin(incl)*math.sin(azi), dist*math.cos(incl))
            # up = (math.sin(rotZ), 0, math.cos(rotZ))
            pos = (-dist * rot[0], -dist * rot[2], -dist * rot[1])
            up = (0, 0, 1)
            to = (0, 0, 0)

        param_map.set_vector("from", pos[0], pos[1], pos[2])
        param_map.set_vector("up", up[0], up[1], up[2])
        param_map.set_vector("to", to[0], to[1], to[2])
        self.film_yafaray.define_camera(param_map)

    @staticmethod
    def export_aa(scene_blender, param_map):
        param_map.set_int("AA_passes", scene_blender.AA_passes)
        param_map.set_int("AA_minsamples", scene_blender.AA_min_samples)
        param_map.set_int("AA_inc_samples", scene_blender.AA_inc_samples)
        param_map.set_float("AA_pixelwidth", scene_blender.AA_pixelwidth)
        param_map.set_float("AA_threshold", scene_blender.AA_threshold)
        param_map.set_string("filter_type", scene_blender.AA_filter_type)
        param_map.set_float("AA_resampled_floor", scene_blender.yafaray4.noise_control.resampled_floor)
        param_map.set_float("AA_sample_multiplier_factor",
                            scene_blender.yafaray4.noise_control.sample_multiplier_factor)
        param_map.set_float("AA_light_sample_multiplier_factor",
                            scene_blender.yafaray4.noise_control.light_sample_multiplier_factor)
        param_map.set_float("AA_indirect_sample_multiplier_factor",
                            scene_blender.yafaray4.noise_control.indirect_sample_multiplier_factor)
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

    def export_render_settings(self, depsgraph, render_path, render_filename):
        self.logger.print_verbose("Exporting Render Settings")
        scene_blender = scene_from_depsgraph(depsgraph)
        render = scene_blender.render

        [size_x, size_y, b_start_x, b_start_y, b_size_x, b_size_y, cam_data] = get_render_coords(scene_blender)

        param_map = libyafaray4_bindings.ParamMap()

        param_map.set_string("scene_accelerator", scene_blender.gs_accelerator)

        self.export_aa(scene_blender, param_map)

        param_map.set_int("xstart", b_start_x)
        param_map.set_int("ystart", b_start_y)

        # no border when rendering to view
        if render.use_border and cam_data:
            param_map.set_int("width", b_size_x)
            param_map.set_int("height", b_size_y)
        else:
            param_map.set_int("width", size_x)
            param_map.set_int("height", size_y)

        param_map.set_bool("show_sam_pix", scene_blender.gs_show_sam_pix)

        if scene_blender.name == "preview" and bpy.data.scenes[0].yafaray.preview.enable:
            param_map.set_bool("show_sam_pix", False)

        param_map.set_int("tile_size", scene_blender.gs_tile_size)
        param_map.set_string("tiles_order", scene_blender.gs_tile_order)

        if scene_blender.gs_auto_threads:
            param_map.set_int("threads", -1)
            param_map.set_int("threads_photons", -1)
        else:
            param_map.set_int("threads", scene_blender.gs_threads)
            param_map.set_int("threads_photons", scene_blender.gs_threads)

        param_map.set_string("images_autosave_interval_type", scene_blender.gs_images_autosave_interval_type)
        param_map.set_int("images_autosave_interval_passes", scene_blender.gs_images_autosave_interval_passes)
        param_map.set_float("images_autosave_interval_seconds", scene_blender.gs_images_autosave_interval_seconds)

        param_map.set_string("film_load_save_mode", scene_blender.gs_film_save_load)
        param_map.set_string("film_load_save_path", render_path + "/" + render_filename)
        param_map.set_string("film_autosave_interval_type", scene_blender.gs_film_autosave_interval_type)
        param_map.set_int("film_autosave_interval_passes", scene_blender.gs_film_autosave_interval_passes)
        param_map.set_float("film_autosave_interval_seconds", scene_blender.gs_film_autosave_interval_seconds)

        param_map.set_bool("adv_auto_shadow_bias_enabled", scene_blender.adv_auto_shadow_bias_enabled)
        param_map.set_float("adv_shadow_bias_value", scene_blender.adv_shadow_bias_value)
        param_map.set_bool("adv_auto_min_raydist_enabled", scene_blender.adv_auto_min_raydist_enabled)
        param_map.set_float("adv_min_raydist_value", scene_blender.adv_min_raydist_value)
        param_map.set_float("adv_min_raydist_value", scene_blender.adv_min_raydist_value)
        param_map.set_int("adv_base_sampling_offset", scene_blender.adv_base_sampling_offset)
        if bpy.app.version >= (2, 80, 0):
            pass  # FIXME BLENDER >= v2.80
        else:
            param_map.set_int("adv_computer_node",
                              bpy.context.user_preferences.addons["yafaray4"].preferences.yafaray_computer_node)

        param_map.set_int("layer_mask_obj_index", scene_blender.yafaray4.passes.pass_mask_obj_index)
        param_map.set_int("layer_mask_mat_index", scene_blender.yafaray4.passes.pass_mask_mat_index)
        param_map.set_bool("layer_mask_invert", scene_blender.yafaray4.passes.pass_mask_invert)
        param_map.set_bool("layer_mask_only", scene_blender.yafaray4.passes.pass_mask_only)

        param_map.set_int("layer_object_edge_thickness", scene_blender.yafaray4.passes.object_edge_thickness)
        param_map.set_int("layer_faces_edge_thickness", scene_blender.yafaray4.passes.faces_edge_thickness)
        param_map.set_float("layer_object_edge_threshold", scene_blender.yafaray4.passes.object_edge_threshold)
        param_map.set_float("layer_faces_edge_threshold", scene_blender.yafaray4.passes.faces_edge_threshold)
        param_map.set_float("layer_object_edge_smoothness", scene_blender.yafaray4.passes.object_edge_smoothness)
        param_map.set_float("layer_faces_edge_smoothness", scene_blender.yafaray4.passes.faces_edge_smoothness)
        param_map.set_color("layer_toon_edge_color", scene_blender.yafaray4.passes.toon_edge_color[0],
                            scene_blender.yafaray4.passes.toon_edge_color[1],
                            scene_blender.yafaray4.passes.toon_edge_color[2])
        param_map.set_float("layer_toon_pre_smooth", scene_blender.yafaray4.passes.toon_pre_smooth)
        param_map.set_float("layer_toon_post_smooth", scene_blender.yafaray4.passes.toon_post_smooth)
        param_map.set_float("layer_toon_quantization", scene_blender.yafaray4.passes.toon_quantization)

        self.film_yafaray = libyafaray4_bindings.Film(self.logger, self.surface_integrator_yafaray, self.film_name, param_map)

    def set_logging_and_badge_settings(self, scene_blender, param_map):
        self.logger.printVerbose("Exporting Logging and Badge settings")
        param_map.set_bool("badge_draw_render_settings", scene_blender.yafaray4.logging.draw_render_settings)
        param_map.set_bool("badge_draw_aa_noise_settings", scene_blender.yafaray4.logging.draw_aa_noise_settings)
        param_map.set_bool("logging_save_txt", scene_blender.yafaray4.logging.save_log)
        param_map.set_bool("logging_save_html", scene_blender.yafaray4.logging.save_html)
        param_map.set_string("badge_position", scene_blender.yafaray4.logging.params_badge_position)
        param_map.set_string("badge_title", scene_blender.yafaray4.logging.title)
        param_map.set_string("badge_author", scene_blender.yafaray4.logging.author)
        param_map.set_string("badge_contact", scene_blender.yafaray4.logging.contact)
        param_map.set_string("badge_comment", scene_blender.yafaray4.logging.comments)
        if scene_blender.yafaray4.logging.custom_icon != "":
            param_map.set_string("badge_icon_path",
                                 os.path.abspath(bpy.path.abspath(scene_blender.yafaray4.logging.custom_icon)))
        param_map.set_string("badge_font_path", scene_blender.yafaray4.logging.custom_font)
        param_map.set_float("badge_font_size_factor", scene_blender.yafaray4.logging.font_scale)

    def calc_alpha_premultiply(self, scene_blender):
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

    def calc_gamma(self, scene_blender):
        gamma = namedtuple("gamma", ["blender", "secondary_output"])
        gamma_1 = 1.0
        gamma_2 = 1.0
        if scene_blender.gs_type_render == "into_blender" and scene_blender.display_settings.display_device == "None":
            gamma_1 = scene_blender.gs_gamma  # We only use the selected gamma if the output device is set to "None"
            if scene_blender.display_settings.display_device == "None":
                gamma_2 = scene_blender.gs_gamma  # We only use the selected gamma if the output device is set to "None"
        elif scene_blender.display_settings.display_device == "None":
            gamma_1 = scene_blender.gs_gamma  # We only use the selected gamma if the output device is set to "None"

        return gamma(gamma_1, gamma_2)

    def calc_color_space(self, scene_blender):
        color_space = namedtuple("color_space", ["blender", "secondary_output"])
        color_space_2 = "sRGB"

        if scene_blender.gs_type_render == "into_blender":
            if scene_blender.display_settings.display_device == "None":
                color_space_1 = "Raw_Manual_Gamma"
            else:
                color_space_1 = "LinearRGB"  # For all other Blender display devices, it expects a linear output from YafaRay
            # Optional Secondary file output color space
            if scene_blender.img_output == "OPEN_EXR" or scene_blender.img_output == "HDR":  # If the output file is a HDR/EXR file, we force the render output to Linear
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

    def define_layers(self, depsgraph):
        self.logger.printVerbose("Exporting Render Passes settings")
        scene_blender = scene_from_depsgraph(depsgraph)

        def define_layer(layer_type, exported_image_type, exported_image_name):
            param_map = libyafaray4_bindings.ParamMap()
            param_map.set_string("type", layer_type)
            param_map.set_string("image_type", exported_image_type)
            param_map.set_string("exported_image_name", exported_image_name)
            param_map.set_string("exported_image_type", exported_image_type)
            define_layer(param_map)

        define_layer("combined", "ColorAlpha", "Combined")

        if scene_blender.yafaray4.passes.pass_enable:
            if scene_blender.render.layers[0].use_pass_z:
                define_layer(scene_blender.yafaray4.passes.pass_depth, "Gray", "Depth")

            if scene_blender.render.layers[0].use_pass_vector:
                define_layer(scene_blender.yafaray4.passes.pass_vector, "ColorAlpha", "Vector")

            if scene_blender.render.layers[0].use_pass_normal:
                define_layer(scene_blender.yafaray4.passes.pass_normal, "Color", "Normal")

            if scene_blender.render.layers[0].use_pass_uv:
                define_layer(scene_blender.yafaray4.passes.pass_uv, "Color", "UV")

            if scene_blender.render.layers[0].use_pass_color:
                define_layer(scene_blender.yafaray4.passes.pass_color, "ColorAlpha", "Color")

            if scene_blender.render.layers[0].use_pass_emit:
                define_layer(scene_blender.yafaray4.passes.pass_emit, "Color", "Emit")

            if scene_blender.render.layers[0].use_pass_mist:
                define_layer(scene_blender.yafaray4.passes.pass_mist, "Gray", "Mist")

            if scene_blender.render.layers[0].use_pass_diffuse:
                define_layer(scene_blender.yafaray4.passes.pass_diffuse, "Color", "Diffuse")

            if scene_blender.render.layers[0].use_pass_specular:
                define_layer(scene_blender.yafaray4.passes.pass_spec, "Color", "Spec")

            if scene_blender.render.layers[0].use_pass_ambient_occlusion:
                define_layer(scene_blender.yafaray4.passes.pass_ao, "Color", "AO")

            if scene_blender.render.layers[0].use_pass_environment:
                define_layer(scene_blender.yafaray4.passes.pass_env, "Color", "Env")

            if scene_blender.render.layers[0].use_pass_indirect:
                define_layer(scene_blender.yafaray4.passes.pass_indirect, "Color", "Indirect")

            if scene_blender.render.layers[0].use_pass_shadow:
                define_layer(scene_blender.yafaray4.passes.pass_shadow, "Color", "Shadow")

            if scene_blender.render.layers[0].use_pass_reflection:
                define_layer(scene_blender.yafaray4.passes.pass_reflect, "Color", "Reflect")

            if scene_blender.render.layers[0].use_pass_refraction:
                define_layer(scene_blender.yafaray4.passes.pass_refract, "Color", "Refract")

            if scene_blender.render.layers[0].use_pass_object_index:
                define_layer(scene_blender.yafaray4.passes.pass_index_ob, "Gray", "IndexOB")

            if scene_blender.render.layers[0].use_pass_material_index:
                define_layer(scene_blender.yafaray4.passes.pass_index_ma, "Gray", "IndexMA")

            if scene_blender.render.layers[0].use_pass_diffuse_direct:
                define_layer(scene_blender.yafaray4.passes.pass_depth, "pass_DiffDir", "DiffDir")

            if scene_blender.render.layers[0].use_pass_diffuse_indirect:
                define_layer(scene_blender.yafaray4.passes.pass_diff_ind, "Color", "DiffInd")

            if scene_blender.render.layers[0].use_pass_diffuse_color:
                define_layer(scene_blender.yafaray4.passes.pass_diff_col, "Color", "DiffCol")

            if scene_blender.render.layers[0].use_pass_glossy_direct:
                define_layer(scene_blender.yafaray4.passes.pass_gloss_dir, "Color", "GlossDir")

            if scene_blender.render.layers[0].use_pass_glossy_indirect:
                define_layer(scene_blender.yafaray4.passes.pass_gloss_ind, "Color", "GlossInd")

            if scene_blender.render.layers[0].use_pass_glossy_color:
                define_layer(scene_blender.yafaray4.passes.pass_gloss_col, "Color", "GlossCol")

            if scene_blender.render.layers[0].use_pass_transmission_direct:
                define_layer(scene_blender.yafaray4.passes.pass_trans_dir, "Color", "TransDir")

            if scene_blender.render.layers[0].use_pass_transmission_indirect:
                define_layer(scene_blender.yafaray4.passes.pass_trans_ind, "Color", "TransInd")

            if scene_blender.render.layers[0].use_pass_transmission_color:
                define_layer(scene_blender.yafaray4.passes.pass_trans_col, "Color", "TransCol")

            if scene_blender.render.layers[0].use_pass_subsurface_direct:
                define_layer(scene_blender.yafaray4.passes.pass_subsurface_dir, "Color", "SubsurfaceDir")

            if scene_blender.render.layers[0].use_pass_subsurface_indirect:
                define_layer(scene_blender.yafaray4.passes.pass_subsurface_ind, "Color", "SubsurfaceInd")

            if scene_blender.render.layers[0].use_pass_subsurface_color:
                define_layer(scene_blender.yafaray4.passes.pass_subsurface_col, "Color", "SubsurfaceCol")

    def define_image_output(self, output_name, fp, scene_blender, bl_render, color_space, gamma, alpha_premultiply):
        output_file, output, file_type = decide_output_file_name(scene_blender, fp, scene_blender.img_output)
        param_map = libyafaray4_bindings.ParamMap()
        param_map.set_string("image_path", str(output_file))
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
        # self.film_yafaray.setLoggingAndBadgeSettings(self.scene_yafaray, self.scene_blender)
        self.film_yafaray.create_output(output_name, param_map)

    def update_blender_result(self, x, y, w, h, view_name, tiles, callback_name):
        # print(x, y, w, h, view_name, tiles, callback_name, scene.render.use_multiview)
        if self.scene_blender.render.use_multiview:
            blender_result_buffers = self.scene_blender.begin_result(x, y, w, h, "", view_name)
        else:
            blender_result_buffers = self.scene_blender.begin_result(x, y, w, h)
        for tile in tiles:
            tile_name, tile_bitmap = tile
            # print("tile_name:", tile_name, " tile_bitmap:", tile_bitmap, " blender_result_buffers:",
            #       blender_result_buffers)
            try:
                blender_result_buffers.layers[0].passes[0].rect = tile_bitmap
            except Exception:
                print("Exporter: Exception while rendering in " + callback_name + " function:")
                traceback.print_exc()
        self.scene_blender.end_result(blender_result_buffers)

    def highlight_callback(self, *args):
        area_id, x_0, y_0, x_1, y_1, tiles = args
        w = x_1 - x_0
        h = y_1 - y_0
        if self.film_name == "":
            # In case we use Render 3D viewport with Views enabled, it will copy the result to all views
            for view in self.scene_blender.render.views:
                self.update_blender_result(x_0, y_0, w, h, view.name, tiles, "highlightCallback")
        else:
            # Normal rendering
            self.update_blender_result(x_0, y_0, w, h, self.film_name, tiles, "highlightCallback")

    def flush_area_callback(self, *args):
        # view_name, area_id, x_0, y_0, x_1, y_1, tiles = args
        area_id, x_0, y_0, x_1, y_1, tiles = args
        view_name = "test"
        w = x_1 - x_0
        h = y_1 - y_0
        if view_name == "":
            # In case we use Render 3D viewport with Views enabled, it will copy the result to all views
            for view in self.scene_blender.render.views:
                self.update_blender_result(x_0, y_0, w, h, view.name, tiles, "flushAreaCallback")
        else:
            # Normal rendering
            self.update_blender_result(x_0, y_0, w, h, self.film_name, tiles, "flushAreaCallback")

    def flush_callback(self, *args):
        w, h, tiles = args
        view_name = "test"
        if view_name == "":  # In case we use Render 3D viewport with Views enabled, it will copy the result to all views
            for view in self.scene_blender.render.views:
                self.update_blender_result(0, 0, w, h, view.name, tiles, "flushCallback")
        else:  # Normal rendering
            self.update_blender_result(0, 0, w, h, view_name, tiles, "flushCallback")

    def render(self):
        self.film_yafaray.setFlushAreaCallback(self.flush_area_callback)
        self.film_yafaray.setFlushCallback(self.flush_callback)
        self.film_yafaray.setHighlightAreaCallback(self.highlight_callback)
        # Creating RenderControl #
        render_control = libyafaray4_bindings.RenderControl()
        # Creating RenderMonitor #
        render_monitor = libyafaray4_bindings.RenderMonitor(self.scene_blender.progress_callback)
        render_control.setForNormalStart()
        scene_modified_flags = self.scene_yafaray.checkAndClearModifiedFlags()
        self.scene_yafaray.preprocess(render_control, scene_modified_flags)
        self.integrator_yafaray.preprocess(render_monitor, render_control, self.scene_yafaray)
        self.integrator_yafaray.render(render_control, render_monitor, self.film_yafaray)
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
