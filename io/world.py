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

import math
import bpy
from bpy.path import abspath
from os.path import realpath, normpath
import libyafaray4_bindings

class World:
    def __init__(self, scene, logger):
        self.scene = scene
        self.yaf_logger = logger

    def export(self, bl_scene, yaf_scene, is_preview):

        bl_world = bl_scene.world

        if bl_world:
            bg_type = bl_world.bg_type
            use_ibl = bl_world.bg_use_ibl
            ibl_samples = bl_world.bg_ibl_samples
            bg_power = bl_world.bg_power
            c = bl_world.bg_single_color
        else:
            bg_type = "Single Color"
            c = (0.0, 0.0, 0.0)
            use_ibl = False
            ibl_samples = 16
            bg_power = 1

        self.yaf_logger.printInfo("Exporting World, type: {0}".format(bg_type))
        yaf_param_map = libyafaray4_bindings.ParamMap()

        if bg_type == 'Texture':
            if bl_world.active_texture is not None:
                world_tex = bl_world.active_texture
                self.yaf_logger.printInfo("World Texture, name: {0}".format(world_tex.name))
            else:
                world_tex = None

            if world_tex is not None:

                if world_tex.type == "IMAGE" and (world_tex.image is not None):

                    image_file = abspath(world_tex.image.filepath)
                    image_file = realpath(image_file)
                    image_file = normpath(image_file)

                    yaf_param_map.set_string("filename", image_file)

                    texture_color_space = "sRGB"
                    texture_gamma = 1.0

                    if world_tex.image.colorspace_settings.name == "sRGB" or world_tex.image.colorspace_settings.name == "VD16":
                        texture_color_space = "sRGB"

                    elif world_tex.image.colorspace_settings.name == "XYZ":
                        texture_color_space = "XYZ"

                    elif world_tex.image.colorspace_settings.name == "Linear" or world_tex.image.colorspace_settings.name == "Linear ACES" or world_tex.image.colorspace_settings.name == "Non-Color":
                        texture_color_space = "LinearRGB"

                    elif world_tex.image.colorspace_settings.name == "Raw":
                        texture_color_space = "Raw_manualGamma"
                        texture_gamma = world_tex.yaf_gamma_input  #We only use the selected gamma if the color space is set to "Raw"

                    yaf_param_map.set_string("color_space", texture_color_space)
                    yaf_param_map.set_float("gamma", texture_gamma)

                    image_name = "world_texture_image"
                    self.scene.createImage(image_name)
                    yaf_param_map = libyafaray4_bindings.ParamMap()

                    yaf_param_map.set_string("image_name", image_name)
                    yaf_param_map.set_string("type", "image")
                    # exposure_adjust not restricted to integer range anymore
                    #yaf_param_map.set_float("exposure_adjust", world.exposure) #bg_exposure)
                    interpolate = 'none'
                    if world_tex.use_interpolation == True:
                        interpolate = 'bilinear'
                    yaf_param_map.set_string("interpolate", interpolate)

                    # FIXME DAVID color adjustments and texture params for non-image textures??
                    yaf_param_map.set_float("adj_mult_factor_red", world_tex.factor_red)
                    yaf_param_map.set_float("adj_mult_factor_green", world_tex.factor_green)
                    yaf_param_map.set_float("adj_mult_factor_blue", world_tex.factor_blue)
                    yaf_param_map.set_float("adj_intensity", world_tex.intensity)
                    yaf_param_map.set_float("adj_contrast", world_tex.contrast)
                    yaf_param_map.set_float("adj_saturation", world_tex.saturation)
                    yaf_param_map.set_float("adj_hue", math.degrees(world_tex.yaf_adj_hue))
                    yaf_param_map.set_bool("adj_clamp", world_tex.use_clamp)
                    self.scene.createTexture("world_texture")
                    yaf_param_map = libyafaray4_bindings.ParamMap()

                    # Export the actual background
                    #texco = world.texture_slots[world.active_texture_index].texture_coords
                    text_coord = bl_world.yaf_mapworld_type
                    #
                    mappingType = {'ANGMAP': 'angular',
                                   'SPHERE': 'sphere'}
                    texco = mappingType.get(text_coord, "angular")
                    yaf_param_map.set_string("mapping", texco)

                    # now, this msg is not need , but....
                    if text_coord not in {'ANGMAP', 'SPHERE'}:
                        self.yaf_logger.printWarning("World texture mapping neither Sphere or AngMap, set it to AngMap now by default!")

                    yaf_param_map.set_string("type", "textureback")
                    yaf_param_map.set_string("texture", "world_texture")
                    yaf_param_map.set_bool("ibl", use_ibl)
                    #yaf_param_map.set_float("ibl_clamp_sampling", world.ibl_clamp_sampling) #No longer needed after this issue was solved in Core (http://www.yafaray.org/node/752#comment-1621), but I will leave it here for now just in case...
                    if is_preview:
                        yaf_param_map.set_float("smartibl_blur", 0.0) #To avoid causing Blender UI freezing while waiting for the blur process to complete in the material/world previews
                    else:
                        yaf_param_map.set_float("smartibl_blur", bl_world.bg_smartibl_blur)
                    # 'with_caustic' and 'with_diffuse' settings gets checked in textureback.cc,
                    # so if IBL enabled when they are used...
                    yaf_param_map.set_int("ibl_samples", ibl_samples)
                    yaf_param_map.set_float("power", bg_power)
                    yaf_param_map.set_float("rotation", bl_world.bg_rotation)

        elif bg_type == 'Gradient':
            c = bl_world.bg_horizon_color
            yaf_param_map.set_color("horizon_color", c[0], c[1], c[2])

            c = bl_world.bg_zenith_color
            yaf_param_map.set_color("zenith_color", c[0], c[1], c[2])

            c = bl_world.bg_horizon_ground_color
            yaf_param_map.set_color("horizon_ground_color", c[0], c[1], c[2])

            c = bl_world.bg_zenith_ground_color
            yaf_param_map.set_color("zenith_ground_color", c[0], c[1], c[2])

            yaf_param_map.set_float("power", bg_power)
            yaf_param_map.set_bool("ibl", use_ibl)
            yaf_param_map.set_int("ibl_samples", ibl_samples)
            yaf_param_map.set_string("type", "gradientback")

        elif bg_type == 'Sunsky1':
            f = bl_world.bg_from
            yaf_param_map.set_vector("from", f[0], f[1], f[2])
            yaf_param_map.set_float("turbidity", bl_world.bg_turbidity)
            yaf_param_map.set_float("a_var", bl_world.bg_a_var)
            yaf_param_map.set_float("b_var", bl_world.bg_b_var)
            yaf_param_map.set_float("c_var", bl_world.bg_c_var)
            yaf_param_map.set_float("d_var", bl_world.bg_d_var)
            yaf_param_map.set_float("e_var", bl_world.bg_e_var)
            yaf_param_map.set_bool("add_sun", bl_world.bg_add_sun)
            yaf_param_map.set_float("sun_power", bl_world.bg_sun_power)
            yaf_param_map.set_bool("background_light", bl_world.bg_background_light)
            yaf_param_map.set_int("light_samples", bl_world.bg_light_samples)
            yaf_param_map.set_float("power", bl_world.bg_power)
            yaf_param_map.set_string("type", "sunsky")
            yaf_param_map.set_bool("cast_shadows_sun", bl_world.bg_cast_shadows_sun)

        elif bg_type == "Sunsky2":
            f = bl_world.bg_from
            yaf_param_map.set_vector("from", f[0], f[1], f[2])
            yaf_param_map.set_float("turbidity", bl_world.bg_ds_turbidity)
            yaf_param_map.set_float("altitude", bl_world.bg_dsaltitude)
            yaf_param_map.set_float("a_var", bl_world.bg_a_var)
            yaf_param_map.set_float("b_var", bl_world.bg_b_var)
            yaf_param_map.set_float("c_var", bl_world.bg_c_var)
            yaf_param_map.set_float("d_var", bl_world.bg_d_var)
            yaf_param_map.set_float("e_var", bl_world.bg_e_var)
            yaf_param_map.set_bool("add_sun", bl_world.bg_add_sun)
            if bl_world.bg_add_sun:
                yaf_param_map.set_float("sun_power", bl_world.bg_sun_power)
            yaf_param_map.set_bool("background_light", bl_world.bg_background_light)
            if bl_world.bg_background_light:
                yaf_param_map.set_float("power", bl_world.bg_power)
            yaf_param_map.set_int("light_samples", bl_world.bg_light_samples)
            yaf_param_map.set_float("bright", bl_world.bg_dsbright)
            yaf_param_map.set_bool("night", bl_world.bg_dsnight)
            yaf_param_map.set_float("exposure", bl_world.bg_exposure)
            yaf_param_map.set_bool("clamp_rgb", bl_world.bg_clamp_rgb)
            yaf_param_map.set_bool("gamma_enc", bl_world.bg_gamma_enc)
            yaf_param_map.set_string("color_space", bl_world.bg_color_space)
            yaf_param_map.set_string("type", "darksky")
            yaf_param_map.set_bool("cast_shadows_sun", bl_world.bg_cast_shadows_sun)

        else:
            yaf_param_map.set_color("color", c[0], c[1], c[2])
            yaf_param_map.set_bool("ibl", use_ibl)
            yaf_param_map.set_int("ibl_samples", ibl_samples)
            yaf_param_map.set_float("power", bg_power)
            yaf_param_map.set_string("type", "constant")

        if bl_world is not None:
            yaf_param_map.set_bool("cast_shadows", bl_world.bg_cast_shadows)
            yaf_param_map.set_bool("with_caustic", bl_world.bg_with_caustic)
            yaf_param_map.set_bool("with_diffuse", bl_world.bg_with_diffuse)

        yaf_scene.defineBackground(yaf_param_map)

        return True
