import bpy
from bpy.props import *

Material = bpy.types.Material

Material.mat_type = EnumProperty(
    items = [
        ("shinydiffusemat", "Shiny Diffuse Material", "Assign a Material Type"),
        ("glossy", "Glossy", "Assign a Material Type"),
        ("coated_glossy", "Coated Glossy", "Assign a Material Type"),
        ("glass", "Glass", "Assign a Material Type"),
        ("rough_glass", "Rough Glass", "Assign a Material Type"),
        ("blend", "Blend", "")],  # <-- not implemented yet...
    default = "shinydiffusemat",
    name = "Material Types")

Material.diffuse_reflect =      FloatProperty(
                                        description = "Amount of diffuse reflection",
                                        min = 0.0, max = 1.0,
                                        default = 1.0, step = 1,
                                        precision = 3,
                                        soft_min = 0.0, soft_max = 1.0)
Material.specular_reflect =     FloatProperty(
                                        description = "Amount of perfect specular reflection (mirror)",
                                        min = 0.0, max = 1.0,
                                        default = 0.0, step = 1,
                                        precision = 3,
                                        soft_min = 0.0, soft_max = 1.0)
Material.transparency =         FloatProperty(
                                        description = "Material transparency",
                                        min = 0.0, max = 1.0,
                                        default = 0.0, step = 1,
                                        precision = 3,
                                        soft_min = 0.0, soft_max = 1.0)
Material.transmit_filter =      FloatProperty(
                                        description = "Amount of tinting of light passing through the Material",
                                        min = 0.0, max = 1.0,
                                        default = 1.0, step = 1,
                                        precision = 3,
                                        soft_min = 0.0, soft_max = 1.0)
Material.fresnel_effect =   BoolProperty(
                                        description = "Apply a fresnel effect to specular reflection",
                                        default = False)
Material.brdf_type = EnumProperty(
    items = (
        ("oren-nayar", "Oren-Nayar", "BRDF Shader Type"),
        ("lambert", "Normal (Lambert)", "BRDF Shader Type")),
    default = "lambert",
    name = "BRDF Type")

Material.glossy_color =         FloatVectorProperty(
                                        description = "Glossy Color",
                                        subtype = "COLOR",
                                        min = 0.0, max = 1.0,
                                        default = (1.0, 1.0, 1.0)
                                        )
Material.coat_mir_col =         FloatVectorProperty(  # added mirror col property for coated glossy material
                                        description = "Reflection color of coated layer",
                                        subtype = "COLOR",
                                        min = 0.0, max = 1.0,
                                        default = (1.0, 1.0, 1.0)
                                        )
Material.glass_mir_col =        FloatVectorProperty(  # added mirror color property for glass material
                                        description = "Reflection color of glass material",
                                        subtype = "COLOR",
                                        min = 0.0, max = 1.0,
                                        default = (1.0, 1.0, 1.0)
                                        )
Material.glossy_reflect =       FloatProperty(
                                        description = "Amount of glossy reflection",
                                        min = 0.0, max = 1.0,
                                        default = 0.0, step = 1,
                                        precision = 3,
                                        soft_min = 0.0, soft_max = 1.0)
Material.exp_u =                FloatProperty(
                                        description = "Horizontal anisotropic exponent value",
                                        min = 1.0, max = 10000.0,
                                        default = 50.0, step = 10,
                                        precision = 2,
                                        soft_min = 1.0, soft_max = 10000.0)
Material.exp_v =                FloatProperty(
                                        description = "Vertical anisotropic exponent value",
                                        min = 1.0, max = 10000.0,
                                        default = 50.0, step = 10,
                                        precision = 2,
                                        soft_min = 1.0, soft_max = 10000.0)
Material.exponent =             FloatProperty(
                                        description = "Blur of the glossy reflection, higher exponent = sharper reflections",
                                        min = 1.0, max = 10000.0,
                                        default = 500.0, step = 10,
                                        precision = 2,
                                        soft_min = 1.0, soft_max = 10000.0)
Material.as_diffuse =           BoolProperty(
                                        description = "Treat glossy component as diffuse",
                                        default = False)
Material.anisotropic =          BoolProperty(
                                        description = "Use anisotropic reflections",
                                        default = False)
