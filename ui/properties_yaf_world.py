import bpy

from bpy.props import PointerProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, FloatProperty, FloatVectorProperty, CollectionProperty

bpy.types.World.bg_type=EnumProperty(name="bg_type",
	items = (
		("Yafaray Background","Yafaray Background",""),
		("Gradient","Gradient",""),
		("Texture","Texture",""),
		("Sunsky","Sunsky",""),
		("Darktide's Sunsky","Darktide's Sunsky",""),
		("Single Color","Single Color",""),
),default="Single Color")
bpy.types.World.bg_zenith_ground_color=FloatVectorProperty(name="bg_zenith_ground_color",description = "Color Settings", subtype = "COLOR", step = 1, precision = 2, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)
bpy.types.World.bg_use_IBL=BoolProperty(name="bg_use_IBL")
bpy.types.World.bg_IBL_samples=IntProperty(name="bg_IBL_samples", default = 16)
bpy.types.World.bg_rotation=FloatProperty(name="bg_rotation", default = 0.0)
bpy.types.World.bg_turbidity=FloatProperty(name="bg_turbidity", default = 3.0)
bpy.types.World.bg_a_var=FloatProperty(name="bg_a_var", default = 1.0)
bpy.types.World.bg_b_var=FloatProperty(name="bg_b_var", default = 1.0)
bpy.types.World.bg_c_var=FloatProperty(name="bg_c_var", default = 1.0)
bpy.types.World.bg_d_var=FloatProperty(name="bg_d_var", default = 1.0)
bpy.types.World.bg_e_var=FloatProperty(name="bg_e_var", default = 1.0)
bpy.types.World.bg_from=FloatVectorProperty(name="bg_from",description = "Point Info", subtype = "XYZ", step = 10, precision = 3)
bpy.types.World.bg_add_sun=BoolProperty(name="bg_add_sun")
bpy.types.World.bg_sun_power=FloatProperty(name="bg_sun_power", default = 1.0)
bpy.types.World.bg_background_light=BoolProperty(name="bg_background_light")
bpy.types.World.bg_light_samples=IntProperty(name="bg_light_samples", default = 8)
bpy.types.World.bg_dsaltitude=FloatProperty(name="bg_dsaltitude", default = 0.0)
bpy.types.World.bg_dsnight=BoolProperty(name="bg_dsnight")
bpy.types.World.bg_sdbright=FloatProperty(name="bg_dsbright", default = 1.0)
bpy.types.World.bg_power=FloatProperty(name="bg_power", default = 1.0)

bpy.types.World.bg_exposure=FloatProperty(name="bg_exposure", default = 1.0)
bpy.types.World.bg_clamp_rgb=BoolProperty(name="bg_clamp_rgb")
bpy.types.World.bg_gamma_enc=BoolProperty(name="bg_gamma_enc", default = True)

bpy.types.World.use_image=BoolProperty(name="use_image", default = False)


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
			col.prop(context.world,"bg_use_IBL", text= "Use IBL")

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
			col.prop(context.world,"bg_exposure", text= "Exposure")
			col.prop(context.world,"bg_clamp_rgb", text= "Clamp RGB")
			col.prop(context.world,"bg_gamma_enc", text= "Gamma Encoding")

		if context.world.bg_type == 'Single Color':
			col.prop(context.world,"horizon_color", text= "Color")
			col.prop(context.world,"bg_use_IBL", text= "Use IBL")

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
