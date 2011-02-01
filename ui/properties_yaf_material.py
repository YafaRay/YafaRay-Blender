import bpy
from rna_prop_ui import PropertyPanel # need ?
from bpy.props import *

Material = bpy.types.Material

Material.mat_type = EnumProperty(
    items = (
        ("Material Types","Material Types",""),
        ("shinydiffusemat","Shinydiffusemat",""),
        ("glossy","Glossy",""),
        ("coated_glossy","Coated Glossy",""),
        ("glass","Glass",""),
        ("rough_glass","Rough Glass",""),
        ("blend","Blend","")),default="shinydiffusemat")

######## Yafaray ######                         ##### Blender values, for test link #####
Material.color =                FloatVectorProperty(
                                        description = "Color",
                                        default = (1.0, 1.0, 1.0),
                                        subtype = "COLOR", step = 1,
                                        precision = 2, min = 0.0, max = 1.0,
                                        soft_min = 0.0, soft_max = 1.0)
#Material.mirror_color =         FloatVectorProperty(
#                                        description = "Color",
#                                        default = (0.7,0.7,0.7),
#                                        subtype = "COLOR", step = 1,
#                                        precision = 2, min = 0.0, max = 1.0,
#                                        soft_min = 0.0, soft_max = 1.0)
Material.diffuse_reflect =      FloatProperty(
                                        description = "",
                                        min = 0.0, max = 1.0,
                                        default = 0.95, step = 1,
                                        precision = 2,
                                        soft_min = 0.0, soft_max = 1.0)
Material.specular_reflect =     FloatProperty(
                                        description = "",
                                        min = 0.0, max = 1.0,
                                        default = 0.0, step = 1,
                                        precision = 2,
                                        soft_min = 0.0, soft_max = 1.0)
Material.transparency =         FloatProperty(
                                        description = "",
                                        min = 0.0, max = 1.0,
                                        default = 0.0, step = 1,
                                        precision = 2,
                                        soft_min = 0.0, soft_max = 1.0)
#Material.translucency =         FloatProperty(
#                                        description = "",
#                                        min = 0.0, max = 1.0,
#                                        default = 0.0, step = 1,
#                                        precision = 2,
#                                        soft_min = 0.0, soft_max = 1.0)
Material.transmit_filter =      FloatProperty(
                                        description = "",
                                        min = 0.0, max = 1.0,
                                        default = 1.0, step = 1,
                                        precision = 2,
                                        soft_min = 0.0, soft_max = 1.0)
#Material.emit =                 FloatProperty(
#                                        description = "",
#                                        min = 0.0, max = 1.0,
#                                        default = 0.0, step = 1,
#                                        precision = 2,
#                                        soft_min = 0.0, soft_max = 1.0)
Material.fresnel_effect =   BoolProperty(
                                        description = "",
                                        default = False)
Material.brdf_type = EnumProperty(
    items = (
        ("BRDF Type", "BRDF Type", ""),
        ("oren-nayar", "Oren-Nayar", ""),
        ("lambert", "Normal (Lambert)", "")),
    default="lambert")

#Material.diffuse_color =        FloatVectorProperty(
#                                        description = "Diffuse Color",
#                                        subtype = "COLOR",
#                                        min = 0.0, max = 1.0,
#                                        default = (0.7,0.7,0.7), step = 1,
#                                        precision = 2,
#                                        soft_min = 0.0, soft_max = 1.0)
Material.glossy_reflect =       FloatProperty(
                                        description = "",
                                        min = 0.0, max = 1.0,
                                        default = 0.0, step = 1,
                                        precision = 2,
                                        soft_min = 0.0, soft_max = 1.0)
Material.exp_u =                FloatProperty(
                                        description = "",
                                        min = 1.0, max = 10000.0,
                                        default = 50.0, step = 10,
                                        precision = 2,
                                        soft_min = 1.0, soft_max = 10000.0)
