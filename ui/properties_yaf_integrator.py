import bpy

#import types and props ---->
from bpy.props import *
narrowui = 300

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
                                        description = "Enable photon map for caustics only",
                                        default = False)
Scene.intg_photons =        IntProperty(attr="intg_photons",
                                        description = "Number of photons to be shot",
                                        min = 1, max = 100000000,
                                        default = 500000)
Scene.intg_caustic_mix =    IntProperty(attr="intg_caustic_mix",
                                        description = "Max. number of photons to mix (blur)",
                                        min = 1, max = 10000,
                                        default = 100)
Scene.intg_caustic_depth =  IntProperty(attr="intg_caustic_depth",
                                        description = "Max. number of scatter events for photons",
                                        min = 0, max = 50,
                                        default = 10)
Scene.intg_caustic_radius = FloatProperty(attr="intg_caustic_radius",
                                        description = "Max. radius to search for photons",
                                        min = 0.0001, max = 100.0,
                                        default = 1.0)
Scene.intg_use_AO =         BoolProperty(attr="intg_use_AO",
                                        description = "Enable ambient occlusion",
                                        default = False)
Scene.intg_AO_samples =     IntProperty(attr="intg_AO_samples",
                                        description = "Number of samples for ambient occlusion",
                                        min = 1, max = 1000,
                                        default = 32)
Scene.intg_AO_distance =    FloatProperty(attr="intg_AO_distance",
                                        description = "Max. occlusion distance. Surfaces further away do not occlude ambient light",
                                        min = 0.0, max = 10000.0,
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
                                        description = "Radius to search for diffuse photons",
                                        min = 0.001,
                                        default = 1.0)
Scene.intg_cPhotons =       IntProperty(attr="intg_cPhotons",
                                        description = "Number of caustic photons to be shot",
                                        min = 1,
                                        default = 500000)
Scene.intg_search =         IntProperty(attr="intg_search",
                                        description = "Maximum number of diffuse photons to be filtered",
                                        min = 1, max = 10000,
                                        default = 100)
Scene.intg_final_gather =   BoolProperty(attr="intg_final_gather",
                                        description = "Use final gathering (recommended)",
                                        default = True)
Scene.intg_fg_bounces =     IntProperty(attr="intg_fg_bounces",
                                        description = "Allow gather rays to extend to paths of this length",
                                        min = 1, max = 20,
                                        default = 3)
Scene.intg_fg_samples =     IntProperty(attr="intg_fg_samples",
                                        description = "Number of samples for final gathering",
                                        min = 1,
                                        default = 16)
Scene.intg_show_map =       BoolProperty(attr="intg_show_map",
                                        description = "Directly show radiance map (disables final gathering step)",
                                        default = False)
Scene.intg_use_bg =         BoolProperty(attr="intg_use_bg",
                                        description = "",
                                        default = False)
Scene.intg_caustic_method = EnumProperty(attr="intg_caustic_method",
                                        description = "Choose caustic rendering method",
    items = (
        ("Caustic Method","Caustic Method",""),
        ("None","None",""),
        ("Path","Path",""),
        ("Path+Photon","Path+Photon",""),
        ("Photon","Photon",""),
),default="None")
Scene.intg_path_samples =   IntProperty(attr="intg_path_samples",
                                        description = "Number of path samples per pixel sample",
                                        min = 1,
                                        default = 32)
Scene.intg_no_recursion =   BoolProperty(attr="intg_no_recursion",
                                        description = "No recursive raytracing, only pure path tracing",
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
                                        description = "Show the normals perturbed by bump and normal maps",
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
        row = layout.row()
        wide_ui = context.region.width < narrowui

        col = layout.row()

        row.prop(context.scene,"intg_light_method", text= "Lighting Methods")


        if context.scene.intg_light_method == 'Direct Lighting':
            col.prop(context.scene,"intg_use_caustics", text= "Use Caustics")

            if context.scene.intg_use_caustics:
                col = layout.row()
                col.prop(context.scene,"intg_photons", text= "Photons")
                col.prop(context.scene,"intg_caustic_mix", text= "Caustic Mix")
                col = layout.row()
                col.prop(context.scene,"intg_caustic_depth", text= "Caustic Depth")
                col.prop(context.scene,"intg_caustic_radius", text= "Caustic Radius")
            col = layout.row()
            col.prop(context.scene,"intg_use_AO", text= "Use AO")

            if context.scene.intg_use_AO:
                col = layout.row()
                col.prop(context.scene,"intg_AO_samples", text= "AO Samples")
                col.prop(context.scene,"intg_AO_distance", text= "AO Distance")
                col = layout.row()
                col.prop(context.scene,"intg_AO_color", text= "AO Color")


        if context.scene.intg_light_method == 'Photon Mapping':
            col = layout.row()
            col.prop(context.scene,"intg_bounces", text= "Depth")
            col.prop(context.scene,"intg_photons", text= "Diff. Photons")
            col = layout.row()
            col.prop(context.scene,"intg_diffuse_radius", text= "Diff. Radius")
            col.prop(context.scene,"intg_cPhotons", text= "Caus. Photons")
            col = layout.row()
            col.prop(context.scene,"intg_caustic_radius", text= "Caus. Radius")
            col.prop(context.scene,"intg_search", text= "Search")
            col = layout.row()
            col.prop(context.scene,"intg_caustic_mix", text= "Caus. Mix")
            col.prop(context.scene,"intg_final_gather", text= "Final Gather")

            if context.scene.intg_final_gather:
                col = layout.row()
                col.prop(context.scene,"intg_fg_bounces", text= "FG Bounces")
                col.prop(context.scene,"intg_fg_samples", text= "FG Samples")

            col = layout.row()
            col.prop(context.scene,"intg_show_map", text= "Show Map")
            col.prop(context.scene,"intg_use_bg", text= "Use Background")




        #col = layout.column() # only afect to pathtracing bloq
        if context.scene.intg_light_method == 'Pathtracing':
            col = layout.row()
            col.prop(context.scene,"intg_caustic_method", text= "Caustic Method")

            col = layout.row()

            if context.scene.intg_caustic_method == 'Path+Photon':
                #col = layout.row()
                col.prop(context.scene,"intg_photons", text= "Photons")
                col.prop(context.scene,"intg_caustic_mix", text= "Caus. Mix")
                col = layout.row()
                col.prop(context.scene,"intg_caustic_depth", text= "Caus. Depth")
                col.prop(context.scene,"intg_caustic_radius", text= "Caus. Radius")

            if context.scene.intg_caustic_method == 'Photon':
                col = layout.row()
                col.prop(context.scene,"intg_photons", text= "Photons")
                col.prop(context.scene,"intg_caustic_mix", text= "Caus. Mix")
                col = layout.row()
                col.prop(context.scene,"intg_caustic_depth", text= "Caus. Depth")
                col.prop(context.scene,"intg_caustic_radius", text= "Caus. Radius")

            col = layout.row()
            col.prop(context.scene,"intg_path_samples", text= "Path Samples")
            col.prop(context.scene,"intg_bounces", text= "Depth")
            col = layout.row()
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

