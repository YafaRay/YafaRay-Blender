import os
import bpy
import re
from  math import *


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

        if tex.type == 'BLEND':
            yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type BLEND")
            yi.paramsSetString("type", "blend")

            switchBlendType = {
                'LINEAR': 'lin',
                'QUADRATIC': 'quad',
                'EASING': 'ease',
                'DIAGONAL': 'diag',
                'SPHERICAL': 'sphere',
                'QUADRATIC_SPHERE': 'halo',
                'RADIAL': 'radial',
            }

            stype = switchBlendType.get(tex.progression, 'lin')  # set blend type for blend texture, default is 'lin'
            yi.paramsSetString("stype", stype)

            textureConfigured = True

        elif tex.type == 'CLOUDS':
            yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type CLOUDS")
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

            textureConfigured = True

        elif tex.type == 'WOOD':
            yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type WOOD")
            yi.paramsSetString("type", "wood")

            yi.paramsSetInt("depth", 0)

            turb       = 0.0
            noise_size = 0.25
            hard       = True

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

            if tex.noise_basis == 'SAW':
                ts = "saw"
            elif tex.noise_basis == 'TRI':
                ts = "tri"
            else:
                ts = "sin"

            yi.paramsSetString("shape", ts)

            textureConfigured = True

        elif tex.type == 'MARBLE':
            yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type MARBLE")
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

        elif tex.type == 'VORONOI':
            yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type VORONOI")
            yi.paramsSetString("type", "voronoi")

            if tex.color_mode == 'POSITION':
                ts = "col1"
            elif tex.color_mode  == 'POSITION_OUTLINE':
                ts = "col2"
            elif tex.color_mode  == 'POSITION_OUTLINE_INTENSITY':
                ts = "col3"
            else:
                ts = "int"

            yi.paramsSetString("color_type", ts)

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

        elif tex.type == 'MUSGRAVE':
            yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type MUSGRAVE")
            yi.paramsSetString("type", "musgrave")

            ts = "fBm"
            if tex.musgrave_type == 'MULTIFRACTAL':
                ts = "multifractal"
            elif tex.musgrave_type == 'RIDGED_MULTIFRACTAL':
                ts = "ridgedmf"
            elif tex.musgrave_type == 'HYBRID_MULTIFRACTAL':
                ts = "hybridmf"
            elif tex.musgrave_type == 'HETERO_TERRAIN':
                ts = "heteroterrain"

            yi.paramsSetString("musgrave_type", ts)
            yi.paramsSetString("noise_type", noise2string(tex.noise_basis))
            yi.paramsSetFloat("H", tex.dimension_max)
            yi.paramsSetFloat("lacunarity", tex.lacunarity)
            yi.paramsSetFloat("octaves", tex.octaves)

            noise_size = tex.noise_scale
            if  noise_size > 0:
                noise_size = 1.0 / noise_size
            yi.paramsSetFloat("size", noise_size)

            yi.paramsSetFloat("intensity", tex.offset)

            textureConfigured = True

        elif tex.type == 'DISTORTED_NOISE':
            yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type DISTORTED NOISE")
            yi.paramsSetString("type", "distorted_noise")

            yi.paramsSetFloat("distort", tex.distortion)

            noise_size = tex.noise_scale
            if  noise_size > 0:
                noise_size = 1.0 / noise_size
            yi.paramsSetFloat("size", noise_size)

            yi.paramsSetString("noise_type1", noise2string(tex.noise_basis))
            yi.paramsSetString("noise_type2", noise2string(tex.noise_distortion))

            textureConfigured = True

        elif tex.type == 'IMAGE' and tex.image:
            image_tex = tex.image
            image_file = bpy.path.abspath(image_tex.filepath)
            image_file = os.path.realpath(image_file)
            image_file = os.path.normpath(image_file)

            if image_file != "" and not os.path.exists(image_file):
                yi.printInfo("Exporter: No valid texture image supplied.")
                return False

            yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type IMAGE: " + image_file)

            yi.paramsSetString("type", "image")
            yi.paramsSetString("filename", image_file)

            yi.paramsSetBool("use_alpha", tex.use_alpha)
            yi.paramsSetBool("calc_alpha", tex.use_calculate_alpha)
            yi.paramsSetBool("normalmap", tex.yaf_is_normal_map)
            yi.paramsSetFloat("gamma", scene.gs_gamma_input)
            yi.paramsSetFloat("exposure_adjust", tex.yaf_tex_expadj)  # experimental?
            if not tex.yaf_tex_interpolate == 'bilinear':  # bilinear is set by default
                yi.paramsSetString("interpolate", tex.yaf_tex_interpolate)

            # repeat
            repeat_x = 1
            repeat_y = 1

            if tex.extension == 'REPEAT':
                repeat_x = tex.repeat_x
                repeat_y = tex.repeat_y

            yi.paramsSetInt("xrepeat", repeat_x)
            yi.paramsSetInt("yrepeat", repeat_y)

            # clipping
            ext = tex.extension

            if ext == 'EXTEND':
                yi.paramsSetString("clipping", "extend")
            elif ext == 'CLIP':
                yi.paramsSetString("clipping", "clip")
            elif ext == 'CLIP_CUBE':
                yi.paramsSetString("clipping", "clipcube")
            elif ext == "CHECKER":
                yi.paramsSetString("clipping", "checker")
                yi.paramsSetBool("even_tiles", tex.use_checker_even)
                yi.paramsSetBool("odd_tiles", tex.use_checker_odd)
            else:
                yi.paramsSetString("clipping", "repeat")

            # crop min/max
            yi.paramsSetFloat("cropmin_x", tex.crop_min_x)
            yi.paramsSetFloat("cropmin_y", tex.crop_min_y)
            yi.paramsSetFloat("cropmax_x", tex.crop_max_x)
            yi.paramsSetFloat("cropmax_y", tex.crop_max_y)

            yi.paramsSetBool("rot90", tex.use_flip_axis)
            textureConfigured = True

        if textureConfigured:
            yi.createTexture(name)
            self.loadedTextures.add(name)

        return textureConfigured
