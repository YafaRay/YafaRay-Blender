import bpy
from bpy.props import *
Object = bpy.types.Object
#TODO: update default values, edit description


Object.ml_enable =      BoolProperty(attr="ml_enable",
                                        description = "Makes the mesh emit light")
Object.ml_color =       FloatVectorProperty(attr="ml_color",
                                        description = "Color Settings", subtype = "COLOR",
                                        default = (0.7, 0.7, 0.7), # gris
                                        step = 1, precision = 2,
                                        min = 0.0, max = 1.0,
                                        soft_min = 0.0, soft_max = 1.0)
Object.ml_power =       FloatProperty(attr="ml_power",
                                        description = "Intensity multiplier for color",
                                        min = 0,
                                        default = 1)
Object.ml_samples =     IntProperty(attr="ml_samples",
                                        description = "Number of samples to be taken for direct lighting",
                                        min = 0, max = 512,
                                        default = 16)
Object.ml_double_sided = BoolProperty(attr="ml_double_sided",
                                        description = "Emit light at both sides of every face")
Object.bgp_enable =     BoolProperty(attr="bgp_enable",
                                        description = "BG Portal Light Settings")
Object.bgp_power =      FloatProperty(attr="bgp_power",
                                        description = "Intensity multiplier for color",
                                        min = 0,
                                        default = 1)
Object.bgp_samples =    IntProperty(attr="bgp_samples",
                                        description = "Number of samples to be taken for the light",
                                        min = 0, max = 512,
                                        default = 16)
Object.bgp_with_caustic = BoolProperty(attr="bgp_with_caustic",
                                        description = "Allow BG Portal Light to shoot caustic photons",
                                        default = True)
Object.bgp_with_diffuse = BoolProperty(attr="bgp_with_diffuse",
                                        description = "Allow BG Portal Light to shoot diffuse photons",
                                        default = True)
Object.bgp_photon_only = BoolProperty(attr="bgp_photon_only",
                                        description = "Set BG Portal Light in photon only mode (no direct light contribution)",
                                        default = False)

Object.vol_enable =     BoolProperty(attr="vol_enable",
                                        description="Makes the mesh a volume at its bounding box")
Object.vol_region =     EnumProperty(
    description="Set the volume region",
    items = (
        ("ExpDensity Volume","ExpDensity Volume",""),
        ("Noise Volume","Noise Volume",""),
        ("Uniform Volume","Uniform Volume","")
        #("Grid Volume","Grid Volume",""),
        #("Sky Volume","Sky Volume","")
        ),
    default="ExpDensity Volume",
    name = "Volume Type")
Object.vol_height =     FloatProperty(attr="vol_height",
                                            description="",
                                            min = 0,
                                            default = 1.0)
Object.vol_steepness =  FloatProperty(attr="vol_steepness",
                                            description="",
                                            min = 0,
                                            default = 1.0)
Object.vol_sharpness =  FloatProperty(attr="vol_sharpness",
                                            description="",
                                            min = 1.0,
                                            default = 1.0)
Object.vol_cover =      FloatProperty(attr="vol_cover",
                                            description="",
                                            min = 0.0, max = 1.0,
                                            default = 1)
Object.vol_density =    FloatProperty(attr="vol_density",
                                            description="Overall density multiplier",
                                            min = 0.1,
                                            default = 1)
Object.vol_absorp =     FloatProperty(attr="vol_absorp",
                                            description="Absorption coefficient",
                                            min = 0, max = 1,
                                            default = .1)
Object.vol_scatter =    FloatProperty(attr="vol_scatter",
                                            description="Scattering coefficient",
                                            min = 0,max = 1,
                                            default = .1)

class YAF_PT_object_light(bpy.types.Panel):

	bl_label = 'Object Light'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'object'
	COMPAT_ENGINES =['YAFA_RENDER']

	@classmethod
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
#			col.prop(context.object,"vol_g", text= "Phase Coefficient")
#			col.prop(context.object,"vol_l_e", text= "Emitted Light")
		
		
		
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

