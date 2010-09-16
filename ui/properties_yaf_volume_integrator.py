import bpy

"""
FloatProperty = bpy.types.World.FloatProperty
IntProperty = bpy.types.World.IntProperty
BoolProperty = bpy.types.World.BoolProperty
CollectionProperty = bpy.types.World.CollectionProperty
EnumProperty = bpy.types.World.EnumProperty
FloatVectorProperty = bpy.types.World.FloatVectorProperty
StringProperty = bpy.types.World.StringProperty
IntVectorProperty = bpy.types.World.IntVectorProperty
"""

bpy.types.World.v_int_type = bpy.props.EnumProperty(attr="v_int_type",
	items = (
		("Volume Integrator","Volume Integrator",""),
		("None","None",""),
		("Single Scatter","Single Scatter",""),
		#("Sky","Sky",""),
),default="None")
bpy.types.World.v_int_step_size = bpy.props.FloatProperty(attr="v_int_step_size", precision = 3)
bpy.types.World.v_int_adaptive = bpy.props.BoolProperty(attr="v_int_adaptive")
bpy.types.World.v_int_optimize = bpy.props.BoolProperty(attr="v_int_optimize")
bpy.types.World.v_int_attgridres = bpy.props.IntProperty(attr="v_int_attgridres")
bpy.types.World.v_int_scale = bpy.props.FloatProperty(attr="v_int_scale")
bpy.types.World.v_int_alpha = bpy.props.FloatProperty(attr="v_int_alpha")
bpy.types.World.v_int_dsturbidity = bpy.props.FloatProperty(attr="v_int_dsturbidity")

class YAF_PT_vol_integrator(bpy.types.Panel):

	bl_label = 'YafaRay Volume Integrator'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'world'
	COMPAT_ENGINES =['YAFA_RENDER']

	@classmethod
	def poll(self, context):

		engine = context.scene.render.engine
		return (context.world and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):

		layout = self.layout
		split = layout.split()
		col = split.column()

		col.prop(context.world,"v_int_type", text= "Volume Integrator")

		if context.world.v_int_type == 'None':
			col.prop(context.world,"v_int_step_size", text= "Step Size")

		if context.world.v_int_type == 'Single Scatter':
			col.prop(context.world,"v_int_step_size", text= "Step Size")
			col.prop(context.world,"v_int_attgridres", text= "Att. grid resolution")
			col.prop(context.world,"v_int_adaptive", text= "Adaptive")
			col.prop(context.world,"v_int_optimize", text= "Optimize")
			

		#if context.world.v_int_type == 'Sky':
		#	col.prop(context.world,"v_int_step_size", text= "Step Size")
		#	col.prop(context.world,"v_int_dsturbidity", text= "Turbidity")
		#	col.prop(context.world,"v_int_scale", text= "Scale")
		#	col.prop(context.world,"v_int_alpha", text= "Alpha")




classes = [
	YAF_PT_vol_integrator,
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
