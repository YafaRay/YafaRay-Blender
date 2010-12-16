import bpy
from bpy.props import *
Scene = bpy.types.Scene


Scene.AA_min_samples = IntProperty(attr="AA_min_samples",
                        description = "Number of samples for first AA pass",
                        min = 1,
                        default = 1)
Scene.AA_inc_samples = IntProperty(attr="AA_inc_samples",
                        description = "Number of samples for additional AA passes",
                        min = 1,
                        default = 1)
Scene.AA_passes =      IntProperty(attr="AA_passes",
                        description = "Number of anti-aliasing passes. Adaptive sampling (passes > 1) uses different pattern",
                        min = 1,
                        default = 1)
Scene.AA_threshold =   FloatProperty(attr="AA_threshold",
                        description = "Color threshold for additional AA samples in next pass",
                        min = 0, max = 1,
                        default = 0.05, precision = 4)
Scene.AA_pixelwidth =  FloatProperty(attr="AA_pixelwidth",
                        description = "AA filter size",
                        min = 1,
                        default = 1.5)
Scene.AA_filter_type = EnumProperty(attr="AA_filter_type",
                    items = (
                    ("AA Filter Type","AA Filter Type",""),
                    ("Box","Box",""),
                    ("Mitchell","Mitchell",""),
                    ("Gauss","Gauss",""),
                    ("Lanczos","Lanczos","")
                    ),default="Gauss")


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




classes = [
    YAF_PT_AA_settings,
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

