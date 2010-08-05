import bpy


FloatProperty = bpy.types.World.FloatProperty
IntProperty = bpy.types.World.IntProperty
BoolProperty = bpy.types.World.BoolProperty
CollectionProperty = bpy.types.World.CollectionProperty
EnumProperty = bpy.types.World.EnumProperty
FloatVectorProperty = bpy.types.World.FloatVectorProperty
StringProperty = bpy.types.World.StringProperty
IntVectorProperty = bpy.types.World.IntVectorProperty


EnumProperty(attr="bg_type",
	items = (
		("Yafaray Background","Yafaray Background",""),
		("Gradient","Gradient",""),
		("Texture","Texture",""),
		("Sunsky","Sunsky",""),
		("Darktide's Sunsky","Darktide's Sunsky",""),
		("Single Color","Single Color",""),
),default="Single Color")
FloatVectorProperty(attr="bg_zenith_ground_color",description = "Color Settings", subtype = "COLOR", step = 1, precision = 2, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)
BoolProperty(attr="bg_use_IBL")
IntProperty(attr="bg_IBL_samples")
IntProperty(attr="bg_rotation")
FloatProperty(attr="bg_turbidity")
FloatProperty(attr="bg_a_var")
FloatProperty(attr="bg_b_var")
FloatProperty(attr="bg_c_var")
FloatProperty(attr="bg_d_var")
FloatProperty(attr="bg_e_var")
FloatVectorProperty(attr="bg_from",description = "Point Info", subtype = "XYZ", step = 10, precision = 3)
BoolProperty(attr="bg_add_sun")
FloatProperty(attr="bg_sun_power")
BoolProperty(attr="bg_background_light")
IntProperty(attr="bg_light_samples")
FloatProperty(attr="bg_dsaltitude")
BoolProperty(attr="bg_dsnight")
FloatProperty(attr="bg_dsbright")
FloatProperty(attr="bg_power", default = 1.0)

BoolProperty(attr="use_image", default = False)


class YAF_PT_world(bpy.types.Panel):

	bl_label = 'YafaRay Background'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'world'
	COMPAT_ENGINES =['YAFA_RENDER']


	def poll(self, context):

		engine = context.scene.render.engine

		import properties_world


		import properties_texture

		if (context.world and  (engine in self.COMPAT_ENGINES) ) :
			try :
				properties_world.unregister()
			except: 
				pass
		else:
			try:
				properties_world.register()
			except: 
				pass
		#if (context.world and  (engine in self.COMPAT_ENGINES) ) :
		#	try :
		#		properties_texture.unregister()
		#	except: 
		#		pass
		#else:
		#	try:
		#		properties_texture.register()
		#	except: 
		#		pass
		return (context.world and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):

		layout = self.layout
		split = layout.split()
		col = split.column()

		col.prop(context.world,"bg_type", text= "Yafaray Background")

		if context.world.bg_type == 'Gradient':
			col.prop(context.world,"horizon_color", text= "Horizon Color")
			context.world.real_sky = True
			col.prop(context.world,"ambient_color", text= "Horizon Ground Color")
			context.world.blend_sky = True
			col.prop(context.world,"zenith_color", text= "Zenith Color")
			col.prop(context.world,"bg_zenith_ground_color", text= "Zenith Ground Color")

		if context.world.bg_type == 'Texture':
			col.prop(context.world,"bg_use_IBL", text= "Use IBL")
			col.prop(context.world,"bg_IBL_samples", text= "IBL Samples")
			col.prop(context.world,"bg_rotation", text= "Rotation")
			
			

			col.template_ID(context.world,"active_texture",new="texture.new")
			tex = context.scene.world.active_texture
			if tex is not None :
				col.separator()
				#col.prop(tex,"type",text = "Texture Type")
				col.prop(context.world,"use_image",text = "Use image as background")
				if context.world.use_image :
					tex.type = 'IMAGE'
					#print(tex.type)
					try:
						col.template_image(tex, "image", tex.image_user)
					except:
						pass

		if context.world.bg_type == 'Sunsky':
			col.prop(context.world,"bg_turbidity", text= "Turbidity")
			col.prop(context.world,"bg_a_var", text= "HorBrght")
			col.prop(context.world,"bg_b_var", text= "HorSprd")
			col.prop(context.world,"bg_c_var", text= "SunBrght")
			col.prop(context.world,"bg_d_var", text= "SunSize")
			col.prop(context.world,"bg_e_var", text= "Backlight")
			col.operator("world.get_position",text = "Get Position")
			col.operator("world.get_angle",text = "Get Angle")
			col.operator("world.update_sun",text = "Update Sun")
			col.prop(context.world,"bg_from", text= "From")
			col.prop(context.world,"bg_add_sun", text= "Add Sun")

			col.prop(context.world,"bg_sun_power", text= "Sun Power")
			col.prop(context.world,"bg_background_light", text= "Skylight")

			col.prop(context.world,"bg_light_samples", text= "Samples")

		if context.world.bg_type == 'Darktide\'s Sunsky':
			col.prop(context.world,"bg_turbidity", text= "Turbidity")
			col.prop(context.world,"bg_a_var", text= "Brightness of horizon gradient")
			col.prop(context.world,"bg_b_var", text= "Luminance of horizon")
			col.prop(context.world,"bg_c_var", text= "Solar region intensity")
			col.prop(context.world,"bg_d_var", text= "Width of circumsolar region")
			col.prop(context.world,"bg_e_var", text= "Backscattered light")
			
			col.operator("world.get_position",text = "Get Position")
			col.operator("world.get_angle",text = "Get Angle")
			col.operator("world.update_sun",text = "Update Sun")
			
			col.prop(context.world,"bg_from", text= "From")
			col.prop(context.world,"bg_dsaltitude", text= "Altitude")
			col.prop(context.world,"bg_add_sun", text= "Add Sun")

			col.prop(context.world,"bg_sun_power", text= "Sun Power")
			col.prop(context.world,"bg_background_light", text= "Add Skylight")

			col.prop(context.world,"bg_dsnight", text= "Night")

			col.prop(context.world,"bg_dsbright", text= "Sky Brightness")
			col.prop(context.world,"bg_light_samples", text= "Samples")

		if context.world.bg_type == 'Single Color':
			col.prop(context.world,"horizon_color", text= "Color")

		col.prop(context.world,"bg_power", text= "Multiplier for Background Color")


from properties_world import WORLD_PT_preview
from properties_world import WORLD_PT_context_world

classes = [
	YAF_PT_world,
]

def register():
	YAF_PT_world.prepend( WORLD_PT_preview.draw )
	YAF_PT_world.prepend( WORLD_PT_context_world.draw )
	register = bpy.types.register
	for cls in classes:
		register(cls)


def unregister():
	bpy.types.YAF_PT_world.remove( WORLD_PT_preview.draw )
	bpy.types.YAF_PT_world.remove( WORLD_PT_context_world.draw )
	unregister = bpy.types.unregister
	for cls in classes:
		unregister(cls)


if __name__ == "__main__":
	register()
