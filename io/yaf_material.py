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
import libyafaray4_bindings


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
    def __init__(self, scene, logger, texMap):
        self.yaf_scene = scene
        self.logger = logger
        self.textureMap = texMap

    def getUsedTextures(self, material):
        used_textures = []
        if bpy.app.version >= (2, 80, 0):
            if material.node_tree and False:
                for node in material.node_tree.nodes:
                    pprint(getmembers(node))
                    if node.type.startswith("TEX_IMAGE"):   # FIXME BLENDER 2.80-3.00 TEX_ but later getting .texture attribute does not work
                        used_textures.append(node)
        else:
            for tex_slot in material.texture_slots:
                if tex_slot and tex_slot.use and tex_slot.texture:
                    used_textures.append(tex_slot)

        return used_textures

    def writeTexLayer(self, param_map_list, name, tex_in, ulayer, mtex, chanflag, dcol, factor):
        if mtex.name not in self.textureMap:
            return False
        if not chanflag:
            return False

        param_map = libyafaray4_bindings.ParamMap()
        param_map.setString("type", "layer")
        param_map.setString("name", name)
        param_map.setString("input", tex_in)  # SEE the defination later

        #mtex is an instance of MaterialTextureSlot class

        switchBlendMode = {
            'MIX': "mix",
            'ADD': "add",
            'MULTIPLY': "multiply",
            'SUBTRACT': "subtract",
            'SCREEN': "screen",
            'DIVIDE': "divide",
            'DIFFERENCE': "difference",
            'DARKEN': "darken",
            'LIGHTEN': "lighten",
        }

        mode = switchBlendMode.get(mtex.blend_type, 'MIX')  # set texture blend mode, if not a supported mode then set it to 'MIX'
        param_map.setString("blend_mode", mode)
        param_map.setBool("stencil", mtex.use_stencil)

        negative = mtex.invert
        param_map.setBool("negative", negative)

        if factor < 0:  # added a check for negative values
            factor = factor * -1
            param_map.setBool("negative", True)

        # "hack", scalar maps should always convert the RGB intensity to scalar
        # not clear why without this and noRGB == False, maps on scalar values seem to be "white" everywhere   <-- ???
        noRGB = mtex.use_rgb_to_intensity

        # if len(dcol) == 1:    # disabled this 'hack' again, does not work with procedurals and alpha mapping (e.g. PNG image with 'use alpha')
        #     noRGB = True      # user should decide if rgb_to_intensity will be used or not...

        param_map.setBool("noRGB", noRGB)

        param_map.setColor("def_col", mtex.color[0], mtex.color[1], mtex.color[2])
        param_map.setFloat("def_val", mtex.default_value)

        tex = mtex.texture  # texture object instance
        # lots to do...

        isImage = tex.yaf_tex_type == 'IMAGE'

        if (isImage or tex.use_color_ramp or (tex.yaf_tex_type == 'VORONOI' and tex.color_mode not in 'INTENSITY')):
            isColored = True
        else:
            isColored = False

        useAlpha = False
        param_map.setBool("color_input", isColored)

        if isImage:
            useAlpha = (tex.yaf_use_alpha) and not(tex.use_calculate_alpha)

        param_map.setBool("use_alpha", useAlpha)

        do_color = len(dcol) >= 3  # see defination of dcol later on, watch the remaining parts from now on.

        if ulayer == "":
            if do_color:
                param_map.setColor("upper_color", dcol[0], dcol[1], dcol[2])
                param_map.setFloat("upper_value", 0)
            else:
                param_map.setColor("upper_color", 0, 0, 0)
                param_map.setFloat("upper_value", dcol[0])
        else:
            param_map.setString("upper_layer", ulayer)

        if do_color:
            param_map.setFloat("colfac", factor)
        else:
            param_map.setFloat("valfac", factor)

        param_map.setBool("do_color", do_color)
        param_map.setBool("do_scalar", not do_color)

        param_map_list.addParamMap(param_map)
        return True

    def writeMappingNode(self, param_map_list, name, texname, mtex):

        param_map = libyafaray4_bindings.ParamMap()

        param_map.setString("type", "texture_mapper")
        param_map.setString("name", name)
        param_map.setString("texture", texname)

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
        param_map.setString("texco", texco)

        if mtex.object:
            texmat = mtex.object.matrix_world.inverted()
            param_map.setMatrix("transform", texmat[0][0], texmat[0][1], texmat[0][2], texmat[0][3], texmat[1][0], texmat[1][1], texmat[1][2], texmat[1][3], texmat[2][0], texmat[2][1], texmat[2][2], texmat[2][3], texmat[3][0], texmat[3][1], texmat[3][2], texmat[3][3], False)

        param_map.setInt("proj_x", proj2int(mtex.mapping_x))
        param_map.setInt("proj_y", proj2int(mtex.mapping_y))
        param_map.setInt("proj_z", proj2int(mtex.mapping_z))

        switchMappingCoords = {
            'FLAT': 'plain',
            'CUBE': 'cube',
            'TUBE': 'tube',
            'SPHERE': 'sphere',
        }
        mappingCoords = switchMappingCoords.get(mtex.mapping, 'plain')
        param_map.setString("mapping", mappingCoords)

        param_map.setVector("scale", mtex.scale[0], mtex.scale[1], mtex.scale[2])
        param_map.setVector("offset", mtex.offset[0], mtex.offset[1], mtex.offset[2])

        if mtex.use_map_normal:  # || mtex->maptoneg & MAP_NORM )
            # scale up the normal factor, it resembles
            # blender a bit more
            nf = mtex.normal_factor * 2
            param_map.setFloat("bump_strength", nf)

        param_map_list.addParamMap(param_map)

    def writeGlassShader(self, mat, scene, rough):

        # mat : is an instance of material

        param_map_list = libyafaray4_bindings.ParamMapList()
        param_map = libyafaray4_bindings.ParamMap()

        param_map.setInt("mat_pass_index", mat.pass_index)

        if rough:  # create bool property "rough"
            param_map.setString("type", "rough_glass")
            param_map.setFloat("alpha", mat.refr_roughness)  # added refraction roughness for roughglass material
        else:
            param_map.setString("type", "glass")

        param_map.setFloat("IOR", mat.IOR_refraction)  # added IOR for refraction
        if scene.gs_clay_render and not mat.clay_exclude:
            filt_col = (1.0, 1.0, 1.0)
            abs_col = (1.0, 1.0, 1.0)
        else:
            filt_col = mat.filter_color
            abs_col = mat.absorption
        mir_col = mat.glass_mir_col
        tfilt = mat.glass_transmit

        param_map.setColor("filter_color", filt_col[0], filt_col[1], filt_col[2])
        param_map.setColor("mirror_color", mir_col[0], mir_col[1], mir_col[2])
        param_map.setFloat("transmit_filter", tfilt)

        param_map.setColor("absorption", abs_col[0], abs_col[1], abs_col[2])
        param_map.setFloat("absorption_dist", mat.absorption_dist)
        param_map.setFloat("dispersion_power", mat.dispersion_power)
        param_map.setBool("fake_shadows", mat.fake_shadows)
        param_map.setString("visibility", mat.visibility)
        param_map.setBool("receive_shadows", mat.receive_shadows)
        param_map.setBool("flat_material", False)
        param_map.setInt("additionaldepth", mat.additionaldepth)
        param_map.setFloat("samplingfactor", mat.samplingfactor)
        
        param_map.setFloat("wireframe_amount", mat.wireframe_amount)
        param_map.setColor("wireframe_color", mat.wireframe_color[0], mat.wireframe_color[1], mat.wireframe_color[2])
        param_map.setFloat("wireframe_thickness", mat.wireframe_thickness)
        param_map.setFloat("wireframe_exponent", mat.wireframe_exponent)

        mcolRoot = ''
        # fcolRoot = '' /* UNUSED */
        bumpRoot = ''
        filterColorRoot = ''
        IORRoot = ''
        WireframeRoot = ''
        roughnessRoot = ''

        i = 0
        used_textures = self.getUsedTextures(mat)

        for mtex in used_textures:
            used = False
            mappername = "map%x" % i

            lname = "mircol_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, mcolRoot, mtex, mtex.use_map_mirror, mir_col, mtex.mirror_factor):
                used = True
                mcolRoot = lname
            lname = "bump_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, bumpRoot, mtex, mtex.use_map_normal, [0], mtex.normal_factor):
                used = True
                bumpRoot = lname
            lname = "filter_color_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, filterColorRoot, mtex, mtex.use_map_color_reflection, filt_col, mtex.reflection_color_factor):
                used = True
                filterColorRoot = lname
            lname = "IOR_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, IORRoot, mtex, mtex.use_map_warp, [0], mtex.warp_factor):
                used = True
                IORRoot = lname
            lname = "wireframe_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, WireframeRoot, mtex, mtex.use_map_displacement, [0], mtex.displacement_factor):
                used = True
                WireframeRoot = lname
            lname = "roughness_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, roughnessRoot, mtex, mtex.use_map_hardness, [0], mtex.hardness_factor):
                used = True
                roughnessRoot = lname                
            if used:
                self.writeMappingNode(param_map_list, mappername, mtex.texture.name, mtex)
                i += 1

        
        if len(mcolRoot) > 0:
            param_map.setString("mirror_color_shader", mcolRoot)
        if len(bumpRoot) > 0:
            param_map.setString("bump_shader", bumpRoot)
        if len(filterColorRoot) > 0:
            param_map.setString("filter_color_shader", filterColorRoot)
        if len(IORRoot) > 0:
            param_map.setString("IOR_shader", IORRoot)             
        if len(WireframeRoot) > 0:
            param_map.setString("wireframe_shader", WireframeRoot)
        if len(roughnessRoot) > 0:
            param_map.setString("roughness_shader", roughnessRoot)   
        return self.yaf_scene.createMaterial(mat.name, param_map, param_map_list)

    def writeGlossyShader(self, mat, scene, coated):  # mat : instance of material class

        param_map_list = libyafaray4_bindings.ParamMapList()
        param_map = libyafaray4_bindings.ParamMap()

        param_map.setInt("mat_pass_index", mat.pass_index)

        bSpecr = mat.specular_reflect

        if coated:  # create bool property
            param_map.setString("type", "coated_glossy")
            param_map.setFloat("IOR", mat.IOR_reflection)  # IOR for reflection
            mir_col = mat.coat_mir_col  # added mirror color for coated glossy
            param_map.setColor("mirror_color", mir_col[0], mir_col[1], mir_col[2])
            param_map.setFloat("specular_reflect", bSpecr)
        else:
            param_map.setString("type", "glossy")
            mir_col = mat.diffuse_color

        diffuse_color = mat.diffuse_color
        color = mat.glossy_color

        param_map.setColor("diffuse_color", diffuse_color[0], diffuse_color[1], diffuse_color[2])
        param_map.setColor("color", color[0], color[1], color[2])
        param_map.setFloat("glossy_reflect", mat.glossy_reflect)
        param_map.setFloat("exponent", mat.exponent)
        param_map.setFloat("diffuse_reflect", mat.diffuse_reflect)
        param_map.setBool("as_diffuse", mat.as_diffuse)
        param_map.setBool("anisotropic", mat.anisotropic)
        param_map.setFloat("exp_u", mat.exp_u)
        param_map.setFloat("exp_v", mat.exp_v)
        param_map.setString("visibility", mat.visibility)
        param_map.setBool("receive_shadows", mat.receive_shadows)
        param_map.setBool("flat_material", False)
        param_map.setInt("additionaldepth", mat.additionaldepth)
        param_map.setFloat("samplingfactor", mat.samplingfactor)
        
        param_map.setFloat("wireframe_amount", mat.wireframe_amount)
        param_map.setColor("wireframe_color", mat.wireframe_color[0], mat.wireframe_color[1], mat.wireframe_color[2])
        param_map.setFloat("wireframe_thickness", mat.wireframe_thickness)
        param_map.setFloat("wireframe_exponent", mat.wireframe_exponent)

        diffRoot = ''
        # mcolRoot = ''  /* UNUSED */
        glossRoot = ''
        glRefRoot = ''
        bumpRoot = ''
        sigmaOrenRoot = ''
        exponentRoot = ''
        IORRoot = ''
        WireframeRoot = ''
        diffReflectRoot = ''
        mirrorRoot = ''
        mcolRoot = ''

        i = 0
        used_textures = self.getUsedTextures(mat)

        for mtex in used_textures:
            used = False
            mappername = "map%x" % i

            lname = "diff_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, diffRoot, mtex, mtex.use_map_color_diffuse, diffuse_color, mtex.diffuse_color_factor):
                used = True
                diffRoot = lname
            lname = "gloss_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, glossRoot, mtex, mtex.use_map_color_spec, color, mtex.specular_color_factor):
                used = True
                glossRoot = lname
            lname = "glossref_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, glRefRoot, mtex, mtex.use_map_specular, [mat.glossy_reflect], mtex.specular_factor):
                used = True
                glRefRoot = lname
            lname = "bump_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, bumpRoot, mtex, mtex.use_map_normal, [0], mtex.normal_factor):
                used = True
                bumpRoot = lname
            lname = "sigma_oren_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, sigmaOrenRoot, mtex, mtex.use_map_hardness, [0], mtex.hardness_factor):
                used = True
                sigmaOrenRoot = lname                
            lname = "exponent_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, exponentRoot, mtex, mtex.use_map_ambient, [0], mtex.ambient_factor):
                used = True
                exponentRoot = lname
            lname = "IOR_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, IORRoot, mtex, mtex.use_map_warp, [0], mtex.warp_factor):
                used = True
                IORRoot = lname
            lname = "wireframe_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, WireframeRoot, mtex, mtex.use_map_displacement, [0], mtex.displacement_factor):
                used = True
                WireframeRoot = lname
            lname = "diff_refl_layer%x" % i
            if self.writeTexLayer(param_map_list, lname, mappername, diffReflectRoot, mtex, mtex.use_map_diffuse, [0], mtex.diffuse_factor):
                used = True
                diffReflectRoot = lname

            if coated:
                lname = "mircol_layer%x" % i
                if self.writeTexLayer(param_map_list, lname, mappername, mcolRoot, mtex, mtex.use_map_mirror, mir_col, mtex.mirror_factor):
                    used = True
                    mcolRoot = lname
                lname = "mirr_layer%x" % i
                if self.writeTexLayer(param_map_list, lname, mappername, mirrorRoot, mtex, mtex.use_map_raymir, [bSpecr], mtex.raymir_factor):
                    used = True
                    mirrorRoot = lname

            if used:
                self.writeMappingNode(param_map_list, mappername, mtex.texture.name, mtex)
            i += 1

        
        if len(diffRoot) > 0:
            param_map.setString("diffuse_shader", diffRoot)
        if len(glossRoot) > 0:
            param_map.setString("glossy_shader", glossRoot)
        if len(glRefRoot) > 0:
            param_map.setString("glossy_reflect_shader", glRefRoot)
        if len(bumpRoot) > 0:
            param_map.setString("bump_shader", bumpRoot)
        if len(sigmaOrenRoot) > 0:
            param_map.setString("sigma_oren_shader", sigmaOrenRoot)     
        if len(exponentRoot) > 0:
            param_map.setString("exponent_shader", exponentRoot) 
        if len(IORRoot) > 0:
            param_map.setString("IOR_shader", IORRoot) 
        if len(WireframeRoot) > 0:
            param_map.setString("wireframe_shader", WireframeRoot)
        if len(diffReflectRoot) > 0:
            param_map.setString("diffuse_refl_shader", diffReflectRoot)       
        if coated:
            if len(mcolRoot) > 0:
                param_map.setString("mirror_color_shader", mcolRoot)
            if len(mirrorRoot) > 0:
                param_map.setString("mirror_shader", mirrorRoot)
                               
        if mat.brdf_type == "oren-nayar":  # oren-nayar fix for glossy
            param_map.setString("diffuse_brdf", "oren_nayar")
            param_map.setFloat("sigma", mat.sigma)

        return self.yaf_scene.createMaterial(mat.name, param_map, param_map_list)


    def writeShinyDiffuseShader(self, mat, scene):

        param_map_list = libyafaray4_bindings.ParamMapList()
        param_map = libyafaray4_bindings.ParamMap()

        param_map.setInt("mat_pass_index", mat.pass_index)

        param_map.setString("type", "shinydiffusemat")

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
        WireframeRoot = ''

        for mtex in used_textures:
            if not mtex.texture:
                continue
            used = False
            mappername = "map%x" % i

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "diff_layer%x" % i
                if self.writeTexLayer(param_map_list, lname, mappername, diffRoot, mtex, mtex.use_map_color_diffuse, bCol, mtex.diffuse_color_factor):
                    used = True
                    diffRoot = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "mircol_layer%x" % i
                if self.writeTexLayer(param_map_list, lname, mappername, mcolRoot, mtex, mtex.use_map_mirror, mirCol, mtex.mirror_factor):
                    used = True
                    mcolRoot = lname

            if mat.clay_exclude or scene.gs_clay_render_keep_transparency or not scene.gs_clay_render:
                lname = "transp_layer%x" % i
                if self.writeTexLayer(param_map_list, lname, mappername, transpRoot, mtex, mtex.use_map_alpha, [bTransp], mtex.alpha_factor):
                    used = True
                    transpRoot = lname

            if mat.clay_exclude or scene.gs_clay_render_keep_transparency or not scene.gs_clay_render:
                lname = "translu_layer%x" % i
                if self.writeTexLayer(param_map_list, lname, mappername, translRoot, mtex, mtex.use_map_translucency, [bTransl], mtex.translucency_factor):
                    used = True
                    translRoot = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "mirr_layer%x" % i
                if self.writeTexLayer(param_map_list, lname, mappername, mirrorRoot, mtex, mtex.use_map_raymir, [bSpecr], mtex.raymir_factor):
                    used = True
                    mirrorRoot = lname

            if mat.clay_exclude or scene.gs_clay_render_keep_normals or not scene.gs_clay_render:
                lname = "bump_layer%x" % i
                if self.writeTexLayer(param_map_list, lname, mappername, bumpRoot, mtex, mtex.use_map_normal, [0], mtex.normal_factor):
                    used = True
                    bumpRoot = lname

            if mat.clay_exclude or scene.gs_clay_render_keep_normals or not scene.gs_clay_render:
                lname = "sigma_oren_layer%x" % i
                if self.writeTexLayer(param_map_list, lname, mappername, sigmaOrenRoot, mtex, mtex.use_map_hardness, [0], mtex.hardness_factor):
                    used = True
                    sigmaOrenRoot = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "diff_refl_layer%x" % i
                if self.writeTexLayer(param_map_list, lname, mappername, diffReflectRoot, mtex, mtex.use_map_diffuse, [0], mtex.diffuse_factor):
                    used = True
                    diffReflectRoot = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "IOR_layer%x" % i
                if self.writeTexLayer(param_map_list, lname, mappername, IORRoot, mtex, mtex.use_map_warp, [0], mtex.warp_factor):
                    used = True
                    IORRoot = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "wireframe_layer%x" % i
                if self.writeTexLayer(param_map_list, lname, mappername, WireframeRoot, mtex, mtex.use_map_displacement, [0], mtex.displacement_factor):
                    used = True
                    WireframeRoot = lname

            if used:
                self.writeMappingNode(param_map_list, mappername, mtex.texture.name, mtex)
            i += 1

        
        if len(diffRoot) > 0:
            param_map.setString("diffuse_shader", diffRoot)
        if len(mcolRoot) > 0:
            param_map.setString("mirror_color_shader", mcolRoot)
        if len(transpRoot) > 0:
            param_map.setString("transparency_shader", transpRoot)
        if len(translRoot) > 0:
            param_map.setString("translucency_shader", translRoot)
        if len(mirrorRoot) > 0:
            param_map.setString("mirror_shader", mirrorRoot)
        if len(bumpRoot) > 0:
            param_map.setString("bump_shader", bumpRoot)
        if len(sigmaOrenRoot) > 0:
            param_map.setString("sigma_oren_shader", sigmaOrenRoot)        
        if len(diffReflectRoot) > 0:
            param_map.setString("diffuse_refl_shader", diffReflectRoot)             
        if len(IORRoot) > 0:
            param_map.setString("IOR_shader", IORRoot)
        if len(WireframeRoot) > 0:
            param_map.setString("wireframe_shader", WireframeRoot)

        param_map.setColor("color", bCol[0], bCol[1], bCol[2])
        param_map.setFloat("transparency", bTransp)
        param_map.setFloat("translucency", bTransl)
        param_map.setFloat("diffuse_reflect", bDiffRefl)
        param_map.setFloat("emit", bEmit)
        param_map.setFloat("transmit_filter", bTransmit)

        param_map.setFloat("specular_reflect", bSpecr)
        param_map.setColor("mirror_color", mirCol[0], mirCol[1], mirCol[2])
        param_map.setBool("fresnel_effect", mat.fresnel_effect)
        param_map.setFloat("IOR", mat.IOR_reflection)  # added IOR for reflection
        param_map.setString("visibility", mat.visibility)
        param_map.setBool("receive_shadows", mat.receive_shadows)
        param_map.setBool("flat_material", mat.flat_material)
        param_map.setInt("additionaldepth", mat.additionaldepth)
        param_map.setFloat("transparentbias_factor", mat.transparentbias_factor)
        param_map.setBool("transparentbias_multiply_raydepth", mat.transparentbias_multiply_raydepth)
        
        param_map.setFloat("samplingfactor", mat.samplingfactor)
        
        param_map.setFloat("wireframe_amount", mat.wireframe_amount)
        param_map.setColor("wireframe_color", mat.wireframe_color[0], mat.wireframe_color[1], mat.wireframe_color[2])
        param_map.setFloat("wireframe_thickness", mat.wireframe_thickness)
        param_map.setFloat("wireframe_exponent", mat.wireframe_exponent)
        
        if scene.gs_clay_render and not mat.clay_exclude:
             if scene.gs_clay_oren_nayar:
                 param_map.setString("diffuse_brdf", "oren_nayar")
                 param_map.setFloat("sigma", scene.gs_clay_sigma)
        elif mat.brdf_type == "oren-nayar":  # oren-nayar fix for shinydiffuse
            param_map.setString("diffuse_brdf", "oren_nayar")
            param_map.setFloat("sigma", mat.sigma)

        return self.yaf_scene.createMaterial(mat.name, param_map, param_map_list)

    def writeBlendShader(self, mat, scene):

        param_map_list = libyafaray4_bindings.ParamMapList()
        param_map = libyafaray4_bindings.ParamMap()

        self.logger.printInfo("Exporter: Blend material with: [" + mat.material1name + "] [" + mat.material2name + "]")
        param_map.setString("type", "blend_mat")
        param_map.setString("material1", mat.material1name)
        param_map.setString("material2", mat.material2name)
        
        param_map.setFloat("wireframe_amount", mat.wireframe_amount)
        param_map.setColor("wireframe_color", mat.wireframe_color[0], mat.wireframe_color[1], mat.wireframe_color[2])
        param_map.setFloat("wireframe_thickness", mat.wireframe_thickness)
        param_map.setFloat("wireframe_exponent", mat.wireframe_exponent)

        i = 0

        diffRoot = ''
        WireframeRoot = ''
        used_textures = self.getUsedTextures(mat)

        for mtex in used_textures:
            if mtex.texture.type == 'NONE':
                continue

            used = False
            mappername = "map%x" % i

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "diff_layer%x" % i
                if self.writeTexLayer(param_map_list, lname, mappername, diffRoot, mtex, mtex.use_map_diffuse, [0], mtex.diffuse_factor):
                    used = True
                    diffRoot = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "wireframe_layer%x" % i
                if self.writeTexLayer(param_map_list, lname, mappername, WireframeRoot, mtex, mtex.use_map_displacement, [0], mtex.displacement_factor):
                    used = True
                    WireframeRoot = lname
                    
            if used:
                self.writeMappingNode(param_map_list, mappername, mtex.texture.name, mtex)
            i += 1

        # if we have a blending map, disable the blend_value
        if len(diffRoot) > 0:
            param_map.setString("blend_shader", diffRoot)
            param_map.setFloat("blend_value", 0)
        else:
            param_map.setFloat("blend_value", mat.blend_value)
            
        if len(WireframeRoot) > 0:
            param_map.setString("wireframe_shader", WireframeRoot)

        param_map.setString("visibility", mat.visibility)
        param_map.setBool("receive_shadows", mat.receive_shadows)
        param_map.setBool("flat_material", False)
        param_map.setInt("additionaldepth", mat.additionaldepth)
        param_map.setFloat("samplingfactor", mat.samplingfactor)

        return self.yaf_scene.createMaterial(mat.name, param_map, param_map_list)

    def writeMatteShader(self, mat):

        param_map_list = libyafaray4_bindings.ParamMapList()
        param_map = libyafaray4_bindings.ParamMap()
        param_map.setString("type", "shadow_mat")
        return self.yaf_scene.createMaterial(mat.name, param_map, param_map_list)

    def writeNullMat(self, mat, scene):

        param_map_list = libyafaray4_bindings.ParamMapList()
        param_map = libyafaray4_bindings.ParamMap()
        param_map.setString("type", "null")
        return self.yaf_scene.createMaterial(mat.name, param_map, param_map_list)

    def writeMaterial(self, mat, scene, preview=False):
        self.preview = preview
        self.logger.printInfo("Exporter: Creating Material: \"" + mat.name + "\"")
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
