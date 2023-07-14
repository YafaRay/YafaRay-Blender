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

import re
import math
import bpy
import os
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


class Texture:
    def __init__(self, scene, logger):
        self.yaf_scene = scene
        self.yaf_logger = logger
        self.loadedTextures = set()

    def writeTexture(self, scene, tex):
        name = tex.name

        if name in self.loadedTextures:
            return

        yaf_param_map = libyafaray4_bindings.ParamMap()

        textureConfigured = False
        
        if tex.yaf_tex_type == 'BLEND':
            self.yaf_logger.printInfo("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            yaf_param_map.set_string("type", "blend")

            switchBlendType = {
                'LINEAR': 'linear',
                'QUADRATIC': 'quadratic',
                'EASING': 'easing',
                'DIAGONAL': 'diagonal',
                'SPHERICAL': 'sphere',
                'QUADRATIC_SPHERE': 'quad_sphere',
                'RADIAL': 'radial',
            }

            blend_type = switchBlendType.get(tex.progression, 'linear')  # set blend type for blend texture, default is linear
            yaf_param_map.set_string("blend_type", blend_type)
            
            if tex.use_flip_axis == "HORIZONTAL":
                yaf_param_map.set_bool("use_flip_axis", False)
            if tex.use_flip_axis == "VERTICAL":
                yaf_param_map.set_bool("use_flip_axis", True)
                
            textureConfigured = True

        elif tex.yaf_tex_type == 'CLOUDS':
            self.yaf_logger.printInfo("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            yaf_param_map.set_string("type", "clouds")

            noise_size = tex.noise_scale
            if  noise_size > 0:
                noise_size = 1.0 / noise_size

            yaf_param_map.set_float("size", noise_size)

            if tex.noise_type == 'HARD_NOISE':
                hard = True
            else:
                hard = False

            yaf_param_map.set_bool("hard", hard)
            yaf_param_map.set_int("depth", tex.noise_depth)
            yaf_param_map.set_string("noise_type", noise2string(tex.noise_basis))

            textureConfigured = True

        elif tex.yaf_tex_type == 'WOOD':
            self.yaf_logger.printInfo("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            yaf_param_map.set_string("type", "wood")

            yaf_param_map.set_int("depth", 0)

            turb = 0.0
            noise_size = 0.25
            hard = True

            if tex.wood_type == 'BANDNOISE' or tex.wood_type == 'RINGNOISE':

                turb = tex.turbulence
                noise_size = tex.noise_scale

                if  noise_size > 0:
                    noise_size = 1.0 / noise_size
                if tex.noise_type == 'SOFT_NOISE':
                    hard = False

            yaf_param_map.set_float("turbulence", turb)
            yaf_param_map.set_float("size", noise_size)
            yaf_param_map.set_bool("hard", hard)

            ts = "bands"

            if tex.wood_type == 'RINGS' or tex.wood_type == 'RINGNOISE':
                ts = "rings"

            yaf_param_map.set_string("wood_type", ts)
            yaf_param_map.set_string("noise_type", noise2string(tex.noise_basis))

            # shape parameter

            if tex.noise_basis_2 == 'SAW':
                ts = "saw"
            elif tex.noise_basis_2 == 'TRI':
                ts = "tri"
            else:
                ts = "sin"

            yaf_param_map.set_string("shape", ts)

            textureConfigured = True

        elif tex.yaf_tex_type == 'MARBLE':
            self.yaf_logger.printInfo("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            yaf_param_map.set_string("type", "marble")

            yaf_param_map.set_int("depth", tex.noise_depth)
            yaf_param_map.set_float("turbulence", tex.turbulence)

            noise_size = tex.noise_scale
            if  noise_size > 0:
                noise_size = 1.0 / noise_size

            if tex.noise_type == 'HARD_NOISE':
                hard = True
            else:
                hard = False

            yaf_param_map.set_float("size", noise_size)
            yaf_param_map.set_bool("hard", hard)

            sharp = 4.0
            if tex.marble_type == 'SOFT':
                sharp = 2.0
            elif tex.marble_type == 'SHARP':
                sharp = 4.0
            elif tex.marble_type == 'SHARPER':
                sharp = 8.0

            yaf_param_map.set_float("sharpness", sharp)
            yaf_param_map.set_string("noise_type", noise2string(tex.noise_basis))

            if tex.noise_basis_2 == 'SAW':
                ts = "saw"
            elif tex.noise_basis_2 == 'TRI':
                ts = "tri"
            else:
                ts = "sin"

            yaf_param_map.set_string("shape", ts)

            textureConfigured = True

        elif tex.yaf_tex_type == 'VORONOI':
            self.yaf_logger.printInfo("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            yaf_param_map.set_string("type", "voronoi")

            if tex.color_mode == 'POSITION':
                ts = "position"
            elif tex.color_mode == 'POSITION_OUTLINE':
                ts = "position-outline"
            elif tex.color_mode == 'POSITION_OUTLINE_INTENSITY':
                ts = "position-outline-intensity"
            else:
                ts = "intensity-without-color"

            yaf_param_map.set_string("color_mode", ts)

            yaf_param_map.set_float("weight1", tex.weight_1)
            yaf_param_map.set_float("weight2", tex.weight_2)
            yaf_param_map.set_float("weight3", tex.weight_3)
            yaf_param_map.set_float("weight4", tex.weight_4)

            yaf_param_map.set_float("mk_exponent", tex.minkovsky_exponent)
            yaf_param_map.set_float("intensity", tex.noise_intensity)

            noise_size = tex.noise_scale
            if  noise_size > 0:
                noise_size = 1.0 / noise_size
            yaf_param_map.set_float("size", noise_size)

            switchDistMetric = {
                'DISTANCE_SQUARED': 'squared',
                'MANHATTAN': 'manhattan',
                'CHEBYCHEV': 'chebychev',
                'MINKOVSKY_HALF': 'minkovsky_half',
                'MINKOVSKY_FOOUR': 'minkovsky_four',
                'MINKOVSKY': 'minkovsky',
            }

            ts = switchDistMetric.get(tex.distance_metric, 'minkovsky')  # set distance metric for VORONOI Texture, default is 'minkovsky'
            yaf_param_map.set_string("distance_metric", ts)

            textureConfigured = True

        elif tex.yaf_tex_type == 'MUSGRAVE':
            self.yaf_logger.printInfo("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            yaf_param_map.set_string("type", "musgrave")

            switchMusgraveType = {
                'MULTIFRACTAL': 'multifractal',
                'RIDGED_MULTIFRACTAL': 'ridgedmf',
                'HYBRID_MULTIFRACTAL': 'hybridmf',
                'HETERO_TERRAIN': 'heteroterrain',
                'FBM': 'fBm',
                }
            ts = switchMusgraveType.get(tex.musgrave_type, 'multifractal')  # set MusgraveType, default is 'multifractal'

            yaf_param_map.set_string("musgrave_type", ts)
            yaf_param_map.set_string("noise_type", noise2string(tex.noise_basis))
            yaf_param_map.set_float("H", tex.dimension_max)
            yaf_param_map.set_float("lacunarity", tex.lacunarity)
            yaf_param_map.set_float("octaves", tex.octaves)

            noise_size = tex.noise_scale
            if  noise_size > 0:
                noise_size = 1.0 / noise_size
            yaf_param_map.set_float("size", noise_size)
            yaf_param_map.set_float("offset", tex.offset)
            yaf_param_map.set_float("intensity", tex.noise_intensity)
            yaf_param_map.set_float("gain", tex.gain)

            textureConfigured = True

        elif tex.yaf_tex_type == 'DISTORTED_NOISE':
            self.yaf_logger.printInfo("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            yaf_param_map.set_string("type", "distorted_noise")

            yaf_param_map.set_float("distort", tex.distortion)

            noise_size = tex.noise_scale
            if  noise_size > 0:
                noise_size = 1.0 / noise_size
            yaf_param_map.set_float("size", noise_size)

            yaf_param_map.set_string("noise_type1", noise2string(tex.noise_basis))
            yaf_param_map.set_string("noise_type2", noise2string(tex.noise_distortion))

            textureConfigured = True

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
                        self.yaf_logger.printError("Exporter: Image texture {0} not found on: {1}".format(tex.name, image_tex))
                        return False
            if tex.image.source == 'SEQUENCE':
                if tex.image.packed_file:
                    image_tex = "yaf_extracted_image_{0}.{1}".format(clean_name(tex.name), file_format)
                    image_tex = os.path.join(save_dir, extract_path, image_tex)
                    image_tex = abspath(image_tex)
                    tex.image.save_render(image_tex, scene)
                else:
                    #Try to figure out the correct file name depending on the frame, guessing the calculations done by Blender
                    if tex.image_user.use_cyclic:
                        image_number = scene.frame_current - tex.image_user.frame_start
                        if image_number < 0:
                            image_number += (divmod(-1 * image_number, tex.image_user.frame_duration)[0]+1) * tex.image_user.frame_duration

                        image_number = (image_number % tex.image_user.frame_duration) + tex.image_user.frame_offset + 1

                    else:
                        image_number = scene.frame_current - (tex.image_user.frame_start - 1) + tex.image_user.frame_offset
                        if image_number < tex.image_user.frame_start:
                            image_number = tex.image_user.frame_start
                        elif image_number > (tex.image_user.frame_duration + tex.image_user.frame_offset):
                            image_number = (tex.image_user.frame_duration + tex.image_user.frame_offset)

                    tex_image_filepath = abspath(tex.image.filepath)
                    tex_image_filepath_splitext = os.path.splitext(tex_image_filepath)
                    tex_image_filepath_searchnumber = re.search(r'\d+$', tex_image_filepath_splitext[0])
                    tex_image_filepath_base = tex_image_filepath[0:tex_image_filepath_searchnumber.span()[0]] if tex_image_filepath_searchnumber else tex_image_filepath_splitext[0]
                    tex_image_filepath_number = tex_image_filepath_searchnumber.group() if tex_image_filepath_searchnumber else None
                    tex_image_filepath_number_numdigits = len(tex_image_filepath_number) if tex_image_filepath_number else 0
                    tex_image_filepath_ext = tex_image_filepath_splitext[1]
                    if tex_image_filepath_number is not None:
                        tex_image_filepath_sequence = tex_image_filepath_base + str(image_number).zfill(tex_image_filepath_number_numdigits) + tex_image_filepath_ext
                    else:
                        tex_image_filepath_sequence = tex_image_filepath_base + str(image_number) + tex_image_filepath_ext

                    if tex.image.library is not None:
                        image_tex = abspath(tex_image_filepath_sequence, library=tex.image.library)
                    else:
                        image_tex = abspath(tex_image_filepath_sequence)
                    if not os.path.exists(image_tex):
                        self.yaf_logger.printError("Exporter: Image texture {0} not found on: {1}".format(tex.name, image_tex))
                        return False

            image_tex = os.path.realpath(image_tex)
            image_tex = os.path.normpath(image_tex)

            texture_color_space = "sRGB"
            texture_gamma = 1.0

            if tex.image.colorspace_settings.name == "sRGB" or tex.image.colorspace_settings.name == "VD16":
                texture_color_space = "sRGB"
            elif tex.image.colorspace_settings.name == "XYZ":
                texture_color_space = "XYZ"
            elif tex.image.colorspace_settings.name == "Linear" or tex.image.colorspace_settings.name == "Linear ACES" or tex.image.colorspace_settings.name == "Non-Color":
                texture_color_space = "LinearRGB"
            elif tex.image.colorspace_settings.name == "Raw":
                texture_color_space = "Raw_Manual_Gamma"
                texture_gamma = tex.yaf_gamma_input  #We only use the selected gamma if the color space is set to "Raw"
            yaf_param_map.set_string("color_space", texture_color_space)
            yaf_param_map.set_float("gamma", texture_gamma)

            if tex.yaf_tex_optimization == "default":
                texture_optimization = scene.gs_tex_optimization
            else:
                texture_optimization = tex.yaf_tex_optimization
            yaf_param_map.set_string("image_optimization", texture_optimization)
            yaf_param_map.set_string("filename", image_tex)
            image_name = name + "_image"
            self.yaf_scene.createImage(image_name, yaf_param_map)
            yaf_param_map = libyafaray4_bindings.ParamMap()

            self.yaf_logger.printInfo("Exporter: Creating Texture: '{0}' type {1}: {2}. Texture Color Space: '{3}', gamma={4}. Texture optimization='{5}'".format(name, tex.yaf_tex_type, image_tex, texture_color_space, texture_gamma, texture_optimization))

            yaf_param_map.set_string("type", "image")
            yaf_param_map.set_string("image_name", image_name)

            yaf_param_map.set_string("interpolate", tex.yaf_tex_interpolate)

            yaf_param_map.set_bool("use_alpha", tex.yaf_use_alpha)
            yaf_param_map.set_bool("calc_alpha", tex.use_calculate_alpha)
            yaf_param_map.set_bool("normalmap", tex.yaf_is_normal_map)

            # repeat
            repeat_x = 1
            repeat_y = 1

            if tex.extension == 'REPEAT':
                repeat_x = tex.repeat_x
                repeat_y = tex.repeat_y

            yaf_param_map.set_int("xrepeat", repeat_x)
            yaf_param_map.set_int("yrepeat", repeat_y)

            # clipping
            extension = tex.extension
            switchExtension = {
                'EXTEND': 'extend',
                'CLIP': 'clip',
                'CLIP_CUBE': 'clipcube',
                'CHECKER': 'checker',
                }
            clipping = switchExtension.get(extension, 'repeat')  # set default clipping to 'repeat'
            yaf_param_map.set_string("clipping", clipping)
            if clipping == 'checker':
                yaf_param_map.set_bool("even_tiles", tex.use_checker_even)
                yaf_param_map.set_bool("odd_tiles", tex.use_checker_odd)

            # crop min/max
            yaf_param_map.set_float("cropmin_x", tex.crop_min_x)
            yaf_param_map.set_float("cropmin_y", tex.crop_min_y)
            yaf_param_map.set_float("cropmax_x", tex.crop_max_x)
            yaf_param_map.set_float("cropmax_y", tex.crop_max_y)
            yaf_param_map.set_bool("rot90", tex.use_flip_axis)
            yaf_param_map.set_bool("mirror_x", tex.use_mirror_x)
            yaf_param_map.set_bool("mirror_y", tex.use_mirror_y)
            yaf_param_map.set_float("trilinear_level_bias", tex.yaf_trilinear_level_bias)
            yaf_param_map.set_float("ewa_max_anisotropy", tex.yaf_ewa_max_anisotropy)

            textureConfigured = True

        #yaf_param_map.set_bool("img_grayscale", tex.yaf_img_grayscale)
        yaf_param_map.set_float("adj_mult_factor_red", tex.factor_red)
        yaf_param_map.set_float("adj_mult_factor_green", tex.factor_green)
        yaf_param_map.set_float("adj_mult_factor_blue", tex.factor_blue)
        yaf_param_map.set_float("adj_intensity", tex.intensity)
        yaf_param_map.set_float("adj_contrast", tex.contrast)
        yaf_param_map.set_float("adj_saturation", tex.saturation)
        yaf_param_map.set_float("adj_hue", math.degrees(tex.yaf_adj_hue))
        yaf_param_map.set_bool("adj_clamp", tex.use_clamp)

        if tex.use_color_ramp:
            yaf_param_map.set_string("ramp_color_mode", tex.color_ramp.color_mode)
            yaf_param_map.set_string("ramp_hue_interpolation", tex.color_ramp.hue_interpolation)
            yaf_param_map.set_string("ramp_interpolation", tex.color_ramp.interpolation)
            i = 0
            for item in tex.color_ramp.elements:
                yaf_param_map.set_color("ramp_item_" + str(i) + "_color", item.color[0], item.color[1], item.color[2], item.color[3])
                yaf_param_map.set_float("ramp_item_" + str(i) + "_position", item.position)
                i += 1
            yaf_param_map.set_int("ramp_num_items", i)

        if textureConfigured:
            self.yaf_scene.createTexture(name, yaf_param_map)
            self.loadedTextures.add(name)

        return textureConfigured