Material.IOR_refraction =                  FloatProperty(  # added IOR property for refraction
                                        description = "Index of refraction",
                                        min = 0.0, max = 30.0,
                                        default = 1.52, step = 1,
                                        precision = 2,
                                        soft_min = 0.0, soft_max = 30.0)
Material.IOR_reflection =       FloatProperty(  # added IOR property for reflection
                                        description = "Fresnel reflection strength",
                                        min = 1.0, max = 30.0,
                                        default = 1.8, step = 1,
                                        precision = 2,
                                        soft_min = 1.0, soft_max = 30.0)
Material.absorption =           FloatVectorProperty(
                                        description = "Glass volumetric absorption color. White disables absorption", subtype = "COLOR",
                                        min = 0.0, max = 1.0,
                                        default = (1.0, 1.0, 1.0), step = 1,
                                        precision = 3,
                                        soft_min = 0.0, soft_max = 1.0)
Material.absorption_dist =      FloatProperty(
                                        description = "Absorption distance scale",
                                        min = 0.0, max = 100.0,
                                        default = 1.0, step = 1,
                                        precision = 3,
                                        soft_min = 0.0, soft_max = 100.0)
Material.glass_transmit =       FloatProperty(  # added transmit filter for glass material
                                        description = "Filter strength applied to refracted light",
                                        min = 0.0, max = 1.0,
                                        default = 1.0, step = 1,
                                        precision = 3, soft_min = 0.0, soft_max = 1.0)
Material.filter_color =         FloatVectorProperty(
                                        description = "Filter color for refracted light of glass, also tint transparent shadows if enabled", subtype = "COLOR",
                                        min = 0.0, max = 1.0,
                                        default = (1.0, 1.0, 1.0), step = 1,
                                        precision = 3,
                                        soft_min = 0.0, soft_max = 1.0)
Material.dispersion_power =     FloatProperty(
                                        description = "Strength of dispersion effect, disabled when 0",
                                        min = 0.0, max = 5.0,
                                        default = 0.0, step = 1,
                                        precision = 3,
                                        soft_min = 0.0, soft_max = 5.0)
Material.refr_roughness =       FloatProperty(  # added refraction roughness propertie for roughglass material
                                        description = "Roughness factor for glass material",
                                        min = 0.0, max = 1.0,
                                        default = 0.2, step = 1,
                                        precision = 3,
                                        soft_min = 0.0, soft_max = 1.0)
Material.fake_shadows =         BoolProperty(
                                        description = "Let light straight through for shadow calculation. Not to be used with dispersion",
                                        default = False)
Material.blend_value =          FloatProperty(
                                        description = "",
                                        min = 0.0, max = 1.0,
                                        default = 0.5, step = 3,
                                        precision = 3,
                                        soft_min = 0.0, soft_max = 1.0)
Material.sigma =                FloatProperty(
                                        description = "Roughness of the surface",
                                        min = 0.0, max = 1.0,
                                        default = 0.1, step = 1,
                                        precision = 5,
                                        soft_min = 0.0, soft_max = 1.0)
Material.rough =                BoolProperty(
                                        description = "",
                                        default = False)
Material.coated =               BoolProperty(
                                        description = "",
                                        default = False)
Material.material1 =            StringProperty(
                                name = "Material One",
                                description = "First Blend Material. Same material if nothing is set.",
                                default = "")
Material.material2 =            StringProperty(
                                name = "Material Two",
                                description = "Second Blend Material. Same material if nothing is set.",
                                default = "")


class YAF_MaterialButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(self, context):
        return (context.scene.render.engine in self.COMPAT_ENGINES)


