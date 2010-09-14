import bpy

from bpy.props import PointerProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, FloatProperty, FloatVectorProperty, CollectionProperty

bpy.types.Scene.ml_enable=BoolProperty(name="ml_enable")
bpy.types.Scene.ml_color=FloatVectorProperty(name="ml_color",description = "Color Settings", subtype = "COLOR", step = 1, precision = 2, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)
bpy.types.Scene.ml_power=FloatProperty(name="ml_power")
bpy.types.Scene.ml_samples=IntProperty(name="ml_samples")
bpy.types.Scene.ml_double_sided=BoolProperty(name="ml_double_sided")
bpy.types.Scene.bgp_enable=BoolProperty(name="bgp_enable")
bpy.types.Scene.bgp_power=FloatProperty(name="bgp_power")
bpy.types.Scene.bgp_samples=IntProperty(name="bgp_samples")
bpy.types.Scene.bgp_with_caustic=BoolProperty(name="bgp_with_caustic")
bpy.types.Scene.bgp_with_diffuse=BoolProperty(name="bgp_with_diffuse")
bpy.types.Scene.bgp_photon_only=BoolProperty(name="bgp_photon_only")
bpy.types.Scene.vol_enable=BoolProperty(name="vol_enable")
bpy.types.Scene.vol_region=EnumProperty(name="vol_region",
	items = (
		("Volume Region","Volume Region",""),
		("ExpDensity Volume","ExpDensity Volume",""),
		("Noise Volume","Noise Volume",""),
		("Uniform Volume","Uniform Volume",""),
		#("Grid Volume","Grid Volume",""),
		("Sky Volume","Sky Volume",""),
),default="Uniform Volume")
bpy.types.Scene.vol_height=FloatProperty(name="vol_height")
bpy.types.Scene.vol_steepness=FloatProperty(name="vol_steepness")
bpy.types.Scene.vol_sharpness=FloatProperty(name="vol_sharpness")
bpy.types.Scene.vol_cover=FloatProperty(name="vol_cover")
bpy.types.Scene.vol_Density=FloatProperty(name="vol_density")
bpy.types.Scene.vol_absorp=FloatProperty(name="vol_absorp")
bpy.types.Scene.vol_scatter=FloatProperty(name="vol_scatter")
bpy.types.Scene.vol_l_e=FloatProperty(name="vol_l_e", default = 0.0, min = -1.0, max = 1.0, soft_min = -1.0, soft_max = 1.0)
bpy.types.Scene.vol_g=FloatProperty(name="vol_g", default = 0.0, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)

#volume Integrator
#EnumProperty(attr="v_int_type",
#	items = (
#		("Volume Integrator","Volume Integrator",""),
#		("None","None",""),
#		("Single Scatter","Single Scatter",""),
#		("Sky","Sky",""),
#),default="Sky")
#FloatProperty(attr="v_int_step_size")
#BoolProperty(attr="v_int_adaptive")
#BoolProperty(attr="v_int_optimize")
#IntProperty(attr="v_int_attgridres")
#FloatProperty(attr="v_int_scale")
#FloatProperty(attr="v_int_alpha")


class YAF_PT_object_light(bpy.types.Panel):

	bl_label = 'Object Light'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'object'
	COMPAT_ENGINES =['YAFA_RENDER']


	def poll(self, context):

		engine = context.scene.render.engine

		import properties_object

		if (True  and  (engine in self.COMPAT_ENGINES) ) :
			try :
				properties_object.unregister()
			except: 
				pass
		else:
			try:
				properties_object.register()
			except: 
				pass
		return (context.object.type == 'MESH'  and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):

		layout = self.layout
		split = layout.split()
		col = split.column()

		col.prop(context.object,"ml_enable", text= "Enable Meshlight", toggle = True)

		if context.object.ml_enable:
			col.prop(context.object,"ml_color", text= "Meshlight Color")
			col.prop(context.object,"ml_power", text= "Power")
			col.prop(context.object,"ml_samples", text= "Samples")
			col.prop(context.object,"ml_double_sided", text= "Double Sided")


		col.prop(context.object,"bgp_enable", text= "Enable Bgportallight", toggle = True)

		if context.object.bgp_enable:
			col.prop(context.object,"bgp_power", text= "Power")
			col.prop(context.object,"bgp_samples", text= "Samples")
			col.prop(context.object,"bgp_with_caustic", text= "With Caustic")

			col.prop(context.object,"bgp_with_diffuse", text= "With Diffuse")

			col.prop(context.object,"bgp_photon_only", text= "Photons Only")


		col.prop(context.object,"vol_enable", text= "Enable Volume", toggle = True)

		if context.object.vol_enable:
			col.prop(context.object,"vol_region", text= "Volume Region")

			if context.object.vol_region == 'ExpDensity Volume':
				col.prop(context.object,"vol_height", text= "Height")
				col.prop(context.object,"vol_steepness", text= "Steepness")

			if context.object.vol_region == 'Noise Volume':
				col.prop(context.object,"vol_sharpness", text= "Sharpness")
				col.prop(context.object,"vol_cover", text= "Cover")
				col.prop(context.object,"vol_density", text= "Density")

			col.prop(context.object,"vol_absorp", text= "Absroption")
			col.prop(context.object,"vol_scatter", text= "Scatter")
			col.prop(context.object,"vol_g", text= "Phase Coefficient")
			col.prop(context.object,"vol_l_e", text= "Emitted Light")
		
		
		
		#col.prop(context.object,"v_int_type", text= "Volume Integrator")
		#
		#if context.object.v_int_type == 'None':
		#	col.prop(context.object,"v_int_step_size", text= "Step Size")
		#
		#if context.object.v_int_type == 'Single Scatter':
		#	col.prop(context.object,"v_int_adaptive", text= "Adaptive")
		#
		#	col.prop(context.object,"v_int_optimize", text= "Optimize")
		#
		#	col.prop(context.object,"v_int_attgridres", text= "Att. grid resolution")
		#
		#if context.object.v_int_type == 'Sky':
		#	col.prop(context.object,"v_int_scale", text= "Scale")
		#	col.prop(context.object,"v_int_alpha", text= "Alpha")




classes = [
	YAF_PT_object_light,
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
