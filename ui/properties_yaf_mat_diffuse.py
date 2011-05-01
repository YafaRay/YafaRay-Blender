import bpy
from yafaray.ui.properties_yaf_material import YAF_MaterialButtonsPanel
from yafaray.ui.ior_values import *


def draw_generator(ior_n):
    def draw(self, context):
        sl = self.layout
        for values in ior_n:
            ior_name, ior_index = values
            sl.operator('material.set_ior_preset', text = ior_name).index = ior_index
    return draw

submenus = []
for ior_group, ior_n in ior_list:
    submenu_idname = 'YAF_MT_presets_ior_list_cat%d' % len(submenus)
    submenu = type(
        submenu_idname,
        (bpy.types.Menu,),
        {
            'bl_idname': submenu_idname,
            'bl_label': ior_group,
            'draw': draw_generator(ior_n)
        }
    )
    bpy.utils.register_class(submenu)
    submenus.append(submenu)


class YAF_MT_presets_ior_list(bpy.types.Menu):
    bl_label = 'IOR Presets'

    def draw(self, context):
        sl = self.layout
        for sm in submenus:
            sl.menu(sm.bl_idname)


class YAF_PT_material_panel_diffuse(YAF_MaterialButtonsPanel, bpy.types.Panel):
        bl_label = ' '
        bl_space_type = 'PROPERTIES'
        bl_region_type = 'WINDOW'
        bl_context = 'material'
        COMPAT_ENGINES = ['YAFA_RENDER']

        def draw(self, context):
                layout = self.layout
                yaf_mat = context.material

                if yaf_mat.mat_type == 'shinydiffusemat':
                    self.bl_label = "Diffuse reflection"
                    split = layout.split()
                    col = split.column()
                    col.prop(yaf_mat, "diffuse_color", text= "Diffuse color")
                    col.prop(yaf_mat, "emit", text= "Emit")
                    layout.row().prop(yaf_mat, "diffuse_reflect", text= "Reflection stength", slider = True)

                    col = split.column()
                    sub = col.column()
                    sub.label(text = "Reflectance model:")
                    sub.prop(yaf_mat, "brdf_type", text= "")
                    brdf = sub.column()
                    brdf.enabled = yaf_mat.brdf_type == "oren-nayar"
                    brdf.prop(yaf_mat, "sigma", text = "Sigma")

                    layout.separator()

                    box = layout.box()
                    box.label(text = "Transparency and translucency:")
                    split = box.split()
                    col = split.column()
                    col.prop(yaf_mat, "transparency", text= "Transparency", slider = True)
                    col = split.column()
                    col.prop(yaf_mat, "translucency", text= "Translucency")
                    box.row().prop(yaf_mat, "transmit_filter", text= "Transmit filter", slider = True)

                if yaf_mat.mat_type == 'glossy' or yaf_mat.mat_type == 'coated_glossy':
                    self.bl_label = 'Diffuse reflection'
                    split = layout.split()
                    col = split.column()
                    col.prop(yaf_mat, "diffuse_color", text= "Diffuse Color")

                    col = split.column()
                    ref = col.column(align = True)
                    ref.label(text = "Reflectance model:")
                    ref.prop(yaf_mat, "brdf_type", text = "")
                    sig = col.column()
                    sig.enabled = yaf_mat.brdf_type == 'oren-nayar'
                    sig.prop(yaf_mat, "sigma", text = "Sigma")
                    layout.row().prop(yaf_mat, "diffuse_reflect", text= "Reflection strength", slider = True)

                if yaf_mat.mat_type == 'glass' or yaf_mat.mat_type == 'rough_glass':
                    self.bl_label = 'Real glass settings'
                    layout.label(text = "Refraction and Reflections:")
                    split = layout.split()
                    col = split.column()
                    col.prop(yaf_mat, "IOR_refraction", text = "IOR")

                    col = split.column()
                    col.menu("YAF_MT_presets_ior_list", text = bpy.types.YAF_MT_presets_ior_list.bl_label)

                    split = layout.split()
                    col = split.column(align = True)
                    col.prop(yaf_mat, "absorption", text = "Color and Absorption")
                    col.prop(yaf_mat, "absorption_dist", text = "Abs. Distance")

                    col = split.column(align = True)
                    col.label(text = "Dispersion:")
                    col.prop(yaf_mat, "dispersion_power", text = "Disp. Power")

                    if yaf_mat.mat_type == 'rough_glass':
                        box = layout.box()
                        box.label(text = "Glass roughness:")
                        box.row().prop(yaf_mat, "refr_roughness", text = "Exponent", slider = True)

                if yaf_mat.mat_type == 'blend':
                    self.bl_label = "Blend Material Settings"
                    split = layout.split()
                    col = split.column()
                    col.label(text = "")
                    col.prop(yaf_mat, "blend_value", text= "Blend value", slider = True)

                    layout.separator()

                    box = layout.box()
                    box.label(text = "Choose the two materials you wish to blend.")
                    split = box.split()
                    col = split.column()
                    col.label(text = "Material One:")
                    col.prop_search(yaf_mat, "material1", bpy.data, 'materials', text = "")

                    col = split.column()
                    col.label(text = "Material Two:")
                    col.prop_search(yaf_mat, "material2", bpy.data, 'materials', text = "")
