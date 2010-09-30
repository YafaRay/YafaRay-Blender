import bpy

"""
FloatProperty = bpy.types.Scene.FloatProperty
IntProperty = bpy.types.Scene.IntProperty
BoolProperty = bpy.types.Scene.BoolProperty
CollectionProperty = bpy.types.Scene.CollectionProperty
EnumProperty = bpy.types.Scene.EnumProperty
FloatVectorProperty = bpy.types.Scene.FloatVectorProperty
StringProperty = bpy.types.Scene.StringProperty
IntVectorProperty = bpy.types.Scene.IntVectorProperty
"""

bpy.types.Scene.AA_min_samples = bpy.props.IntProperty(attr="AA_min_samples",
		min = 1, default = 1)
bpy.types.Scene.AA_inc_samples = bpy.props.IntProperty(attr="AA_inc_samples",
		min = 1, default = 1)
bpy.types.Scene.AA_passes = bpy.props.IntProperty(attr="AA_passes",
		min = 1, default = 1)
bpy.types.Scene.AA_threshold = bpy.props.FloatProperty(attr="AA_threshold",
		min = 0.0, max = 1.0, default = 0.05, precision = 4)
bpy.types.Scene.AA_pixelwidth = bpy.props.FloatProperty(attr="AA_pixelwidth",
		min = 1, default = 1.5)
bpy.types.Scene.AA_filter_type = bpy.props.EnumProperty(attr="AA_filter_type",
	items = (
		("AA Filter Type","AA Filter Type",""),
		("Box","Box",""),
		("Mitchell","Mitchell",""),
		("Gauss","Gauss",""),
		("Lanczos","Lanczos",""),
),default="Box")


class YAF_PT_AA_settings(bpy.types.Panel):

	bl_label = 'AA Settings'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'render'
	COMPAT_ENGINES =['YAFA_RENDER']

	@classmethod
	def poll(self, context):

		engine = context.scene.render.engine
		return (True  and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):
		
		self.list = [1,2,4,5]
		layout = self.layout
		split = layout.split()

		col = split.column()
		col.prop(context.scene,"AA_filter_type", text= "Filter Type")
		col.prop(context.scene,"AA_min_samples", text= "AA Samples")
		col.prop(context.scene,"AA_pixelwidth", text= "AA Pixelwidth")

		col = split.column()
		col.prop(context.scene,"AA_passes", text= "AA Passes")
		if context.scene.AA_passes > 1:
			col.prop(context.scene,"AA_inc_samples", text= "AA Inc. Samples")
			col.prop(context.scene,"AA_threshold", text= "AA Threshold")


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
