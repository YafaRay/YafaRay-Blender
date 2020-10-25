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
from ..ui.ior_values import ior_list
from bpy.types import Panel, Menu, NodeTree, NodeSocket
from bl_ui.properties_material import (MaterialButtonsPanel)
from bpy_extras.node_utils import find_node_input
import bpy

def blend_one_draw(layout, mat):
    try:
        layout.prop_search(mat, "material1name", bpy.data, "materials")
    except:
        return False
    
    return True

def blend_two_draw(layout, mat):
    try:
        layout.prop_search(mat, "material2name", bpy.data, "materials")
    except:
        return False
    return True


class YAFARAY4_PT_MaterialTypePanel(MaterialButtonsPanel, Panel):
    bl_label = ""
    bl_options = {'HIDE_HEADER'}
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):
        yaf_mat = context.material
        engine = context.scene.render.engine
        return yaf_mat and (yaf_mat.mat_type in cls.material_type) and (engine in cls.COMPAT_ENGINES)

def panel_node_draw(layout, ntree, _output_type, input_name):
    node = ntree.get_output_node('ALL')

    if node:
        input = find_node_input(node, input_name)
        if input:
            layout.template_node_view(ntree, node, input)
        else:
            layout.label(text="Incompatible output node")
    else:
        layout.label(text="No output node")


class YAFARAY4_PT_context_material(MaterialButtonsPanel, Panel):
    bl_label = ""
    bl_options = {'HIDE_HEADER'}
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

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

        if yaf_mat:
            layout.prop(yaf_mat, "use_nodes", icon='NODETREE')
            layout.separator()

        if ob:
            row = layout.row()
            row.template_list("MATERIAL_UL_matslots", "", ob, "material_slots", ob, "active_material_index", rows=2)

            col = row.column(align=True)
            col.operator("object.material_slot_add", icon='ADD', text="")
            col.operator("object.material_slot_remove", icon='REMOVE', text="")

            # TODO: code own operators to copy yaf material settings...
            col.menu("MATERIAL_MT_context_menu", icon='DOWNARROW_HLT', text="")

            if ob.mode == 'EDIT':
                row = layout.row(align=True)
                row.operator("object.material_slot_assign", text="Assign")
                row.operator("object.material_slot_select", text="Select")
                row.operator("object.material_slot_deselect", text="Deselect")

        split = layout.split(factor=0.75)

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


class YAFARAY4_MATERIAL_PT_preview(MaterialButtonsPanel, Panel):
    bl_label = "Preview"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        self.layout.template_preview(context.material)

class YAFARAY4_PT_preview_controls(MaterialButtonsPanel, Panel):
    bl_label = "Preview Controls"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    #bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        scene = context.scene
        self.layout.prop(context.scene.yafaray.preview, "enable", text="")
    
    def draw(self, context):
        if context.scene.yafaray.preview.enable:
            layout = self.layout
            yaf_mat = context.material
            split = layout.split() 
            col = split.column()
            col.label(text="Preview dynamic rotation/zoom")
            split = layout.split() 
            col = split.column()
            col.prop(context.scene.yafaray.preview, "camRot", text="")
            col = split.column()
            row = col.row()
            #FIXME DAVID! row.operator("preview.camzoomout", text='Zoom Out', icon='ZOOM_OUT')
            col2 = row.column()
            #FIXME DAVID! col2.operator("preview.camzoomin", text='Zoom In', icon='ZOOM_IN')
            row = col.row()
            row.label(text="")
            row = col.row()
            #FIXME DAVID! row.operator("preview.camrotreset", text='Reset dynamic rotation/zoom')
            split = layout.split() 
            col = split.column()
            col.label(text="Preview object control")
            split = layout.split()
            col = split.column()
            col.prop(context.scene.yafaray.preview, "objScale", text="Scale")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "rotZ", text="Z Rotation")
            col = split.column()
            col.prop_search(context.scene.yafaray.preview, "previewObject", bpy.data, "objects", text="")
            split = layout.split() 
            col = split.column()
            col.label(text="Preview lights control")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "lightRotZ", text="lights Z Rotation")
            split = layout.split()
            col = split.column()
            col.label(text="Key light:")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "keyLightPowerFactor", text="Power factor")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "keyLightColor", text="")
            split = layout.split() 
            col = split.column()
            col.label(text="Fill lights:")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "fillLightPowerFactor", text="Power factor")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "fillLightColor", text="")
            split = layout.split() 
            col = split.column()
            col.label(text="Preview scene control")
            split = layout.split()
            col = split.column()
            col.prop(context.scene.yafaray.preview, "previewRayDepth", text="Ray Depth")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "previewAApasses", text="AA samples")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "previewBackground", text="")


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
    submenu_idname = 'YAFARAY4_MT_presets_ior_list_cat%d' % len(submenus)
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


class YAFARAY4_MT_presets_ior_list(Menu):
    bl_label = "Glass"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        sl = self.layout
        for sm in submenus:
            sl.menu(sm.bl_idname)


