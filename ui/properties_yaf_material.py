import bpy


FloatProperty = bpy.types.Material.FloatProperty
IntProperty = bpy.types.Material.IntProperty
BoolProperty = bpy.types.Material.BoolProperty
CollectionProperty = bpy.types.Material.CollectionProperty
EnumProperty = bpy.types.Material.EnumProperty
FloatVectorProperty = bpy.types.Material.FloatVectorProperty
StringProperty = bpy.types.Material.StringProperty
IntVectorProperty = bpy.types.Material.IntVectorProperty


EnumProperty(attr="mat_type",
	items = (
		("Material Types","Material Types",""),
		("shinydiffusemat","Shinydiffusemat",""),
		("glossy","Glossy",""),
		("coated_glossy","Coated Glossy",""),
		("glass","Glass",""),
		("rough_glass","Rough Glass",""),
		("blend","Blend",""),
),default="shinydiffusemat")
FloatVectorProperty(attr="mat_color",description = "Color Settings", default = (0.2,0.3,0.8),subtype = "COLOR", step = 1, precision = 2, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)
FloatVectorProperty(attr="mat_mirror_color",description = "Color Settings",default = (0.8,0.3,0.2), subtype = "COLOR", step = 1, precision = 2, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)
FloatProperty(attr="mat_diffuse_reflect", min = 0.0, max = 1.0, default = 1.0, step = 1, precision = 2, soft_min = 0.0, soft_max = 1.0)
FloatProperty(attr="mat_mirror_strength", min = 0.0, max = 1.0, default = 0.0, step = 1, precision = 2, soft_min = 0.0, soft_max = 1.0)
FloatProperty(attr="mat_transparency", min = 0.0, max = 1.0, default = 0.0, step = 1, precision = 2, soft_min = 0.0, soft_max = 1.0)
FloatProperty(attr="mat_translucency", min = 0.0, max = 1.0, default = 0.0, step = 1, precision = 2, soft_min = 0.0, soft_max = 1.0)
FloatProperty(attr="mat_transmit_filter", min = 0.0, max = 1.0, default = 1.0, step = 1, precision = 2, soft_min = 0.0, soft_max = 1.0)
FloatProperty(attr="mat_emit", min = 0.0, max = 1.0, default = 0.0, step = 1, precision = 2, soft_min = 0.0, soft_max = 1.0)
BoolProperty(attr="mat_fresnel_effect")
EnumProperty(attr="mat_brdf_type",
	items = (
		("BRDF Type","BRDF Type",""),
		("Oren-Nayar","Oren-Nayar",""),
		("Normal (Lambert)","Normal (Lambert)",""),
),default="Normal(Lambert)")
FloatVectorProperty(attr="mat_diff_color",description = "Color Settings", subtype = "COLOR",default = (0.4,0.4,0.8), step = 1, precision = 2, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)
FloatVectorProperty(attr="mat_glossy_color",description = "Color Settings", subtype = "COLOR", default = (0.2,0.8,0.4),step = 1, precision = 2, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)
FloatProperty(attr="mat_glossy_reflect", min = 0.0, max = 1.0, default = 0.0, step = 1, precision = 2, soft_min = 0.0, soft_max = 1.0)
FloatProperty(attr="mat_exp_u", min = 1.0, max = 5000.0, default = 50.0, step = 10, precision = 2, soft_min = 1.0, soft_max = 500.0)
FloatProperty(attr="mat_exp_v", min = 1.0, max = 5000.0, default = 50.0, step = 10, precision = 2, soft_min = 1.0, soft_max = 500.0)
FloatProperty(attr="mat_exponent", min = 1.0, max = 500.0, default = 50.0, step = 10, precision = 2, soft_min = 1.0, soft_max = 500.0)
FloatProperty(attr="mat_alpha", min = 0.0, max = 1.0, default = 0.2, step = 1, precision = 2, soft_min = 0.0, soft_max = 1.0)
BoolProperty(attr="mat_as_diffuse")
#FloatVectorProperty(attr="mat_anisotropic",description = "Color Settings", subtype = "COLOR", step = 1, precision = 2, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)
BoolProperty(attr="mat_anisotropic")
FloatProperty(attr="mat_ior", min = 1.0, max = 30.0, default = 1.0, step = 10, precision = 2, soft_min = 1.0, soft_max = 30.0)
FloatVectorProperty(attr="mat_absorp_color",description = "Color Settings", subtype = "COLOR",default = (0.2,0.6,0.5), step = 1, precision = 2, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)
FloatProperty(attr="mat_absorp_distance", min = 1.0, max = 100.0, default = 1.0, step = 3, precision = 2, soft_min = 1.0, soft_max = 100.0)
FloatVectorProperty(attr="mat_filter_color",description = "Color Settings", subtype = "COLOR", default = (0.9,0.1,0.6),step = 1, precision = 2, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)
FloatProperty(attr="mat_dispersion_power", min = 0.0, max = 1000.0, default = 0.0, step = 20, precision = 2, soft_min = 0.0, soft_max = 1000.0)
BoolProperty(attr="mat_fake_shadows")
FloatProperty(attr="mat_blend_value", min = 0.0, max = 1.0, default = 0.3, step = 1, precision = 2, soft_min = 0.0, soft_max = 1.0)
FloatProperty(attr="mat_sigma", min = 0.0, max = 1.0, default = 0.1, step = 1, precision = 2, soft_min = 0.0, soft_max = 1.0)
FloatProperty(attr="mat_specular_reflect", min = 0.0, max = 1.0, default = 0.0, step = 1, precision = 2, soft_min = 0.0, soft_max = 1.0)


