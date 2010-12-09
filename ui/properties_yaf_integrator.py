import bpy

#import types and props ---->
from bpy.props import *
Scene = bpy.types.Scene


Scene.intg_light_method =   EnumProperty(attr="intg_light_method",
	items = (
		("Lighting Methods","Lighting Methods",""),
		("Direct Lighting","Direct Lighting",""),
		("Photon Mapping","Photon Mapping",""),
		("Pathtracing","Pathtracing",""),
		("Debug","Debug",""),
		("Bidirectional","Bidirectional",""),
),default="Direct Lighting")
Scene.intg_use_caustics =   BoolProperty(attr="intg_use_caustics",
                                        description = "",
                                        default = False)
Scene.intg_photons =        IntProperty(attr="intg_photons",
                                        description = "",
                                        default = 500000)
Scene.intg_caustic_mix =    IntProperty(attr="intg_caustic_mix",
                                        description = "",
                                        default = 100)
Scene.intg_caustic_depth =  IntProperty(attr="intg_caustic_depth",
                                        description = "",
                                        default = 10)
Scene.intg_caustic_radius = FloatProperty(attr="intg_caustic_radius",
                                        description = "",
                                        default = 1.0)
Scene.intg_use_AO =         BoolProperty(attr="intg_use_AO",
                                        description = "",
                                        default = False)
Scene.intg_AO_samples =     IntProperty(attr="intg_AO_samples",
                                        description = "",
                                        default = 32)
Scene.intg_AO_distance =    FloatProperty(attr="intg_AO_distance",
                                        description = "",
                                        default = 1.0)
Scene.intg_AO_color =       FloatVectorProperty(attr="intg_AO_color",
                                        description = "Color Settings", subtype = "COLOR",
                                        default = (0.9, 0.9, 0.9),
                                        step = 1, precision = 2,
                                        min = 0.0, max = 1.0,
                                        soft_min = 0.0, soft_max = 1.0)
Scene.intg_bounces =        IntProperty(attr="intg_bounces",
                                        description = "",
                                        min = 4, default = 4, soft_min = 4)
Scene.intg_diffuse_radius = FloatProperty(attr="intg_diffuse_radius",
                                        description = "",
                                        default = 1.0)
Scene.intg_cPhotons =       IntProperty(attr="intg_cPhotons",
                                        description = "",
                                        default = 500000)
Scene.intg_search =         IntProperty(attr="intg_search",
                                        description = "",
                                        default = 100)
Scene.intg_final_gather =   BoolProperty(attr="intg_final_gather",
                                        description = "",
                                        default = True)
Scene.intg_fg_bounces =     IntProperty(attr="intg_fg_bounces",
                                        description = "",
                                        default = 3)
Scene.intg_fg_samples =     IntProperty(attr="intg_fg_samples",
                                        description = "",
                                        default = 16)
Scene.intg_show_map =       BoolProperty(attr="intg_show_map",
                                        description = "",
                                        default = False)
Scene.intg_use_bg =         BoolProperty(attr="intg_use_bg",
                                        description = "",
                                        default = False)
Scene.intg_caustic_method = EnumProperty(attr="intg_caustic_method",
	items = (
		("Caustic Method","Caustic Method",""),
		("None","None",""),
		("Path","Path",""),
		("Path+Photon","Path+Photon",""),
		("Photon","Photon",""),
),default="None")
Scene.intg_path_samples =   IntProperty(attr="intg_path_samples",
                                        description = "",
                                        default = 32)
Scene.intg_no_recursion =   BoolProperty(attr="intg_no_recursion",
                                        description = "",
                                        default = False)
Scene.intg_debug_type =     EnumProperty(attr="intg_debug_type",
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
Scene.intg_show_perturbed_normals = BoolProperty(attr="intg_show_perturbed_normals",
                                        description = "",
                                        default = False)


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

