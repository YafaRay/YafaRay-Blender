import bpy
#import types and props ---->
from bpy.props import *
Material = bpy.types.Material

Material.mat_type = EnumProperty(
    items = [
        ("shinydiffusemat", "Shiny Diffuse", "Assign a Material Type"),
        ("glossy", "Glossy", "Assign a Material Type"),
        ("coated_glossy", "Coated Glossy", "Assign a Material Type"),
        ("glass", "Glass", "Assign a Material Type"),
        ("rough_glass", "Rough Glass", "Assign a Material Type"),
        ("blend", "Blend", "")],
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
                                        name = "Fresnel Effect",
                                        description = "Apply a fresnel effect to specular reflection",
                                        default = False)
Material.brdf_type = EnumProperty(
    items = (
        ("oren-nayar", "Oren-Nayar", "Reflectance Model"),
        ("lambert", "Lambert", "Reflectance Model")),
    default = "lambert",
    name = "Reflectance Model")

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
Material.IOR_refraction =       FloatProperty(  # added IOR property for refraction
                                        description = "Index of refraction",
                                        min = 0.0, max = 30.0,
                                        default = 1.52, step = 1,
                                        precision = 3,
                                        soft_min = 0.0, soft_max = 30.0)
Material.IOR_reflection =       FloatProperty(  # added IOR property for reflection
                                        description = "Fresnel reflection strength",
                                        min = 1.0, max = 30.0,
                                        default = 1.8, step = 1,
                                        precision = 2,
                                        soft_min = 1.0, soft_max = 30.0)
Material.absorption =           FloatVectorProperty(
                                        description = "Glass volumetric absorption color. White disables absorption",
                                        min = 0.0, max = 1.0, subtype = "COLOR",
                                        default = (1.0, 1.0, 1.0)
                                        )
Material.absorption_dist =      FloatProperty(
                                        description = "Absorption distance scale",
                                        min = 0.0, max = 100.0,
                                        default = 1.0, step = 1,
                                        precision = 4,
                                        soft_min = 0.0, soft_max = 100.0)
Material.glass_transmit =       FloatProperty(  # added transmit filter for glass material
                                        description = "Filter strength applied to refracted light",
                                        min = 0.0, max = 1.0,
                                        default = 1.0, step = 1,
                                        precision = 3, soft_min = 0.0, soft_max = 1.0)
Material.filter_color =         FloatVectorProperty(
                                        description = "Filter color for refracted light of glass, also tint transparent shadows if enabled",
                                        min = 0.0, max = 1.0, subtype = "COLOR",
                                        default = (1.0, 1.0, 1.0)
                                        )
Material.dispersion_power =     FloatProperty(
                                        description = "Strength of dispersion effect, disabled when 0",
                                        min = 0.0, max = 5.0,
                                        default = 0.0, step = 1,
                                        precision = 4,
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
        engine = context.scene.render.engine
        return ((context.material or context.object) and  (engine in self.COMPAT_ENGINES))


class YAF_PT_material(YAF_MaterialButtonsPanel, bpy.types.Panel):
        bl_label = 'YafaRay Material'
        bl_space_type = 'PROPERTIES'
        bl_region_type = 'WINDOW'
        bl_context = 'material'
        COMPAT_ENGINES = ['YAFA_RENDER']

        def draw(self, context):
                layout = self.layout

                mat = context.material
                yaf_mat = context.material
                ob = context.object
                slot = context.material_slot
                space = context.space_data
                #load preview
                layout.template_preview(context.material, True, context.material)
                layout.operator("RENDER_OT_refresh_preview", text="Refresh preview", icon="RENDER_STILL")

                if ob:
                    row = layout.row()

                    row.template_list(ob, "material_slots", ob, "active_material_index", rows=2)
                    col = row.column(align=True)
                    col.operator("object.material_slot_add", icon='ZOOMIN', text="")
                    col.operator("object.material_slot_remove", icon='ZOOMOUT', text="")

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

                layout.separator()
                layout.prop(context.material, "mat_type", text = 'Material type')
