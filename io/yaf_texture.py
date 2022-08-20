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


class yafTexture:
    def __init__(self, interface):
        self.yi = interface
        self.loadedTextures = set()

    def writeTexture(self, scene, tex):
        name = tex.name

        if name in self.loadedTextures:
            return

        yi = self.yi
        yi.paramsClearAll()

        textureConfigured = False
        
        if tex.yaf_tex_type == 'BLEND':
            yi.printInfo("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            yi.paramsSetString("type", "blend")

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
            yi.paramsSetString("blend_type", blend_type)
            
            if tex.use_flip_axis == "HORIZONTAL":
                yi.paramsSetBool("use_flip_axis", False)
            if tex.use_flip_axis == "VERTICAL":
                yi.paramsSetBool("use_flip_axis", True)
                
            textureConfigured = True

        elif tex.yaf_tex_type == 'CLOUDS':
            yi.printInfo("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            yi.paramsSetString("type", "clouds")

            noise_size = tex.noise_scale
            if  noise_size > 0:
                noise_size = 1.0 / noise_size

            yi.paramsSetFloat("size", noise_size)

            if tex.noise_type == 'HARD_NOISE':
                hard = True
            else:
                hard = False

            yi.paramsSetBool("hard", hard)
            yi.paramsSetInt("depth", tex.noise_depth)
            yi.paramsSetString("noise_type", noise2string(tex.noise_basis))

            textureConfigured = True

        elif tex.yaf_tex_type == 'WOOD':
            yi.printInfo("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            yi.paramsSetString("type", "wood")

            yi.paramsSetInt("depth", 0)

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

            yi.paramsSetFloat("turbulence", turb)
            yi.paramsSetFloat("size", noise_size)
            yi.paramsSetBool("hard", hard)

            ts = "bands"

            if tex.wood_type == 'RINGS' or tex.wood_type == 'RINGNOISE':
                ts = "rings"

            yi.paramsSetString("wood_type", ts)
            yi.paramsSetString("noise_type", noise2string(tex.noise_basis))

            # shape parameter

            if tex.noise_basis_2 == 'SAW':
                ts = "saw"
            elif tex.noise_basis_2 == 'TRI':
                ts = "tri"
            else:
                ts = "sin"

            yi.paramsSetString("shape", ts)

            textureConfigured = True

        elif tex.yaf_tex_type == 'MARBLE':
            yi.printInfo("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            yi.paramsSetString("type", "marble")

            yi.paramsSetInt("depth", tex.noise_depth)
            yi.paramsSetFloat("turbulence", tex.turbulence)

            noise_size = tex.noise_scale
            if  noise_size > 0:
                noise_size = 1.0 / noise_size

            if tex.noise_type == 'HARD_NOISE':
                hard = True
            else:
                hard = False

            yi.paramsSetFloat("size", noise_size)
            yi.paramsSetBool("hard", hard)

            sharp = 4.0
            if tex.marble_type == 'SOFT':
                sharp = 2.0
            elif tex.marble_type == 'SHARP':
                sharp = 4.0
            elif tex.marble_type == 'SHARPER':
                sharp = 8.0

            yi.paramsSetFloat("sharpness", sharp)
            yi.paramsSetString("noise_type", noise2string(tex.noise_basis))

            if tex.noise_basis_2 == 'SAW':
                ts = "saw"
            elif tex.noise_basis_2 == 'TRI':
                ts = "tri"
            else:
                ts = "sin"

            yi.paramsSetString("shape", ts)

            textureConfigured = True

        elif tex.yaf_tex_type == 'VORONOI':
            yi.printInfo("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            yi.paramsSetString("type", "voronoi")

            if tex.color_mode == 'POSITION':
                ts = "position"
            elif tex.color_mode == 'POSITION_OUTLINE':
                ts = "position-outline"
            elif tex.color_mode == 'POSITION_OUTLINE_INTENSITY':
                ts = "position-outline-intensity"
            else:
                ts = "intensity-without-color"

            yi.paramsSetString("color_mode", ts)

            yi.paramsSetFloat("weight1", tex.weight_1)
            yi.paramsSetFloat("weight2", tex.weight_2)
            yi.paramsSetFloat("weight3", tex.weight_3)
            yi.paramsSetFloat("weight4", tex.weight_4)

            yi.paramsSetFloat("mk_exponent", tex.minkovsky_exponent)
            yi.paramsSetFloat("intensity", tex.noise_intensity)

            noise_size = tex.noise_scale
            if  noise_size > 0:
                noise_size = 1.0 / noise_size
            yi.paramsSetFloat("size", noise_size)

            switchDistMetric = {
                'DISTANCE_SQUARED': 'squared',
                'MANHATTAN': 'manhattan',
                'CHEBYCHEV': 'chebychev',
                'MINKOVSKY_HALF': 'minkovsky_half',
                'MINKOVSKY_FOOUR': 'minkovsky_four',
                'MINKOVSKY': 'minkovsky',
            }

            ts = switchDistMetric.get(tex.distance_metric, 'minkovsky')  # set distance metric for VORONOI Texture, default is 'minkovsky'
            yi.paramsSetString("distance_metric", ts)

            textureConfigured = True

        elif tex.yaf_tex_type == 'MUSGRAVE':
            yi.printInfo("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            yi.paramsSetString("type", "musgrave")

            switchMusgraveType = {
                'MULTIFRACTAL': 'multifractal',
                'RIDGED_MULTIFRACTAL': 'ridgedmf',
                'HYBRID_MULTIFRACTAL': 'hybridmf',
                'HETERO_TERRAIN': 'heteroterrain',
                'FBM': 'fBm',
                }
            ts = switchMusgraveType.get(tex.musgrave_type, 'multifractal')  # set MusgraveType, default is 'multifractal'

            yi.paramsSetString("musgrave_type", ts)
            yi.paramsSetString("noise_type", noise2string(tex.noise_basis))
            yi.paramsSetFloat("H", tex.dimension_max)
            yi.paramsSetFloat("lacunarity", tex.lacunarity)
            yi.paramsSetFloat("octaves", tex.octaves)

            noise_size = tex.noise_scale
            if  noise_size > 0:
                noise_size = 1.0 / noise_size
            yi.paramsSetFloat("size", noise_size)
            yi.paramsSetFloat("offset", tex.offset)
            yi.paramsSetFloat("intensity", tex.noise_intensity)
            yi.paramsSetFloat("gain", tex.gain)

            textureConfigured = True

        elif tex.yaf_tex_type == 'DISTORTED_NOISE':
            yi.printInfo("Exporter: Creating Texture: '{0}' type {1}".format(name, tex.yaf_tex_type))
            yi.paramsSetString("type", "distorted_noise")

            yi.paramsSetFloat("distort", tex.distortion)

            noise_size = tex.noise_scale
            if  noise_size > 0:
                noise_size = 1.0 / noise_size
            yi.paramsSetFloat("size", noise_size)

            yi.paramsSetString("noise_type1", noise2string(tex.noise_basis))
            yi.paramsSetString("noise_type2", noise2string(tex.noise_distortion))

            textureConfigured = True

        elif tex.yaf_tex_type == 'IMAGE' and tex.image and tex.image.source in {'FILE', 'SEQUENCE', 'GENERATED'}:

            filename = os.path.splitext(os.path.basename(bpy.data.filepath))[0]

            if not any(filename):
                filename = "untitled"
                save_dir = os.path.expanduser("~")
            else:
                save_dir = "//"

            filename = clean_name(filename)
            fileformat = scene.render.image_settings.file_format.lower()
            extract_path = os.path.join(filename, "{:05d}".format(scene.frame_current))

            if tex.image.source == 'GENERATED':
                image_tex = "yaf_baked_image_{0}.{1}".format(clean_name(tex.name), fileformat)
                image_tex = os.path.join(save_dir, extract_path, image_tex)
                image_tex = abspath(image_tex)
                tex.image.save_render(image_tex, scene)
            if tex.image.source == 'FILE':
                if tex.image.packed_file:
                    image_tex = "yaf_extracted_image_{0}.{1}".format(clean_name(tex.name), fileformat)
                    image_tex = os.path.join(save_dir, extract_path, image_tex)
                    image_tex = abspath(image_tex)
                    tex.image.save_render(image_tex, scene)
                else:
                    if tex.image.library is not None:
                        image_tex = abspath(tex.image.filepath, library=tex.image.library)
                    else:
                        image_tex = abspath(tex.image.filepath)
                    if not os.path.exists(image_tex):
                        yi.printError("Exporter: Image texture {0} not found on: {1}".format(tex.name, image_tex))
                        return False
            if tex.image.source == 'SEQUENCE':
                if tex.image.packed_file:
                    image_tex = "yaf_extracted_image_{0}.{1}".format(clean_name(tex.name), fileformat)
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
                        yi.printError("Exporter: Image texture {0} not found on: {1}".format(tex.name, image_tex))
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
            yi.paramsSetString("color_space", texture_color_space)
            yi.paramsSetFloat("gamma", texture_gamma)

            if tex.yaf_tex_optimization == "default":
                texture_optimization = scene.gs_tex_optimization
            else:
                texture_optimization = tex.yaf_tex_optimization
            yi.paramsSetString("image_optimization", texture_optimization)
            yi.paramsSetString("filename", image_tex)
            image_name = name + "_image"
            yi.createImage(image_name)
            yi.paramsClearAll()

            yi.printInfo("Exporter: Creating Texture: '{0}' type {1}: {2}. Texture Color Space: '{3}', gamma={4}. Texture optimization='{5}'".format(name, tex.yaf_tex_type, image_tex, texture_color_space, texture_gamma, texture_optimization))

            yi.paramsSetString("type", "image")
            yi.paramsSetString("image_name", image_name)

            yi.paramsSetString("interpolate", tex.yaf_tex_interpolate)

            yi.paramsSetBool("use_alpha", tex.yaf_use_alpha)
            yi.paramsSetBool("calc_alpha", tex.use_calculate_alpha)
            yi.paramsSetBool("normalmap", tex.yaf_is_normal_map)

            # repeat
            repeat_x = 1
            repeat_y = 1

            if tex.extension == 'REPEAT':
                repeat_x = tex.repeat_x
                repeat_y = tex.repeat_y

            yi.paramsSetInt("xrepeat", repeat_x)
            yi.paramsSetInt("yrepeat", repeat_y)

            # clipping
            extension = tex.extension
            switchExtension = {
                'EXTEND': 'extend',
                'CLIP': 'clip',
                'CLIP_CUBE': 'clipcube',
                'CHECKER': 'checker',
                }
            clipping = switchExtension.get(extension, 'repeat')  # set default clipping to 'repeat'
            yi.paramsSetString("clipping", clipping)
            if clipping == 'checker':
                yi.paramsSetBool("even_tiles", tex.use_checker_even)
                yi.paramsSetBool("odd_tiles", tex.use_checker_odd)

            # crop min/max
            yi.paramsSetFloat("cropmin_x", tex.crop_min_x)
            yi.paramsSetFloat("cropmin_y", tex.crop_min_y)
            yi.paramsSetFloat("cropmax_x", tex.crop_max_x)
            yi.paramsSetFloat("cropmax_y", tex.crop_max_y)
            yi.paramsSetBool("rot90", tex.use_flip_axis)
            yi.paramsSetBool("mirror_x", tex.use_mirror_x)
            yi.paramsSetBool("mirror_y", tex.use_mirror_y)
            yi.paramsSetFloat("trilinear_level_bias", tex.yaf_trilinear_level_bias)
            yi.paramsSetFloat("ewa_max_anisotropy", tex.yaf_ewa_max_anisotropy)

            textureConfigured = True

        #yi.paramsSetBool("img_grayscale", tex.yaf_img_grayscale)
        yi.paramsSetFloat("adj_mult_factor_red", tex.factor_red)
        yi.paramsSetFloat("adj_mult_factor_green", tex.factor_green)
        yi.paramsSetFloat("adj_mult_factor_blue", tex.factor_blue)
        yi.paramsSetFloat("adj_intensity", tex.intensity)
        yi.paramsSetFloat("adj_contrast", tex.contrast)
        yi.paramsSetFloat("adj_saturation", tex.saturation)
        yi.paramsSetFloat("adj_hue", math.degrees(tex.yaf_adj_hue))
        yi.paramsSetBool("adj_clamp", tex.use_clamp)

        if tex.use_color_ramp:
            yi.paramsSetString("ramp_color_mode", tex.color_ramp.color_mode)
            yi.paramsSetString("ramp_hue_interpolation", tex.color_ramp.hue_interpolation)
            yi.paramsSetString("ramp_interpolation", tex.color_ramp.interpolation)
            i = 0
            for item in tex.color_ramp.elements:
                yi.paramsSetColor("ramp_item_" + str(i) + "_color", item.color[0], item.color[1], item.color[2], item.color[3])
                yi.paramsSetFloat("ramp_item_" + str(i) + "_position", item.position)
                i += 1
            yi.paramsSetInt("ramp_num_items", i)

        if textureConfigured:
            yi.createTexture(name)
            yi.paramsClearAll()
            self.loadedTextures.add(name)

        return textureConfigured
