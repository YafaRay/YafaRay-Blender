import bpy

"""
FloatProperty = bpy.types.Scene.FloatProperty
IntProperty = bpy.types.Scene.IntProperty
BoolProperty = bpy.types.Scene.BoolProperty
CollectionProperty = bpy.types.Scene.CollectionProperty
EnumProperty = bpy.types.Scene.EnumProperty
FloatVectorProperty = bpy.types.Scene.FloatVectorProperty
IntVectorProperty = bpy.types.Scene.IntVectorProperty
"""

bpy.types.Scene.intg_light_method = bpy.props.EnumProperty(attr="intg_light_method",
	items = (
		("Lighting Methods","Lighting Methods",""),
		("Direct Lighting","Direct Lighting",""),
		("Photon Mapping","Photon Mapping",""),
		("Pathtracing","Pathtracing",""),
		("Debug","Debug",""),
		("Bidirectional","Bidirectional",""),
),default="Direct Lighting")
bpy.types.Scene.intg_use_caustics = bpy.props.BoolProperty(attr="intg_use_caustics")
bpy.types.Scene.intg_photons = bpy.props.IntProperty(attr="intg_photons", default = 500000)
bpy.types.Scene.intg_caustic_mix = bpy.props.IntProperty(attr="intg_caustic_mix", default = 100)
bpy.types.Scene.intg_caustic_depth = bpy.props.IntProperty(attr="intg_caustic_depth", default = 10)
bpy.types.Scene.intg_caustic_radius = bpy.props.FloatProperty(attr="intg_caustic_radius", default = 1.0)
bpy.types.Scene.intg_use_AO = bpy.props.BoolProperty(attr="intg_use_AO")
bpy.types.Scene.intg_AO_samples = bpy.props.IntProperty(attr="intg_AO_samples", default = 32)
bpy.types.Scene.intg_AO_distance = bpy.props.FloatProperty(attr="intg_AO_distance", default = 1.0)
bpy.types.Scene.intg_AO_color = bpy.props.FloatVectorProperty(attr="intg_AO_color",description = "Color Settings", subtype = "COLOR", step = 1, precision = 2, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)
bpy.types.Scene.intg_bounces = bpy.props.IntProperty(attr="intg_bounces", min = 4, default = 4, soft_min = 4)
bpy.types.Scene.intg_diffuse_radius = bpy.props.FloatProperty(attr="intg_diffuse_radius", default = 1.0)
bpy.types.Scene.intg_cPhotons = bpy.props.IntProperty(attr="intg_cPhotons", default = 500000)
bpy.types.Scene.intg_search = bpy.props.IntProperty(attr="intg_search", default = 100)
bpy.types.Scene.intg_final_gather = bpy.props.BoolProperty(attr="intg_final_gather", default = True)
bpy.types.Scene.intg_fg_bounces = bpy.props.IntProperty(attr="intg_fg_bounces", default = 3)
bpy.types.Scene.intg_fg_samples = bpy.props.IntProperty(attr="intg_fg_samples", default = 16)
bpy.types.Scene.intg_show_map = bpy.props.BoolProperty(attr="intg_show_map")
bpy.types.Scene.intg_use_bg = bpy.props.BoolProperty(attr="intg_use_bg")
bpy.types.Scene.intg_caustic_method = bpy.props.EnumProperty(attr="intg_caustic_method",
	items = (
		("Caustic Method","Caustic Method",""),
		("None","None",""),
		("Path","Path",""),
		("Path+Photon","Path+Photon",""),
		("Photon","Photon",""),
),default="None")
bpy.types.Scene.intg_path_samples = bpy.props.IntProperty(attr="intg_path_samples", default = 32)
bpy.types.Scene.intg_no_recursion = bpy.props.BoolProperty(attr="intg_no_recursion")
bpy.types.Scene.intg_debug_type = bpy.props.EnumProperty(attr="intg_debug_type",
	items = (
		("Debug Type","Debug Type",""),
		("N","N",""),
		("dPdU","dPdU",""),
		("dPdV","dPdV",""),
		("NU","NU",""),
		("NV","NV",""),
		("dSdU","dSdU",""),
		("dSdV","dSdV",""),
),default="dSdV")
bpy.types.Scene.intg_show_perturbed_normals = bpy.props.BoolProperty(attr="intg_show_perturbed_normals")


