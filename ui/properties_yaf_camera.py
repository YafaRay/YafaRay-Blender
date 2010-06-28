import bpy


FloatProperty = bpy.types.Scene.FloatProperty
IntProperty = bpy.types.Scene.IntProperty
BoolProperty = bpy.types.Scene.BoolProperty
CollectionProperty = bpy.types.Scene.CollectionProperty
EnumProperty = bpy.types.Scene.EnumProperty
FloatVectorProperty = bpy.types.Scene.FloatVectorProperty
IntVectorProperty = bpy.types.Scene.IntVectorProperty


EnumProperty(attr="camera_type",
	items = (
		("camera_type","camera_type",""),
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
		("bokeh_type","bokeh_type",""),
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
		("bokeh_bias","bokeh_bias",""),
		("Uniform","Uniform",""),
		("Center","Center",""),
		("Edge","Edge",""),
),default="Edge")

class YAF_PT_camera(bpy.types.Panel):

	bl_label = 'Camera'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'data'
	COMPAT_ENGINES =['YAFA_RENDER']


	def poll(self, context):

		engine = context.scene.render.engine
		return (context.camera and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):

		layout = self.layout
		split = layout.split()
		col = split.column()


		col.label(text="camera_type")
		col.prop(context.scene,"camera_type", text= "")

		if context.scene.camera_type == 'angular':
			context.camera.type = 'PERSP'
			col.prop(context.camera,"lens", text= "Angle")
			col.prop(context.scene,"max_angle", text= "Max Angle")
			col.prop(context.scene,"mirrored", text= "Mirrored")
			col.prop(context.scene,"circular", text= "Circular")

		if context.scene.camera_type == 'orthographic':
			context.camera.type = 'ORTHO'
			col.prop(context.camera,"ortho_scale", text= "Scale")

		if context.scene.camera_type == 'perspective':
			context.camera.type = 'PERSP'
			col.label(text="bokeh_type")
			col.prop(context.scene,"bokeh_type", text= "")

			col.prop(context.scene,"aperture", text= "Aperture")
			col.prop(context.camera,"dof_distance", text= "DOF distance")
			col.prop(context.scene,"bokeh_rotation", text= "Bokeh Rotation")
			col = split.column()

			col.label(text="bokeh_bias")
			col.prop(context.scene,"bokeh_bias", text= "")

			col.prop(context.camera,"lens", text= "Focal Length")

		if context.scene.camera_type == 'architect':

			col.label(text="bokeh_type")
			col.prop(context.scene,"bokeh_type", text= "")

			col.prop(context.scene,"aperture", text= "Aperture")
			col.prop(context.camera,"dof_distance", text= "DOF distance")
			col.prop(context.scene,"bokeh_rotation", text= "Bokeh Rotation")
			col = split.column()

			col.label(text="bokeh_bias")
			col.prop(context.scene,"bokeh_bias", text= "")

			col.prop(context.camera,"lens", text= "Focal Length")

classes = [YAF_PT_camera]

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
