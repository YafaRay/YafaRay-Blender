import bpy


FloatProperty = bpy.types.Scene.FloatProperty
IntProperty = bpy.types.Scene.IntProperty
BoolProperty = bpy.types.Scene.BoolProperty
CollectionProperty = bpy.types.Scene.CollectionProperty
EnumProperty = bpy.types.Scene.EnumProperty
FloatVectorProperty = bpy.types.Scene.FloatVectorProperty
StringProperty = bpy.types.Scene.StringProperty
IntVectorProperty = bpy.types.Scene.IntVectorProperty


BoolProperty(attr="ml_enable")
FloatVectorProperty(attr="ml_color",description = "Color Settings", subtype = "COLOR", step = 1, precision = 2, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)
FloatProperty(attr="ml_power")
IntProperty(attr="ml_samples")
BoolProperty(attr="ml_double_sided")
BoolProperty(attr="bgp_enable")
FloatProperty(attr="bgp_power")
IntProperty(attr="bgp_samples")
BoolProperty(attr="bgp_with_caustic")
BoolProperty(attr="bgp_with_diffuse")
BoolProperty(attr="bgp_photon_only")
BoolProperty(attr="vol_enable")
EnumProperty(attr="vol_region",
	items = (
		("Volume Region","Volume Region",""),
		("ExpDensity Volume","ExpDensity Volume",""),
		("Noise Volume","Noise Volume",""),
		("Uniform Volume","Uniform Volume",""),
),default="Uniform Volume")
FloatProperty(attr="vol_height")
FloatProperty(attr="vol_steepness")
FloatProperty(attr="vol_sharpness")
FloatProperty(attr="vol_cover")
FloatProperty(attr="vol_density")
FloatProperty(attr="vol_absorp")
FloatProperty(attr="vol_scatter")


class YAF_PT_object_light(bpy.types.Panel):

	bl_label = 'Object Light'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'object'
	COMPAT_ENGINES =['YAFA_RENDER']


	def poll(self, context):

		engine = context.scene.render.engine

		import properties_object

		if (True  and  (engine in self.COMPAT_ENGINES) ) :
			try :
				properties_object.unregister()
			except: 
				pass
		else:
			try:
				properties_object.register()
			except: 
				pass
		return (True  and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):

		layout = self.layout
		split = layout.split()
		col = split.column()

		col.prop(context.scene,"ml_enable", text= "Enable Meshlight", toggle = True)

		if context.scene.ml_enable:
			col.prop(context.scene,"ml_color", text= "Meshlight Color")
			col.prop(context.scene,"ml_power", text= "Power")
			col.prop(context.scene,"ml_samples", text= "Samples")
			col.prop(context.scene,"ml_double_sided", text= "Double Sided")


		col.prop(context.scene,"bgp_enable", text= "Enable Bgportallight", toggle = True)

		if context.scene.bgp_enable:
			col.prop(context.scene,"bgp_power", text= "Power")
			col.prop(context.scene,"bgp_samples", text= "Samples")
			col.prop(context.scene,"bgp_with_caustic", text= "With Caustic")

			col.prop(context.scene,"bgp_with_diffuse", text= "With Diffuse")

			col.prop(context.scene,"bgp_photon_only", text= "Photons Only")


		col.prop(context.scene,"vol_enable", text= "Enable Volume", toggle = True)

		if context.scene.vol_enable:
			col.prop(context.scene,"vol_region", text= "Volume Region")

			if context.scene.vol_region == 'ExpDensity Volume':
				col.prop(context.scene,"vol_height", text= "Height")
				col.prop(context.scene,"vol_steepness", text= "Steepness")

			if context.scene.vol_region == 'Noise Volume':
				col.prop(context.scene,"vol_sharpness", text= "Sharpness")
				col.prop(context.scene,"vol_cover", text= "Cover")
				col.prop(context.scene,"vol_density", text= "Density")

			col.prop(context.scene,"vol_absorp", text= "Absroption")
			col.prop(context.scene,"vol_scatter", text= "Scatter")




classes = [
	YAF_PT_object_light,
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