Material.exp_v =                FloatProperty(
                                        description = "",
                                        min = 1.0, max = 10000.0,
                                        default = 50.0, step = 10,
                                        precision = 2,
                                        soft_min = 1.0, soft_max = 10000.0)
Material.exponent =             FloatProperty(
                                        description = "",
                                        min = 1.0, max = 10000.0,
                                        default = 50.0, step = 10,
                                        precision = 2,
                                        soft_min = 1.0, soft_max = 10000.0)
#Material.alpha =                FloatProperty(
#                                        description = "",
#                                        min = 0.0, max = 1.0,
#                                        default = 0.2, step = 1,
#                                        precision = 2,
#                                        soft_min = 0.0, soft_max = 1.0)
Material.as_diffuse =           BoolProperty(
                                        description = "",
                                        default = False)
Material.anisotropic =          BoolProperty(
                                        description = "",
                                        default = False)
Material.IOR =                  FloatProperty(
                                        description = "",
                                        min = 1.0, max = 30.0,
                                        default = 1.5, step = 1,
                                        precision = 2,
                                        soft_min = 1.0, soft_max = 30.0)
Material.absorption =           FloatVectorProperty(
                                        description = "Color Settings", subtype = "COLOR",
                                        min = 0.0, max = 1.0,
                                        default = (1.0,1.0,1.0), step = 1,
                                        precision = 2,
                                        soft_min = 0.0, soft_max = 1.0)
Material.absorption_dist =      FloatProperty(
                                        description = "",
                                        min = 1.0, max = 100.0,
                                        default = 1.0, step = 1,
                                        precision = 2,
                                        soft_min = 1.0, soft_max = 100.0)
Material.filter_color =         FloatVectorProperty(
                                        description = "Color Settings", subtype = "COLOR",
                                        min = 0.0, max = 1.0,
                                        default = (1.0, 1.0, 1.0),step = 1,
                                        precision = 2,
                                        soft_min = 0.0, soft_max = 1.0)
Material.dispersion_power =     FloatProperty(
                                        description = "",
                                        min = 0.0, max = 5.0,
                                        default = 0.0, step = 1,
                                        precision = 2,
                                        soft_min = 0.0, soft_max = 5.0)
Material.fake_shadows =         BoolProperty(
                                        description = "",
                                        default = False)
Material.blend_value =          FloatProperty(
                                        description = "",
                                        min = 0.0, max = 1.0,
                                        default = 0.5, step = 3,
                                        precision = 2,
                                        soft_min = 0.0, soft_max = 1.0)
Material.sigma =                FloatProperty(
                                        description = "",
                                        min = 0.0, max = 1.0,
                                        default = 0.1, step = 1,
                                        precision = 2,
                                        soft_min = 0.0, soft_max = 1.0)
Material.rough =                BoolProperty(
                                        description = "",
                                        default = False)
Material.coated =               BoolProperty(
                                        description = "",
                                        default = False)

