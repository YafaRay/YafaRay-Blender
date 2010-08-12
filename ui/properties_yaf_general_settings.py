import bpy


FloatProperty = bpy.types.Scene.FloatProperty
IntProperty = bpy.types.Scene.IntProperty
BoolProperty = bpy.types.Scene.BoolProperty
CollectionProperty = bpy.types.Scene.CollectionProperty
EnumProperty = bpy.types.Scene.EnumProperty
FloatVectorProperty = bpy.types.Scene.FloatVectorProperty
StringProperty = bpy.types.Scene.StringProperty
IntVectorProperty = bpy.types.Scene.IntVectorProperty


IntProperty(attr="gs_ray_depth",
		default = 2)
IntProperty(attr="gs_shadow_depth",
		default = 2)
IntProperty(attr="gs_threads",
		default = 1)
FloatProperty(attr="gs_gamma",
		default = 1.8)
FloatProperty(attr="gs_gamma_input",
		default = 1.8)
IntProperty(attr="gs_tile_size",
		default = 32)
EnumProperty(attr="gs_tile_order",
	items = (
		("Tile order","Tile order",""),
		("Linear","Linear",""),
		("Random","Random",""),
),default="Random")
BoolProperty(attr="gs_auto_threads", default = True)
BoolProperty(attr="gs_clay_render")
BoolProperty(attr="gs_draw_params")
StringProperty(attr="gs_custom_string")
BoolProperty(attr="gs_auto_save")
BoolProperty(attr="gs_auto_alpha")
BoolProperty(attr="gs_premult")
BoolProperty(attr="gs_transp_shad")
BoolProperty(attr="gs_clamp_rgb")
BoolProperty(attr="gs_show_sam_pix")
BoolProperty(attr="gs_z_channel")


class YAF_PT_general_settings(bpy.types.Panel):

	bl_label = 'General Settings'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'render'
	COMPAT_ENGINES =['YAFA_RENDER']


	def poll(self, context):

		engine = context.scene.render.engine
		return (True  and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):

		layout = self.layout
		split = layout.split()
		col = split.column()

		col.prop(context.scene,"gs_ray_depth", text= "Ray Depth")
		col.prop(context.scene,"gs_shadow_depth", text= "Shadow Depth")
		if not context.scene.gs_auto_threads:
			col.prop(context.scene,"gs_threads", text= "Threads")
		
		col.prop(context.scene,"gs_gamma", text= "Gamma")
		col.prop(context.scene,"gs_gamma_input", text= "Gamma Input")
		col.prop(context.scene,"gs_tile_size", text= "Tile Size")
		col.prop(context.scene,"gs_tile_order", text= "Tile order")

		col.prop(context.scene,"gs_auto_threads", text= "Auto Threads")

		col = split.column()
		col.prop(context.scene,"gs_clay_render", text= "Clay Render")

		col.prop(context.scene,"gs_auto_save", text= "Auto Save")

		col.prop(context.scene,"gs_auto_alpha", text= "Auto Alpha")

		col.prop(context.scene,"gs_premult", text= "Premult")

		col.prop(context.scene,"gs_transp_shad", text= "Transp. Shadow")

		col.prop(context.scene,"gs_clamp_rgb", text= "Clamp RGB")

		#col.prop(context.scene,"gs_show_sam_pix", text= "Show Sam Pix")
		
		col.prop(context.scene,"gs_draw_params", text= "Draw Params")
		
		col.prop(context.scene,"gs_z_channel", text= "Render Z-buffer")
		if context.scene.gs_draw_params:
			row = layout.row()	
			row.prop(context.scene,"gs_custom_string", text= "Custom String")




classes = [
	YAF_PT_general_settings,
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
