import bpy
from bpy.props import *
Scene = bpy.types.Scene


Scene.AA_min_samples = IntProperty(attr="AA_min_samples",
                        description = "Minin samples for pase",
                        default = 1)
Scene.AA_inc_samples = IntProperty(attr="AA_inc_samples",
                        description = "Increment samples per passes",
                        default = 1)
Scene.AA_passes =      IntProperty(attr="AA_passes",
                        description = "Number of passes",
                        default = 1)
Scene.AA_threshold =   FloatProperty(attr="AA_threshold",
                        description = "",
                        default = 0.05, precision = 4)
Scene.AA_pixelwidth =  FloatProperty(attr="AA_pixelwidth",
                        description = "",
                        default = 1.5)
Scene.AA_filter_type = EnumProperty(attr="AA_filter_type",
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

	@classmethod
	def poll(self, context):
		engine = context.scene.render.engine
		return (True  and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):

		layout = self.layout
		split = layout.split()
		col = split.column()

		col.prop(context.scene,"AA_min_samples", text= "AA Samples")
		col.prop(context.scene,"AA_inc_samples", text= "AA Inc. Samples")
		col.prop(context.scene,"AA_passes", text= "AA Passes")
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