class YAF_PT_material(bpy.types.Panel):

        bl_label = 'YafaRay Material'
        bl_space_type = 'PROPERTIES'
        bl_region_type = 'WINDOW'
        bl_context = 'material'
        COMPAT_ENGINES =['YAFA_RENDER']


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
                #mat = context.material
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
                
                if context.material.mat_type == 'shinydiffusemat':
                       col.prop(context.material,"mat_color", text= "Color")
                       col.prop(context.material,"mat_mirror_color", text= "Mirror Color")
                       col.separator()
                       col.prop(context.material,"mat_diffuse_reflect", text= "Diffuse Reflection", slider = True)
                       col.prop(context.material,"mat_specular_reflect", text= "Specular Reflection", slider = True)
                       col.prop(context.material,"mat_mirror_strength", text= "Mirror Strength", slider = True)
                       col.prop(context.material,"mat_transparency", text= "Transparency", slider = True)
                       col.prop(context.material,"mat_translucency", text= "Translucency", slider = True)
                       col.prop(context.material,"mat_transmit_filter", text= "Transmit Filter", slider = True)
                       col.prop(context.material,"mat_emit", text= "Emit", slider = True)
                       col.prop(context.material,"mat_ior", text= "IOR", slider = True)
                       col.prop(context.material,"mat_fresnel_effect", text= "Fresnel Effect")
                
                       col.prop(context.material,"mat_brdf_type", text= "BRDF Type")
                
                
                if context.material.mat_type == 'glossy':
                       col.prop(context.material,"mat_diff_color", text= "Diffuse Color")
                       col.prop(context.material,"mat_glossy_color", text= "Glossy Color")
                       col.separator()
                       col.prop(context.material,"mat_diffuse_reflect", text= "Diffuse Reflection", slider = True)
                       col.prop(context.material,"mat_glossy_reflect", text= "Glossy Reflection", slider = True)
                       col.prop(context.material,"mat_exp_u", text= "Exponent U", slider = True)
                       col.prop(context.material,"mat_exp_v", text= "Exponent V", slider = True)
                       col.prop(context.material,"mat_exponent", text= "Exponent", slider = True)
                       col.prop(context.material,"mat_sigma", text= "Sigma", slider = True)
                       col.prop(context.material,"mat_as_diffuse", text= "As Diffuse")
                
                       col.prop(context.material,"mat_anisotropic", text= "Anisotropic")
                       col.prop(context.material,"mat_brdf_type", text= "BRDF Type")
                
                if context.material.mat_type == 'coated_glossy':
                       col.prop(context.material,"mat_diff_color", text= "Diffuse Color")
                       col.prop(context.material,"mat_glossy_color", text= "Glossy Color")
                       col.separator()
                       col.prop(context.material,"mat_diffuse_reflect", text= "Diffuse Reflection", slider = True)
                       col.prop(context.material,"mat_glossy_reflect", text= "Glossy Reflection", slider = True)
                       col.prop(context.material,"mat_exp_u", text= "Exponent U", slider = True)
                       col.prop(context.material,"mat_exp_v", text= "Exponent V", slider = True)
                       col.prop(context.material,"mat_exponent", text= "Exponent", slider = True)
                       col.prop(context.material,"mat_as_diffuse", text= "As Diffuse")
                
                       col.prop(context.material,"mat_anisotropic", text= "Anisotropic")
                       col.prop(context.material,"mat_ior", text= "IOR", slider = True)
                
                if context.material.mat_type == 'glass':
                       col.prop(context.material,"mat_absorp_color", text= "Absorption Color")
                       col.prop(context.material,"mat_filter_color", text= "Filter Color")
                       col.prop(context.material,"mat_mirror_color", text= "Absorption Color")
                       col.separator()
                       col.prop(context.material,"mat_ior", text= "IOR", slider = True)
                       col.prop(context.material,"mat_absorp_distance", text= "Absorption Distance", slider = True)
                       col.prop(context.material,"mat_transmit_filter", text= "Transmit Filter", slider = True)
                       col.prop(context.material,"mat_dispersion_power", text= "Dispersion Power", slider = True)
                       #col.prop(context.material,"mat_exponent", text= "Exponent", slider = True)
                       col.prop(context.material,"mat_fake_shadows", text= "Fake Shadows")
                
                if context.material.mat_type == 'rough_glass':
                       col.prop(context.material,"mat_absorp_color", text= "Absorption Color")
                       col.prop(context.material,"mat_filter_color", text= "Filter Color")
                       col.prop(context.material,"mat_mirror_color", text= "Absorption Color")
                       col.separator()
                       col.prop(context.material,"mat_absorp_distance", text= "Absorption Distance", slider = True)
                       col.prop(context.material,"mat_ior", text= "IOR", slider = True)
                       col.prop(context.material,"mat_transmit_filter", text= "Transmit Filter", slider = True)
                       col.prop(context.material,"mat_dispersion_power", text= "Dispersion Power", slider = True)
                       col.prop(context.material,"mat_exponent", text= "Exponent", slider = True)
                       col.prop(context.material,"mat_alpha", text= "Alpha", slider = True)
                       col.prop(context.material,"mat_fake_shadows", text= "Fake Shadows")
                
                if context.material.mat_type == 'blend':
                       col.prop(context.material,"mat_blend_value", text= "Blend Value", slider = True)
                       
                       values = [("Material One","Material One", "")]
                       for item in bpy.data.materials:
                               values.append((item.name,item.name,""))
                       
                       var = tuple(values)
                       
                       values = [("Material Two","Material Two", "")]
                       for item in bpy.data.materials:
                               values.append((item.name,item.name,""))
                               
                       var2 = tuple(values)
                       
                       #if not hasattr(context.material,'mat_material_one') :
                       EnumProperty(attr="mat_material_one", items = var, default = item.name)
                       EnumProperty(attr="mat_material_two", items = var2, default = item.name)
                       
                       col.prop(context.material,"mat_material_one", text= "Material One")
                       col.prop(context.material,"mat_material_two", text= "Material Two")




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
