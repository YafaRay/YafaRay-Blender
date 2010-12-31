import bpy
# import all props
from bpy.props import *

Scene = bpy.types.Scene

Scene.gs_ray_depth =    IntProperty(attr="gs_ray_depth",
                        description = "Maximum depth for recursive raytracing", # for description tooltips
                        min = 0, max = 64,
                        default = 2)
Scene.gs_shadow_depth = IntProperty(attr="gs_shadow_depth",
                        description = "Max. depth for transparent shadows calculation (if enabled)",
                        min = 0, max = 64,
                        default = 2)
Scene.gs_threads =      IntProperty(attr="gs_threads",
                        description = "Number of threads to use for rendering",
                        min = 1,
                        default = 1)
Scene.gs_gamma =        FloatProperty(attr="gs_gamma",
                        description = "Gamma correction applied to final output, inverse correction of textures and colors is performed",
                        min = 0, max = 5,
                        default = 1.8)
Scene.gs_gamma_input =  FloatProperty(attr="gs_gamma_input",
                        description = "Gamma correction applied to input",
                        min = 0, max = 5,
                        default = 1.8)
Scene.gs_tile_size =    IntProperty(attr="gs_tile_size",
                        description = "Size of the render buckets (tiles)",
                        min = 0, max = 1024,
                        default = 32)
Scene.gs_tile_order =   EnumProperty(attr="gs_tile_order",
                        description = "Selects tiles order type",
                        items = (
                        ("Tile order","Tile order",""),
                        ("linear","Linear",""),
                        ("random","Random",""),
                        ),default="random")
Scene.gs_auto_threads = BoolProperty(attr="gs_auto_threads",
                        description = "Activate thread number auto detection",
                        default = True)
Scene.gs_clay_render =  BoolProperty(attr="gs_clay_render",
                        description = "Override all materials with a white diffuse material",
                        default = False)
Scene.gs_draw_params =  BoolProperty(attr="gs_draw_params",
                        description = "Write the render parameters below the image",
                        default = False)
Scene.gs_custom_string = StringProperty(attr="gs_custom_string",
                        description = "Custom string will be added to the info bar, use it for CPU, RAM etc.",
                        default = "")
Scene.gs_auto_save =    BoolProperty(attr="gs_auto_save",
                        description = "Save each rendering result automatically",
                        default = False)
Scene.gs_auto_alpha =   BoolProperty(attr="gs_auto_alpha",
                        description = "Save alpha channel when rendering to autosave or doing animation",
                        default = False)
Scene.gs_premult =      BoolProperty(attr="gs_premult",
                        description = "Premultipy Alpha channel for renders with transparent background",
                        default = False)
Scene.gs_transp_shad =  BoolProperty(attr="gs_transp_shad",
                        description = "Compute transparent shadows",
                        default = False)
Scene.gs_clamp_rgb =    BoolProperty(attr="gs_clamp_rgb",
                        description = "Reduce the colors' brightness to a low dynamic",
                        default = False)
Scene.gs_show_sam_pix = BoolProperty(attr="gs_show_sam_pix",
                        description = "Masks pixels marked for resampling during adaptive passes",
                        default = False)
Scene.gs_z_channel =    BoolProperty(attr="gs_z_channel",
                        description = "Render depth map (Z-Buffer)",
                        default = False)
Scene.gs_type_render =  EnumProperty(attr="gs_type_render",
                        description = "Render to view Blender or to File, (load at the end)",
                        items = (
                        ("Render Type","Type render",""),
                        ("file","File, load at the end",""),
                        ("into_blender","Into Blender",""),
                        ), default = "into_blender")

class YAF_PT_general_settings(bpy.types.Panel):

    bl_label = 'General Settings'
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
        split = layout.split(percentage=0.6)
        col = split.column()
        row = layout.row()

        col.prop(context.scene,"gs_ray_depth", text= "Ray Depth")
        if context.scene.gs_transp_shad:
            col.prop(context.scene,"gs_shadow_depth", text= "Shadow Depth")
        if context.scene.gs_auto_threads == False:
            col.prop(context.scene,"gs_threads", text= "Threads")
        col.prop(context.scene,"gs_gamma", text= "Gamma")
        col.prop(context.scene,"gs_gamma_input", text= "Gamma Input")

        col.prop(context.scene,"gs_type_render", text = "Render")
        if context.scene.gs_type_render == "into_blender":
            col.prop(context.scene,"gs_tile_order", text= "Tile order")
            col.prop(context.scene,"gs_tile_size", text= "Tile Size")

        else:
            col.prop(context.scene,"gs_draw_params", text= "Draw Params")
            if context.scene.gs_draw_params:
                col = layout.row()
                col.prop(context.scene,"gs_custom_string", text= "Custom String")

        col = split.column()
        col.prop(context.scene,"gs_clay_render", text= "Clay Render")
        col.prop(context.scene,"gs_transp_shad", text= "Transp. Shadow")
        col.prop(context.scene,"gs_auto_save", text= "Auto Save")
        col.prop(context.scene,"gs_auto_threads", text= "Auto Threads")
        col.prop(context.scene,"gs_auto_alpha", text= "Auto Alpha")
        col.prop(context.scene,"gs_premult", text= "Premultiply")
        col.prop(context.scene,"gs_clamp_rgb", text= "Clamp RGB")
        col.prop(context.scene,"gs_show_sam_pix", text= "Show Sam Pix")




classes = [
    YAF_PT_general_settings,
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