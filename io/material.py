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
from pprint import pprint
from inspect import getmembers


def proj2int(val):
    if val == 'NONE':
        return 0
    elif val == 'X':
        return 1
    elif val == 'Y':
        return 2
    elif val == 'Z':
        return 3


class Material:
    def __init__(self, yaf_scene, yaf_logger, texture_map):
        self.yaf_scene = yaf_scene
        self.yaf_logger = yaf_logger
        self.texture_map = texture_map
        self.is_preview = False

    @staticmethod
    def get_used_textures(material):
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

    def write_tex_layer(self, param_map_list, name, tex_in, ulayer, mtex, chanflag, dcol, factor):
        if mtex.name not in self.texture_map:
            return False
        if not chanflag:
            return False

        yaf_param_map = libyafaray4_bindings.ParamMap()
        yaf_param_map.setString("type", "layer")
        yaf_param_map.setString("name", name)
        yaf_param_map.setString("input", tex_in)  # SEE the defination later

        #mtex is an instance of MaterialTextureSlot class

        switch_blend_mode = {
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

        mode = switch_blend_mode.get(mtex.blend_type, 'MIX')  # set texture blend mode, if not a supported mode then set it to 'MIX'
        yaf_param_map.setString("blend_mode", mode)
        yaf_param_map.setBool("stencil", mtex.use_stencil)

        negative = mtex.invert
        yaf_param_map.setBool("negative", negative)

        if factor < 0:  # added a check for negative values
            factor = factor * -1
            yaf_param_map.setBool("negative", True)

        # "hack", scalar maps should always convert the RGB intensity to scalar
        # not clear why without this and noRGB == False, maps on scalar values seem to be "white" everywhere   <-- ???
        no_rgb = mtex.use_rgb_to_intensity

        # if len(dcol) == 1:    # disabled this 'hack' again, does not work with procedurals and alpha mapping (e.g. PNG image with 'use alpha')
        #     noRGB = True      # user should decide if rgb_to_intensity will be used or not...

        yaf_param_map.setBool("noRGB", no_rgb)

        yaf_param_map.setColor("def_col", mtex.color[0], mtex.color[1], mtex.color[2])
        yaf_param_map.setFloat("def_val", mtex.default_value)

        tex = mtex.texture  # texture object instance
        # lots to do...

        is_image = tex.yaf_tex_type == 'IMAGE'

        if (is_image or tex.use_color_ramp or (tex.yaf_tex_type == 'VORONOI' and tex.color_mode not in 'INTENSITY')):
            is_colored = True
        else:
            is_colored = False

        use_alpha = False
        yaf_param_map.setBool("color_input", is_colored)

        if is_image:
            use_alpha = (tex.yaf_use_alpha) and not(tex.use_calculate_alpha)

        yaf_param_map.setBool("use_alpha", use_alpha)

        do_color = len(dcol) >= 3  # see defination of dcol later on, watch the remaining parts from now on.

        if ulayer == "":
            if do_color:
                yaf_param_map.setColor("upper_color", dcol[0], dcol[1], dcol[2])
                yaf_param_map.setFloat("upper_value", 0)
            else:
                yaf_param_map.setColor("upper_color", 0, 0, 0)
                yaf_param_map.setFloat("upper_value", dcol[0])
        else:
            yaf_param_map.setString("upper_layer", ulayer)

        if do_color:
            yaf_param_map.setFloat("colfac", factor)
        else:
            yaf_param_map.setFloat("valfac", factor)

        yaf_param_map.setBool("do_color", do_color)
        yaf_param_map.setBool("do_scalar", not do_color)

        param_map_list.addParamMap(yaf_param_map)
        return True

    @staticmethod
    def write_mapping_node(param_map_list, name, texname, mtex):

        yaf_param_map = libyafaray4_bindings.ParamMap()

        yaf_param_map.setString("type", "texture_mapper")
        yaf_param_map.setString("name", name)
        yaf_param_map.setString("texture", texname)

        switch_tex_coords = {
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

        texco = switch_tex_coords.get(mtex.texture_coords, 'orco')  # get texture coords, default is 'orco'
        yaf_param_map.setString("texco", texco)

        if mtex.object:
            texmat = mtex.object.matrix_world.inverted()
            yaf_param_map.setMatrix("transform", texmat[0][0], texmat[0][1], texmat[0][2], texmat[0][3], texmat[1][0], texmat[1][1], texmat[1][2], texmat[1][3], texmat[2][0], texmat[2][1], texmat[2][2], texmat[2][3], texmat[3][0], texmat[3][1], texmat[3][2], texmat[3][3], False)

        yaf_param_map.setInt("proj_x", proj2int(mtex.mapping_x))
        yaf_param_map.setInt("proj_y", proj2int(mtex.mapping_y))
        yaf_param_map.setInt("proj_z", proj2int(mtex.mapping_z))

        switch_mapping_coords = {
            'FLAT': 'plain',
            'CUBE': 'cube',
            'TUBE': 'tube',
            'SPHERE': 'sphere',
        }
        mapping_coords = switch_mapping_coords.get(mtex.mapping, 'plain')
        yaf_param_map.setString("mapping", mapping_coords)

        yaf_param_map.setVector("scale", mtex.scale[0], mtex.scale[1], mtex.scale[2])
        yaf_param_map.setVector("offset", mtex.offset[0], mtex.offset[1], mtex.offset[2])

        if mtex.use_map_normal:  # || mtex->maptoneg & MAP_NORM )
            # scale up the normal factor, it resembles
            # blender a bit more
            nf = mtex.normal_factor * 2
            yaf_param_map.setFloat("bump_strength", nf)

        param_map_list.addParamMap(yaf_param_map)

    def write_glass_shader(self, mat, scene, rough):

        # mat : is an instance of material

        param_map_list = libyafaray4_bindings.ParamMapList()
        yaf_param_map = libyafaray4_bindings.ParamMap()

        yaf_param_map.setInt("mat_pass_index", mat.pass_index)

        if rough:  # create bool property "rough"
            yaf_param_map.setString("type", "rough_glass")
            yaf_param_map.setFloat("alpha", mat.refr_roughness)  # added refraction roughness for roughglass material
        else:
            yaf_param_map.setString("type", "glass")

        yaf_param_map.setFloat("IOR", mat.IOR_refraction)  # added IOR for refraction
        if scene.gs_clay_render and not mat.clay_exclude:
            filt_col = (1.0, 1.0, 1.0)
            abs_col = (1.0, 1.0, 1.0)
        else:
            filt_col = mat.filter_color
            abs_col = mat.absorption
        mir_col = mat.glass_mir_col
        tfilt = mat.glass_transmit

        yaf_param_map.setColor("filter_color", filt_col[0], filt_col[1], filt_col[2])
        yaf_param_map.setColor("mirror_color", mir_col[0], mir_col[1], mir_col[2])
        yaf_param_map.setFloat("transmit_filter", tfilt)

        yaf_param_map.setColor("absorption", abs_col[0], abs_col[1], abs_col[2])
        yaf_param_map.setFloat("absorption_dist", mat.absorption_dist)
        yaf_param_map.setFloat("dispersion_power", mat.dispersion_power)
        yaf_param_map.setBool("fake_shadows", mat.fake_shadows)
        yaf_param_map.setString("visibility", mat.visibility)
        yaf_param_map.setBool("receive_shadows", mat.receive_shadows)
        yaf_param_map.setBool("flat_material", False)
        yaf_param_map.setInt("additionaldepth", mat.additionaldepth)
        yaf_param_map.setFloat("samplingfactor", mat.samplingfactor)

        yaf_param_map.setFloat("wireframe_amount", mat.wireframe_amount)
        yaf_param_map.setColor("wireframe_color", mat.wireframe_color[0], mat.wireframe_color[1], mat.wireframe_color[2])
        yaf_param_map.setFloat("wireframe_thickness", mat.wireframe_thickness)
        yaf_param_map.setFloat("wireframe_exponent", mat.wireframe_exponent)

        mcol_root = ''
        bump_root = ''
        filter_color_root = ''
        ior_root = ''
        wireframe_root = ''
        roughness_root = ''

        i = 0
        used_textures = self.get_used_textures(mat)

        for mtex in used_textures:
            used = False
            mappername = "map%x" % i

            lname = "mircol_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, mcol_root, mtex, mtex.use_map_mirror, mir_col, mtex.mirror_factor):
                used = True
                mcol_root = lname
            lname = "bump_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, bump_root, mtex, mtex.use_map_normal, [0], mtex.normal_factor):
                used = True
                bump_root = lname
            lname = "filter_color_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, filter_color_root, mtex, mtex.use_map_color_reflection, filt_col, mtex.reflection_color_factor):
                used = True
                filter_color_root = lname
            lname = "IOR_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, ior_root, mtex, mtex.use_map_warp, [0], mtex.warp_factor):
                used = True
                ior_root = lname
            lname = "wireframe_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, wireframe_root, mtex, mtex.use_map_displacement, [0], mtex.displacement_factor):
                used = True
                wireframe_root = lname
            lname = "roughness_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, roughness_root, mtex, mtex.use_map_hardness, [0], mtex.hardness_factor):
                used = True
                roughness_root = lname
            if used:
                self.write_mapping_node(param_map_list, mappername, mtex.texture.name, mtex)
                i += 1


        if len(mcol_root) > 0:
            yaf_param_map.setString("mirror_color_shader", mcol_root)
        if len(bump_root) > 0:
            yaf_param_map.setString("bump_shader", bump_root)
        if len(filter_color_root) > 0:
            yaf_param_map.setString("filter_color_shader", filter_color_root)
        if len(ior_root) > 0:
            yaf_param_map.setString("IOR_shader", ior_root)
        if len(wireframe_root) > 0:
            yaf_param_map.setString("wireframe_shader", wireframe_root)
        if len(roughness_root) > 0:
            yaf_param_map.setString("roughness_shader", roughness_root)
        return self.yaf_scene.createMaterial(mat.name, yaf_param_map, param_map_list)

    def write_glossy_shader(self, mat, scene, coated):  # mat : instance of material class

        param_map_list = libyafaray4_bindings.ParamMapList()
        yaf_param_map = libyafaray4_bindings.ParamMap()

        yaf_param_map.setInt("mat_pass_index", mat.pass_index)

        b_specr = mat.specular_reflect

        if coated:  # create bool property
            yaf_param_map.setString("type", "coated_glossy")
            yaf_param_map.setFloat("IOR", mat.IOR_reflection)  # IOR for reflection
            mir_col = mat.coat_mir_col  # added mirror color for coated glossy
            yaf_param_map.setColor("mirror_color", mir_col[0], mir_col[1], mir_col[2])
            yaf_param_map.setFloat("specular_reflect", b_specr)
        else:
            yaf_param_map.setString("type", "glossy")
            mir_col = mat.diffuse_color

        diffuse_color = mat.diffuse_color
        color = mat.glossy_color

        yaf_param_map.setColor("diffuse_color", diffuse_color[0], diffuse_color[1], diffuse_color[2])
        yaf_param_map.setColor("color", color[0], color[1], color[2])
        yaf_param_map.setFloat("glossy_reflect", mat.glossy_reflect)
        yaf_param_map.setFloat("exponent", mat.exponent)
        yaf_param_map.setFloat("diffuse_reflect", mat.diffuse_reflect)
        yaf_param_map.setBool("as_diffuse", mat.as_diffuse)
        yaf_param_map.setBool("anisotropic", mat.anisotropic)
        yaf_param_map.setFloat("exp_u", mat.exp_u)
        yaf_param_map.setFloat("exp_v", mat.exp_v)
        yaf_param_map.setString("visibility", mat.visibility)
        yaf_param_map.setBool("receive_shadows", mat.receive_shadows)
        yaf_param_map.setBool("flat_material", False)
        yaf_param_map.setInt("additionaldepth", mat.additionaldepth)
        yaf_param_map.setFloat("samplingfactor", mat.samplingfactor)

        yaf_param_map.setFloat("wireframe_amount", mat.wireframe_amount)
        yaf_param_map.setColor("wireframe_color", mat.wireframe_color[0], mat.wireframe_color[1], mat.wireframe_color[2])
        yaf_param_map.setFloat("wireframe_thickness", mat.wireframe_thickness)
        yaf_param_map.setFloat("wireframe_exponent", mat.wireframe_exponent)

        diff_root = ''
        gloss_root = ''
        gl_ref_root = ''
        bump_root = ''
        sigma_oren_root = ''
        exponent_root = ''
        ior_root = ''
        wireframe_root = ''
        diff_reflect_root = ''
        mirror_root = ''
        mcol_root = ''

        i = 0
        used_textures = self.get_used_textures(mat)

        for mtex in used_textures:
            used = False
            mappername = "map%x" % i

            lname = "diff_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, diff_root, mtex, mtex.use_map_color_diffuse, diffuse_color, mtex.diffuse_color_factor):
                used = True
                diff_root = lname
            lname = "gloss_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, gloss_root, mtex, mtex.use_map_color_spec, color, mtex.specular_color_factor):
                used = True
                gloss_root = lname
            lname = "glossref_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, gl_ref_root, mtex, mtex.use_map_specular, [mat.glossy_reflect], mtex.specular_factor):
                used = True
                gl_ref_root = lname
            lname = "bump_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, bump_root, mtex, mtex.use_map_normal, [0], mtex.normal_factor):
                used = True
                bump_root = lname
            lname = "sigma_oren_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, sigma_oren_root, mtex, mtex.use_map_hardness, [0], mtex.hardness_factor):
                used = True
                sigma_oren_root = lname
            lname = "exponent_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, exponent_root, mtex, mtex.use_map_ambient, [0], mtex.ambient_factor):
                used = True
                exponent_root = lname
            lname = "IOR_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, ior_root, mtex, mtex.use_map_warp, [0], mtex.warp_factor):
                used = True
                ior_root = lname
            lname = "wireframe_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, wireframe_root, mtex, mtex.use_map_displacement, [0], mtex.displacement_factor):
                used = True
                wireframe_root = lname
            lname = "diff_refl_layer%x" % i
            if self.write_tex_layer(param_map_list, lname, mappername, diff_reflect_root, mtex, mtex.use_map_diffuse, [0], mtex.diffuse_factor):
                used = True
                diff_reflect_root = lname

            if coated:
                lname = "mircol_layer%x" % i
                if self.write_tex_layer(param_map_list, lname, mappername, mcol_root, mtex, mtex.use_map_mirror, mir_col, mtex.mirror_factor):
                    used = True
                    mcol_root = lname
                lname = "mirr_layer%x" % i
                if self.write_tex_layer(param_map_list, lname, mappername, mirror_root, mtex, mtex.use_map_raymir, [b_specr], mtex.raymir_factor):
                    used = True
                    mirror_root = lname

            if used:
                self.write_mapping_node(param_map_list, mappername, mtex.texture.name, mtex)
            i += 1


        if len(diff_root) > 0:
            yaf_param_map.setString("diffuse_shader", diff_root)
        if len(gloss_root) > 0:
            yaf_param_map.setString("glossy_shader", gloss_root)
        if len(gl_ref_root) > 0:
            yaf_param_map.setString("glossy_reflect_shader", gl_ref_root)
        if len(bump_root) > 0:
            yaf_param_map.setString("bump_shader", bump_root)
        if len(sigma_oren_root) > 0:
            yaf_param_map.setString("sigma_oren_shader", sigma_oren_root)
        if len(exponent_root) > 0:
            yaf_param_map.setString("exponent_shader", exponent_root)
        if len(ior_root) > 0:
            yaf_param_map.setString("IOR_shader", ior_root)
        if len(wireframe_root) > 0:
            yaf_param_map.setString("wireframe_shader", wireframe_root)
        if len(diff_reflect_root) > 0:
            yaf_param_map.setString("diffuse_refl_shader", diff_reflect_root)
        if coated:
            if len(mcol_root) > 0:
                yaf_param_map.setString("mirror_color_shader", mcol_root)
            if len(mirror_root) > 0:
                yaf_param_map.setString("mirror_shader", mirror_root)

        if mat.brdf_type == "oren-nayar":  # oren-nayar fix for glossy
            yaf_param_map.setString("diffuse_brdf", "oren_nayar")
            yaf_param_map.setFloat("sigma", mat.sigma)

        return self.yaf_scene.createMaterial(mat.name, yaf_param_map, param_map_list)


    def write_shiny_diffuse_shader(self, mat, scene):

        param_map_list = libyafaray4_bindings.ParamMapList()
        yaf_param_map = libyafaray4_bindings.ParamMap()

        yaf_param_map.setInt("mat_pass_index", mat.pass_index)

        yaf_param_map.setString("type", "shinydiffusemat")

        b_col = mat.diffuse_color
        b_mir_col = mat.mirror_color
        b_specr = mat.specular_reflect
        b_diff_refl = mat.diffuse_reflect
        b_transp = mat.transparency
        b_transl = mat.translucency
        b_transmit = mat.transmit_filter
        b_emit = mat.emit

        if scene.gs_clay_render and not mat.clay_exclude:
            b_col = scene.gs_clay_col
            b_specr = 0.0
            b_emit = 0.0
            b_diff_refl = 1.0
            if not scene.gs_clay_render_keep_transparency:
                b_transp = 0.0
                b_transl = 0.0

        if self.is_preview:
            if mat.name.startswith("checker"):
                b_emit = 2.50

        i = 0
        used_textures = self.get_used_textures(mat)

        diff_root = ''
        mcol_root = ''
        transp_root = ''
        transl_root = ''
        mirror_root = ''
        bump_root = ''
        sigma_oren_root = ''
        diff_reflect_root = ''
        ior_root = ''
        wireframe_root = ''

        for mtex in used_textures:
            if not mtex.texture:
                continue
            used = False
            mappername = "map%x" % i

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "diff_layer%x" % i
                if self.write_tex_layer(param_map_list, lname, mappername, diff_root, mtex, mtex.use_map_color_diffuse, b_col, mtex.diffuse_color_factor):
                    used = True
                    diff_root = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "mircol_layer%x" % i
                if self.write_tex_layer(param_map_list, lname, mappername, mcol_root, mtex, mtex.use_map_mirror, b_mir_col, mtex.mirror_factor):
                    used = True
                    mcol_root = lname

            if mat.clay_exclude or scene.gs_clay_render_keep_transparency or not scene.gs_clay_render:
                lname = "transp_layer%x" % i
                if self.write_tex_layer(param_map_list, lname, mappername, transp_root, mtex, mtex.use_map_alpha, [b_transp], mtex.alpha_factor):
                    used = True
                    transp_root = lname

            if mat.clay_exclude or scene.gs_clay_render_keep_transparency or not scene.gs_clay_render:
                lname = "translu_layer%x" % i
                if self.write_tex_layer(param_map_list, lname, mappername, transl_root, mtex, mtex.use_map_translucency, [b_transl], mtex.translucency_factor):
                    used = True
                    transl_root = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "mirr_layer%x" % i
                if self.write_tex_layer(param_map_list, lname, mappername, mirror_root, mtex, mtex.use_map_raymir, [b_specr], mtex.raymir_factor):
                    used = True
                    mirror_root = lname

            if mat.clay_exclude or scene.gs_clay_render_keep_normals or not scene.gs_clay_render:
                lname = "bump_layer%x" % i
                if self.write_tex_layer(param_map_list, lname, mappername, bump_root, mtex, mtex.use_map_normal, [0], mtex.normal_factor):
                    used = True
                    bump_root = lname

            if mat.clay_exclude or scene.gs_clay_render_keep_normals or not scene.gs_clay_render:
                lname = "sigma_oren_layer%x" % i
                if self.write_tex_layer(param_map_list, lname, mappername, sigma_oren_root, mtex, mtex.use_map_hardness, [0], mtex.hardness_factor):
                    used = True
                    sigma_oren_root = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "diff_refl_layer%x" % i
                if self.write_tex_layer(param_map_list, lname, mappername, diff_reflect_root, mtex, mtex.use_map_diffuse, [0], mtex.diffuse_factor):
                    used = True
                    diff_reflect_root = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "IOR_layer%x" % i
                if self.write_tex_layer(param_map_list, lname, mappername, ior_root, mtex, mtex.use_map_warp, [0], mtex.warp_factor):
                    used = True
                    ior_root = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "wireframe_layer%x" % i
                if self.write_tex_layer(param_map_list, lname, mappername, wireframe_root, mtex, mtex.use_map_displacement, [0], mtex.displacement_factor):
                    used = True
                    wireframe_root = lname

            if used:
                self.write_mapping_node(param_map_list, mappername, mtex.texture.name, mtex)
            i += 1


        if len(diff_root) > 0:
            yaf_param_map.setString("diffuse_shader", diff_root)
        if len(mcol_root) > 0:
            yaf_param_map.setString("mirror_color_shader", mcol_root)
        if len(transp_root) > 0:
            yaf_param_map.setString("transparency_shader", transp_root)
        if len(transl_root) > 0:
            yaf_param_map.setString("translucency_shader", transl_root)
        if len(mirror_root) > 0:
            yaf_param_map.setString("mirror_shader", mirror_root)
        if len(bump_root) > 0:
            yaf_param_map.setString("bump_shader", bump_root)
        if len(sigma_oren_root) > 0:
            yaf_param_map.setString("sigma_oren_shader", sigma_oren_root)
        if len(diff_reflect_root) > 0:
            yaf_param_map.setString("diffuse_refl_shader", diff_reflect_root)
        if len(ior_root) > 0:
            yaf_param_map.setString("IOR_shader", ior_root)
        if len(wireframe_root) > 0:
            yaf_param_map.setString("wireframe_shader", wireframe_root)

        yaf_param_map.setColor("color", b_col[0], b_col[1], b_col[2])
        yaf_param_map.setFloat("transparency", b_transp)
        yaf_param_map.setFloat("translucency", b_transl)
        yaf_param_map.setFloat("diffuse_reflect", b_diff_refl)
        yaf_param_map.setFloat("emit", b_emit)
        yaf_param_map.setFloat("transmit_filter", b_transmit)

        yaf_param_map.setFloat("specular_reflect", b_specr)
        yaf_param_map.setColor("mirror_color", b_mir_col[0], b_mir_col[1], b_mir_col[2])
        yaf_param_map.setBool("fresnel_effect", mat.fresnel_effect)
        yaf_param_map.setFloat("IOR", mat.IOR_reflection)  # added IOR for reflection
        yaf_param_map.setString("visibility", mat.visibility)
        yaf_param_map.setBool("receive_shadows", mat.receive_shadows)
        yaf_param_map.setBool("flat_material", mat.flat_material)
        yaf_param_map.setInt("additionaldepth", mat.additionaldepth)
        yaf_param_map.setFloat("transparentbias_factor", mat.transparentbias_factor)
        yaf_param_map.setBool("transparentbias_multiply_raydepth", mat.transparentbias_multiply_raydepth)

        yaf_param_map.setFloat("samplingfactor", mat.samplingfactor)

        yaf_param_map.setFloat("wireframe_amount", mat.wireframe_amount)
        yaf_param_map.setColor("wireframe_color", mat.wireframe_color[0], mat.wireframe_color[1], mat.wireframe_color[2])
        yaf_param_map.setFloat("wireframe_thickness", mat.wireframe_thickness)
        yaf_param_map.setFloat("wireframe_exponent", mat.wireframe_exponent)

        if scene.gs_clay_render and not mat.clay_exclude:
             if scene.gs_clay_oren_nayar:
                 yaf_param_map.setString("diffuse_brdf", "oren_nayar")
                 yaf_param_map.setFloat("sigma", scene.gs_clay_sigma)
        elif mat.brdf_type == "oren-nayar":  # oren-nayar fix for shinydiffuse
            yaf_param_map.setString("diffuse_brdf", "oren_nayar")
            yaf_param_map.setFloat("sigma", mat.sigma)

        return self.yaf_scene.createMaterial(mat.name, yaf_param_map, param_map_list)

    def write_blend_shader(self, mat, scene):

        param_map_list = libyafaray4_bindings.ParamMapList()
        yaf_param_map = libyafaray4_bindings.ParamMap()

        self.yaf_logger.printInfo("Exporter: Blend material with: [" + mat.material1name + "] [" + mat.material2name + "]")
        yaf_param_map.setString("type", "blend_mat")
        yaf_param_map.setString("material1", mat.material1name)
        yaf_param_map.setString("material2", mat.material2name)

        yaf_param_map.setFloat("wireframe_amount", mat.wireframe_amount)
        yaf_param_map.setColor("wireframe_color", mat.wireframe_color[0], mat.wireframe_color[1], mat.wireframe_color[2])
        yaf_param_map.setFloat("wireframe_thickness", mat.wireframe_thickness)
        yaf_param_map.setFloat("wireframe_exponent", mat.wireframe_exponent)

        i = 0

        diff_root = ''
        wireframe_root = ''
        used_textures = self.get_used_textures(mat)

        for mtex in used_textures:
            if mtex.texture.type == 'NONE':
                continue

            used = False
            mappername = "map%x" % i

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "diff_layer%x" % i
                if self.write_tex_layer(param_map_list, lname, mappername, diff_root, mtex, mtex.use_map_diffuse, [0], mtex.diffuse_factor):
                    used = True
                    diff_root = lname

            if mat.clay_exclude or not scene.gs_clay_render:
                lname = "wireframe_layer%x" % i
                if self.write_tex_layer(param_map_list, lname, mappername, wireframe_root, mtex, mtex.use_map_displacement, [0], mtex.displacement_factor):
                    used = True
                    wireframe_root = lname

            if used:
                self.write_mapping_node(param_map_list, mappername, mtex.texture.name, mtex)
            i += 1

        # if we have a blending map, disable the blend_value
        if len(diff_root) > 0:
            yaf_param_map.setString("blend_shader", diff_root)
            yaf_param_map.setFloat("blend_value", 0)
        else:
            yaf_param_map.setFloat("blend_value", mat.blend_value)

        if len(wireframe_root) > 0:
            yaf_param_map.setString("wireframe_shader", wireframe_root)

        yaf_param_map.setString("visibility", mat.visibility)
        yaf_param_map.setBool("receive_shadows", mat.receive_shadows)
        yaf_param_map.setBool("flat_material", False)
        yaf_param_map.setInt("additionaldepth", mat.additionaldepth)
        yaf_param_map.setFloat("samplingfactor", mat.samplingfactor)

        return self.yaf_scene.createMaterial(mat.name, yaf_param_map, param_map_list)

    def write_matte_shader(self, mat):

        param_map_list = libyafaray4_bindings.ParamMapList()
        yaf_param_map = libyafaray4_bindings.ParamMap()
        yaf_param_map.setString("type", "shadow_mat")
        return self.yaf_scene.createMaterial(mat.name, yaf_param_map, param_map_list)

    def write_null_mat(self, mat, scene):

        param_map_list = libyafaray4_bindings.ParamMapList()
        yaf_param_map = libyafaray4_bindings.ParamMap()
        yaf_param_map.setString("type", "null")
        return self.yaf_scene.createMaterial(mat.name, yaf_param_map, param_map_list)

    def write_material(self, bl_material, bl_scene, is_preview=False):
        self.is_preview = is_preview
        self.yaf_logger.printInfo("Exporter: Creating Material: \"" + bl_material.name + "\"")
        if bl_material.name == "y_null":
            self.write_null_mat(bl_material, bl_scene)
        elif bl_scene.gs_clay_render and not bl_material.clay_exclude and not (bl_scene.gs_clay_render_keep_transparency and bl_material.mat_type == "glass"):
            self.write_shiny_diffuse_shader(bl_material, bl_scene)
        elif bl_material.mat_type == "glass":
            self.write_glass_shader(bl_material, bl_scene, False)
        elif bl_material.mat_type == "rough_glass":
            self.write_glass_shader(bl_material, bl_scene, True)
        elif bl_material.mat_type == "glossy":
            self.write_glossy_shader(bl_material, bl_scene, False)
        elif bl_material.mat_type == "coated_glossy":
            self.write_glossy_shader(bl_material, bl_scene, True)
        elif bl_material.mat_type == "shinydiffusemat":
            self.write_shiny_diffuse_shader(bl_material, bl_scene)
        elif bl_material.mat_type == "blend":
            self.write_blend_shader(bl_material, bl_scene)   #FIXME: in the new Clay render two limitations:
                #We cannot yet keep transparency in Blend objects. If that's needed to test a scene, better to exclude that particular material from the Clay
                #We cannot exclude just the blended material from the Clay render, the individual materials that are used to make the blend also have to be excluded
        else:
            self.write_null_mat(bl_material, bl_scene)


    def handle_blend_mat(self, mat):
        blendmat_error = False
        try:
            mat1 = bpy.data.materials[mat.material1name]
        except:
            self.yaf_logger.printWarning(
                "Exporter: Problem with blend material:\"{0}\". Could not find the first material:\"{1}\"".format(
                    mat.name, mat.material1name))
            blendmat_error = True
        try:
            mat2 = bpy.data.materials[mat.material2name]
        except:
            self.yaf_logger.printWarning(
                "Exporter: Problem with blend material:\"{0}\". Could not find the second material:\"{1}\"".format(
                    mat.name, mat.material2name))
            blendmat_error = True
        if blendmat_error:
            return blendmat_error
        if mat1.name == mat2.name:
            self.yaf_logger.printWarning(
                "Exporter: Problem with blend material \"{0}\". \"{1}\" and \"{2}\" to blend are the same materials".format(
                    mat.name, mat1.name, mat2.name))

        if mat1.mat_type == 'blend':
            blendmat_error = self.handle_blend_mat(mat1)
            if blendmat_error:
                return

        elif mat1 not in self.materials:
            self.materials.add(mat1)
            self.material.write_material(mat1, self.bl_scene)

        if mat2.mat_type == 'blend':
            blendmat_error = self.handle_blend_mat(mat2)
            if blendmat_error:
                return

        elif mat2 not in self.materials:
            self.materials.add(mat2)
            self.material.write_material(mat2, self.bl_scene)

        if mat not in self.materials:
            self.materials.add(mat)
            self.material.write_material(mat, self.bl_scene)

    def export_material(self, bl_material):
        if bl_material:
            if bl_material.mat_type == 'blend':
                # must make sure all materials used by a blend mat
                # are written before the blend mat itself
                self.handle_blend_mat(bl_material)
            else:
                self.materials.add(bl_material)
                material = Material(self.yaf_scene, self.yaf_logger, bl_material.texture_map)
                material.write_material(bl_material, self.bl_scene, self.is_preview)