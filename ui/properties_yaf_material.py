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
from yafaray.ui.ior_values import ior_list
from bpy.types import Panel, Menu
from bl_ui.properties_material import (MaterialButtonsPanel,
                                       active_node_mat,
                                       check_material)

MaterialButtonsPanel.COMPAT_ENGINES = {'YAFA_RENDER'}


class MaterialTypePanel(MaterialButtonsPanel):
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):
        yaf_mat = context.material
        engine = context.scene.render.engine
        return check_material(yaf_mat) and (yaf_mat.mat_type in cls.material_type) and (engine in cls.COMPAT_ENGINES)


class YAF_PT_context_material(MaterialButtonsPanel, Panel):
    bl_label = ""
    bl_options = {'HIDE_HEADER'}
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):
        # An exception, dont call the parent poll func because
        # this manages materials for all engine types
        engine = context.scene.render.engine
        return (context.material or context.object) and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        yaf_mat = context.material
        ob = context.object
        slot = context.material_slot
        space = context.space_data

        if ob:
            row = layout.row()
            if bpy.app.version < (2, 65, 3 ):
                row.template_list(ob, "material_slots", ob, "active_material_index", rows=2)
            else:
                row.template_list("MATERIAL_UL_matslots", "", ob, "material_slots", ob, "active_material_index", rows=2)

            col = row.column(align=True)
            col.operator("object.material_slot_add", icon='ZOOMIN', text="")
            col.operator("object.material_slot_remove", icon='ZOOMOUT', text="")

            # TODO: code own operators to copy yaf material settings...
            col.menu("MATERIAL_MT_specials", icon='DOWNARROW_HLT', text="")

            if ob.mode == 'EDIT':
                row = layout.row(align=True)
                row.operator("object.material_slot_assign", text="Assign")
                row.operator("object.material_slot_select", text="Select")
                row.operator("object.material_slot_deselect", text="Deselect")

        split = layout.split(percentage=0.75)

        if ob:
            split.template_ID(ob, "active_material", new="material.new")
            row = split.row()
            if slot:
                row.prop(slot, "link", text="")
            else:
                row.label()

        elif yaf_mat:
            split.template_ID(space, "pin_id")
            split.separator()

        if yaf_mat:
            layout.separator()
            layout.prop(yaf_mat, "mat_type")
            layout.row().prop(yaf_mat, "clay_exclude")


class YAF_MATERIAL_PT_preview(MaterialButtonsPanel, Panel):
    bl_label = "Preview"

    def draw(self, context):
        self.layout.template_preview(context.material)


def draw_generator(ior_n):
    def draw(self, context):
        sl = self.layout
        for values in ior_n:
            ior_name, ior_index = values
            props = sl.operator('material.set_ior_preset', text=ior_name)
            # two values given to ior preset operator
            props.index = ior_index
            props.name = ior_name
    return draw

submenus = []

for ior_group, ior_n in ior_list:
    submenu_idname = 'YAF_MT_presets_ior_list_cat%d' % len(submenus)
    submenu = type(
        submenu_idname,
        (Menu,),
        {
            'bl_idname': submenu_idname,
            'bl_label': ior_group,
            'draw': draw_generator(ior_n)
        }
    )
    bpy.utils.register_class(submenu)
    submenus.append(submenu)


class YAF_MT_presets_ior_list(Menu):
    bl_label = "Glass"

    def draw(self, context):
        sl = self.layout
        for sm in submenus:
            sl.menu(sm.bl_idname)


class YAF_PT_shinydiffuse_diffuse(MaterialTypePanel, Panel):
    bl_label = "Diffuse reflection"
    material_type = 'shinydiffusemat'

    def draw(self, context):
        layout = self.layout
        yaf_mat = active_node_mat(context.material)

        split = layout.split()
        col = split.column()
        col.prop(yaf_mat, "diffuse_color")
        col.prop(yaf_mat, "emit")
        layout.row().prop(yaf_mat, "diffuse_reflect", slider=True)

        col = split.column()
        sub = col.column()
        sub.label(text="Reflectance model:")
        sub.prop(yaf_mat, "brdf_type", text="")
        brdf = sub.column()
        brdf.enabled = yaf_mat.brdf_type == "oren-nayar"
        brdf.prop(yaf_mat, "sigma")

        layout.separator()

        box = layout.box()
        box.label(text="Transparency and translucency:")
        split = box.split()
        col = split.column()
        col.prop(yaf_mat, "transparency", slider=True)
        col = split.column()
        col.prop(yaf_mat, "translucency", slider=True)
        box.row().prop(yaf_mat, "transmit_filter", slider=True)


class YAF_PT_shinydiffuse_specular(MaterialTypePanel, Panel):
    bl_label = "Specular reflection"
    material_type = 'shinydiffusemat'

    def draw(self, context):
        layout = self.layout
        yaf_mat = active_node_mat(context.material)

        split = layout.split()
        col = split.column()
        col.label(text="Mirror color:")
        col.prop(yaf_mat, "mirror_color", text="")

        col = split.column()
        col.prop(yaf_mat, "fresnel_effect")
        sub = col.column()
        sub.enabled = yaf_mat.fresnel_effect
        sub.prop(yaf_mat, "IOR_reflection", slider=True)
        layout.row().prop(yaf_mat, "specular_reflect", slider=True)


