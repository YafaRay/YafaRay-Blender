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

import bpy
from bpy.path import abspath
from os.path import realpath, normpath


class yafWorld:
        def __init__(self, interface):
                self.yi = interface

        def exportWorld(self, scene):
                yi = self.yi

                world = scene.world

                if world:
                    bg_type = world.bg_type
                    useIBL = world.bg_use_ibl
                    iblSamples = world.bg_ibl_samples
                    bgPower = world.bg_power
                    with_caustic = world.bg_with_caustic
                    with_diffuse = world.bg_with_diffuse
                    c = world.bg_single_color
                else:
                    bg_type = "Single Color"
                    c = (0.0, 0.0, 0.0)
                    useIBL = False
                    iblSamples = 16
                    bgPower = 1

                self.yi.printInfo("Exporting World, type: {0}".format(bg_type))
                yi.paramsClearAll()

                if bg_type == 'Texture':
                    if world.active_texture is not None:
                        worldTex = world.active_texture
                        self.yi.printInfo("World Texture, name: {0}".format(worldTex.name))
                    else:
                        worldTex = None

                    if worldTex is not None:

                        if worldTex.type == "IMAGE" and (worldTex.image is not None):

                            yi.paramsSetString("type", "image")

                            image_file = abspath(worldTex.image.filepath)
                            image_file = realpath(image_file)
                            image_file = normpath(image_file)

                            yi.paramsSetString("filename", image_file)

                            # exposure_adjust not restricted to integer range anymore
                            yi.paramsSetFloat("exposure_adjust", world.bg_exposure)

                            if worldTex.use_interpolation == True:
                                yi.paramsSetString("interpolate", "bilinear")
                            else:
                                yi.paramsSetString("interpolate", "none")

                            yi.createTexture("world_texture")

                            # Export the actual background
                            texco = world.texture_slots[world.active_texture_index].texture_coords
                            yi.paramsClearAll()

                            if texco == 'ANGMAP':
                                yi.paramsSetString("mapping", "probe")
                            elif texco == 'SPHERE':
                                yi.paramsSetString("mapping", "sphere")
                            else:
                                yi.printWarning("World texture mapping neither Sphere nor AngMap, set it to Sphere now by default!")
                                yi.paramsSetString("mapping", "sphere")

                            yi.paramsSetString("type", "textureback")
                            yi.paramsSetString("texture", "world_texture")
                            yi.paramsSetBool("ibl", useIBL)
                            # 'with_caustic' and 'with_diffuse' settings gets checked in textureback.cc,
                            # so if IBL enabled when they are used...
                            yi.paramsSetBool("with_caustic", with_caustic)
                            yi.paramsSetBool("with_diffuse", with_diffuse)
                            yi.paramsSetInt("ibl_samples", iblSamples)
                            yi.paramsSetFloat("power", bgPower)
                            yi.paramsSetFloat("rotation", world.bg_rotation)

                elif bg_type == 'Gradient':
                    c = world.bg_horizon_color
                    yi.paramsSetColor("horizon_color", c[0], c[1], c[2])

                    c = world.bg_zenith_color
                    yi.paramsSetColor("zenith_color", c[0], c[1], c[2])

                    c = world.bg_horizon_ground_color
                    yi.paramsSetColor("horizon_ground_color", c[0], c[1], c[2])

                    c = world.bg_zenith_ground_color
                    yi.paramsSetColor("zenith_ground_color", c[0], c[1], c[2])

                    yi.paramsSetFloat("power", bgPower)
                    yi.paramsSetBool("ibl", useIBL)
                    yi.paramsSetInt("ibl_samples", iblSamples)
                    yi.paramsSetString("type", "gradientback")

                elif bg_type == 'Sunsky1':
                    f = world.bg_from
                    yi.paramsSetPoint("from", f[0], f[1], f[2])
                    yi.paramsSetFloat("turbidity", world.bg_turbidity)
                    yi.paramsSetFloat("a_var", world.bg_a_var)
                    yi.paramsSetFloat("b_var", world.bg_b_var)
                    yi.paramsSetFloat("c_var", world.bg_c_var)
                    yi.paramsSetFloat("d_var", world.bg_d_var)
                    yi.paramsSetFloat("e_var", world.bg_e_var)
                    yi.paramsSetBool("add_sun", world.bg_add_sun)
                    yi.paramsSetFloat("sun_power", world.bg_sun_power)
                    yi.paramsSetBool("background_light", world.bg_background_light)
                    yi.paramsSetInt("light_samples", world.bg_light_samples)
                    yi.paramsSetFloat("power", world.bg_power)
                    yi.paramsSetString("type", "sunsky")

                elif bg_type == "Sunsky2":
                    f = world.bg_from
                    yi.paramsSetPoint("from", f[0], f[1], f[2])
                    yi.paramsSetFloat("turbidity", world.bg_ds_turbidity)
                    yi.paramsSetFloat("altitude", world.bg_dsaltitude)
                    yi.paramsSetFloat("a_var", world.bg_a_var)
                    yi.paramsSetFloat("b_var", world.bg_b_var)
                    yi.paramsSetFloat("c_var", world.bg_c_var)
                    yi.paramsSetFloat("d_var", world.bg_d_var)
                    yi.paramsSetFloat("e_var", world.bg_e_var)
                    yi.paramsSetBool("add_sun", world.bg_add_sun)
                    yi.paramsSetFloat("sun_power", world.bg_sun_power)
                    yi.paramsSetBool("background_light", world.bg_background_light)
                    yi.paramsSetBool("with_caustic", world.bg_with_caustic)
                    yi.paramsSetBool("with_diffuse", world.bg_with_diffuse)
                    yi.paramsSetInt("light_samples", world.bg_light_samples)
                    yi.paramsSetFloat("power", world.bg_power)
                    yi.paramsSetFloat("bright", world.bg_dsbright)
                    yi.paramsSetBool("night", world.bg_dsnight)
                    yi.paramsSetFloat("exposure", world.bg_exposure)
                    yi.paramsSetBool("clamp_rgb", world.bg_clamp_rgb)
                    yi.paramsSetBool("gamma_enc", world.bg_gamma_enc)
                    yi.paramsSetString("color_space", world.bg_color_space)
                    yi.paramsSetString("type", "darksky")

                else:
                    yi.paramsSetColor("color", c[0], c[1], c[2])
                    yi.paramsSetBool("ibl", useIBL)
                    yi.paramsSetInt("ibl_samples", iblSamples)
                    yi.paramsSetFloat("power", bgPower)
                    yi.paramsSetString("type", "constant")

                yi.createBackground("world_background")

                return True
