import bpy

FloatProperty = bpy.types.Scene.FloatProperty
IntProperty = bpy.types.Scene.IntProperty
BoolProperty = bpy.types.Scene.BoolProperty
CollectionProperty = bpy.types.Scene.CollectionProperty
EnumProperty = bpy.types.Scene.EnumProperty
FloatVectorProperty = bpy.types.Scene.FloatVectorProperty
IntVectorProperty = bpy.types.Scene.IntVectorProperty


EnumProperty(attr="lamp_type",
	items = (
		("Area","Area",""),
		("Directional","Directional",""),
		("MeshLight","MeshLight",""),
		("Point","Point",""),
		("Sphere","Sphere",""),
		("Spot","Spot",""),
		("Sun","Sun",""),
),default="Sun")

BoolProperty(attr="infinite")

IntProperty(attr="angle",
		max = 80,
		min = 0)

class YAF_PT_lamp(bpy.types.Panel):

	bl_label = 'Lamp'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'data'
	COMPAT_ENGINES =['YAF_RENDER_ENGINE']


	def poll(self, context):

		engine = context.scene.render.engine
		return (context.lamp and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):

		layout = self.layout
		split = layout.split()
		col = split.column()


		col.label(text="lamp_type")
		col.prop(context.scene,"lamp_type", text= "")

		if context.scene.lamp_type == 'Area':
			context.lamp.type = 'AREA'
			col.prop(context.lamp,"shadow_ray_samples", text= "Samples")
			

		if context.scene.lamp_type == 'Directional':
			context.lamp.type = 'SUN'
			col.prop(context.scene,"infinite", text= "Infinite")
			col.prop(context.lamp,"shadow_soft_size", text= "Radius")
			

		if context.scene.lamp_type == 'Sphere':
			context.lamp.type = 'POINT'
			col.prop(context.lamp,"shadow_soft_size", text= "Radius")
			col.prop(context.lamp,"shadow_ray_samples", text= "Samples")
			

		if context.scene.lamp_type == 'Spot':
			context.lamp.type = 'SPOT'
			col.prop(context.lamp,"spot_blend", text= "Blend")
			col.prop(context.lamp,"spot_size", text= "Cone Angle")
			

		if context.scene.lamp_type == 'Sun':
			context.lamp.type = 'SUN'
			col.prop(context.scene,"angle", text= "Angle")
			col.prop(context.lamp,"shadow_ray_samples", text= "Samples")
			
		
		if context.scene.lamp_type == 'Area':
			context.lamp.type = 'POINT'

		col.prop(context.lamp,"color", text= "Color")
		col.prop(context.lamp,"energy", text= "Power")





classes = [YAF_PT_lamp]

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