class YAF_PT_glossy_diffuse(MaterialTypePanel, Panel):
    bl_label = "Diffuse reflection"
    material_type = 'glossy', 'coated_glossy'

    def draw(self, context):
        layout = self.layout
        yaf_mat = active_node_mat(context.material)

        split = layout.split()
        col = split.column()
        col.prop(yaf_mat, "diffuse_color")

        col = split.column()
        ref = col.column(align=True)
        ref.label(text="Reflectance model:")
        ref.prop(yaf_mat, "brdf_type", text="")
        sig = col.column()
        sig.enabled = yaf_mat.brdf_type == "oren-nayar"
        sig.prop(yaf_mat, "sigma")
        layout.row().prop(yaf_mat, "diffuse_reflect", slider=True)


class YAF_PT_glossy_specular(MaterialTypePanel, Panel):
    bl_label = "Specular reflection"
    material_type = 'glossy', 'coated_glossy'

    def draw(self, context):
        layout = self.layout
        yaf_mat = active_node_mat(context.material)

        split = layout.split()
        col = split.column()
        col.prop(yaf_mat, "glossy_color")
        exp = col.column()
        exp.enabled = yaf_mat.anisotropic == False
        exp.prop(yaf_mat, "exponent")

        col = split.column()
        sub = col.column(align=True)
        sub.prop(yaf_mat, "anisotropic")
        ani = sub.column()
        ani.enabled = yaf_mat.anisotropic == True
        ani.prop(yaf_mat, "exp_u")
        ani.prop(yaf_mat, "exp_v")
        layout.row().prop(yaf_mat, "glossy_reflect", slider=True)
        layout.row().prop(yaf_mat, "as_diffuse")

        layout.separator()

        if yaf_mat.mat_type == "coated_glossy":
            box = layout.box()
            box.label(text="Coated layer for glossy:")
            split = box.split()
            col = split.column()
            col.prop(yaf_mat, "coat_mir_col")
            col = split.column(align=True)
            col.label(text="Fresnel reflection:")
            col.prop(yaf_mat, "IOR_reflection")
            col.label()
            layout.row().prop(yaf_mat, "specular_reflect", slider=True)


class YAF_PT_glass_real(MaterialTypePanel, Panel):
    bl_label = "Real glass settings"
    material_type = 'glass', 'rough_glass'

    def draw(self, context):
        layout = self.layout
        yaf_mat = active_node_mat(context.material)

        layout.label(text="Refraction and Reflections:")
        split = layout.split()
        col = split.column()
        col.prop(yaf_mat, "IOR_refraction")

        col = split.column()
        col.menu("YAF_MT_presets_ior_list", text=bpy.types.YAF_MT_presets_ior_list.bl_label)

        split = layout.split()
        col = split.column(align=True)
        col.prop(yaf_mat, "absorption")
        col.prop(yaf_mat, "absorption_dist")

        col = split.column(align=True)
        col.label(text="Dispersion:")
        col.prop(yaf_mat, "dispersion_power")

        if yaf_mat.mat_type == "rough_glass":
            box = layout.box()
            box.label(text="Glass roughness:")
            box.row().prop(yaf_mat, "refr_roughness", slider=True)


class YAF_PT_glass_fake(MaterialTypePanel, Panel):
    bl_label = "Fake glass settings"
    material_type = 'glass', 'rough_glass'

    def draw(self, context):
        layout = self.layout
        yaf_mat = active_node_mat(context.material)

        split = layout.split()
        col = split.column()
        col.prop(yaf_mat, "filter_color")
        col = split.column()
        col.prop(yaf_mat, "glass_mir_col")
        layout.row().prop(yaf_mat, "glass_transmit", slider=True)
        layout.row().prop(yaf_mat, "fake_shadows")


class YAF_PT_blend_(MaterialTypePanel, Panel):
    bl_label = "Blend material settings"
    material_type = 'blend'

    def draw(self, context):
        layout = self.layout
        yaf_mat = active_node_mat(context.material)

        split = layout.split()
        col = split.column()
        col.label(text="")
        col.prop(yaf_mat, "blend_value", slider=True)

        layout.separator()

        box = layout.box()
        box.label(text="Choose the two materials you wish to blend.")

        #old blend material Enum properties - deprecated
        #split = box.split()
        #col = split.column()
        #col.label(text="Material one:")
        #col.prop(yaf_mat, "material1", text="")

        #col = split.column()
        #col.label(text="Material two:")
        #col.prop(yaf_mat, "material2", text="")

        split = box.split()
        col = split.column()
        col.label(text="Material one:")
        col.prop(yaf_mat, "material1name", text="")

        col = split.column()
        col.label(text="Material two:")
        col.prop(yaf_mat, "material2name", text="")



if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
