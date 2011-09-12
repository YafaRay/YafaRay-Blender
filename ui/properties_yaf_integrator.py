import bpy
#import types and props ---->
from bpy.types import Panel
from bl_ui.properties_render import RenderButtonsPanel
RenderButtonsPanel.COMPAT_ENGINES = {'YAFA_RENDER'}
from bpy.props import (IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolProperty,
                       EnumProperty)
Scene = bpy.types.Scene

Scene.intg_light_method = EnumProperty(
    name="Lighting Method",
    items=(
        ('Direct Lighting', "Direct Lighting", ""),
        ('Photon Mapping', "Photon Mapping", ""),
        ('Pathtracing', "Pathtracing", ""),
        ('Debug', "Debug", ""),
        ('Bidirectional', "Bidirectional", ""),
        ('SPPM', "SPPM", "")
    ),
    default='Direct Lighting')

Scene.intg_use_caustics = BoolProperty(
    name="Caustic Photons",
    description="Enable photon map for caustics only",
    default=False)

Scene.intg_photons = IntProperty(
    name="Photons",
    description="Number of photons to be shot",
    min=1, max=100000000,
    default=500000)

Scene.intg_caustic_mix = IntProperty(
    name="Caustic Mix",
    description="Max. number of photons to mix (blur)",
    min=1, max=10000,
    default=100)

Scene.intg_caustic_depth = IntProperty(
    name="Caustic Depth",
    description="Max. number of scatter events for photons",
    min=0, max=50,
    default=10)

Scene.intg_caustic_radius = FloatProperty(
    name="Caustic Radius",
    description="Max. radius to search for photons",
    min=0.0001, max=100.0,
    default=1.0)

Scene.intg_use_AO = BoolProperty(
    name="Ambient Occlusion",
    description="Enable ambient occlusion",
    default=False)

Scene.intg_AO_samples = IntProperty(
    name="Samples",
    description="Number of samples for ambient occlusion",
    min=1, max=1000,
    default=32)

Scene.intg_AO_distance = FloatProperty(
    name="Distance",
    description=("Max. occlusion distance."
                 " Surfaces further away do not occlude ambient light"),
    min=0.0, max=10000.0,
    default=1.0)

Scene.intg_AO_color = FloatVectorProperty(
    name="AO Color",
    description="Color Settings", subtype='COLOR',
    min=0.0, max=1.0,
    default=(0.9, 0.9, 0.9))

Scene.intg_bounces = IntProperty(
    name="Depth",
    description="",
    min=1,
    default=4)

Scene.intg_diffuse_radius = FloatProperty(
    name="Search radius",
    description="Radius to search for diffuse photons",
    min=0.001,
    default=1.0)

Scene.intg_cPhotons = IntProperty(
    name="Count",
    description="Number of caustic photons to be shot",
    min=1, default=500000)

Scene.intg_search = IntProperty(
    name="Search count",
    description="Maximum number of diffuse photons to be filtered",
    min=1, max=10000,
    default=100)

Scene.intg_final_gather = BoolProperty(
    name="Final Gather",
    description="Use final gathering (recommended)",
    default=True)

Scene.intg_fg_bounces = IntProperty(
    name="Bounces",
    description="Allow gather rays to extend to paths of this length",
    min=1, max=20,
    default=3)

Scene.intg_fg_samples = IntProperty(
    name="Samples",
    description="Number of samples for final gathering",
    min=1,
    default=16)

Scene.intg_show_map = BoolProperty(
    name="Show radiance map",
    description="Directly show radiance map, useful to calibrate the photon map (disables final gathering step)",
    default=False)

Scene.intg_caustic_method = EnumProperty(
    name="Caustic Method",
    items=(
        ('None', "None", ""),
        ('Path', "Path", ""),
        ('Path+Photon', "Path+Photon", ""),
        ('Photon', "Photon", "")),
    description="Choose caustic rendering method",
    default='None')

Scene.intg_path_samples = IntProperty(
    name="Path Samples",
    description="Number of path samples per pixel sample",
    min=1,
    default=32)

Scene.intg_no_recursion = BoolProperty(
    name="No Recursion",
    description="No recursive raytracing, only pure path tracing",
    default=False)