class YAFARAY4_PT_shinydiffuse_diffuse(YAFARAY4_PT_MaterialTypePanel):
    bl_label = "Diffuse reflection"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    material_type = 'shinydiffusemat'

    def draw(self, context):
        layout = self.layout
        yaf_mat = context.material

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


class YAFARAY4_PT_shinydiffuse_specular(YAFARAY4_PT_MaterialTypePanel):
    bl_label = "Specular reflection"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    material_type = 'shinydiffusemat'

    def draw(self, context):
        layout = self.layout
        yaf_mat = context.material

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


class YAFARAY4_PT_glossy_diffuse(YAFARAY4_PT_MaterialTypePanel):
    bl_label = "Diffuse reflection"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    material_type = 'glossy', 'coated_glossy'

    def draw(self, context):
        layout = self.layout
        yaf_mat = context.material

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


class YAFARAY4_PT_glossy_specular(YAFARAY4_PT_MaterialTypePanel):
    bl_label = "Specular reflection"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    material_type = 'glossy', 'coated_glossy'

    def draw(self, context):
        layout = self.layout
        yaf_mat = context.material

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


class YAFARAY4_PT_glass_real(YAFARAY4_PT_MaterialTypePanel):
    bl_label = "Real glass settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    material_type = 'glass', 'rough_glass'

    def draw(self, context):
        layout = self.layout
        yaf_mat = context.material

        layout.label(text="Refraction and Reflections:")
        split = layout.split()
        col = split.column()
        col.prop(yaf_mat, "IOR_refraction")

        col = split.column()
        col.menu("YAFARAY4_MT_presets_ior_list", text=bpy.types.YAFARAY4_MT_presets_ior_list.bl_label)

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
        

class YAFARAY4_PT_glass_fake(YAFARAY4_PT_MaterialTypePanel):
    bl_label = "Fake glass settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    material_type = 'glass', 'rough_glass'

    def draw(self, context):
        layout = self.layout
        yaf_mat = context.material

        split = layout.split()
        col = split.column()
        col.prop(yaf_mat, "filter_color")
        col = split.column()
        col.prop(yaf_mat, "glass_mir_col")
        layout.row().prop(yaf_mat, "glass_transmit", slider=True)
        layout.row().prop(yaf_mat, "fake_shadows")


class YAFARAY4_PT_blend(YAFARAY4_PT_MaterialTypePanel):
    bl_label = "Blend material settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    material_type = 'blend'

    def draw(self, context):
        layout = self.layout
        yaf_mat = context.material

        split = layout.split()
        col = split.column()
        col.label(text="")
        col.prop(yaf_mat, "blend_value", slider=True)

        layout.separator()

        box = layout.box()
        box.label(text="Choose the two materials you wish to blend.")

        blend_one_draw(layout, yaf_mat)
        blend_two_draw(layout, yaf_mat)


class YAFARAY4_PT_ZWireframe(MaterialButtonsPanel, Panel):
    bl_label = "Wireframe shading options"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        yaf_mat = context.material

        split = layout.split()
        col = split.column()
        col.prop(yaf_mat, "wireframe_amount", slider=True, text="Amount")
        col.prop(yaf_mat, "wireframe_color", text="")
        col = split.column()
        col.prop(yaf_mat, "wireframe_thickness", slider=True, text="Thickness")
        col.prop(yaf_mat, "wireframe_exponent", slider=True, text="Softness")


class YAFARAY4_PT_ZAdvanced(MaterialButtonsPanel, Panel):
    bl_label = "Advanced settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        yaf_mat = context.material

        layout.prop(yaf_mat, "pass_index")

        split = layout.split()
        col = split.column()
        layout.row().prop(yaf_mat, "visibility")

        split = layout.split()
        col = split.column()
        layout.row().prop(yaf_mat, "receive_shadows")
        
        if yaf_mat.mat_type == "shinydiffusemat":
            split = layout.split()
            col = split.column()
            layout.row().prop(yaf_mat, "flat_material")
            split = layout.split()
            col = split.column()
            row = layout.row()
            row.prop(yaf_mat, "transparentbias_factor")
            col = row.column()
            col.prop(yaf_mat, "transparentbias_multiply_raydepth")

        if yaf_mat.mat_type != "blend":
            split = layout.split()
            col = split.column()
            layout.row().prop(yaf_mat, "additionaldepth")

        split = layout.split()
        col = split.column()
        layout.row().prop(yaf_mat, "samplingfactor")



classes = (
    YAFARAY4_PT_context_material,
    YAFARAY4_MATERIAL_PT_preview,
    YAFARAY4_PT_preview_controls,
    YAFARAY4_MT_presets_ior_list,
    YAFARAY4_PT_shinydiffuse_diffuse,
    YAFARAY4_PT_shinydiffuse_specular,
    YAFARAY4_PT_glossy_diffuse,
    YAFARAY4_PT_glossy_specular,
    YAFARAY4_PT_glass_real,
    YAFARAY4_PT_glass_fake,
    YAFARAY4_PT_blend,
    YAFARAY4_PT_ZWireframe,
    YAFARAY4_PT_ZAdvanced,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

        
if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
