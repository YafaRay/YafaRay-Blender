import bpy


FloatProperty = bpy.types.World.FloatProperty
IntProperty = bpy.types.World.IntProperty
BoolProperty = bpy.types.World.BoolProperty
CollectionProperty = bpy.types.World.CollectionProperty
EnumProperty = bpy.types.World.EnumProperty
FloatVectorProperty = bpy.types.World.FloatVectorProperty
StringProperty = bpy.types.World.StringProperty
IntVectorProperty = bpy.types.World.IntVectorProperty


EnumProperty(attr="v_int_type",
	items = (
		("Volume Integrator","Volume Integrator",""),
		("None","None",""),
		("Single Scatter","Single Scatter",""),
		#("Sky","Sky",""),
),default="None")
FloatProperty(attr="v_int_step_size", precision = 3)
BoolProperty(attr="v_int_adaptive")
BoolProperty(attr="v_int_optimize")
IntProperty(attr="v_int_attgridres")
FloatProperty(attr="v_int_scale")
FloatProperty(attr="v_int_alpha")
FloatProperty(attr="v_int_dsturbidity")

class YAF_PT_vol_integrator(bpy.types.Panel):

	bl_label = 'YafaRay Volume Integrator'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'world'
	COMPAT_ENGINES =['YAFA_RENDER']


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
