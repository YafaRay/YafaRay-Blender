import bpy

"""
FloatProperty = bpy.types.Lamp.FloatProperty
IntProperty = bpy.types.Lamp.IntProperty
BoolProperty = bpy.types.Lamp.BoolProperty
CollectionProperty = bpy.types.Lamp.CollectionProperty
EnumProperty = bpy.types.Lamp.EnumProperty
FloatVectorProperty = bpy.types.Lamp.FloatVectorProperty
StringProperty = bpy.types.Lamp.StringProperty
IntVectorProperty = bpy.types.Lamp.IntVectorProperty
"""

bpy.types.Lamp.lamp_type = bpy.props.EnumProperty(attr="lamp_type",
	items = (
		("Light Type","Light Type",""),
		("Area","Area",""),
		("Directional","Directional",""),
		#("MeshLight","MeshLight",""),
		("Point","Point",""),
		("Sphere","Sphere",""),
		("Spot","Spot",""),
		("Sun","Sun",""),
		("IES","IES",""),
),default="Sun")
bpy.types.Lamp.create_geometry = bpy.props.BoolProperty(attr="create_geometry")
bpy.types.Lamp.infinite = bpy.props.BoolProperty(attr="infinite")
bpy.types.Lamp.spot_soft_shadows = bpy.props.BoolProperty(attr="spot_soft_shadows")
bpy.types.Lamp.shadow_fuzzyness = bpy.props.FloatProperty(attr="shadow_fuzzyness", default = 1.0)
bpy.types.Lamp.photon_only = bpy.props.BoolProperty(attr="photon_only")
bpy.types.Lamp.angle = bpy.props.IntProperty(attr="angle",
		max = 80,
		min = 0)
bpy.types.Lamp.ies_file = bpy.props.StringProperty(attr="ies_file",subtype = 'FILE_PATH')
bpy.types.Lamp.yaf_samples = bpy.props.IntProperty(attr="yaf_samples", default = 16)
bpy.types.Lamp.ies_cone_angle = bpy.props.FloatProperty(attr="ies_cone_angle", default = 10.0)
bpy.types.Lamp.ies_soft_shadows = bpy.props.BoolProperty(attr="ies_soft_shadows")


class YAF_PT_lamp(bpy.types.Panel):

	bl_label = 'Lamp'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'data'
	COMPAT_ENGINES =['YAFA_RENDER']

	@classmethod
	def poll(self, context):

		engine = context.scene.render.engine

		import properties_data_lamp

		if (context.lamp and  (engine in self.COMPAT_ENGINES) ) :
			try :
				properties_data_lamp.unregister()
			except: 
				pass
		else:
			try:
				properties_data_lamp.register()
			except: 
				pass
		return (context.lamp and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):

		layout = self.layout
		split = layout.split()
		col = split.column()

		col.prop(context.lamp,"type", text= "Light Type")
		row = layout.row()
		split = row.split()
		col = row.column()
		
		#context.lamp.shadow_ray_samples = 16

		if context.lamp.type == 'AREA':
			
			col.prop(context.lamp,"yaf_samples", text= "Samples")
			if context.lamp.type != 'AREA':
				context.lamp.type = 'AREA'
			col.prop(context.lamp,"size", text= "SizeX")
			col.prop(context.lamp,"size_y", text= "SizeY")
			col.prop(context.lamp,"create_geometry", text= "Create Geometry")


		elif context.lamp.type == 'Directional':
			if context.lamp.type != 'SUN':
				context.lamp.type = 'SUN'
			col.prop(context.lamp,"shadow_soft_size", text= "Radius")
			col.prop(context.lamp,"infinite", text= "Infinite")

		elif context.lamp.type == 'Sphere':
			if context.lamp.type != 'POINT':
				context.lamp.type = 'POINT'
			col.prop(context.lamp,"shadow_soft_size", text= "Radius")
			col.prop(context.lamp,"yaf_samples", text= "Samples")
			col.prop(context.lamp,"create_geometry", text= "Create Geometry")


		elif context.lamp.type == 'SPOT':
			
			if context.lamp.type != 'SPOT':
				context.lamp.type = 'SPOT'
			
			col.prop(context.lamp,"spot_size", text= "Cone Angle")
			col.prop(context.lamp,"spot_soft_shadows", text= "Soft Shadow")
			
			if context.lamp.spot_soft_shadows:
				col.prop(context.lamp,"yaf_samples", text= "Samples")
				col.prop(context.lamp,"shadow_fuzzyness", text= "Shadow Fuzzyness")
			col.prop(context.lamp,"spot_blend", text= "Blend")
			col.prop(context.lamp,"distance", text= "Distance")
			col.prop(context.lamp,"photon_only", text= "Photon Only")
			
			
		elif context.lamp.type == 'SUN':
			
			if context.lamp.type != 'SUN':
				context.lamp.type = 'SUN'
			col.prop(context.lamp,"angle", text= "Angle")
			col.prop(context.lamp,"yaf_samples", text= "Samples")
		
		elif context.lamp.type == 'POINT':
			
			if context.lamp.type != 'POINT':
				context.lamp.type = 'POINT'
			
		
		elif context.lamp.type == 'IES':
			col.prop(context.lamp,"ies_file",text = "IES File")
			if context.lamp.ies_soft_shadows:
				col.prop(context.lamp,"yaf_samples",text = "IES Samples")
			col.prop(context.lamp,"ies_cone_angle",text = "IES Cone Angle")
			col.prop(context.lamp,"ies_soft_shadows",text = "IES Soft Shadows")




		col.prop(context.lamp,"color", text= "Color")
		col.prop(context.lamp,"energy", text= "Power")


from properties_data_lamp import DATA_PT_preview
from properties_data_lamp import DATA_PT_context_lamp

classes = [
	YAF_PT_lamp,
]

def register():
	YAF_PT_lamp.prepend( DATA_PT_preview.draw )
	YAF_PT_lamp.prepend( DATA_PT_context_lamp.draw )
	register = bpy.types.register
	for cls in classes:
		register(cls)


def unregister():
	bpy.types.YAF_PT_lamp.remove( DATA_PT_preview.draw )
	bpy.types.YAF_PT_lamp.remove( DATA_PT_context_lamp.draw )
	unregister = bpy.types.unregister
	for cls in classes:
		unregister(cls)


if __name__ == "__main__":
	register()