class YAF_PT_render(bpy.types.Panel):

	bl_label = 'Yafaray Integrator'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'render'
	COMPAT_ENGINES =['YAFA_RENDER']

	@classmethod
	def poll(self, context):

		engine = context.scene.render.engine
		return (context.scene.render and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):

		layout = self.layout
		split = layout.split()
		col = split.column()

		col.prop(context.scene,"intg_light_method", text= "Lighting Methods")

		if context.scene.intg_light_method == 'Direct Lighting':
			col.prop(context.scene,"intg_use_caustics", text= "Use Caustics")

			if context.scene.intg_use_caustics:
				col.prop(context.scene,"intg_photons", text= "Photons")
				col.prop(context.scene,"intg_caustic_mix", text= "Caustic Mix")
				col.prop(context.scene,"intg_caustic_depth", text= "Caustic Depth")
				col.prop(context.scene,"intg_caustic_radius", text= "Caustic Radius")

			col.prop(context.scene,"intg_use_AO", text= "Use AO")

			if context.scene.intg_use_AO:
				col.prop(context.scene,"intg_AO_samples", text= "AO Samples")
				col.prop(context.scene,"intg_AO_distance", text= "AO Distance")
				col.prop(context.scene,"intg_AO_color", text= "AO Color")


		if context.scene.intg_light_method == 'Photon Mapping':
			col.prop(context.scene,"intg_bounces", text= "Depth")
			col.prop(context.scene,"intg_photons", text= "Diff. Photons")
			col.prop(context.scene,"intg_diffuse_radius", text= "Diff. Radius")
			col.prop(context.scene,"intg_cPhotons", text= "Caus. Photons")
			col.prop(context.scene,"intg_caustic_radius", text= "Caus. Radius")
			col.prop(context.scene,"intg_search", text= "Search")
			col.prop(context.scene,"intg_caustic_mix", text= "Caus. Mix")
			col.prop(context.scene,"intg_final_gather", text= "Final Gather")

			col.prop(context.scene,"intg_fg_bounces", text= "FG Bounces")
			col.prop(context.scene,"intg_fg_samples", text= "FG Samples")
			col.prop(context.scene,"intg_show_map", text= "Show Map")

			col.prop(context.scene,"intg_use_bg", text= "Use Background")


		if context.scene.intg_light_method == 'Pathtracing':
			col.prop(context.scene,"intg_caustic_method", text= "Caustic Method")

			if context.scene.intg_caustic_method == 'Path+Photon':
				col.prop(context.scene,"intg_photons", text= "Photons")
				col.prop(context.scene,"intg_caustic_mix", text= "Caus. Mix")
				col.prop(context.scene,"intg_caustic_depth", text= "Caus. Depth")
				col.prop(context.scene,"intg_caustic_radius", text= "Caus. Radius")

			if context.scene.intg_caustic_method == 'Photon':
				col.prop(context.scene,"intg_photons", text= "Photons")
				col.prop(context.scene,"intg_caustic_mix", text= "Caus. Mix")
				col.prop(context.scene,"intg_caustic_depth", text= "Caus. Depth")
				col.prop(context.scene,"intg_caustic_radius", text= "Caus. Radius")

			col.prop(context.scene,"intg_path_samples", text= "Path Samples")
			col.prop(context.scene,"intg_bounces", text= "Depth")
			col.prop(context.scene,"intg_no_recursion", text= "No Recursion")

			col.prop(context.scene,"intg_use_bg", text= "Use Background")


		if context.scene.intg_light_method == 'Debug':
			col.prop(context.scene,"intg_debug_type", text= "Debug Type")

			col.prop(context.scene,"intg_show_perturbed_normals", text= "Perturbed Normals")





classes = [
	YAF_PT_render,
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
