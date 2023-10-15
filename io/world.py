# SPDX-License-Identifier: GPL-2.0-or-later

import math
from os.path import realpath, normpath

import libyafaray4_bindings
from bpy.path import abspath
from ..util.io import scene_from_depsgraph


class WorldControl:
    def __init__(self, depsgraph, scene_yafaray, logger, is_preview):
        self.depsgraph = depsgraph
        self.scene = scene_from_depsgraph(depsgraph)
        self.scene_yafaray = scene_yafaray
        self.logger = logger
        self.is_preview = is_preview

    def export(self, scene_blender, scene_yafaray, is_preview):

        world = scene_blender.world

        if world:
            bg_type = world.bg_type
            use_ibl = world.bg_use_ibl
            ibl_samples = world.bg_ibl_samples
            bg_power = world.bg_power
            c = world.bg_single_color
        else:
            bg_type = "Single Color"
            c = (0.0, 0.0, 0.0)
            use_ibl = False
            ibl_samples = 16
            bg_power = 1

        self.logger.print_info("Exporting World, type: {0}".format(bg_type))
        param_map = libyafaray4_bindings.ParamMap()

        if bg_type == 'Texture':
            if world.active_texture is not None:
                world_tex = world.active_texture
                self.logger.print_info("World Texture, name: {0}".format(world_tex.name))
            else:
                world_tex = None

            if world_tex is not None:

                if world_tex.type == "IMAGE" and (world_tex.image is not None):

                    image_file = abspath(world_tex.image.filepath)
                    image_file = realpath(image_file)
                    image_file = normpath(image_file)

                    param_map.set_string("filename", image_file)

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
                        texture_gamma = world_tex.yaf_gamma_input  # We only use the selected gamma if the color space is set to "Raw"

                    param_map.set_string("color_space", texture_color_space)
                    param_map.set_float("gamma", texture_gamma)

                    image_name = "world_texture_image"
                    self.scene_yafaray.create_image(image_name, param_map)
                    param_map = libyafaray4_bindings.ParamMap()

                    param_map.set_string("image_name", image_name)
                    param_map.set_string("type", "image")
                    # exposure_adjust not restricted to integer range anymore
                    # param_map.set_float("exposure_adjust", world.exposure) #bg_exposure)
                    interpolate = 'none'
                    if world_tex.use_interpolation == True:
                        interpolate = 'bilinear'
                    param_map.set_string("interpolate", interpolate)

                    # FIXME DAVID color adjustments and texture params for non-image textures??
                    param_map.set_float("adj_mult_factor_red", world_tex.factor_red)
                    param_map.set_float("adj_mult_factor_green", world_tex.factor_green)
                    param_map.set_float("adj_mult_factor_blue", world_tex.factor_blue)
                    param_map.set_float("adj_intensity", world_tex.intensity)
                    param_map.set_float("adj_contrast", world_tex.contrast)
                    param_map.set_float("adj_saturation", world_tex.saturation)
                    param_map.set_float("adj_hue", math.degrees(world_tex.yaf_adj_hue))
                    param_map.set_bool("adj_clamp", world_tex.use_clamp)
                    self.scene_yafaray.create_texture("world_texture", param_map)
                    param_map = libyafaray4_bindings.ParamMap()

                    # Export the actual background
                    # texco = world.texture_slots[world.active_texture_index].texture_coords
                    text_coord = world.yaf_mapworld_type
                    #
                    mappingType = {'ANGMAP': 'angular',
                                   'SPHERE': 'sphere'}
                    texco = mappingType.get(text_coord, "angular")
                    param_map.set_string("mapping", texco)

                    # now, this msg is not need , but....
                    if text_coord not in {'ANGMAP', 'SPHERE'}:
                        self.logger.printWarning(
                            "World texture mapping neither Sphere or AngMap, set it to AngMap now by default!")

                    param_map.set_string("type", "textureback")
                    param_map.set_string("texture", "world_texture")
                    param_map.set_bool("ibl", use_ibl)
                    # param_map.set_float("ibl_clamp_sampling", world.ibl_clamp_sampling) #No longer needed after this issue was solved in Core (http://www.yafaray.org/node/752#comment-1621), but I will leave it here for now just in case...
                    if is_preview:
                        param_map.set_float("smartibl_blur",
                                            0.0)  # To avoid causing Blender UI freezing while waiting for the blur process to complete in the material/world previews
                    else:
                        param_map.set_float("smartibl_blur", world.bg_smartibl_blur)
                    # 'with_caustic' and 'with_diffuse' settings gets checked in textureback.cc,
                    # so if IBL enabled when they are used...
                    param_map.set_int("ibl_samples", ibl_samples)
                    param_map.set_float("power", bg_power)
                    param_map.set_float("rotation", world.bg_rotation)

        elif bg_type == 'Gradient':
            c = world.bg_horizon_color
            param_map.set_color("horizon_color", c[0], c[1], c[2])

            c = world.bg_zenith_color
            param_map.set_color("zenith_color", c[0], c[1], c[2])

            c = world.bg_horizon_ground_color
            param_map.set_color("horizon_ground_color", c[0], c[1], c[2])

            c = world.bg_zenith_ground_color
            param_map.set_color("zenith_ground_color", c[0], c[1], c[2])

            param_map.set_float("power", bg_power)
            param_map.set_bool("ibl", use_ibl)
            param_map.set_int("ibl_samples", ibl_samples)
            param_map.set_string("type", "gradientback")

        elif bg_type == 'Sunsky1':
            f = world.bg_from
            param_map.set_vector("from", f[0], f[1], f[2])
            param_map.set_float("turbidity", world.bg_turbidity)
            param_map.set_float("a_var", world.bg_a_var)
            param_map.set_float("b_var", world.bg_b_var)
            param_map.set_float("c_var", world.bg_c_var)
            param_map.set_float("d_var", world.bg_d_var)
            param_map.set_float("e_var", world.bg_e_var)
            param_map.set_bool("add_sun", world.bg_add_sun)
            param_map.set_float("sun_power", world.bg_sun_power)
            param_map.set_bool("background_light", world.bg_background_light)
            param_map.set_int("light_samples", world.bg_light_samples)
            param_map.set_float("power", world.bg_power)
            param_map.set_string("type", "sunsky")
            param_map.set_bool("cast_shadows_sun", world.bg_cast_shadows_sun)

        elif bg_type == "Sunsky2":
            f = world.bg_from
            param_map.set_vector("from", f[0], f[1], f[2])
            param_map.set_float("turbidity", world.bg_ds_turbidity)
            param_map.set_float("altitude", world.bg_dsaltitude)
            param_map.set_float("a_var", world.bg_a_var)
            param_map.set_float("b_var", world.bg_b_var)
            param_map.set_float("c_var", world.bg_c_var)
            param_map.set_float("d_var", world.bg_d_var)
            param_map.set_float("e_var", world.bg_e_var)
            param_map.set_bool("add_sun", world.bg_add_sun)
            if world.bg_add_sun:
                param_map.set_float("sun_power", world.bg_sun_power)
            param_map.set_bool("background_light", world.bg_background_light)
            if world.bg_background_light:
                param_map.set_float("power", world.bg_power)
            param_map.set_int("light_samples", world.bg_light_samples)
            param_map.set_float("bright", world.bg_dsbright)
            param_map.set_bool("night", world.bg_dsnight)
            param_map.set_float("exposure", world.bg_exposure)
            param_map.set_bool("clamp_rgb", world.bg_clamp_rgb)
            param_map.set_bool("gamma_enc", world.bg_gamma_enc)
            param_map.set_string("color_space", world.bg_color_space)
            param_map.set_string("type", "darksky")
            param_map.set_bool("cast_shadows_sun", world.bg_cast_shadows_sun)

        else:
            param_map.set_color("color", c[0], c[1], c[2])
            param_map.set_bool("ibl", use_ibl)
            param_map.set_int("ibl_samples", ibl_samples)
            param_map.set_float("power", bg_power)
            param_map.set_string("type", "constant")

        if world is not None:
            param_map.set_bool("cast_shadows", world.bg_cast_shadows)
            param_map.set_bool("with_caustic", world.bg_with_caustic)
            param_map.set_bool("with_diffuse", world.bg_with_diffuse)

        scene_yafaray.define_background(param_map)

        return True
