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
        self.logger = logger

    def exportWorld(self, scene, yaf_scene, is_preview):

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

        self.logger.printInfo("Exporting World, type: {0}".format(bg_type))
        yaf_param_map = libyafaray4_bindings.ParamMap()

        if bg_type == 'Texture':
            if world.active_texture is not None:
                worldTex = world.active_texture
                self.logger.printInfo("World Texture, name: {0}".format(worldTex.name))
            else:
                worldTex = None

            if worldTex is not None:

                if worldTex.type == "IMAGE" and (worldTex.image is not None):

                    image_file = abspath(worldTex.image.filepath)
                    image_file = realpath(image_file)
                    image_file = normpath(image_file)

                    yaf_param_map.setString("filename", image_file)

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
                
                    yaf_param_map.setString("color_space", texture_color_space)
                    yaf_param_map.setFloat("gamma", texture_gamma)

                    image_name = "world_texture_image"
                    self.scene.createImage(image_name)
                    yaf_param_map = libyafaray4_bindings.ParamMap()

                    yaf_param_map.setString("image_name", image_name)
                    yaf_param_map.setString("type", "image")
                    # exposure_adjust not restricted to integer range anymore
                    #yaf_param_map.setFloat("exposure_adjust", world.exposure) #bg_exposure)
                    interpolate = 'none'
                    if worldTex.use_interpolation == True:
                        interpolate = 'bilinear'
                    yaf_param_map.setString("interpolate", interpolate)

                    # FIXME DAVID color adjustments and texture params for non-image textures??
                    yaf_param_map.setFloat("adj_mult_factor_red", worldTex.factor_red)
                    yaf_param_map.setFloat("adj_mult_factor_green", worldTex.factor_green)
                    yaf_param_map.setFloat("adj_mult_factor_blue", worldTex.factor_blue)
                    yaf_param_map.setFloat("adj_intensity", worldTex.intensity)
                    yaf_param_map.setFloat("adj_contrast", worldTex.contrast)
                    yaf_param_map.setFloat("adj_saturation", worldTex.saturation)
                    yaf_param_map.setFloat("adj_hue", math.degrees(worldTex.yaf_adj_hue))
                    yaf_param_map.setBool("adj_clamp", worldTex.use_clamp)
                    self.scene.createTexture("world_texture")
                    yaf_param_map = libyafaray4_bindings.ParamMap()

                    # Export the actual background
                    #texco = world.texture_slots[world.active_texture_index].texture_coords
                    textcoord = world.yaf_mapworld_type
                    #
                    mappingType = {'ANGMAP': 'angular',
                                   'SPHERE': 'sphere'}                    
                    texco = mappingType.get(textcoord, "angular")
                    yaf_param_map.setString("mapping", texco)
                    
                    # now, this msg is not need , but....
                    if textcoord not in {'ANGMAP', 'SPHERE'}:
                        self.logger.printWarning("World texture mapping neither Sphere or AngMap, set it to AngMap now by default!")
                        
                    yaf_param_map.setString("type", "textureback")
                    yaf_param_map.setString("texture", "world_texture")
                    yaf_param_map.setBool("ibl", useIBL)
                    #yaf_param_map.setFloat("ibl_clamp_sampling", world.ibl_clamp_sampling) #No longer needed after this issue was solved in Core (http://www.yafaray.org/node/752#comment-1621), but I will leave it here for now just in case...
                    if is_preview:
                        yaf_param_map.setFloat("smartibl_blur", 0.0) #To avoid causing Blender UI freezing while waiting for the blur process to complete in the material/world previews
                    else:
                        yaf_param_map.setFloat("smartibl_blur", world.bg_smartibl_blur)
                    # 'with_caustic' and 'with_diffuse' settings gets checked in textureback.cc,
                    # so if IBL enabled when they are used...
                    yaf_param_map.setInt("ibl_samples", iblSamples)
                    yaf_param_map.setFloat("power", bgPower)
                    yaf_param_map.setFloat("rotation", world.bg_rotation)

        elif bg_type == 'Gradient':
            c = world.bg_horizon_color
            yaf_param_map.setColor("horizon_color", c[0], c[1], c[2])

            c = world.bg_zenith_color
            yaf_param_map.setColor("zenith_color", c[0], c[1], c[2])

            c = world.bg_horizon_ground_color
            yaf_param_map.setColor("horizon_ground_color", c[0], c[1], c[2])

            c = world.bg_zenith_ground_color
            yaf_param_map.setColor("zenith_ground_color", c[0], c[1], c[2])

            yaf_param_map.setFloat("power", bgPower)
            yaf_param_map.setBool("ibl", useIBL)
            yaf_param_map.setInt("ibl_samples", iblSamples)
            yaf_param_map.setString("type", "gradientback")

        elif bg_type == 'Sunsky1':
            f = world.bg_from
            yaf_param_map.setVector("from", f[0], f[1], f[2])
            yaf_param_map.setFloat("turbidity", world.bg_turbidity)
            yaf_param_map.setFloat("a_var", world.bg_a_var)
            yaf_param_map.setFloat("b_var", world.bg_b_var)
            yaf_param_map.setFloat("c_var", world.bg_c_var)
            yaf_param_map.setFloat("d_var", world.bg_d_var)
            yaf_param_map.setFloat("e_var", world.bg_e_var)
            yaf_param_map.setBool("add_sun", world.bg_add_sun)
            yaf_param_map.setFloat("sun_power", world.bg_sun_power)
            yaf_param_map.setBool("background_light", world.bg_background_light)
            yaf_param_map.setInt("light_samples", world.bg_light_samples)
            yaf_param_map.setFloat("power", world.bg_power)
            yaf_param_map.setString("type", "sunsky")
            yaf_param_map.setBool("cast_shadows_sun", world.bg_cast_shadows_sun)

        elif bg_type == "Sunsky2":
            f = world.bg_from
            yaf_param_map.setVector("from", f[0], f[1], f[2])
            yaf_param_map.setFloat("turbidity", world.bg_ds_turbidity)
            yaf_param_map.setFloat("altitude", world.bg_dsaltitude)
            yaf_param_map.setFloat("a_var", world.bg_a_var)
            yaf_param_map.setFloat("b_var", world.bg_b_var)
            yaf_param_map.setFloat("c_var", world.bg_c_var)
            yaf_param_map.setFloat("d_var", world.bg_d_var)
            yaf_param_map.setFloat("e_var", world.bg_e_var)
            yaf_param_map.setBool("add_sun", world.bg_add_sun)
            if world.bg_add_sun:
                yaf_param_map.setFloat("sun_power", world.bg_sun_power)
            yaf_param_map.setBool("background_light", world.bg_background_light)
            if world.bg_background_light:
                yaf_param_map.setFloat("power", world.bg_power)
            yaf_param_map.setInt("light_samples", world.bg_light_samples)
            yaf_param_map.setFloat("bright", world.bg_dsbright)
            yaf_param_map.setBool("night", world.bg_dsnight)
            yaf_param_map.setFloat("exposure", world.bg_exposure)
            yaf_param_map.setBool("clamp_rgb", world.bg_clamp_rgb)
            yaf_param_map.setBool("gamma_enc", world.bg_gamma_enc)
            yaf_param_map.setString("color_space", world.bg_color_space)
            yaf_param_map.setString("type", "darksky")
            yaf_param_map.setBool("cast_shadows_sun", world.bg_cast_shadows_sun)

        else:
            yaf_param_map.setColor("color", c[0], c[1], c[2])
            yaf_param_map.setBool("ibl", useIBL)
            yaf_param_map.setInt("ibl_samples", iblSamples)
            yaf_param_map.setFloat("power", bgPower)
            yaf_param_map.setString("type", "constant")
            
                    
        if world is not None:
            yaf_param_map.setBool("cast_shadows", world.bg_cast_shadows)
            yaf_param_map.setBool("with_caustic", world.bg_with_caustic)
            yaf_param_map.setBool("with_diffuse", world.bg_with_diffuse)
            
        yaf_scene.defineBackground(yaf_param_map)

        return True
