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
                        default = 1.5)
Scene.AA_filter_type = EnumProperty(
                    items = (
                        ("AA Filter Type","AA Filter Type",""),
                        ("box","Box",""),
                        ("mitchell","Mitchell",""),
                        ("gauss","Gauss",""),
                        ("lanczos","Lanczos","")
                        ),
                    default="gauss")


class YAF_PT_AA_settings(bpy.types.Panel):

    bl_label = 'AA Settings'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    COMPAT_ENGINES =['YAFA_RENDER']

    @classmethod
    def poll(self, context):
        engine = context.scene.render.engine
        return (True  and  (engine in self.COMPAT_ENGINES) ) 


    def draw(self, context):

        layout = self.layout
        split = layout.split()
        col = split.column()
        col.prop(context.scene,"AA_filter_type", text= "AA Filter Type")
        col.prop(context.scene,"AA_min_samples", text= "AA Samples")
        col.prop(context.scene,"AA_pixelwidth", text= "AA Pixelwidth")
        col = split.column()
        col.prop(context.scene,"AA_passes", text= "AA Passes")
        if context.scene.AA_passes > 1:
            col.prop(context.scene,"AA_inc_samples", text= "AA Inc. Samples")
            col.prop(context.scene,"AA_threshold", text= "AA Threshold")

