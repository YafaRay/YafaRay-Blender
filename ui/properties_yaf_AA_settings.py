import bpy


FloatProperty = bpy.types.Scene.FloatProperty
IntProperty = bpy.types.Scene.IntProperty
BoolProperty = bpy.types.Scene.BoolProperty
CollectionProperty = bpy.types.Scene.CollectionProperty
EnumProperty = bpy.types.Scene.EnumProperty
FloatVectorProperty = bpy.types.Scene.FloatVectorProperty
StringProperty = bpy.types.Scene.StringProperty
IntVectorProperty = bpy.types.Scene.IntVectorProperty


IntProperty(attr="AA_min_samples",
		default = 1)
IntProperty(attr="AA_inc_samples",
		default = 1)
IntProperty(attr="AA_passes",
		default = 1)
FloatProperty(attr="AA_threshold",
		default = 0.05, precision = 4)
FloatProperty(attr="AA_pixelwidth",
		default = 1.5)
EnumProperty(attr="AA_filter_type",
	items = (
		("AA Filter Type","AA Filter Type",""),
		("Box","Box",""),
		("Mitchell","Mitchell",""),
		("Gauss","Gauss",""),
),default="Gauss")


class YAF_PT_AA_settings(bpy.types.Panel):

	bl_label = 'AA Settings'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'render'
	COMPAT_ENGINES =['YAFA_RENDER']


	def poll(self, context):

		engine = context.scene.render.engine
		return (True  and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):
		
		self.list = [1,2,4,5]
		layout = self.layout
		split = layout.split()
		col = split.column()

		col.prop(context.scene,"AA_min_samples", text= "AA Samples")

		col.prop(context.scene,"AA_passes", text= "AA Passes")
		if context.scene.AA_passes > 1:
			col.prop(context.scene,"AA_inc_samples", text= "AA Inc. Samples")
		
		col = split.column()
		col.prop(context.scene,"AA_threshold", text= "AA Threshold")
		col.prop(context.scene,"AA_pixelwidth", text= "AA Pixelwidth")
		col.prop(context.scene,"AA_filter_type", text= "AA Filter Type")




classes = [
	YAF_PT_AA_settings,
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
