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

import bpy
import yafrayinterface


def proj2int(val):
    if val == 'NONE':
        return 0
    elif val == 'X':
        return 1
    elif val == 'Y':
        return 2
    elif val == 'Z':
        return 3


class yafMaterial:
    def __init__(self, interface, mMap, texMap):
        self.yi = interface
        self.materialMap = mMap
        self.textureMap = texMap

    def namehash(self, obj):
        nh = obj.name + "-" + str(obj.__hash__())
        return nh

    def getUsedTextures(self, material):
        used_textures = []
        for tex_slot in material.texture_slots:
            if tex_slot and tex_slot.use and tex_slot.texture:
                used_textures.append(tex_slot)

        return used_textures

    def writeTexLayer(self, name, tex_in, ulayer, mtex, chanflag, dcol, factor):
        if mtex.name not in self.textureMap:
            return False
        if not chanflag:
            return False

        yi = self.yi
        yi.paramsPushList()
        yi.paramsSetString("element", "shader_node")
        yi.paramsSetString("type", "layer")
        yi.paramsSetString("name", name)

        yi.paramsSetString("input", tex_in)  # SEE the defination later

        #mtex is an instance of MaterialTextureSlot class

        switchBlendMode = {
            'MIX': 0,
            'ADD': 1,
            'MULTIPLY': 2,
            'SUBTRACT': 3,
            'SCREEN': 4,
            'DIVIDE': 5,
            'DIFFERENCE': 6,
            'DARKEN': 7,
            'LIGHTEN': 8,
        }

        mode = switchBlendMode.get(mtex.blend_type, 0)  # set texture blend mode, if not a supported mode then set it to 'MIX'
        yi.paramsSetInt("mode", mode)
        yi.paramsSetBool("stencil", mtex.use_stencil)

        negative = mtex.invert
        yi.paramsSetBool("negative", negative)

        if factor < 0:  # added a check for negative values
            factor = factor * -1
            yi.paramsSetBool("negative", True)

        # "hack", scalar maps should always convert the RGB intensity to scalar
        # not clear why without this and noRGB == False, maps on scalar values seem to be "white" everywhere   <-- ???
        noRGB = mtex.use_rgb_to_intensity

        # if len(dcol) == 1:    # disabled this 'hack' again, does not work with procedurals and alpha mapping (e.g. PNG image with 'use alpha')
        #     noRGB = True      # user should decide if rgb_to_intensity will be used or not...

        yi.paramsSetBool("noRGB", noRGB)

        yi.paramsSetColor("def_col", mtex.color[0], mtex.color[1], mtex.color[2])
        yi.paramsSetFloat("def_val", mtex.default_value)

        tex = mtex.texture  # texture object instance
        # lots to do...

        isImage = tex.yaf_tex_type == 'IMAGE'

        if (isImage or (tex.yaf_tex_type == 'VORONOI' and tex.color_mode not in 'INTENSITY')):
            isColored = True
        else:
            isColored = False

        useAlpha = False
        yi.paramsSetBool("color_input", isColored)

        if isImage:
            useAlpha = (tex.yaf_use_alpha) and not(tex.use_calculate_alpha)

        yi.paramsSetBool("use_alpha", useAlpha)

        do_color = len(dcol) >= 3  # see defination of dcol later on, watch the remaining parts from now on.

        if ulayer == "":
            if do_color:
                yi.paramsSetColor("upper_color", dcol[0], dcol[1], dcol[2])
                yi.paramsSetFloat("upper_value", 0)
            else:
                yi.paramsSetColor("upper_color", 0, 0, 0)
                yi.paramsSetFloat("upper_value", dcol[0])
        else:
            yi.paramsSetString("upper_layer", ulayer)

        if do_color:
            yi.paramsSetFloat("colfac", factor)
        else:
            yi.paramsSetFloat("valfac", factor)

        yi.paramsSetBool("do_color", do_color)
        yi.paramsSetBool("do_scalar", not do_color)

        return True

    def writeMappingNode(self, name, texname, mtex):
        yi = self.yi
        yi.paramsPushList()

        yi.paramsSetString("element", "shader_node")
        yi.paramsSetString("type", "texture_mapper")
        yi.paramsSetString("name", name)
        yi.paramsSetString("texture", texname)

        switchTexCoords = {
            'UV': 'uv',
            'GLOBAL': 'global',
            'ORCO': 'orco',
            'WINDOW': 'window',
            'NORMAL': 'normal',
            'REFLECTION': 'reflect',
            'STICKY': 'stick',
            'STRESS': 'stress',
            'TANGENT': 'tangent',
            'OBJECT': 'transformed',
        }

        texco = switchTexCoords.get(mtex.texture_coords, 'orco')  # get texture coords, default is 'orco'
        yi.paramsSetString("texco", texco)

        if mtex.object:
            texmat = mtex.object.matrix_world.inverted()
            rtmatrix = yafrayinterface.new_floatArray(4 * 4)

            for x in range(4):
                for y in range(4):
                    idx = (y + x * 4)
                    yafrayinterface.floatArray_setitem(rtmatrix, idx, texmat[x][y])
            yi.paramsSetMemMatrix("transform", rtmatrix, False)
            yafrayinterface.delete_floatArray(rtmatrix)

        yi.paramsSetInt("proj_x", proj2int(mtex.mapping_x))
        yi.paramsSetInt("proj_y", proj2int(mtex.mapping_y))
        yi.paramsSetInt("proj_z", proj2int(mtex.mapping_z))

        switchMappingCoords = {
            'FLAT': 'plain',
            'CUBE': 'cube',
            'TUBE': 'tube',
            'SPHERE': 'sphere',
        }
        mappingCoords = switchMappingCoords.get(mtex.mapping, 'plain')
        yi.paramsSetString("mapping", mappingCoords)

        if self.preview and bpy.data.scenes[0].yafaray.preview.enable:
            yi.paramsSetPoint("scale", mtex.scale[0]*bpy.data.scenes[0].yafaray.preview.textureScale[0], mtex.scale[1]*bpy.data.scenes[0].yafaray.preview.textureScale[1], mtex.scale[2])
            yi.paramsSetPoint("offset", mtex.offset[0]+bpy.data.scenes[0].yafaray.preview.textureOffset[0], mtex.offset[1]+bpy.data.scenes[0].yafaray.preview.textureOffset[1], mtex.offset[2])
        else:
            yi.paramsSetPoint("scale", mtex.scale[0], mtex.scale[1], mtex.scale[2])
            yi.paramsSetPoint("offset", mtex.offset[0], mtex.offset[1], mtex.offset[2])

        if mtex.use_map_normal:  # || mtex->maptoneg & MAP_NORM )
            # scale up the normal factor, it resembles
            # blender a bit more
            nf = mtex.normal_factor * 2
            yi.paramsSetFloat("bump_strength", nf)

    def writeGlassShader(self, mat, scene, rough):

        # mat : is an instance of material
        yi = self.yi
        yi.paramsClearAll()

        yi.paramsSetInt("mat_pass_index", mat.pass_index)

        if rough:  # create bool property "rough"
            yi.paramsSetString("type", "rough_glass")
            yi.paramsSetFloat("alpha", mat.refr_roughness)  # added refraction roughness for roughglass material
        else:
            yi.paramsSetString("type", "glass")

        yi.paramsSetFloat("IOR", mat.IOR_refraction)  # added IOR for refraction
        if scene.gs_clay_render and not mat.clay_exclude:
            filt_col = (1.0, 1.0, 1.0)
            abs_col = (1.0, 1.0, 1.0)
        else:
            filt_col = mat.filter_color
            abs_col = mat.absorption
        mir_col = mat.glass_mir_col
        tfilt = mat.glass_transmit

        yi.paramsSetColor("filter_color", filt_col[0], filt_col[1], filt_col[2])
        yi.paramsSetColor("mirror_color", mir_col[0], mir_col[1], mir_col[2])
        yi.paramsSetFloat("transmit_filter", tfilt)

        yi.paramsSetColor("absorption", abs_col[0], abs_col[1], abs_col[2])
        yi.paramsSetFloat("absorption_dist", mat.absorption_dist)
        yi.paramsSetFloat("dispersion_power", mat.dispersion_power)
        yi.paramsSetBool("fake_shadows", mat.fake_shadows)
        yi.paramsSetString("visibility", mat.visibility)
        yi.paramsSetBool("receive_shadows", mat.receive_shadows)

        mcolRoot = ''
        # fcolRoot = '' /* UNUSED */
        bumpRoot = ''
        filterColorRoot = ''
        IORRoot = ''
        roughnessRoot = ''

        i = 0
        used_textures = self.getUsedTextures(mat)

        for mtex in used_textures:
            used = False
            mappername = "map%x" % i

            lname = "mircol_layer%x" % i
            if self.writeTexLayer(lname, mappername, mcolRoot, mtex, mtex.use_map_mirror, mir_col, mtex.mirror_factor):
                used = True
                mcolRoot = lname
            lname = "bump_layer%x" % i
            if self.writeTexLayer(lname, mappername, bumpRoot, mtex, mtex.use_map_normal, [0], mtex.normal_factor):
                used = True
                bumpRoot = lname
            lname = "filter_color_layer%x" % i
            if self.writeTexLayer(lname, mappername, filterColorRoot, mtex, mtex.use_map_color_reflection, filt_col, mtex.reflection_color_factor):
                used = True
                filterColorRoot = lname
            lname = "IOR_layer%x" % i
            if self.writeTexLayer(lname, mappername, IORRoot, mtex, mtex.use_map_warp, [0], mtex.warp_factor):
                used = True
                IORRoot = lname
            lname = "roughness_layer%x" % i
            if self.writeTexLayer(lname, mappername, roughnessRoot, mtex, mtex.use_map_hardness, [0], mtex.hardness_factor):
                used = True
                roughnessRoot = lname                
            if used:
                self.writeMappingNode(mappername, mtex.texture.name, mtex)
                i += 1

        yi.paramsEndList()
        if len(mcolRoot) > 0:
            yi.paramsSetString("mirror_color_shader", mcolRoot)
        if len(bumpRoot) > 0:
            yi.paramsSetString("bump_shader", bumpRoot)
        if len(filterColorRoot) > 0:
            yi.paramsSetString("filter_color_shader", filterColorRoot)
        if len(IORRoot) > 0:
            yi.paramsSetString("IOR_shader", IORRoot) 
        if len(roughnessRoot) > 0:
            yi.paramsSetString("roughness_shader", roughnessRoot)   
        return yi.createMaterial(self.namehash(mat))

    def writeGlossyShader(self, mat, scene, coated):  # mat : instance of material class
        yi = self.yi
        yi.paramsClearAll()

        yi.paramsSetInt("mat_pass_index", mat.pass_index)

        if coated:  # create bool property
            yi.paramsSetString("type", "coated_glossy")
            yi.paramsSetFloat("IOR", mat.IOR_reflection)  # IOR for reflection
            mir_col = mat.coat_mir_col  # added mirror color for coated glossy
            yi.paramsSetColor("mirror_color", mir_col[0], mir_col[1], mir_col[2])
        else:
            yi.paramsSetString("type", "glossy")
            mir_col = mat.diffuse_color

        diffuse_color = mat.diffuse_color
        bSpecr = mat.specular_reflect
        color = mat.glossy_color

        yi.paramsSetColor("diffuse_color", diffuse_color[0], diffuse_color[1], diffuse_color[2])
        yi.paramsSetColor("color", color[0], color[1], color[2])
        yi.paramsSetFloat("glossy_reflect", mat.glossy_reflect)
        yi.paramsSetFloat("exponent", mat.exponent)
        yi.paramsSetFloat("diffuse_reflect", mat.diffuse_reflect)
        yi.paramsSetBool("as_diffuse", mat.as_diffuse)
        yi.paramsSetBool("anisotropic", mat.anisotropic)
        yi.paramsSetFloat("exp_u", mat.exp_u)
        yi.paramsSetFloat("exp_v", mat.exp_v)
        yi.paramsSetFloat("specular_reflect", bSpecr)
        yi.paramsSetString("visibility", mat.visibility)
        yi.paramsSetBool("receive_shadows", mat.receive_shadows)

        diffRoot = ''
        # mcolRoot = ''  /* UNUSED */
        glossRoot = ''
        glRefRoot = ''
        bumpRoot = ''
        sigmaOrenRoot = ''
        exponentRoot = ''
        IORRoot = ''
        diffReflectRoot = ''
        mirrorRoot = ''
        mcolRoot = ''

        i = 0
        used_textures = self.getUsedTextures(mat)

        for mtex in used_textures:
            used = False
            mappername = "map%x" % i

            lname = "diff_layer%x" % i
            if self.writeTexLayer(lname, mappername, diffRoot, mtex, mtex.use_map_color_diffuse, diffuse_color, mtex.diffuse_color_factor):
                used = True
                diffRoot = lname
            lname = "gloss_layer%x" % i
            if self.writeTexLayer(lname, mappername, glossRoot, mtex, mtex.use_map_color_spec, color, mtex.specular_color_factor):
                used = True
                glossRoot = lname
            lname = "glossref_layer%x" % i
            if self.writeTexLayer(lname, mappername, glRefRoot, mtex, mtex.use_map_specular, [mat.glossy_reflect], mtex.specular_factor):
                used = True
                glRefRoot = lname
            lname = "bump_layer%x" % i
            if self.writeTexLayer(lname, mappername, bumpRoot, mtex, mtex.use_map_normal, [0], mtex.normal_factor):
                used = True
                bumpRoot = lname
            lname = "sigma_oren_layer%x" % i
            if self.writeTexLayer(lname, mappername, sigmaOrenRoot, mtex, mtex.use_map_hardness, [0], mtex.hardness_factor):
                used = True
                sigmaOrenRoot = lname                
            lname = "exponent_layer%x" % i
            if self.writeTexLayer(lname, mappername, exponentRoot, mtex, mtex.use_map_ambient, [0], mtex.ambient_factor):
                used = True
                exponentRoot = lname
            lname = "IOR_layer%x" % i
            if self.writeTexLayer(lname, mappername, IORRoot, mtex, mtex.use_map_warp, [0], mtex.warp_factor):
                used = True
                IORRoot = lname
            lname = "diff_refl_layer%x" % i
            if self.writeTexLayer(lname, mappername, diffReflectRoot, mtex, mtex.use_map_diffuse, [0], mtex.diffuse_factor):
                used = True
                diffReflectRoot = lname
            lname = "mircol_layer%x" % i
            if self.writeTexLayer(lname, mappername, mcolRoot, mtex, mtex.use_map_mirror, mir_col, mtex.mirror_factor):
                used = True
                mcolRoot = lname
            lname = "mirr_layer%x" % i
            if self.writeTexLayer(lname, mappername, mirrorRoot, mtex, mtex.use_map_raymir, [bSpecr], mtex.raymir_factor):
                used = True
                mirrorRoot = lname

                
            if used:
                self.writeMappingNode(mappername, mtex.texture.name, mtex)
            i += 1

        yi.paramsEndList()
        if len(diffRoot) > 0:
            yi.paramsSetString("diffuse_shader", diffRoot)
        if len(glossRoot) > 0:
            yi.paramsSetString("glossy_shader", glossRoot)
        if len(glRefRoot) > 0:
            yi.paramsSetString("glossy_reflect_shader", glRefRoot)
        if len(bumpRoot) > 0:
            yi.paramsSetString("bump_shader", bumpRoot)
        if len(sigmaOrenRoot) > 0:
            yi.paramsSetString("sigma_oren_shader", sigmaOrenRoot)     
        if len(exponentRoot) > 0:
            yi.paramsSetString("exponent_shader", exponentRoot) 
        if len(IORRoot) > 0:
            yi.paramsSetString("IOR_shader", IORRoot) 
        if len(diffReflectRoot) > 0:
            yi.paramsSetString("diffuse_refl_shader", diffReflectRoot)       
        if len(mcolRoot) > 0:
            yi.paramsSetString("mirror_color_shader", mcolRoot)
        if len(mirrorRoot) > 0:
            yi.paramsSetString("mirror_shader", mirrorRoot)
                               
        if mat.brdf_type == "oren-nayar":  # oren-nayar fix for glossy
            yi.paramsSetString("diffuse_brdf", "Oren-Nayar")
            yi.paramsSetFloat("sigma", mat.sigma)

        return yi.createMaterial(self.namehash(mat))


    def writeShinyDiffuseShader(self, mat, scene):
        yi = self.yi
        yi.paramsClearAll()

        yi.paramsSetInt("mat_pass_index", mat.pass_index)

        yi.paramsSetString("type", "shinydiffusemat")

        bCol = mat.diffuse_color
        mirCol = mat.mirror_color
        bSpecr = mat.specular_reflect
        bDiffRefl = mat.diffuse_reflect
        bTransp = mat.transparency
        bTransl = mat.translucency
        bTransmit = mat.transmit_filter
        bEmit = mat.emit

        if scene.gs_clay_render and not mat.clay_exclude:
            bCol = scene.gs_clay_col
            bSpecr = 0.0
            bEmit = 0.0
            bDiffRefl = 1.0
            if not scene.gs_clay_render_keep_transparency:
                bTransp = 0.0
                bTransl = 0.0

        if self.preview:
            if mat.name.startswith("checker"):
                bEmit = 2.50

        i = 0
        used_textures = self.getUsedTextures(mat)

        diffRoot = ''
        mcolRoot = ''
        transpRoot = ''
        translRoot = ''
        mirrorRoot = ''
        bumpRoot = ''
        sigmaOrenRoot = ''
        diffReflectRoot = ''
        IORRoot = ''

        for mtex in used_textures:
            if not mtex.texture:
                continue
            used = False
            mappername = "map%x" % i

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "diff_layer%x" % i
                if self.writeTexLayer(lname, mappername, diffRoot, mtex, mtex.use_map_color_diffuse, bCol, mtex.diffuse_color_factor):
                    used = True
                    diffRoot = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "mircol_layer%x" % i
                if self.writeTexLayer(lname, mappername, mcolRoot, mtex, mtex.use_map_mirror, mirCol, mtex.mirror_factor):
                    used = True
                    mcolRoot = lname

            if mat.clay_exclude or scene.gs_clay_render_keep_transparency or not scene.gs_clay_render:
                lname = "transp_layer%x" % i
                if self.writeTexLayer(lname, mappername, transpRoot, mtex, mtex.use_map_alpha, [bTransp], mtex.alpha_factor):
                    used = True
                    transpRoot = lname

            if mat.clay_exclude or scene.gs_clay_render_keep_transparency or not scene.gs_clay_render:
                lname = "translu_layer%x" % i
                if self.writeTexLayer(lname, mappername, translRoot, mtex, mtex.use_map_translucency, [bTransl], mtex.translucency_factor):
                    used = True
                    translRoot = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "mirr_layer%x" % i
                if self.writeTexLayer(lname, mappername, mirrorRoot, mtex, mtex.use_map_raymir, [bSpecr], mtex.raymir_factor):
                    used = True
                    mirrorRoot = lname

            if mat.clay_exclude or scene.gs_clay_render_keep_normals or not scene.gs_clay_render:
                lname = "bump_layer%x" % i
                if self.writeTexLayer(lname, mappername, bumpRoot, mtex, mtex.use_map_normal, [0], mtex.normal_factor):
                    used = True
                    bumpRoot = lname

            if mat.clay_exclude or scene.gs_clay_render_keep_normals or not scene.gs_clay_render:
                lname = "sigma_oren_layer%x" % i
                if self.writeTexLayer(lname, mappername, sigmaOrenRoot, mtex, mtex.use_map_hardness, [0], mtex.hardness_factor):
                    used = True
                    sigmaOrenRoot = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "diff_refl_layer%x" % i
                if self.writeTexLayer(lname, mappername, diffReflectRoot, mtex, mtex.use_map_diffuse, [0], mtex.diffuse_factor):
                    used = True
                    diffReflectRoot = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "IOR_layer%x" % i
                if self.writeTexLayer(lname, mappername, IORRoot, mtex, mtex.use_map_warp, [0], mtex.warp_factor):
                    used = True
                    IORRoot = lname

            if used:
                self.writeMappingNode(mappername, mtex.texture.name, mtex)
            i += 1

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
        if len(sigmaOrenRoot) > 0:
            yi.paramsSetString("sigma_oren_shader", sigmaOrenRoot)        
        if len(diffReflectRoot) > 0:
            yi.paramsSetString("diffuse_refl_shader", diffReflectRoot)             
        if len(IORRoot) > 0:
            yi.paramsSetString("IOR_shader", IORRoot) 

        yi.paramsSetColor("color", bCol[0], bCol[1], bCol[2])
        yi.paramsSetFloat("transparency", bTransp)
        yi.paramsSetFloat("translucency", bTransl)
        yi.paramsSetFloat("diffuse_reflect", bDiffRefl)
        yi.paramsSetFloat("emit", bEmit)
        yi.paramsSetFloat("transmit_filter", bTransmit)

        yi.paramsSetFloat("specular_reflect", bSpecr)
        yi.paramsSetColor("mirror_color", mirCol[0], mirCol[1], mirCol[2])
        yi.paramsSetBool("fresnel_effect", mat.fresnel_effect)
        yi.paramsSetFloat("IOR", mat.IOR_reflection)  # added IOR for reflection
        yi.paramsSetString("visibility", mat.visibility)
        yi.paramsSetBool("receive_shadows", mat.receive_shadows)

        if scene.gs_clay_render and not mat.clay_exclude:
             if scene.gs_clay_oren_nayar:
                 yi.paramsSetString("diffuse_brdf", "oren_nayar")
                 yi.paramsSetFloat("sigma", scene.gs_clay_sigma)
        elif mat.brdf_type == "oren-nayar":  # oren-nayar fix for shinydiffuse
            yi.paramsSetString("diffuse_brdf", "oren_nayar")
            yi.paramsSetFloat("sigma", mat.sigma)

        return yi.createMaterial(self.namehash(mat))

    def writeBlendShader(self, mat, scene):
        yi = self.yi
        yi.paramsClearAll()

        yi.printInfo("Exporter: Blend material with: [" + mat.material1name + "] [" + mat.material2name + "]")
        yi.paramsSetString("type", "blend_mat")
        yi.paramsSetString("material1", self.namehash(bpy.data.materials[mat.material1name]))
        yi.paramsSetString("material2", self.namehash(bpy.data.materials[mat.material2name]))

        i = 0

        diffRoot = ''
        used_textures = self.getUsedTextures(mat)

        for mtex in used_textures:
            if mtex.texture.type == 'NONE':
                continue

            used = False
            mappername = "map%x" % i

            lname = "diff_layer%x" % i
            if self.writeTexLayer(lname, mappername, diffRoot, mtex, mtex.use_map_diffuse, [0], mtex.diffuse_factor):
                used = True
                diffRoot = lname
            if used:
                self.writeMappingNode(mappername, mtex.texture.name, mtex)
            i += 1

        yi.paramsEndList()

        # if we have a blending map, disable the blend_value
        if len(diffRoot) > 0:
            yi.paramsSetString("mask", diffRoot)
            yi.paramsSetFloat("blend_value", 0)
        else:
            yi.paramsSetFloat("blend_value", mat.blend_value)

        yi.paramsSetString("visibility", mat.visibility)
        yi.paramsSetBool("receive_shadows", mat.receive_shadows)

        return yi.createMaterial(self.namehash(mat))

    def writeMatteShader(self, mat, scene):
        yi = self.yi
        yi.paramsClearAll()
        yi.paramsSetString("type", "shadow_mat")
        return yi.createMaterial(self.namehash(mat))

    def writeNullMat(self, mat, scene):
        yi = self.yi
        yi.paramsClearAll()
        yi.paramsSetString("type", "null")
        return yi.createMaterial(self.namehash(mat))

    def writeMaterial(self, mat, scene, preview=False):
        self.preview = preview
        self.yi.printInfo("Exporter: Creating Material: \"" + self.namehash(mat) + "\"")
        ymat = None
        if mat.name == "y_null":
            ymat = self.writeNullMat(mat, scene)
        elif scene.gs_clay_render and not mat.clay_exclude and not (scene.gs_clay_render_keep_transparency and mat.mat_type == "glass"):
            ymat = self.writeShinyDiffuseShader(mat, scene)
        elif mat.mat_type == "glass":
            ymat = self.writeGlassShader(mat, scene, False)
        elif mat.mat_type == "rough_glass":
            ymat = self.writeGlassShader(mat, scene, True)
        elif mat.mat_type == "glossy":
            ymat = self.writeGlossyShader(mat, scene, False)
        elif mat.mat_type == "coated_glossy":
            ymat = self.writeGlossyShader(mat, scene, True)
        elif mat.mat_type == "shinydiffusemat":
            ymat = self.writeShinyDiffuseShader(mat, scene)
        elif mat.mat_type == "blend":
            ymat = self.writeBlendShader(mat, scene)   #FIXME: in the new Clay render two limitations:
                #We cannot yet keep transparency in Blend objects. If that's needed to test a scene, better to exclude that particular material from the Clay
                #We cannot exclude just the blended material from the Clay render, the individual materials that are used to make the blend also have to be excluded
        else:
            ymat = self.writeNullMat(mat, scene)

        self.materialMap[mat] = ymat
