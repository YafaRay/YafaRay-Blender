import bpy
# import types and props ---->
from bpy.props import (IntProperty,
                       FloatProperty,
                       EnumProperty)
from bpy.types import Panel
from bl_ui.properties_render import RenderButtonsPanel
RenderButtonsPanel.COMPAT_ENGINES = {'YAFA_RENDER'}

Scene = bpy.types.Scene

Scene.AA_min_samples = IntProperty(
    name="Samples",
    description="Number of samples for first AA pass",
    min=1,
    default=1)

Scene.AA_inc_samples = IntProperty(
    name="Additional Samples",
    description="Number of samples for additional AA passes",
    min=1,
    default=1)

Scene.AA_passes = IntProperty(
    name="Passes",
    description=("Number of anti-aliasing passes."
                 " Adaptive sampling (passes > 1) uses different pattern"),
    min=1,
    default=1)

Scene.AA_threshold = FloatProperty(
    name="Threshold",
    description="Color threshold for additional AA samples in next pass",
    min=0.0, max=1.0, precision=4,
    default=0.05)

Scene.AA_pixelwidth = FloatProperty(
    name="Pixelwidth",
    description="AA filter size",
    min=1.0, max=20.0, precision=3,
    default=1.5)

Scene.AA_filter_type = EnumProperty(
    name="Filter",
    items=(
        ('box', "Box", "AA filter type"),
        ('mitchell', "Mitchell", "AA filter type"),
        ('gauss', "Gauss", "AA filter type"),
        ('lanczos', "Lanczos", "AA filter type")
    ),
    default="gauss")


class YAF_PT_AA_settings(RenderButtonsPanel, Panel):
    bl_label = "Anti-Aliasing Settings"

    def draw(self, context):

        scene = context.scene
        layout = self.layout

        split = layout.split()
        col = split.column()
        col.prop(scene, 'AA_filter_type')
        col.prop(scene, 'AA_min_samples')
        col.prop(scene, 'AA_pixelwidth')

        col = split.column()
        col.prop(scene, 'AA_passes')
        sub = col.column()
        sub.enabled = scene.AA_passes > 1
        sub.prop(scene, 'AA_inc_samples')
        sub.prop(scene, 'AA_threshold')