Material.material1 =            EnumProperty(items = [])
Material.material2 =            EnumProperty(items = [])



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
        COMPAT_ENGINES =['YAFA_RENDER']

        @classmethod
        def poll(self, context):
                engine = context.scene.render.engine
                return ( (context.material or context.object) and  (engine in self.COMPAT_ENGINES) )


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

                if context.material == None: return

                col.separator()

                col.prop(context.material,"mat_type", text= "Material Types")

                if yaf_mat.mat_type == 'shinydiffusemat':
                    col.prop(yaf_mat,"color", text= "Color")
                    col.prop(yaf_mat,"mirror_color", text= "Mirror Color")
                    col.separator()
                    col.prop(yaf_mat,"diffuse_reflect", text= "Diffuse Reflection", slider = True)
                    col.prop(yaf_mat,"specular_reflect", text= "Mirror Strength", slider = True)
                    col.prop(yaf_mat,"transparency", text= "Transparency", slider = True)
                    col.prop(yaf_mat,"translucency", text= "Translucency", slider = True) # link
                    col.prop(yaf_mat,"transmit_filter", text= "Transmit Filter", slider = True)
                    col.prop(yaf_mat,"emit", text= "Emit", slider = True) # link
                    col.prop(yaf_mat,"fresnel_effect", text= "Fresnel Effect")

                    if yaf_mat.fresnel_effect:
                        col.prop(yaf_mat, "IOR", text= "IOR", slider = True)

                    col.prop(yaf_mat, "brdf_type", text= "BRDF Type")

                    if yaf_mat.brdf_type == "oren-nayar":
                        col.prop(yaf_mat,"sigma", text= "Sigma", slider = True)

                #--------
                # delete unused code after integration
                #--------

                if yaf_mat.mat_type == 'glossy' or yaf_mat.mat_type == 'coated_glossy':
                    col.prop(yaf_mat,"diffuse_color", text= "Diffuse Color")#link, not changed in proprerty definition, for test
                    col.prop(yaf_mat,"color", text= "Glossy Color")
                    col.separator()
                    col.prop(yaf_mat,"diffuse_reflect", text= "Diffuse Reflection", slider = True)
                    col.prop(yaf_mat,"glossy_reflect", text= "Glossy Reflection", slider = True)
                    col.prop(yaf_mat,"anisotropic", text= "Anisotropic", toggle=True)

                    if yaf_mat.anisotropic == True:
                        col.prop(yaf_mat,"exp_u", text= "Exponent U", slider = True)
                        col.prop(yaf_mat,"exp_v", text= "Exponent V", slider = True)
                    else:
                        col.prop(yaf_mat,"exponent", text= "Exponent", slider = True)
                    col.prop(yaf_mat,"as_diffuse", text= "As Diffuse")

                    if yaf_mat.mat_type == 'glossy':
                        col.prop(yaf_mat,"brdf_type", text= "BRDF Type")
                        if yaf_mat.brdf_type == "oren-nayar":
                            col.prop(yaf_mat,"sigma", text= "Sigma", slider = True)
                            coated = False # created boolean property
                    else: #if yaf_mat.mat_type == 'coated_glossy': # only this part is diferent for coated
                        col.prop(yaf_mat,"IOR", text= "IOR", slider = True)
                        coated = True

                #--------
                # delete unused code
                # -------

                if yaf_mat.mat_type == 'glass' or yaf_mat.mat_type == 'rough_glass':

                    col.prop(yaf_mat,"absorption", text= "Absorption Color")
                    col.prop(yaf_mat,"filter_color", text= "Filter Color")
                    col.prop(yaf_mat,"mirror_color", text= "Mirror Color")
                    col.separator()
                    col.prop(yaf_mat,"IOR", text= "IOR", slider = True)
                    col.prop(yaf_mat,"absorption_dist", text= "Absorption Distance", slider = True)
                    col.prop(yaf_mat,"transmit_filter", text= "Transmit Filter", slider = True)
                    col.prop(yaf_mat,"dispersion_power", text= "Dispersion Power", slider = True)
                    col.prop(yaf_mat,"fake_shadows", text= "Fake Shadows")
                    rough = False # created boolean property
                    if yaf_mat.mat_type == 'rough_glass': # only this part is diferent for rough_glass
                        col.prop(yaf_mat,"exponent", text= "Exponent", slider = True)
                        col.prop(yaf_mat,"alpha", text= "Alpha", slider = True)
                        rough = True


                if yaf_mat.mat_type == 'blend':
                    col.prop(yaf_mat, "blend_value", text= "Blend Value", slider = True)

                    values = [("Material One", "Material One", "")]
                    for item in bpy.data.materials:
                        values.append((item.name, item.name,""))

                    materialList1 = tuple(values)

                    values = [("Material Two","Material Two", "")]
                    for item in bpy.data.materials:
                        values.append((item.name, item.name,""))

                    materialList2 = tuple(values)

                    Material.material1 = EnumProperty(items = materialList1)
                    Material.material2 = EnumProperty(items = materialList2)

                    col.prop(yaf_mat, "material1", text= "Material One")
                    col.prop(yaf_mat, "material2", text= "Material Two")

