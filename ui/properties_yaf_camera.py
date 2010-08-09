import bpy


FloatProperty = bpy.types.Camera.FloatProperty
IntProperty = bpy.types.Camera.IntProperty
BoolProperty = bpy.types.Camera.BoolProperty
CollectionProperty = bpy.types.Camera.CollectionProperty
EnumProperty = bpy.types.Camera.EnumProperty
FloatVectorProperty = bpy.types.Camera.FloatVectorProperty
StringProperty = bpy.types.Camera.StringProperty
IntVectorProperty = bpy.types.Camera.IntVectorProperty


EnumProperty(attr="camera_type",
	items = (
		("Yafaray Camera","Yafaray Camera",""),
		("angular","angular",""),
		("orthographic","orthographic",""),
		("perspective","perspective",""),
		("architect","architect",""),
),default="architect")
FloatProperty(attr="max_angle")
BoolProperty(attr="mirrored")
BoolProperty(attr="circular")
EnumProperty(attr="bokeh_type",
	items = (
		("Bokeh Type","Bokeh Type",""),
		("Disk2","Disk2",""),
		("Triangle","Triangle",""),
		("Square","Square",""),
		("Pentagon","Pentagon",""),
		("Hexagon","Hexagon",""),
		("Ring","Ring",""),
		("Disk1","Disk1",""),
),default="Disk1")
FloatProperty(attr="aperture")
FloatProperty(attr="bokeh_rotation")
EnumProperty(attr="bokeh_bias",
	items = (
		("Bokeh Bias","Bokeh Bias",""),
		("Uniform","Uniform",""),
		("Center","Center",""),
		("Edge","Edge",""),
),default="Edge")
FloatVectorProperty(attr="color_data",description = "Point Info", subtype = "XYZ", step = 10, precision = 3)


class YAF_PT_camera(bpy.types.Panel):

	bl_label = 'Camera'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'data'
	COMPAT_ENGINES =['YAFA_RENDER']


	def poll(self, context):

		engine = context.scene.render.engine

		import properties_data_camera

		if (context.camera and  (engine in self.COMPAT_ENGINES) ) :
			try :
				properties_data_camera.unregister()
			except: 
				pass
		else:
			try:
				properties_data_camera.register()
			except: 
				pass
		return (context.camera and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):

		layout = self.layout
		split = layout.split()
		col = split.column()

		camera = context.camera

			
		#col.prop(bpy.data,"cameras",text = "Available cameras")
		col.prop(context.camera,"camera_type", text= "Yafaray Camera")

		if context.camera.camera_type == 'angular':
			
			if camera.type != 'PERSP':
				camera.type = 'PERSP'	
			#context.camera.type = "PERSP"
			col.prop(context.camera,"lens", text= "Angle")
			col.prop(context.camera,"max_angle", text= "Max Angle")
			col.prop(context.camera,"mirrored", text= "Mirrored")
			
			col.prop(context.camera,"circular", text= "Circular")
			


		if context.camera.camera_type == 'orthographic':
			#context.camera.type = "ORTHO"
			if camera.type != 'ORTHO':
				camera.type = 'ORTHO'
			col.prop(context.camera,"ortho_scale", text= "Scale")

		if context.camera.camera_type == 'perspective':
			col.prop(context.camera,"bokeh_type", text= "Bokeh Type")

			col.prop(context.camera,"aperture", text= "Aperture")
			col.prop(context.camera,"dof_distance", text= "DOF distance")
			col.prop(context.camera,"bokeh_rotation", text= "Bokeh Rotation")
			#col = split.column()
			col.prop(context.camera,"bokeh_bias", text= "Bokeh Bias")

			#context.camera.type = "PERSP"
			if camera.type != 'PERSP':
				camera.type = 'PERSP'
			col.prop(context.camera,"lens", text= "Focal Length")

		if context.camera.camera_type == 'architect':
			col.prop(context.camera,"bokeh_type", text= "Bokeh Type")

			col.prop(context.camera,"aperture", text= "Aperture")
			col.prop(context.camera,"dof_distance", text= "DOF distance")
			col.prop(context.camera,"bokeh_rotation", text= "Bokeh Rotation")
			#col = split.column()
			col.prop(context.camera,"bokeh_bias", text= "Bokeh Bias")

			#context.camera.type = "PERSP"
			if camera.type != 'PERSP':
				camera.type = 'PERSP'
			col.prop(context.camera,"lens", text= "Focal Length")

		col.prop(context.camera,"color_data", text= "Yafaray Camera Point")


from properties_data_camera import DATA_PT_context_camera

classes = [
	YAF_PT_camera,
]

def register():
	#YAF_PT_camera.prepend( DATA_PT_context_camera.draw )
	register = bpy.types.register
	for cls in classes:
		register(cls)


def unregister():
	#bpy.types.YAF_PT_camera.remove( DATA_PT_context_camera.draw )
	unregister = bpy.types.unregister
	for cls in classes:
		unregister(cls)


if __name__ == "__main__":
	register()
