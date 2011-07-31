import bpy
from yafaray.ui.properties_yaf_material import YAF_MaterialButtonsPanel
from bl_ui.properties_material import active_node_mat, check_material


class YAF_PT_material_panel_specular(YAF_MaterialButtonsPanel, bpy.types.Panel):
    bl_label = ' '
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'material'
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(cls, context):
        yaf_mat = context.material
        engine = context.scene.render.engine
        return check_material(yaf_mat) and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout
        yaf_mat = active_node_mat(context.material)

        if yaf_mat.mat_type == 'shinydiffusemat':
            self.bl_label = 'Specular reflection'
            split = layout.split()
            col = split.column()
            col.label(text = "Mirror color:")
            col.prop(yaf_mat, "mirror_color", text= "")

            col = split.column()
            col.prop(yaf_mat, "fresnel_effect", text= "Fresnel effect")
            sub = col.column()
            sub.enabled = yaf_mat.fresnel_effect
            sub.prop(yaf_mat, "IOR_reflection", text= "IOR", slider = True)
            layout.row().prop(yaf_mat, "specular_reflect", text= "Reflection stength", slider = True)

        if yaf_mat.mat_type == 'glossy' or yaf_mat.mat_type == 'coated_glossy':
            self.bl_label = 'Specular reflection'
            split = layout.split()
            col = split.column()
            col.prop(yaf_mat, "glossy_color", text= "Glossy color")
            exp = col.column()
            exp.enabled = yaf_mat.anisotropic == False
            exp.prop(yaf_mat, "exponent", text = "Exponent")

            col = split.column()
            sub = col.column(align = True)
            sub.prop(yaf_mat, "anisotropic", text = "Anisotropic")
            ani = sub.column()
            ani.enabled = yaf_mat.anisotropic == True
            ani.prop(yaf_mat, "exp_u", text = "Exponent U")
            ani.prop(yaf_mat, "exp_v", text = "Exponent V")
            layout.row().prop(yaf_mat, "glossy_reflect", text= "Reflection strength", slider = True)
            layout.row().prop(yaf_mat, "as_diffuse", text = "Use photon map")

            layout.separator()

            if yaf_mat.mat_type == 'coated_glossy':
                box = layout.box()
                box.label(text = "Coated layer for glossy:")
                split = box.split()
                col = split.column()
                col.prop(yaf_mat, "coat_mir_col", text = "Mirror color")
                col = split.column(align = True)
                col.label(text = "Fresnel reflection:")
                col.prop(yaf_mat, "IOR_reflection", text= "IOR")

        if yaf_mat.mat_type == 'glass' or yaf_mat.mat_type == 'rough_glass':
            self.bl_label = 'Fake glass settings'
            split = layout.split()
            col = split.column()
            col.prop(yaf_mat, "filter_color", text = "Filter color")
            col = split.column()
            col.prop(yaf_mat, "glass_mir_col", text = "Reflection color")
            layout.row().prop(yaf_mat, "glass_transmit", text = "Transmit Filter", slider = True)
            layout.row().prop(yaf_mat, "fake_shadows", text = "Fake Shadows")

        if yaf_mat.mat_type == 'blend':  # Blend material settings, none in panel specular
            self.bl_label = ' '
