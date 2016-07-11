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
from bpy.path import abspath
from os.path import realpath, normpath

class yafWorld:
    def __init__(self, interface):
        self.yi = interface

    def exportWorld(self, scene, is_preview):
        yi = self.yi

        world = scene.world

        if world:
            bg_type = world.bg_type
            useIBL = world.bg_use_ibl
            iblSamples = world.bg_ibl_samples
            bgPower = world.bg_power
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
        
                yi.paramsSetFloat("adj_mult_factor_red", worldTex.factor_red)
                yi.paramsSetFloat("adj_mult_factor_green", worldTex.factor_green)
                yi.paramsSetFloat("adj_mult_factor_blue", worldTex.factor_blue)
                yi.paramsSetFloat("adj_intensity", worldTex.intensity)
                yi.paramsSetFloat("adj_contrast", worldTex.contrast)
                yi.paramsSetFloat("adj_saturation", worldTex.saturation)
                yi.paramsSetFloat("adj_hue", math.degrees(worldTex.yaf_adj_hue))
                yi.paramsSetBool("adj_clamp", worldTex.use_clamp)

                if worldTex.type == "IMAGE" and (worldTex.image is not None):

                    yi.paramsSetString("type", "image")

                    image_file = abspath(worldTex.image.filepath)
                    image_file = realpath(image_file)
                    image_file = normpath(image_file)

                    yi.paramsSetString("filename", image_file)

                    # exposure_adjust not restricted to integer range anymore
                    #yi.paramsSetFloat("exposure_adjust", world.exposure) #bg_exposure)

                    interpolate = 'none'
                    if worldTex.use_interpolation == True:
                        interpolate = 'bilinear'
                    #
                    yi.paramsSetString("interpolate", interpolate)

                    texture_color_space = "sRGB"
                    texture_gamma = 1.0

                    if worldTex.image.colorspace_settings.name == "sRGB" or worldTex.image.colorspace_settings.name == "VD16":
                        texture_color_space = "sRGB"
                        
                    elif worldTex.image.colorspace_settings.name == "XYZ":
                        texture_color_space = "XYZ"
                        
                    elif worldTex.image.colorspace_settings.name == "Linear" or worldTex.image.colorspace_settings.name == "Linear ACES" or worldTex.image.colorspace_settings.name == "Non-Color":
                        texture_color_space = "LinearRGB"
                        
                    elif worldTex.image.colorspace_settings.name == "Raw":
                        texture_color_space = "Raw_manualGamma"
                        texture_gamma = worldTex.yaf_gamma_input  #We only use the selected gamma if the color space is set to "Raw"
                
                    yi.paramsSetString("color_space", texture_color_space)
                    yi.paramsSetFloat("gamma", texture_gamma)
                    
                    yi.createTexture("world_texture")

                    # Export the actual background
                    #texco = world.texture_slots[world.active_texture_index].texture_coords
                    textcoord = world.yaf_mapworld_type
                    yi.paramsClearAll()
                    #
                    mappingType = {'ANGMAP': 'angular',
                                   'SPHERE': 'sphere'}                    
                    texco = mappingType.get(textcoord, "angular")
                    yi.paramsSetString("mapping", texco)
                    
                    # now, this msg is not need , but....
                    if textcoord not in {'ANGMAP', 'SPHERE'}:
                        yi.printWarning("World texture mapping neither Sphere or AngMap, set it to AngMap now by default!")
                        
                    yi.paramsSetString("type", "textureback")
                    yi.paramsSetString("texture", "world_texture")
                    yi.paramsSetBool("ibl", useIBL)
                    yi.paramsSetFloat("ibl_clamp_sampling", world.ibl_clamp_sampling)
                    if is_preview:
                        yi.paramsSetFloat("smartibl_blur", 0.0) #To avoid causing Blender UI freezing while waiting for the blur process to complete in the material/world previews
                    else:
                        yi.paramsSetFloat("smartibl_blur", world.bg_smartibl_blur)
                    # 'with_caustic' and 'with_diffuse' settings gets checked in textureback.cc,
                    # so if IBL enabled when they are used...
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
            if world.bg_add_sun:
                yi.paramsSetFloat("sun_power", world.bg_sun_power)
            yi.paramsSetBool("background_light", world.bg_background_light)
            if world.bg_background_light:
                yi.paramsSetFloat("power", world.bg_power)
            yi.paramsSetInt("light_samples", world.bg_light_samples)
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
            
                    
        if world is not None:
            yi.paramsSetBool("cast_shadows", world.bg_cast_shadows)
            yi.paramsSetBool("cast_shadows_sun", world.bg_cast_shadows_sun)
            yi.paramsSetBool("shoot_caustics", world.bg_with_caustic)
            yi.paramsSetBool("shoot_diffuse", world.bg_with_diffuse)
            
        yi.createBackground("world_background")

        return True