Scene.intg_debug_type = EnumProperty(
    name="Debug type",
    items=(
        ('N', "N", ""),
        ('dPdU', "dPdU", ""),
        ('dPdV', "dPdV", ""),
        ('NU', "NU", ""),
        ('NV', "NV", ""),
        ('dSdU', "dSdU", ""),
        ('dSdV', "dSdV", "")),
    default='dSdV')

Scene.intg_show_perturbed_normals = BoolProperty(
    name="Show perturbed normals",
    description="Show the normals perturbed by bump and normal maps",
    default=False)

Scene.intg_pm_ire = BoolProperty(
    name="PM IRE",
    default=False)

Scene.intg_pass_num = IntProperty(
    name="Passes",
    min=1,
    default=1000)

Scene.intg_times = FloatProperty(
    name="Radius factor",
    min=0.0,
    default=1.0)

Scene.intg_photon_radius = FloatProperty(
    name="Search radius",
    min=0.0,
    default=1.0)


class YAF_PT_render(RenderButtonsPanel, Panel):
    bl_label = "Yafaray Integrator"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "intg_light_method")

        if scene.intg_light_method == "Direct Lighting":
            row = layout.row()
            col = row.column(align=True)
            col.prop(scene, "intg_use_caustics", toggle=True)
            if scene.intg_use_caustics:
                col.prop(scene, "intg_caustic_depth")
                col.prop(scene, "intg_photons")
                col.prop(scene, "intg_caustic_radius")
                col.prop(scene, "intg_caustic_mix")

            col = row.column(align=True)
            col.prop(scene, "intg_use_AO", toggle=True)
            if scene.intg_use_AO:
                col.prop(scene, "intg_AO_color")
                col.prop(scene, "intg_AO_samples")
                col.prop(scene, "intg_AO_distance")

        elif scene.intg_light_method == "Photon Mapping":
            row = layout.row()

            row.prop(scene, "intg_bounces")

            row = layout.row()

            col = row.column(align=True)
            col.label(" Diffuse Photons:", icon='MOD_PHYSICS')
            col.prop(scene, "intg_photons")
            col.prop(scene, "intg_diffuse_radius")
            col.prop(scene, "intg_search")

            col = row.column(align=True)
            col.label(" Caustic Photons:", icon='MOD_PARTICLES')
            col.prop(scene, "intg_cPhotons")
            col.prop(scene, "intg_caustic_radius")
            col.prop(scene, "intg_caustic_mix")

            row = layout.row()
            row.prop(scene, "intg_final_gather", toggle=True, icon='FORCE_FORCE')

            if scene.intg_final_gather:
                col = layout.row()
                col.prop(scene, "intg_fg_bounces")
                col.prop(scene, "intg_fg_samples")
                col = layout.row()
                col.prop(scene, "intg_show_map", toggle=True)

        elif scene.intg_light_method == "Pathtracing":
            col = layout.row()
            col.prop(scene, "intg_caustic_method")

            col = layout.row()

            if scene.intg_caustic_method in {"Path+Photon", "Photon"}:
                col.prop(scene, "intg_photons", text="Photons")
                col.prop(scene, "intg_caustic_mix", text="Caus. Mix")
                col = layout.row()
                col.prop(scene, "intg_caustic_depth", text="Caus. Depth")
                col.prop(scene, "intg_caustic_radius", text="Caus. Radius")

            col = layout.row()
            col.prop(scene, "intg_path_samples")
            col.prop(scene, "intg_bounces")
            col = layout.row()
            col.prop(scene, "intg_no_recursion")

        elif scene.intg_light_method == "Debug":
            layout.row().prop(scene, "intg_debug_type")
            layout.row().prop(scene, "intg_show_perturbed_normals")

        elif scene.intg_light_method == "SPPM":
            col = layout.column()
            col.prop(scene, "intg_photons", text="Photons")
            col.prop(scene, "intg_pass_num")
            col.prop(scene, "intg_bounces", text="Bounces")
            col.prop(scene, "intg_times")
            col.prop(scene, "intg_diffuse_radius")
            col.prop(scene, "intg_search")
            col.prop(scene, "intg_pm_ire")
