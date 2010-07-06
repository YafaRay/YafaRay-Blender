import bpy
from  math import *
#import mathutils
#import yafrayinterface

class yafWorld:
        def __init__(self, interface):
                self.yi = interface
                
        def exportWorld(self,scene):
                yi = self.yi

                #context = bpy.context
                #scene   = context.scene
                world   = scene.world
        

                bg_type = scene.bg_type
                print("INFO: Exporting World, type: " + bg_type)
                yi.paramsClearAll();
                
                if bg_type == 'Texture':
                    if world.active_texture is not None :
                        worldTex = world.active_texture
                        print("INFO World Texture, name: " + worldTex.name)
                    else :
                        worldTex = None
                        
                    if worldTex is not None :

                        if worldTex.type == 'IMAGE' and (worldTex.image is not None):
                            
                            yi.paramsSetString("type", "image")
                            yi.paramsSetString("filename", worldTex.image.filename )
                            # exposure_adjust not restricted to integer range anymore
                            yi.paramsSetFloat("exposure_adjust", worldTex.brightness/2)  #this portion is edited
                            
                            if worldTex.interpolation == True:
                                yi.paramsSetString("interpolate", "bilinear")
                            else:
                                yi.paramsSetString("interpolate", "none")
                            yi.createTexture("world_texture")
                                
                            # Export the actual background
                            texco = world.texture_slots[world.active_texture_index].texture_coordinates
                            
                            yi.paramsClearAll();
                            
                            if texco == 'ANGMAP':
                                yi.paramsSetString("mapping", "probe");
                            elif texco == 'SPHERE':
                                yi.paramsSetString("mapping", "sphere");
                                
                            yi.paramsSetString("type", "textureback");
                            yi.paramsSetString("texture", "world_texture");
                            yi.paramsSetBool("ibl", scene.bg_use_IBL)
                            yi.paramsSetBool("with_caustic", True) #this 2 lines are temporary
                            yi.paramsSetBool("with_diffuse", True)
                            yi.paramsSetInt("ibl_samples", scene.bg_IBL_samples)
                            yi.paramsSetFloat("power", scene.bg_power);
                            yi.paramsSetFloat("rotation", scene.bg_rotation)
                        
                elif bg_type == 'Gradient' :
                
                    c = world.horizon_color
                    print(str(c[0]) + ", " + str(c[1]) + ", " + str(c[2]))
                    yi.paramsSetColor("horizon_color", c[0], c[1], c[2])
                    
                    c = world.zenith_color
                    print(str(c[0]) + ", " + str(c[1]) + ", " + str(c[2]))
                    yi.paramsSetColor("zenith_color", c[0], c[1], c[2])
                    
                    c = world.ambient_color
                    print(str(c[0]) + ", " + str(c[1]) + ", " + str(c[2]))
                    yi.paramsSetColor("horizon_ground_color", c[0], c[1], c[2])
                    
                    c = scene.bg_zenith_ground_color
                    print(str(c[0]) + ", " + str(c[1]) + ", " + str(c[2]))
                    yi.paramsSetColor("zenith_ground_color", c[0], c[1], c[2])
                    
                    yi.paramsSetFloat("power", scene.bg_power)
                    yi.paramsSetBool("ibl", scene.bg_use_IBL)
                    yi.paramsSetInt("ibl_samples", scene.bg_IBL_samples)
                    yi.paramsSetString("type", "gradientback")

                elif bg_type == 'Sunsky' :
                        
                    f = scene.bg_from
                    yi.paramsSetPoint("from", f[0], f[1], f[2])
                    
                    yi.paramsSetFloat("turbidity", scene.bg_turbidity)
                    
                    yi.paramsSetFloat("a_var", scene.bg_a_var)
                    yi.paramsSetFloat("b_var", scene.bg_b_var)
                    yi.paramsSetFloat("c_var", scene.bg_c_var)
                    yi.paramsSetFloat("d_var", scene.bg_d_var)
                    yi.paramsSetFloat("e_var", scene.bg_e_var)
                    
                    yi.paramsSetBool("add_sun", scene.bg_add_sun)
                    yi.paramsSetFloat("sun_power", scene.bg_sun_power)
                    yi.paramsSetBool("background_light", scene.bg_background_light)
                    yi.paramsSetInt("light_samples", scene.bg_light_samples)
                    yi.paramsSetFloat("power", scene.bg_power)
                    yi.paramsSetString("type", "sunsky")
                
                elif bg_type == "DarkTide's SunSky" :
                    
                    f = scene.bg_from
                    yi.paramsSetPoint("from", f[0], f[1], f[2])
                    
                    yi.paramsSetFloat("turbidity", scene.bg_turbidity)
                    yi.paramsSetFloat("altitude", scene.bg_dsaltitude)
                    
                    yi.paramsSetFloat("a_var", scene.bg_a_var)
                    yi.paramsSetFloat("b_var", scene.bg_b_var)
                    yi.paramsSetFloat("c_var", scene.bg_c_var)
                    yi.paramsSetFloat("d_var", scene.bg_d_var)
                    yi.paramsSetFloat("e_var", scene.bg_e_var)
                    
                    #yi.paramsSetBool("clamp_rgb", renderprops["clamp_rgb"])
                    yi.paramsSetBool("add_sun", scene.bg_add_sun)
                    yi.paramsSetFloat("sun_power", scene.bg_sun_power)
                    yi.paramsSetBool("background_light", scene.bg_background_light)
                    yi.paramsSetBool("with_caustic", True)
                    yi.paramsSetBool("with_diffuse", True)
                    yi.paramsSetInt("light_samples", scene.bg_light_samples)
                    yi.paramsSetFloat("power", scene.bg_power)
                    yi.paramsSetFloat("bright", scene.bg_dsbright)
                    yi.paramsSetBool("night", scene.bg_dsnight)
                    yi.paramsSetString("type", "darksky")
                
                else:
                    c = world.horizon_color
                    yi.paramsSetColor("color", c[0], c[1], c[2])
                    print(str(c[0]) + " " + str(c[1]) + " " + str(c[2]))
                    yi.paramsSetBool("ibl", 0)
                    yi.paramsSetInt("ibl_samples", 16)
                    yi.paramsSetFloat("power", scene.bg_power)
                    yi.paramsSetString("type", "constant");

                yi.createBackground("world_background")
                return True