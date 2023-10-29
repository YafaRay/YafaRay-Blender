# SPDX-License-Identifier: GPL-2.0-or-later

import math
import os
import re

import bpy
import libyafaray4_bindings
from bpy.path import abspath, clean_name


def noise2string(ntype):
    a = {
        'BLENDER_ORIGINAL': 'blender',
        'ORIGINAL_PERLIN': 'stdperlin',
        'IMPROVED_PERLIN': 'newperlin',
        'VORONOI_F1': 'voronoi_f1',
        'VORONOI_F2': 'voronoi_f2',
        'VORONOI_F3': 'voronoi_f3',
        'VORONOI_F4': 'voronoi_f4',
        'VORONOI_F2_F1': 'voronoi_f2f1',
        'VORONOI_CRACKLE': 'voronoi_crackle',
        'CELL_NOISE': 'cellnoise',
    }

    return a.get(ntype, 'newperlin')


class TexturesExporter:
    def __init__(self, scene_yafaray, logger):
        self.scene_yafaray = scene_yafaray
        self.logger = logger

    def write_texture(self, scene, tex):
        name = tex.name
        param_map = libyafaray4_bindings.ParamMap()

        texture_configured = False

        if tex.yaf_tex_type == 'BLEND':
            self.logger.print_info("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            param_map.set_string("type", "blend")

            switch_blend_type = {
                'LINEAR': 'linear',
                'QUADRATIC': 'quadratic',
                'EASING': 'easing',
                'DIAGONAL': 'diagonal',
                'SPHERICAL': 'sphere',
                'QUADRATIC_SPHERE': 'quad_sphere',
                'RADIAL': 'radial',
            }

            blend_type = switch_blend_type.get(tex.progression,
                                               'linear')  # set blend type for blend texture, default is linear
            param_map.set_string("blend_type", blend_type)

            if tex.use_flip_axis == "HORIZONTAL":
                param_map.set_bool("use_flip_axis", False)
            if tex.use_flip_axis == "VERTICAL":
                param_map.set_bool("use_flip_axis", True)

            texture_configured = True

        elif tex.yaf_tex_type == 'CLOUDS':
            self.logger.print_info("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            param_map.set_string("type", "clouds")

            noise_size = tex.noise_scale
            if noise_size > 0:
                noise_size = 1.0 / noise_size

            param_map.set_float("size", noise_size)

            if tex.noise_type == 'HARD_NOISE':
                hard = True
            else:
                hard = False

            param_map.set_bool("hard", hard)
            param_map.set_int("depth", tex.noise_depth)
            param_map.set_string("noise_type", noise2string(tex.noise_basis))

            texture_configured = True

        elif tex.yaf_tex_type == 'WOOD':
            self.logger.print_info("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            param_map.set_string("type", "wood")

            param_map.set_int("depth", 0)

            turb = 0.0
            noise_size = 0.25
            hard = True

            if tex.wood_type == 'BANDNOISE' or tex.wood_type == 'RINGNOISE':

                turb = tex.turbulence
                noise_size = tex.noise_scale

                if noise_size > 0:
                    noise_size = 1.0 / noise_size
                if tex.noise_type == 'SOFT_NOISE':
                    hard = False

            param_map.set_float("turbulence", turb)
            param_map.set_float("size", noise_size)
            param_map.set_bool("hard", hard)

            ts = "bands"

            if tex.wood_type == 'RINGS' or tex.wood_type == 'RINGNOISE':
                ts = "rings"

            param_map.set_string("wood_type", ts)
            param_map.set_string("noise_type", noise2string(tex.noise_basis))

            # shape parameter

            if tex.noise_basis_2 == 'SAW':
                ts = "saw"
            elif tex.noise_basis_2 == 'TRI':
                ts = "tri"
            else:
                ts = "sin"

            param_map.set_string("shape", ts)

            texture_configured = True

        elif tex.yaf_tex_type == 'MARBLE':
            self.logger.print_info("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            param_map.set_string("type", "marble")

            param_map.set_int("depth", tex.noise_depth)
            param_map.set_float("turbulence", tex.turbulence)

            noise_size = tex.noise_scale
            if noise_size > 0:
                noise_size = 1.0 / noise_size

            if tex.noise_type == 'HARD_NOISE':
                hard = True
            else:
                hard = False

            param_map.set_float("size", noise_size)
            param_map.set_bool("hard", hard)

            sharp = 4.0
            if tex.marble_type == 'SOFT':
                sharp = 2.0
            elif tex.marble_type == 'SHARP':
                sharp = 4.0
            elif tex.marble_type == 'SHARPER':
                sharp = 8.0

            param_map.set_float("sharpness", sharp)
            param_map.set_string("noise_type", noise2string(tex.noise_basis))

            if tex.noise_basis_2 == 'SAW':
                ts = "saw"
            elif tex.noise_basis_2 == 'TRI':
                ts = "tri"
            else:
                ts = "sin"

            param_map.set_string("shape", ts)

            texture_configured = True

        elif tex.yaf_tex_type == 'VORONOI':
            self.logger.print_info("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            param_map.set_string("type", "voronoi")

            if tex.color_mode == 'POSITION':
                ts = "position"
            elif tex.color_mode == 'POSITION_OUTLINE':
                ts = "position-outline"
            elif tex.color_mode == 'POSITION_OUTLINE_INTENSITY':
                ts = "position-outline-intensity"
            else:
                ts = "intensity-without-color"

            param_map.set_string("color_mode", ts)

            param_map.set_float("weight1", tex.weight_1)
            param_map.set_float("weight2", tex.weight_2)
            param_map.set_float("weight3", tex.weight_3)
            param_map.set_float("weight4", tex.weight_4)

            param_map.set_float("mk_exponent", tex.minkovsky_exponent)
            param_map.set_float("intensity", tex.noise_intensity)

            noise_size = tex.noise_scale
            if noise_size > 0:
                noise_size = 1.0 / noise_size
            param_map.set_float("size", noise_size)

            switch_dist_metric = {
                'DISTANCE_SQUARED': 'squared',
                'MANHATTAN': 'manhattan',
                'CHEBYCHEV': 'chebychev',
                'MINKOVSKY_HALF': 'minkovsky_half',
                'MINKOVSKY_FOOUR': 'minkovsky_four',
                'MINKOVSKY': 'minkovsky',
            }

            ts = switch_dist_metric.get(tex.distance_metric,
                                        'minkovsky')  # set distance metric for VORONOI Texture, default is 'minkovsky'
            param_map.set_string("distance_metric", ts)

            texture_configured = True

        elif tex.yaf_tex_type == 'MUSGRAVE':
            self.logger.print_info("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            param_map.set_string("type", "musgrave")

            switch_musgrave_type = {
                'MULTIFRACTAL': 'multifractal',
                'RIDGED_MULTIFRACTAL': 'ridgedmf',
                'HYBRID_MULTIFRACTAL': 'hybridmf',
                'HETERO_TERRAIN': 'heteroterrain',
                'FBM': 'fBm',
            }
            ts = switch_musgrave_type.get(tex.musgrave_type,
                                          'multifractal')  # set MusgraveType, default is 'multifractal'

            param_map.set_string("musgrave_type", ts)
            param_map.set_string("noise_type", noise2string(tex.noise_basis))
            param_map.set_float("H", tex.dimension_max)
            param_map.set_float("lacunarity", tex.lacunarity)
            param_map.set_float("octaves", tex.octaves)

            noise_size = tex.noise_scale
            if noise_size > 0:
                noise_size = 1.0 / noise_size
            param_map.set_float("size", noise_size)
            param_map.set_float("offset", tex.offset)
            param_map.set_float("intensity", tex.noise_intensity)
            param_map.set_float("gain", tex.gain)

            texture_configured = True

        elif tex.yaf_tex_type == 'DISTORTED_NOISE':
            self.logger.print_info("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            param_map.set_string("type", "distorted_noise")

            param_map.set_float("distort", tex.distortion)

            noise_size = tex.noise_scale
            if noise_size > 0:
                noise_size = 1.0 / noise_size
            param_map.set_float("size", noise_size)

            param_map.set_string("noise_type1", noise2string(tex.noise_basis))
            param_map.set_string("noise_type2", noise2string(tex.noise_distortion))

            texture_configured = True

        elif tex.yaf_tex_type == 'IMAGE' and tex.image and tex.image.source in {'FILE', 'SEQUENCE', 'GENERATED'}:

            filename = os.path.splitext(os.path.basename(bpy.data.filepath))[0]

            if not any(filename):
                filename = "untitled"
                save_dir = os.path.expanduser("~")
            else:
                save_dir = "//"

            filename = clean_name(filename)
            file_format = scene.render.image_settings.file_format.lower()
            extract_path = os.path.join(filename, "{:05d}".format(scene.frame_current))
            image_tex = None

            if tex.image.source == 'GENERATED':
                image_tex = "yaf_baked_image_{0}.{1}".format(clean_name(tex.name), file_format)
                image_tex = os.path.join(save_dir, extract_path, image_tex)
                image_tex = abspath(image_tex)
                tex.image.save_render(image_tex, scene)
            if tex.image.source == 'FILE':
                if tex.image.packed_file:
                    image_tex = "yaf_extracted_image_{0}.{1}".format(clean_name(tex.name), file_format)
                    image_tex = os.path.join(save_dir, extract_path, image_tex)
                    image_tex = abspath(image_tex)
                    tex.image.save_render(image_tex, scene)
                else:
                    if tex.image.library is not None:
                        image_tex = abspath(tex.image.filepath, library=tex.image.library)
                    else:
                        image_tex = abspath(tex.image.filepath)
                    if not os.path.exists(image_tex):
                        self.logger.printError(
                            "Exporter: Image texture {0} not found on: {1}".format(tex.name, image_tex))
                        return False
            if tex.image.source == 'SEQUENCE':
                if tex.image.packed_file:
                    image_tex = "yaf_extracted_image_{0}.{1}".format(clean_name(tex.name), file_format)
                    image_tex = os.path.join(save_dir, extract_path, image_tex)
                    image_tex = abspath(image_tex)
                    tex.image.save_render(image_tex, scene)
                else:
                    # Try to figure out the correct file name depending on the frame,
                    # guessing the calculations done by Blender
                    if tex.image_user.use_cyclic:
                        image_number = scene.frame_current - tex.image_user.frame_start
                        if image_number < 0:
                            image_number += (divmod(-1 * image_number, tex.image_user.frame_duration)[
                                                 0] + 1) * tex.image_user.frame_duration

                        image_number = (image_number % tex.image_user.frame_duration) + tex.image_user.frame_offset + 1

                    else:
                        image_number = scene.frame_current - (
                                    tex.image_user.frame_start - 1) + tex.image_user.frame_offset
                        if image_number < tex.image_user.frame_start:
                            image_number = tex.image_user.frame_start
                        elif image_number > (tex.image_user.frame_duration + tex.image_user.frame_offset):
                            image_number = (tex.image_user.frame_duration + tex.image_user.frame_offset)

                    tex_image_filepath = abspath(tex.image.filepath)
                    tex_image_filepath_split_ext = os.path.splitext(tex_image_filepath)
                    tex_image_filepath_search_number = re.search(r'\d+$', tex_image_filepath_split_ext[0])
                    tex_image_filepath_base = tex_image_filepath[0:tex_image_filepath_search_number.span()[
                        0]] if tex_image_filepath_search_number else tex_image_filepath_split_ext[0]
                    if tex_image_filepath_search_number:
                        tex_image_filepath_number = tex_image_filepath_search_number.group()
                    else:
                        tex_image_filepath_number = None

                    tex_image_filepath_number_num_digits = len(
                        tex_image_filepath_number) if tex_image_filepath_number else 0
                    tex_image_filepath_ext = tex_image_filepath_split_ext[1]
                    if tex_image_filepath_number is not None:
                        tex_image_filepath_sequence = tex_image_filepath_base + str(image_number).zfill(
                            tex_image_filepath_number_num_digits) + tex_image_filepath_ext
                    else:
                        tex_image_filepath_sequence = tex_image_filepath_base + str(
                            image_number) + tex_image_filepath_ext

                    if tex.image.library is not None:
                        image_tex = abspath(tex_image_filepath_sequence, library=tex.image.library)
                    else:
                        image_tex = abspath(tex_image_filepath_sequence)
                    if not os.path.exists(image_tex):
                        self.logger.printError(
                            "Exporter: Image texture {0} not found on: {1}".format(tex.name, image_tex))
                        return False

            image_tex = os.path.realpath(image_tex)
            image_tex = os.path.normpath(image_tex)

            texture_color_space = "sRGB"
            texture_gamma = 1.0

            if tex.image.colorspace_settings.name == "sRGB" or tex.image.colorspace_settings.name == "VD16":
                texture_color_space = "sRGB"
            elif tex.image.colorspace_settings.name == "XYZ":
                texture_color_space = "XYZ"
            elif tex.image.colorspace_settings.name == "Linear"\
                    or tex.image.colorspace_settings.name == "Linear ACES"\
                    or tex.image.colorspace_settings.name == "Non-Color":
                texture_color_space = "LinearRGB"
            elif tex.image.colorspace_settings.name == "Raw":
                texture_color_space = "Raw_Manual_Gamma"
                texture_gamma = tex.yaf_gamma_input  # We only use the selected gamma if the color space is set to "Raw"
            param_map.set_string("color_space", texture_color_space)
            param_map.set_float("gamma", texture_gamma)

            if tex.yaf_tex_optimization == "default":
                texture_optimization = scene.gs_tex_optimization
            else:
                texture_optimization = tex.yaf_tex_optimization
            param_map.set_string("image_optimization", texture_optimization)
            param_map.set_string("filename", image_tex)
            image_name = name + "_image"
            self.scene_yafaray.create_image(image_name, param_map)
            param_map = libyafaray4_bindings.ParamMap()

            self.logger.print_info(
                "Exporter: Creating Texture: '{0}' type {1}: {2}. "
                "Texture Color Space: '{3}', gamma={4}. Texture optimization='{5}'".format(
                    name, tex.yaf_tex_type, image_tex, texture_color_space, texture_gamma, texture_optimization))

            param_map.set_string("type", "image")
            param_map.set_string("image_name", image_name)

            param_map.set_string("interpolate", tex.yaf_tex_interpolate)

            param_map.set_bool("use_alpha", tex.yaf_use_alpha)
            param_map.set_bool("calc_alpha", tex.use_calculate_alpha)
            param_map.set_bool("normalmap", tex.yaf_is_normal_map)

            # repeat
            repeat_x = 1
            repeat_y = 1

            if tex.extension == 'REPEAT':
                repeat_x = tex.repeat_x
                repeat_y = tex.repeat_y

            param_map.set_int("xrepeat", repeat_x)
            param_map.set_int("yrepeat", repeat_y)

            # clipping
            extension = tex.extension
            switch_extension = {
                'EXTEND': 'extend',
                'CLIP': 'clip',
                'CLIP_CUBE': 'clipcube',
                'CHECKER': 'checker',
            }
            clipping = switch_extension.get(extension, 'repeat')  # set default clipping to 'repeat'
            param_map.set_string("clipping", clipping)
            if clipping == 'checker':
                param_map.set_bool("even_tiles", tex.use_checker_even)
                param_map.set_bool("odd_tiles", tex.use_checker_odd)

            # crop min/max
            param_map.set_float("cropmin_x", tex.crop_min_x)
            param_map.set_float("cropmin_y", tex.crop_min_y)
            param_map.set_float("cropmax_x", tex.crop_max_x)
            param_map.set_float("cropmax_y", tex.crop_max_y)
            param_map.set_bool("rot90", tex.use_flip_axis)
            param_map.set_bool("mirror_x", tex.use_mirror_x)
            param_map.set_bool("mirror_y", tex.use_mirror_y)
            param_map.set_float("trilinear_level_bias", tex.yaf_trilinear_level_bias)
            param_map.set_float("ewa_max_anisotropy", tex.yaf_ewa_max_anisotropy)

            texture_configured = True

        # param_map.set_bool("img_grayscale", tex.yaf_img_grayscale)
        param_map.set_float("adj_mult_factor_red", tex.factor_red)
        param_map.set_float("adj_mult_factor_green", tex.factor_green)
        param_map.set_float("adj_mult_factor_blue", tex.factor_blue)
        param_map.set_float("adj_intensity", tex.intensity)
        param_map.set_float("adj_contrast", tex.contrast)
        param_map.set_float("adj_saturation", tex.saturation)
        param_map.set_float("adj_hue", math.degrees(tex.yaf_adj_hue))
        param_map.set_bool("adj_clamp", tex.use_clamp)

        if tex.use_color_ramp:
            param_map.set_string("ramp_color_mode", tex.color_ramp.color_mode)
            param_map.set_string("ramp_hue_interpolation", tex.color_ramp.hue_interpolation)
            param_map.set_string("ramp_interpolation", tex.color_ramp.interpolation)
            i = 0
            for item in tex.color_ramp.elements:
                param_map.set_color("ramp_item_" + str(i) + "_color", item.color[0], item.color[1], item.color[2],
                                    item.color[3])
                param_map.set_float("ramp_item_" + str(i) + "_position", item.position)
                i += 1
            param_map.set_int("ramp_num_items", i)

        if texture_configured:
            self.scene_yafaray.create_texture(name, param_map)

        return texture_configured
