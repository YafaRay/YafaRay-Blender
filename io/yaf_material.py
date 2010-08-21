import bpy
import mathutils

def proj2int(val):
	if val ==   'NONE' : return 0
	elif val == 'X'    : return 1
	elif val == 'Y'    : return 2
	elif val == 'Z'    : return 3

class yafMaterial:
        def __init__(self, interface,mMap):
                self.yi          = interface
                self.materialMap = mMap
        
        def namehash(self,obj):
                # TODO: Better hashing using mat.__str__() ?
                nh = obj.name + "." + str(obj.__hash__())
                return nh

        def writeTexLayer(self, name, tex_in, ulayer, mtex, chanflag, dcol):
            if chanflag == 0:
                return False
            
            yi = self.yi
            yi.paramsPushList()
            yi.paramsSetString("element", "shader_node")
            yi.paramsSetString("type", "layer")
            yi.paramsSetString("name", name)
                
            yi.paramsSetString("input", tex_in) # SEE the defination later
            
            #mtex is an instance of MaterialTextureSlot class

            mode = 0
            if mtex.blend_type == 'MIX':
                mode = 0
            elif mtex.blend_type == 'ADD':
                mode = 1
            elif mtex.blend_type == 'MULTIPLY':
                mode = 2
            elif mtex.blend_type == 'SUBTRACT':
                mode = 3
            elif mtex.blend_type == 'SCREEN':
                mode = 4
            elif mtex.blend_type == 'DIVIDE':
                mode = 5
            elif mtex.blend_type == 'DIFFERENCE':
                mode = 6
            elif mtex.blend_type == 'DARKEN':
                mode = 7
            elif mtex.blend_type == 'LIGHTEN':
                mode = 8
            
            
            yi.paramsSetInt("mode", mode)
            yi.paramsSetBool("stencil", mtex.stencil)
            
            negative = chanflag < 0
            if mtex.negate:
                negative = not negative
            
            yi.paramsSetBool("negative", negative)
            yi.paramsSetBool("noRGB", mtex.rgb_to_intensity)
                
            yi.paramsSetColor("def_col", mtex.color[0], mtex.color[1], mtex.color[2])
            yi.paramsSetFloat("def_val", mtex.default_value)
            yi.paramsSetFloat("colfac", mtex.colorspec_factor) #colfac : Factor by which texture affects color. 
            yi.paramsSetFloat("valfac", mtex.hardness_factor) #Factor by which texture affects most variables (material and world only).
            
            
            tex = mtex.texture  # texture object instance
            # lots to do...
            isImage = ( tex.yaf_tex_type == 'IMAGE' )
            
            if (isImage or (tex.yaf_tex_type == 'VORONOI' and tex.coloring != 'INTENSITY') ):
                isColored=True
            else:
                isColored=False
            
            useAlpha = False
            yi.paramsSetBool("color_input", isColored)
            
            if isImage:
                useAlpha = (tex.use_alpha) and not(tex.calculate_alpha)
            
            yi.paramsSetBool("use_alpha", useAlpha)
             
               
            doCol = len(dcol) >= 3 #see defination of dcol later on, watch the remaining parts from now on.
            
            if ulayer == "":
                if doCol:
                    yi.paramsSetColor("upper_color", dcol[0],dcol[1],dcol[2])
                    yi.paramsSetFloat("upper_value", 0)
                else:
                    yi.paramsSetColor("upper_color", 0,0,0)
                    yi.paramsSetFloat("upper_value", dcol[0])
            else:
                yi.paramsSetString("upper_layer", ulayer)
                
            yi.paramsSetBool("do_color", doCol)
            yi.paramsSetBool("do_scalar", not doCol)
                
            return True


        def writeMappingNode(self, name, texname, mtex):
                yi = self.yi
                yi.paramsPushList()
                
                yi.paramsSetString("element", "shader_node")
                yi.paramsSetString("type", "texture_mapper")
                yi.paramsSetString("name", name)
                #yi.paramsSetString("texture", self.namehash(mtex.tex))
                yi.paramsSetString("texture", mtex.texture.name)
                
                #'UV'  'GLOBAL' 'ORCO' , 'WINDOW', 'NORMAL' 'REFLECTION' 'STICKY' 'STRESS' 'TANGENT'
                # texture coordinates, have to disable 'sticky' in Blender
                yi.paramsSetString("texco", "orco")
                if mtex.texture.yaf_texture_coordinates == 'UV'          :          yi.paramsSetString("texco", "uv")
                elif mtex.texture.yaf_texture_coordinates == 'GLOBAL'    :          yi.paramsSetString("texco", "global")
                elif mtex.texture.yaf_texture_coordinates == 'ORCO'      :          yi.paramsSetString("texco", "orco")
                elif mtex.texture.yaf_texture_coordinates == 'WINDOW'    :          yi.paramsSetString("texco", "window")
                elif mtex.texture.yaf_texture_coordinates == 'NORMAL'    :          yi.paramsSetString("texco", "normal")
                elif mtex.texture.yaf_texture_coordinates == 'REFLECTION':          yi.paramsSetString("texco", "reflect")
                elif mtex.texture.yaf_texture_coordinates == 'STICKY'    :          yi.paramsSetString("texco", "stick")
                elif mtex.texture.yaf_texture_coordinates == 'STRESS'    :          yi.paramsSetString("texco", "stress")
                elif mtex.texture.yaf_texture_coordinates == 'TANGENT'   :          yi.paramsSetString("texco", "tangent")
                
                elif mtex.texture.yaf_texture_coordinates == 'OBJECT'    :
                        
                        yi.paramsSetString("texco", "transformed")
                        
                        if mtex.object is not None:
                                
                                texmat = mtex.object.matrix_local.invert()
                                rtmatrix = yafrayinterface.new_floatArray(4*4)
                                
                                for x in range(4):
                                        for y in range(4):
                                                idx = (y + x * 4)
                                                yafrayinterface.floatArray_setitem(rtmatrix, idx, texmat[x][y])
                                
                                yi.paramsSetMemMatrix("transform", rtmatrix, True)
                                yafrayinterface.delete_floatArray(rtmatrix)
                
                yi.paramsSetInt("proj_x", proj2int(mtex.x_mapping) )
                yi.paramsSetInt("proj_y", proj2int(mtex.y_mapping) )
                yi.paramsSetInt("proj_z", proj2int(mtex.z_mapping) )
                
                if   mtex.mapping == 'FLAT'   : yi.paramsSetString("mapping", "plain")
                elif mtex.mapping == 'CUBE'   : yi.paramsSetString("mapping", "cube")
                elif mtex.mapping == 'TUBE'   : yi.paramsSetString("mapping", "tube")
                elif mtex.mapping == 'SPHERE' : yi.paramsSetString("mapping", "sphere")
                
                if mtex.map_normal: #|| mtex->maptoneg & MAP_NORM )
                        nf = mtex.normal_factor
                        yi.paramsSetFloat("bump_strength", nf)

        
        def writeGlassShader(self, mat, rough):
                
                #mat : is an instance of material                 
                yi = self.yi
                yi.paramsClearAll()
                
                if rough: # these properties are not created yet
                        yi.paramsSetString("type", "rough_glass")
                        yi.paramsSetFloat("exponent", mat.mat_exponent )
                        yi.paramsSetFloat("alpha", mat.mat_alpha )
                else:
                        yi.paramsSetString("type", "glass")
                        
                yi.paramsSetFloat("IOR", mat.mat_ior)
                filt_col = mat.mat_filter_color
                mir_col = mat.mat_mirror_color
                tfilt = mat.mat_transmit_filter
                abs_col = mat.mat_absorp_color

                yi.paramsSetColor("filter_color", filt_col[0], filt_col[1], filt_col[2])
                yi.paramsSetColor("mirror_color", mir_col[0], mir_col[1], mir_col[2])
                yi.paramsSetFloat("transmit_filter", tfilt)
                
                yi.paramsSetColor( "absorption", abs_col[0], abs_col[1], abs_col[2] )
                yi.paramsSetFloat("absorption_dist", mat.mat_absorp_distance)
                yi.paramsSetFloat("dispersion_power", mat.mat_dispersion_power)
                yi.paramsSetBool("fake_shadows", mat.mat_fake_shadows)

                mcolRoot = ''
                fcolRoot = ''
                bumpRoot = ''
                
                i=0
                used_textures = []
                for item in mat.texture_slots:
                        
                        if hasattr(item,'enabled') and (item.texture is not None) :
                                used_textures.append(item) # these are instances of materialTextureSlot
                                
                for mtex in used_textures:
                        
                        used = False
                        mappername = "map%x" %i

                        lname = "mircol_layer%x" % i
                        if self.writeTexLayer(lname, mappername, mcolRoot, mtex, mtex.map_mirror, mir_col):
                                used = True
                                mcolRoot = lname
                        lname = "filtcol_layer%x" % i
                        if self.writeTexLayer(lname, mappername, fcolRoot, mtex, mtex.map_mirror, filt_col):
                                used = True
                                fcolRoot = lname
                        lname = "bump_layer%x" % i
                        if self.writeTexLayer(lname, mappername, bumpRoot, mtex, mtex.map_normal, [0]):
                                used = True
                                bumpRoot = lname
                        if used:
                                self.writeMappingNode(mappername, mtex.texture.name , mtex)
                                i +=1
                
                yi.paramsEndList()
                if len(mcolRoot) > 0:	yi.paramsSetString("mirror_color_shader", mcolRoot)
                if len(fcolRoot) > 0:	yi.paramsSetString("filter_color_shader", fcolRoot)
                if len(bumpRoot) > 0:	yi.paramsSetString("bump_shader", bumpRoot)
                
                ymat = yi.createMaterial(self.namehash(mat))
                self.materialMap[mat] = ymat


        def writeGlossyShader(self, mat, coated): #mat : instance of material class
                yi = self.yi
                yi.paramsClearAll()
                
                if coated:
                        yi.paramsSetString("type", "coated_glossy")
                        yi.paramsSetFloat("IOR", mat.mat_ior)
                else:
                        yi.paramsSetString("type", "glossy")
                
                diffuse_color = mat.mat_diff_color
                #color = props["color"]
                color         = mat.mat_glossy_color
                
                #glossy_reflect = props["glossy_reflect"]

                # TODO: textures

                
                yi.paramsSetColor("diffuse_color", diffuse_color[0], diffuse_color[1], diffuse_color[2])
                yi.paramsSetColor("color", color[0],color[1], color[2])
                yi.paramsSetFloat("glossy_reflect", mat.mat_glossy_reflect)
                yi.paramsSetFloat("exponent", mat.mat_exponent)
                yi.paramsSetFloat("diffuse_reflect", mat.mat_diffuse_reflect)
                yi.paramsSetBool("as_diffuse", mat.mat_as_diffuse)
                
                
                yi.paramsSetBool("anisotropic", mat.mat_anisotropic)
                yi.paramsSetFloat("exp_u", mat.mat_exp_u )
                yi.paramsSetFloat("exp_v", mat.mat_exp_v )
                
                diffRoot = ''
                mcolRoot = ''
                glossRoot = ''
                glRefRoot = ''
                bumpRoot = ''
                
                i=0
                used_textures = []
                for item in mat.texture_slots:
                        if hasattr(item,'enabled') and (item.texture is not None) :
                                used_textures.append(item) # these are instances of materialTextureSlot
                
                for mtex in used_textures:
                        
                        used = False
                        mappername = "map%x" %i
                        
                        lname = "diff_layer%x" % i
                        if self.writeTexLayer(lname, mappername, diffRoot, mtex, mtex.map_colordiff, diffuse_color):
                                used = True
                                diffRoot = lname
                        lname = "gloss_layer%x" % i
                        if self.writeTexLayer(lname, mappername, glossRoot, mtex, mtex.map_colorspec, color):
                                used = True
                                glossRoot = lname
                        lname = "glossref_layer%x" % i
                        if self.writeTexLayer(lname, mappername, glRefRoot, mtex, mtex.map_specular, [mat.mat_glossy_reflect]):
                                used = True
                                glRefRoot = lname
                        lname = "bump_layer%x" % i
                        if self.writeTexLayer(lname, mappername, bumpRoot, mtex, mtex.map_normal, [0]):
                                used = True
                                bumpRoot = lname
                        if used:
                                self.writeMappingNode(mappername, mtex.texture.name, mtex)
                        i +=1
                
                yi.paramsEndList()
                if len(diffRoot)  > 0 :  yi.paramsSetString("diffuse_shader", diffRoot)
                if len(glossRoot) > 0 :  yi.paramsSetString("glossy_shader", glossRoot)
                if len(glRefRoot) > 0 :  yi.paramsSetString("glossy_reflect_shader", glRefRoot)
                if len(bumpRoot)  > 0 :  yi.paramsSetString("bump_shader", bumpRoot)
                
                if mat.mat_brdf_type == "Oren-Nayar":
                        yi.paramsSetString("diffuse_brdf", "oren_nayar")
                        yi.paramsSetFloat("sigma", mat.mat_sigma)
                
                ymat = yi.createMaterial(self.namehash(mat))
                self.materialMap[mat] = ymat

        
        def writeShinyDiffuseShader(self, mat):
                
                yi = self.yi
                yi.paramsClearAll()
                
                
                yi.paramsSetString("type", "shinydiffusemat")

                bCol = mat.mat_color
                mirCol = mat.mat_mirror_color
                bSpecr = mat.mat_specular_reflect #look at it later
                bTransp = mat.mat_transparency
                bTransl = mat.mat_translucency
                bTransmit = mat.mat_transmit_filter

                # TODO: all

                i=0
                used_textures = []
                for item in mat.texture_slots:
                        if hasattr(item,'enabled') and (item.texture is not None) :
                                used_textures.append(item)
                
                diffRoot = ''
                mcolRoot = ''
                transpRoot = ''
                translRoot = ''
                mirrorRoot = ''
                bumpRoot = ''



                for mtex in used_textures:
                        #if mtex == None: continue
                        #if mtex.tex == None: continue
                        if mtex.texture.yaf_tex_type == 'NONE':
                                continue
                        
                        used = False
                        mappername = "map%x" %i
                        
                        lname = "diff_layer%x" % i
                        if self.writeTexLayer(lname, mappername, diffRoot, mtex, mtex.map_colordiff, bCol):
                                used = True
                                diffRoot = lname
                        lname = "mircol_layer%x" % i
                        if self.writeTexLayer(lname, mappername, mcolRoot, mtex, mtex.map_mirror, mirCol):
                                used = True
                                mcolRoot = lname
                        lname = "transp_layer%x" % i
                        if self.writeTexLayer(lname, mappername, transpRoot, mtex, mtex.map_alpha, [bTransp]):
                                used = True
                                transpRoot = lname
                        lname = "translu_layer%x" % i
                        if self.writeTexLayer(lname, mappername, translRoot, mtex, mtex.map_translucency, [bTransl]):
                                used = True
                                translRoot = lname
                        lname = "mirr_layer%x" % i
                        if self.writeTexLayer(lname, mappername, mirrorRoot, mtex, mtex.map_raymir, [bSpecr]):
                                used = True
                                mirrorRoot = lname
                        lname = "bump_layer%x" % i
                        if self.writeTexLayer(lname, mappername, bumpRoot, mtex, mtex.map_normal, [0]):
                                used = True
                                bumpRoot = lname
                        if used:
                                self.writeMappingNode(mappername, mtex.texture.name, mtex)
                        i +=1
                
                yi.paramsEndList()
                if len(diffRoot) > 0:
                        yi.paramsSetString("diffuse_shader", diffRoot)
                if len(mcolRoot) > 0:
                        yi.paramsSetString("mirror_color_shader", mcolRoot)
                if len(transpRoot) > 0:
                        yi.paramsSetString("transparency_shader", transpRoot)
                if len(translRoot) > 0:
                        yi.paramsSetString("translucency_shader", translRoot)
                if len(mirrorRoot) > 0:
                        yi.paramsSetString("mirror_shader", mirrorRoot)
                if len(bumpRoot) > 0:
                        yi.paramsSetString("bump_shader", bumpRoot)
                
                yi.paramsSetColor("color", bCol[0], bCol[1], bCol[2])
                yi.paramsSetFloat("transparency", bTransp)
                yi.paramsSetFloat("translucency", bTransl)
                yi.paramsSetFloat("diffuse_reflect", mat.mat_diffuse_reflect)
                yi.paramsSetFloat("emit", mat.mat_emit)
                yi.paramsSetFloat("transmit_filter", bTransmit)
                
                yi.paramsSetFloat("specular_reflect", bSpecr)
                yi.paramsSetColor("mirror_color", mirCol[0], mirCol[1], mirCol[2])
                yi.paramsSetBool("fresnel_effect", mat.mat_fresnel_effect)
                yi.paramsSetFloat("IOR", mat.mat_ior)

                if mat.mat_brdf_type == "Oren-Nayar":
                        yi.paramsSetString("diffuse_brdf", "oren_nayar")
                        yi.paramsSetFloat("sigma", mat.mat_sigma)
                
                ymat = yi.createMaterial(self.namehash(mat))
                self.materialMap[mat] = ymat

        def writeBlendShader(self, mat):
                
                yi = self.yi
                yi.paramsClearAll()
                
                
                #yi.printInfo("Exporter: Blend material with: [" + props["material1"] + "] [" + props["material2"] + "]")
                yi.paramsSetString("type", "blend_mat")
                yi.paramsSetString("material1", self.namehash( bpy.data.materials[mat.mat_material_one] )  )
                yi.paramsSetString("material2", self.namehash( bpy.data.materials[mat.mat_material_two] )  )


                i=0
                
                diffRoot = ''
                used_textures = []
                for item in mat.texture_slots:
                        if hasattr(item, 'enabled') and (item.texture is not None) :
                                used_textures.append(item)


                for mtex in used_textures:
                        
                        if mtex.texture.yaf_tex_type == 'NONE':
                                continue

                        used = False
                        mappername = "map%x" %i
                        
                        lname = "diff_layer%x" % i
                        if self.writeTexLayer(lname, mappername, diffRoot, mtex, mtex.map_colordiff, [mat.mat_blend_value] ):
                                used = True
                                diffRoot = lname
                        if used:
                                self.writeMappingNode(mappername, mtex.texture.name, mtex)
                        i +=1

                yi.paramsEndList()
                if len(diffRoot) > 0:
                        yi.paramsSetString("mask", diffRoot)
                        
                yi.paramsSetFloat("blend_value", mat.mat_blend_value)
                ymat = yi.createMaterial(self.namehash(mat))
                self.materialMap[mat] = ymat



        def writeMatteShader(self, mat):
                yi = self.yi
                yi.paramsClearAll()
                yi.paramsSetString("type", "shadow_mat")
                ymat = yi.createMaterial(self.namehash(mat))
                self.materialMap[mat] = ymat

        def writeNullMat(self, mat):
                yi = self.yi
                yi.paramsClearAll()
                yi.paramsSetString("type", "null")
                ymat = yi.createMaterial(self.namehash(mat))
                self.materialMap[mat] = ymat

        def writeMaterial(self, mat):
                self.yi.printInfo("Exporter: Creating Material: \"" + self.namehash(mat) + "\"")
                if mat.name == "y_null":
                        self.writeNullMat(mat)
                elif mat.mat_type == "glass":
                        self.writeGlassShader(mat, False)
                elif mat.mat_type == "rough_glass":
                        self.writeGlassShader(mat, True)
                elif mat.mat_type == "glossy":
                        self.writeGlossyShader(mat, False)
                elif mat.mat_type == "coated_glossy":
                        self.writeGlossyShader(mat, True)
                elif mat.mat_type == "shinydiffusemat":
                        self.writeShinyDiffuseShader(mat)
                elif mat.mat_type == "blend":
                        self.writeBlendShader(mat)
                else:
                        self.writeNullMat(mat)