class YAF_PT_material(YAF_MaterialButtonsPanel, bpy.types.Panel):
        bl_label = 'YafaRay Material'
        bl_space_type = 'PROPERTIES'
        bl_region_type = 'WINDOW'
        bl_context = 'material'
        COMPAT_ENGINES = ['YAFA_RENDER']

        @classmethod
        def poll(self, context):
                engine = context.scene.render.engine
                return ((context.material or context.object) and  (engine in self.COMPAT_ENGINES))

        def draw(self, context):
                layout = self.layout

                mat = context.material
                yaf_mat = context.material
                ob = context.object
                slot = context.material_slot
                space = context.space_data
                #wide_ui = context.region.width > narrowui

                #load preview
                layout.template_preview(context.material, True, context.material)
                layout.operator("RENDER_OT_refresh_preview", text="Refresh preview", icon="RENDER_STILL")

                if ob:
                    row = layout.row()

                    row.template_list(ob, "material_slots", ob, "active_material_index", rows=2)
                    col = row.column(align=True)
                    col.operator("object.material_slot_add", icon='ZOOMIN', text="")
                    col.operator("object.material_slot_remove", icon='ZOOMOUT', text="")
                    #col.menu("MATERIAL_MT_specials", icon='DOWNARROW_HLT', text="")

                    if ob.mode == 'EDIT':
                        row = layout.row(align=True)
                        row.operator("object.material_slot_assign", text="Assign")
                        row.operator("object.material_slot_select", text="Select")
                        row.operator("object.material_slot_deselect", text="Deselect")

                split = layout.split()
                col = split.column()

                split = col.split(percentage=0.65)
                if ob:
                    split.template_ID(ob, "active_material", new="material.new")
                    row = split.row()
                    if slot:
                        row.prop(slot, "link", text="")
                    else:
                        row.label()
                elif mat:
                    split.template_ID(space, "pin_id")
                    split.separator()

                if context.material == None:
                    return

                for i in range(4):
                    col.separator()

                col.prop(context.material, "mat_type", text= "Material Type")
                col.separator()

                # Shiny Diffuse Material Settings

                if yaf_mat.mat_type == 'shinydiffusemat':
                    split = layout.split()
                    col = split.column()
                    sub = col.column(align = True)
                    sub.label(text = "Diffuse:")
                    sub.prop(yaf_mat, "diffuse_color", text= "")  # linked to Blender Material
                    sub.prop(yaf_mat, "diffuse_reflect", text= "Diffuse Refl.", slider = True)

                    col.prop(yaf_mat, "brdf_type", text= "")
                    brdf = col.column()
                    brdf.enabled = yaf_mat.brdf_type == "oren-nayar"
                    brdf.prop(yaf_mat, "sigma", text = "Sigma", slider = True)

                    col = split.column()
                    sub = col.column(align = True)
                    sub.label(text = "")
                    sub.prop(yaf_mat, "transparency", text= "Transparency", slider = True)
                    sub.prop(yaf_mat, "translucency", text= "Translucency", slider = True)  # linked to Blender Material
                    sub.prop(yaf_mat, "transmit_filter", text= "Transmit Filter", slider = True)
                    col.prop(yaf_mat, "emit", text= "Emit", slider = True)  # linked to Blender Material

                    row = layout.row()
                    for i in range(2):
                        row.separator()

                    split = layout.split()
                    col = split.column()
                    sub = col.column(align = True)
                    sub.label(text = "Reflection:")
                    sub.prop(yaf_mat, "mirror_color", text= "")
                    sub.prop(yaf_mat, "specular_reflect", text= "Mirror Strength", slider = True)

                    col = split.column(align = True)
                    col.label(text = "")
                    col.prop(yaf_mat, "fresnel_effect", text= "Fresnel Effect")
                    sub = col.column()
                    sub.enabled = yaf_mat.fresnel_effect
                    sub.prop(yaf_mat, "IOR_reflection", text= "IOR", slider = True)

                # Glossy and Coated Glossy Material Settings

                if yaf_mat.mat_type == 'glossy' or yaf_mat.mat_type == 'coated_glossy':
                    split = layout.split()
                    col = split.column()
                    sub = col.column(align = True)
                    sub.label(text = "Diffuse:")
                    sub.prop(yaf_mat, "diffuse_color", text= "")  # linked to Blender Material
                    sub.prop(yaf_mat, "diffuse_reflect", text= "Diffuse Refl.", slider = True)

                    col = split.column()
                    sub = col.column(align = True)
                    sub.label(text = "")
                    brdf = sub.column()
                    brdf.enabled = yaf_mat.mat_type == 'glossy'
                    brdf.prop(yaf_mat, "brdf_type", text = "")
                    brdf1 = col.column()
                    brdf1.enabled = yaf_mat.brdf_type == 'oren-nayar' and yaf_mat.mat_type == 'glossy'
                    brdf1.prop(yaf_mat, "sigma", text = "Sigma", slider = True)
                    col.prop(yaf_mat, "as_diffuse", text = "As Diffuse")

                    row = layout.row()
                    for i in range(2):
                        row.separator()

                    split = layout.split()
                    col = split.column()
                    sub = col.column(align = True)
                    sub.label(text = "Reflection:")
                    sub.prop(yaf_mat, "glossy_color", text= "")
                    sub.prop(yaf_mat, "glossy_reflect", text= "Glossy Refl.", slider = True)
                    exp = sub.column()
                    exp.enabled = yaf_mat.anisotropic == False
                    exp.prop(yaf_mat, "exponent", text = "Exponent", slider = True)

                    col = split.column()
                    sub = col.column(align = True)
                    sub.label(text = "")
                    sub.prop(yaf_mat, "anisotropic", text = "Anisotropic")
                    ani = sub.column()
                    ani.enabled = yaf_mat.anisotropic == True
                    ani.prop(yaf_mat, "exp_u", text = "Exponent U", slider = True)
                    ani.prop(yaf_mat, "exp_v", text = "Exponent V", slider = True)

                    split = layout.split()
                    col = split.column()
                    mirc = col.column(align = True)
                    mirc.enabled = yaf_mat.mat_type == 'coated_glossy'
                    mirc.label(text = "Coated Layer:")
                    mirc.prop(yaf_mat, "coat_mir_col", text = "")  # mirror color for 'coated glossy' added
                    mirc.prop(yaf_mat, "IOR_reflection", text= "IOR", slider = True)  # added IOR reflection for coated glossy

                    col = split.column()
                    col.label(text = "")

                # Glass and Roughglass Material Settings
                
                if yaf_mat.mat_type == 'glass' or yaf_mat.mat_type == 'rough_glass':
                    split = layout.split()
                    col = split.column()
                    sub = col.column(align = True)
                    sub.label(text = "Refraction:")
                    sub.prop(yaf_mat, "absorption", text = "")
                    sub.prop(yaf_mat, "absorption_dist", text = "Absorption Dist.", slider = True)
                    col.prop(yaf_mat, "IOR_refraction", text = "IOR", slider = True)  # added IOR refraction for glass

                    col = split.column()
                    sub = col.column(align = True)
                    sub.label(text = "")
                    sub.prop(yaf_mat, "filter_color", text = "")
                    sub.prop(yaf_mat, "glass_transmit", text = "Transmit Filter", slider = True)  # added transmit filter propertie for glass
                    fak = col.column()
                    fak.enabled = yaf_mat.dispersion_power == 0
                    fak.prop(yaf_mat, "fake_shadows", text = "Fake Shadows")


                    for i in range(3):
                        col.separator()

                    split = layout.split()
                    col = split.column()
                    col.prop(yaf_mat, "dispersion_power", text = "Dispersion", slider = True)
                    rog = col.column()
                    rog.enabled = yaf_mat.mat_type == 'rough_glass'
                    rog.prop(yaf_mat, "refr_roughness", text = "Roughness", slider = True)  # changed alpha to refr_roughness for glass, removed exponent

                    col = split.column()
                    col.label(text = "Reflection:")
                    col.prop(yaf_mat, "glass_mir_col", text = "")  # added glass mirror color propertie for glass


                # Blend Material Settings

                if yaf_mat.mat_type == 'blend':
                    split = layout.split()
                    col = split.column()
                    col.label(text = "")
                    col.prop(yaf_mat, "blend_value", text= "Blend Value", slider = True)

                    for i in range(3):
                        col.separator()

                    box = layout.box()

                    box.label(text = "Choose the two materials you wish to blend.")
                    split = box.split()
                    col = split.column()
                    col.label(text = "Material One:")
                    col.prop_search(yaf_mat, "material1", bpy.data, 'materials', text = "")

                    col = split.column()
                    col.label(text = "Material Two:")
                    col.prop_search(yaf_mat, "material2", bpy.data, 'materials', text = "")
