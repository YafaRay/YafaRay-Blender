

import bpy
from bpy.props import *
Material = bpy.types.Material

Material.mat_type = EnumProperty(attr="mat_type",
	items = (
		("Material Types","Material Types",""),
		("shinydiffusemat","Shinydiffusemat",""),
		("glossy","Glossy",""),
		("coated_glossy","Coated Glossy",""),
		("glass","Glass",""),
		("rough_glass","Rough Glass",""),
		("blend","Blend",""),
),default="shinydiffusemat")
Material.mat_color = 		FloatVectorProperty(attr="mat_color",
                                                    description = "Color Settings",
                                                    default = (0.7,0.7,0.7), # not more blue....
                                                    subtype = "COLOR", step = 1,
                                                    precision = 2, min = 0.0, max = 1.0,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_mirror_color = 	FloatVectorProperty(attr="mat_mirror_color",
                                                    description = "Color Settings",
                                                    default = (0.7,0.7,0.7),
                                                    subtype = "COLOR", step = 1,
                                                    precision = 2, min = 0.0, max = 1.0,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_diffuse_reflect = 	FloatProperty(attr="mat_diffuse_reflect",
                                                    description = "",
                                                    min = 0.0, max = 1.0,
                                                    default = 1.0, step = 1,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_mirror_strength = 	FloatProperty(attr="mat_mirror_strength",
                                                    description = "",
                                                    min = 0.0, max = 1.0,
                                                    default = 0.0, step = 1,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_transparency = 	FloatProperty(attr="mat_transparency",
                                                    description = "",
                                                    min = 0.0, max = 1.0,
                                                    default = 0.0, step = 1,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_translucency = 	FloatProperty(attr="mat_translucency",
                                                    description = "",
                                                    min = 0.0, max = 1.0,
                                                    default = 0.0, step = 1,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_transmit_filter = 	FloatProperty(attr="mat_transmit_filter",
                                                    description = "",
                                                    min = 0.0, max = 1.0,
                                                    default = 1.0, step = 1,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_emit = 			FloatProperty(attr="mat_emit",
                                                    description = "",
                                                    min = 0.0, max = 1.0,
                                                    default = 0.0, step = 1,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_fresnel_effect = BoolProperty(attr="mat_fresnel_effect",
                                                    description = "",
                                                    default = False)
Material.mat_brdf_type = EnumProperty(attr="mat_brdf_type",
	items = (
		("BRDF Type","BRDF Type",""),
		("Oren-Nayar","Oren-Nayar",""),
		("Normal (Lambert)","Normal (Lambert)",""),
),default="Normal (Lambert)")

Material.mat_diff_color = 	FloatVectorProperty(attr="mat_diff_color",
                                                    description = "Color Settings",
                                                    subtype = "COLOR",
                                                    min = 0.0, max = 1.0,
                                                    default = (0.7,0.7,0.7), step = 1,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_glossy_color = 	FloatVectorProperty(attr="mat_glossy_color",
                                                    description = "Color Settings",
                                                    subtype = "COLOR",
                                                    min = 0.0, max = 1.0,
                                                    default = (0.7,0.7,0.7),step = 1,
                                                    precision = 2, 
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_glossy_reflect = 	FloatProperty(attr="mat_glossy_reflect",
                                                    description = "",
                                                    min = 0.0, max = 1.0,
                                                    default = 0.0, step = 1,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_exp_u = 		FloatProperty(attr="mat_exp_u",
                                                    description = "",
                                                    min = 1.0, max = 5000.0,
                                                    default = 50.0, step = 10,
                                                    precision = 2,
                                                    soft_min = 1.0, soft_max = 500.0)
Material.mat_exp_v = 		FloatProperty(attr="mat_exp_v",
                                                    description = "",
                                                    min = 1.0, max = 5000.0,
                                                    default = 50.0, step = 10,
                                                    precision = 2,
                                                    soft_min = 1.0, soft_max = 500.0)
Material.mat_exponent = 	FloatProperty(attr="mat_exponent",
                                                    description = "",
                                                    min = 1.0, max = 500.0,
                                                    default = 50.0, step = 10,
                                                    precision = 2,
                                                    soft_min = 1.0, soft_max = 500.0)
Material.mat_alpha = 		FloatProperty(attr="mat_alpha",
                                                    description = "",
                                                    min = 0.0, max = 1.0,
                                                    default = 0.2, step = 1,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_as_diffuse = 	BoolProperty(attr="mat_as_diffuse",
                                                    description = "",
                                                    default = False)
#FloatVectorProperty(attr="mat_anisotropic",description = "Color Settings", subtype = "COLOR", step = 1, precision = 2, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)
Material.mat_anisotropic = 	BoolProperty(attr="mat_anisotropic", 
                                                    description = "",
                                                    default = False)
Material.mat_ior = 			FloatProperty(attr="mat_ior",
                                                    description = "",
                                                    min = 1.0, max = 30.0,
                                                    default = 1.0, step = 10,
                                                    precision = 2,
                                                    soft_min = 1.0, soft_max = 30.0)
Material.mat_absorp_color = 	FloatVectorProperty(attr="mat_absorp_color",
                                                    description = "Color Settings", subtype = "COLOR",
                                                    min = 0.0, max = 1.0,
                                                    default = (0.7,0.7,0.5), step = 1,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_absorp_distance = 	FloatProperty(attr="mat_absorp_distance",
                                                    description = "",
                                                    min = 1.0, max = 100.0,
                                                    default = 1.0, step = 3,
                                                    precision = 2,
                                                    soft_min = 1.0, soft_max = 100.0)
Material.mat_filter_color = 	FloatVectorProperty(attr="mat_filter_color",
                                                    description = "Color Settings", subtype = "COLOR",
                                                    min = 0.0, max = 1.0,
                                                    default = (0.7,0.7,0.6),step = 1,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_dispersion_power = FloatProperty(attr="mat_dispersion_power",
                                                    description = "",
                                                    min = 0.0, max = 1000.0,
                                                    default = 0.0, step = 20,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1000.0)
Material.mat_fake_shadows = 	BoolProperty(attr="mat_fake_shadows", 
                                                    description = "", 
                                                    default = False)
Material.mat_blend_value = 		FloatProperty(attr="mat_blend_value",
                                                    description = "",
                                                    min = 0.0, max = 1.0,
                                                    default = 0.3, step = 1,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_sigma = 			FloatProperty(attr="mat_sigma",
                                                    description = "",
                                                    min = 0.0, max = 1.0,
                                                    default = 0.1, step = 1,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1.0)
Material.mat_specular_reflect = FloatProperty(attr="mat_specular_reflect",
                                                    description = "",
                                                    min = 0.0, max = 1.0,
                                                    default = 0.0, step = 1,
                                                    precision = 2,
                                                    soft_min = 0.0, soft_max = 1.0)



class YAF_PT_material(bpy.types.Panel):

        bl_label = 'YafaRay Material'
        bl_space_type = 'PROPERTIES'
        bl_region_type = 'WINDOW'
        bl_context = 'material'
        COMPAT_ENGINES =['YAFA_RENDER']

        @classmethod
        def poll(self, context):

                engine = context.scene.render.engine

                import properties_material

                if (context.material and  (engine in self.COMPAT_ENGINES) ) :
                        try :
                                properties_material.unregister()
                        except: 
                                pass
                else:
                        try:
                                properties_material.register()
                        except: 
                                pass
                return ( (context.material or context.object) and  (engine in self.COMPAT_ENGINES) ) 


        def draw(self, context):
                
                layout = self.layout

                mat = context.material
                ob = context.object
                slot = context.material_slot
                space = context.space_data
                #wide_ui = context.region.width > narrowui
        
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

                #layout = self.layout
                split = layout.split()
                col = split.column()
                #
                #ob  = context.object
                yaf_mat = context.material
                #slot = context.material_slot
                #
                #
                #
                split = col.split(percentage=0.65)
                if ob:
                       split.template_ID(ob, "active_material", new="material.new")
                       #row = split.row()
                       #if slot:
                       #       row.prop(slot, "link", text="")
                       #else:
                       #       row.label()
                elif mat:
                        split.template_ID(space, "pin_id")
                        split.separator()
                
                col.separator()
                       
                
                col.prop(context.material,"mat_type", text= "Material Types")
                
                if yaf_mat.mat_type == 'shinydiffusemat':
                    col.prop(yaf_mat,"mat_color", text= "Color")
                    col.prop(yaf_mat,"mat_mirror_color", text= "Mirror Color")
                    col.separator()
                    col.prop(yaf_mat,"mat_diffuse_reflect", text= "Diffuse Reflection", slider = True)
                    col.prop(yaf_mat,"mat_specular_reflect", text= "Specular Reflection", slider = True)
                    col.prop(yaf_mat,"mat_mirror_strength", text= "Mirror Strength", slider = True)
                    col.prop(yaf_mat,"mat_transparency", text= "Transparency", slider = True)
                    col.prop(yaf_mat,"mat_translucency", text= "Translucency", slider = True)
                    col.prop(yaf_mat,"mat_transmit_filter", text= "Transmit Filter", slider = True)
                    col.prop(yaf_mat,"mat_emit", text= "Emit", slider = True)
                    col.prop(yaf_mat,"mat_fresnel_effect", text= "Fresnel Effect")
                    if yaf_mat.mat_fresnel_effect:
                        col.prop(yaf_mat,"mat_ior", text= "IOR", slider = True)
                    col.prop(yaf_mat,"mat_brdf_type", text= "BRDF Type")    
                    if yaf_mat.mat_brdf_type == "Oren-Nayar":
                        col.prop(yaf_mat,"mat_sigma", text= "Sigma", slider = True)                        
                
                
                if yaf_mat.mat_type == 'glossy':
                    col.prop(yaf_mat,"mat_diff_color", text= "Diffuse Color")
                    col.prop(yaf_mat,"mat_glossy_color", text= "Glossy Color")
                    col.separator()
                    col.prop(yaf_mat,"mat_diffuse_reflect", text= "Diffuse Reflection", slider = True)
                    col.prop(yaf_mat,"mat_glossy_reflect", text= "Glossy Reflection", slider = True)
                    col.prop(yaf_mat,"mat_anisotropic", text= "Anisotropic")

                    if yaf_mat.mat_anisotropic == True:
                        col.prop(yaf_mat,"mat_exp_u", text= "Exponent U", slider = True)
                        col.prop(yaf_mat,"mat_exp_v", text= "Exponent V", slider = True)
                    else:
                        col.prop(yaf_mat,"mat_exponent", text= "Exponent", slider = True)

                    col.prop(yaf_mat,"mat_as_diffuse", text= "As Diffuse")
                    col.prop(yaf_mat,"mat_brdf_type", text= "BRDF Type")
                    if yaf_mat.mat_brdf_type == "Oren-Nayar":
                        col.prop(yaf_mat,"mat_sigma", text= "Sigma", slider = True)
                
                if yaf_mat.mat_type == 'coated_glossy':
                    col.prop(yaf_mat,"mat_diff_color", text= "Diffuse Color")
                    col.prop(yaf_mat,"mat_glossy_color", text= "Glossy Color")
                    col.separator()
                    col.prop(yaf_mat,"mat_diffuse_reflect", text= "Diffuse Reflection", slider = True)
                    col.prop(yaf_mat,"mat_glossy_reflect", text= "Glossy Reflection", slider = True)
                    col.prop(yaf_mat,"mat_anisotropic", text= "Anisotropic")
                    if yaf_mat.mat_anisotropic == True:
                        col.prop(yaf_mat,"mat_exp_u", text= "Exponent U", slider = True)
                        col.prop(yaf_mat,"mat_exp_v", text= "Exponent V", slider = True)
                    else:
                        col.prop(yaf_mat,"mat_exponent", text= "Exponent", slider = True)
                        
                    col.prop(yaf_mat,"mat_as_diffuse", text= "As Diffuse")
                    col.prop(yaf_mat,"mat_ior", text= "IOR", slider = True)
                
                if yaf_mat.mat_type == 'glass':
                    col.prop(yaf_mat,"mat_absorp_color", text= "Absorption Color")
                    col.prop(yaf_mat,"mat_filter_color", text= "Filter Color")
                    col.prop(yaf_mat,"mat_mirror_color", text= "Mirror Color")
                    col.separator()
                    col.prop(yaf_mat,"mat_ior", text= "IOR", slider = True)
                    col.prop(yaf_mat,"mat_absorp_distance", text= "Absorption Distance", slider = True)
                    col.prop(yaf_mat,"mat_transmit_filter", text= "Transmit Filter", slider = True)
                    col.prop(yaf_mat,"mat_dispersion_power", text= "Dispersion Power", slider = True)
                    #col.prop(yaf_mat,"mat_exponent", text= "Exponent", slider = True)
                    col.prop(yaf_mat,"mat_fake_shadows", text= "Fake Shadows")
                
                if yaf_mat.mat_type == 'rough_glass':
                    col.prop(yaf_mat,"mat_absorp_color", text= "Absorption Color")
                    col.prop(yaf_mat,"mat_filter_color", text= "Filter Color")
                    col.prop(yaf_mat,"mat_mirror_color", text= "Mirror Color")
                    col.separator()
                    col.prop(yaf_mat,"mat_absorp_distance", text= "Absorption Distance", slider = True)
                    col.prop(yaf_mat,"mat_ior", text= "IOR", slider = True)
                    col.prop(yaf_mat,"mat_transmit_filter", text= "Transmit Filter", slider = True)
                    col.prop(yaf_mat,"mat_dispersion_power", text= "Dispersion Power", slider = True)
                    col.prop(yaf_mat,"mat_exponent", text= "Exponent", slider = True)
                    col.prop(yaf_mat,"mat_alpha", text= "Alpha", slider = True)
                    col.prop(yaf_mat,"mat_fake_shadows", text= "Fake Shadows")
                
                if yaf_mat.mat_type == 'blend':
                    col.prop(yaf_mat,"mat_blend_value", text= "Blend Value", slider = True)
                       
                    values = [("Material One","Material One", "")]
                    for item in bpy.data.materials:
                        values.append((item.name,item.name,""))
                       
                        var = tuple(values)
                       
                    values = [("Material Two","Material Two", "")]
                    for item in bpy.data.materials:
                        values.append((item.name,item.name,""))
                               
                    var2 = tuple(values)
                       
                    #if not hasattr(yaf_mat,'mat_material_one') :
                    Material.mat_material_one = EnumProperty(attr="mat_material_one", items = var, default = item.name)
                    Material.mat_material_two = EnumProperty(attr="mat_material_two", items = var2, default = item.name)
                       
                    col.prop(yaf_mat,"mat_material_one", text= "Material One")
                    col.prop(yaf_mat,"mat_material_two", text= "Material Two")



classes = [
	YAF_PT_material,
]

def register():
	register = bpy.types.register
	for cls in classes:
		register(cls)


def unregister():
	unregister = bpy.types.unregister
	for cls in classes:
		unregister(cls)


if __name__ == "__main__":
	register()

