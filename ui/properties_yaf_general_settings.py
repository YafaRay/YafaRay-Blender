
import bpy
# import all props 
from bpy.props import *

Scene = bpy.types.Scene

Scene.gs_ray_depth =    IntProperty(attr="gs_ray_depth",
                        description = "Depth of Raytrace", # for description tooltips
                        default = 2)
Scene.gs_shadow_depth = IntProperty(attr="gs_shadow_depth",
                        description = "",
                        default = 2)
Scene.gs_threads =      IntProperty(attr="gs_threads",
                        description = "",
                        default = 1)
Scene.gs_gamma =        FloatProperty(attr="gs_gamma",
                        default = 1.8)
Scene.gs_gamma_input =  FloatProperty(attr="gs_gamma_input",
                        description = "",
                        default = 1.8)
Scene.gs_tile_size =    IntProperty(attr="gs_tile_size",
                        description = "",
                        default = 32)
Scene.gs_tile_order =   EnumProperty(attr="gs_tile_order",
	items = (
		("Tile order","Tile order",""),
		("Linear","Linear",""),
		("Random","Random",""),
),default="Random")
Scene.gs_auto_threads = BoolProperty(attr="gs_auto_threads",
                        description = "", 
                        default = True)
Scene.gs_clay_render =  BoolProperty(attr="gs_clay_render",
                        description = "",
                        default = False)
Scene.gs_draw_params =  BoolProperty(attr="gs_draw_params",
                        description = "",
                        default = False)
Scene.gs_custom_string = StringProperty(attr="gs_custom_string",
                        description = "",
                        default = "")
Scene.gs_auto_save =    BoolProperty(attr="gs_auto_save",
                        description = "",
                        default = False)
Scene.gs_auto_alpha =   BoolProperty(attr="gs_auto_alpha",
                        description = "",
                        default = False)
Scene.gs_premult =      BoolProperty(attr="gs_premult",
                        description = "",
                        default = False)
Scene.gs_transp_shad =  BoolProperty(attr="gs_transp_shad",
                        description = "",
                        default = False)
Scene.gs_clamp_rgb =    BoolProperty(attr="gs_clamp_rgb",
                        description = "",
                        default = False)
Scene.gs_show_sam_pix = BoolProperty(attr="gs_show_sam_pix",
                        description = "",
                        default = False)
Scene.gs_z_channel =    BoolProperty(attr="gs_z_channel",
                        description = "",
                        default = False)

class YAF_PT_general_settings(bpy.types.Panel):

	bl_label = 'General Settings'
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

		col.prop(context.scene,"gs_ray_depth", text= "Ray Depth")
		col.prop(context.scene,"gs_shadow_depth", text= "Shadow Depth")
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

		col.prop(context.scene,"gs_show_sam_pix", text= "Show Sam Pix")
		col.prop(context.scene,"gs_draw_params", text= "Draw Params")
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
