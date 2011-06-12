import bpy
from bpy.props import *
Scene = bpy.types.Scene

Scene.AA_min_samples = IntProperty(
                        description = "Number of samples for first AA pass",
                        min = 1,
                        default = 1)
Scene.AA_inc_samples = IntProperty(
                        description = "Number of samples for additional AA passes",
                        min = 1,
                        default = 1)
Scene.AA_passes =      IntProperty(
                        description = "Number of anti-aliasing passes. Adaptive sampling (passes > 1) uses different pattern",
                        min = 1,
                        default = 1)
Scene.AA_threshold =   FloatProperty(
                        description = "Color threshold for additional AA samples in next pass",
                        min = 0, max = 1,
                        default = 0.05, precision = 4)
Scene.AA_pixelwidth =  FloatProperty(
                        description = "AA filter size",
                        min = 1,
                        default = 1.5,
                        precision = 3)
Scene.AA_filter_type = EnumProperty(
                    items = (
                        ("box", "Box", ""),
                        ("mitchell", "Mitchell", ""),
                        ("gauss", "Gauss", ""),
                        ("lanczos", "Lanczos", "")
                        ),
                    default = "gauss",
                    name = "Filter Type")


class YAF_PT_AA_settings(bpy.types.Panel):

    bl_label = 'Anti-Aliasing Settings'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(self, context):
        engine = context.scene.render.engine
        return (True  and  (engine in self.COMPAT_ENGINES))

    def draw(self, context):

        sc = context.scene

        layout = self.layout
        split = layout.split()
        col = split.column()
        col.prop(sc, "AA_filter_type", text = "Filter")
        col.prop(sc, "AA_min_samples", text = "Samples")
        col.prop(sc, "AA_pixelwidth", text = "Pixelwidth")
        col = split.column()
        col.prop(sc, "AA_passes", text = "Passes")

        sub = col.column()

        sub.enabled = (context.scene.AA_passes > 1)
        sub.prop(sc, "AA_inc_samples", text = "Additional Samples")
        sub.prop(sc, "AA_threshold", text = "Threshold")
