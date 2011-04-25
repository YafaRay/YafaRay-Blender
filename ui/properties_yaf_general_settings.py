import bpy
import sys
import os
from yafaray.ot import yafaray_presets
#import types and props ---->
from bpy.props import *
Scene = bpy.types.Scene


# Default Gamma values for Windows Platform = 2.2 other Platforms (Linux/MacOS) = 1.8
if sys.platform == 'win32':
    gamma = 2.20
else:
    gamma = 1.80


Scene.gs_ray_depth =    IntProperty(attr = "gs_ray_depth",
                        description = "Maximum depth for recursive raytracing",  # for description tooltips
                        min = 0, max = 64,
                        default = 2)
Scene.gs_shadow_depth = IntProperty(attr = "gs_shadow_depth",
                        description = "Max. depth for transparent shadows calculation (if enabled)",
                        min = 0, max = 64,
                        default = 2)
Scene.gs_threads =      IntProperty(attr = "gs_threads",
                        description = "Number of threads to use for rendering",
                        min = 1,
                        default = 1)
Scene.gs_gamma =        FloatProperty(attr = "gs_gamma",
                        description = "Gamma correction applied to final output, inverse correction of textures and colors is performed",
                        min = 0, max = 5,
                        default = gamma)
Scene.gs_gamma_input =  FloatProperty(attr = "gs_gamma_input",
                        description = "Gamma correction applied to input",
                        min = 0, max = 5,
                        default = gamma)
Scene.gs_tile_size =    IntProperty(attr = "gs_tile_size",
                        description = "Size of the render buckets (tiles)",
                        min = 0, max = 1024,
                        default = 32)
Scene.gs_tile_order =   EnumProperty(
                        description = "Selects tiles order type",
                        items = (
                            ("linear", "Linear", ""),
                            ("random", "Random", "")),
                        default = "random",
                        name = "Tile Order")
Scene.gs_auto_threads = BoolProperty(attr = "gs_auto_threads",
                        description = "Activate thread number auto detection",
                        default = True)
Scene.gs_clay_render =  BoolProperty(attr = "gs_clay_render",
                        description = "Override all materials with a white diffuse material",
                        default = False)
Scene.gs_draw_params =  BoolProperty(attr = "gs_draw_params",
                        description = "Write the render parameters below the image",
                        default = False)
Scene.gs_custom_string = StringProperty(attr = "gs_custom_string",
                        description = "Custom string will be added to the info bar, use it for CPU, RAM etc.",
                        default = "")
Scene.gs_auto_save =    BoolProperty(attr = "gs_auto_save",
                        description = "Save each rendering result automatically",
                        default = False)
Scene.gs_auto_alpha =   BoolProperty(attr = "gs_auto_alpha",
                        description = "Save alpha channel when rendering to autosave or doing animation",
                        default = False)
Scene.gs_premult =      BoolProperty(attr = "gs_premult",
                        description = "Premultipy Alpha channel for renders with transparent background",
                        default = False)
Scene.gs_transp_shad =  BoolProperty(attr = "gs_transp_shad",
                        description = "Compute transparent shadows",
                        default = False)
Scene.gs_clamp_rgb =    BoolProperty(attr = "gs_clamp_rgb",
                        description = "Reduce the colors' brightness to a low dynamic",
                        default = False)
Scene.gs_show_sam_pix = BoolProperty(attr = "gs_show_sam_pix",
                        description = "Masks pixels marked for resampling during adaptive passes",
                        default = True)
Scene.gs_z_channel =    BoolProperty(attr = "gs_z_channel",
                        description = "Render depth map (Z-Buffer)",
                        default = False)
Scene.gs_type_render =  EnumProperty(
                        description = "Choose the Render Method",
                        items = (
                            ("file", "Image File", "Render the Scene and write it to an Image File when finished"),
                            ("into_blender", "Into Blender", "Render the Scene into Blenders Renderbuffer"),
                            ("xml", "XML File", "Export the Scene to a XML File")),
                        default = "into_blender",
                        name = "Output Method")


class YAFARAY_MT_presets_render(bpy.types.Menu):
    bl_label = "Yafaray Render Presets"
    preset_subdir = "render"
    preset_operator = "script.execute_preset"
    draw = yafaray_presets.Yafaray_Menu.draw_preset


class YAF_PT_general_settings(bpy.types.Panel):
    bl_label = 'General Settings'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(self, context):

        engine = context.scene.render.engine
        return (True  and  (engine in self.COMPAT_ENGINES))

    def draw(self, context):

        layout = self.layout

        sc = context.scene
        rd = sc.render

        row = layout.row(align = True)
        row.menu("YAFARAY_MT_presets_render", text = bpy.types.YAFARAY_MT_presets_render.bl_label)
        row.operator("yafaray.preset_add", text = "", icon = "ZOOMIN")
        row.operator("yafaray.preset_add", text = "", icon = "ZOOMOUT").remove_active = True

        layout.separator()

        split = layout.split(percentage = 0.58)
        col = split.column()
        col.prop(sc, "gs_ray_depth", text = "Ray Depth")
        col.prop(sc, "gs_gamma", text = "Gamma")
        col.prop(sc, "gs_type_render", text = "Render")
        sub = col.column()
        sub.enabled = sc.gs_type_render == "into_blender"
        sub.prop(sc, "gs_tile_order", text = "Tile order")

        col = split.column()
        sub = col.column()
        sub.enabled = sc.gs_transp_shad
        sub.prop(sc, "gs_shadow_depth", text = "Shadow Depth")
        col.prop(sc, "gs_gamma_input", text = "Gamma Input")
        sub = col.column()
        sub.enabled = sc.gs_auto_threads == False
        sub.prop(sc, "gs_threads", text = "Threads")
        sub = col.column()
        sub.enabled = sc.gs_type_render == "into_blender"
        sub.prop(sc, "gs_tile_size", text = "Tile Size")

        layout.separator()

        row = layout.row()
        col = row.column()
        col.prop(rd, "use_color_management", text = "Use Linear Workflow")
        col.prop(sc, "gs_clay_render", text = "Clay Render")
        col.prop(sc, "gs_transp_shad", text = "Transparent Shadow")
        col.prop(sc, "gs_auto_save", text = "Auto Save")
        sub = col.column()
        sub.enabled = sc.gs_type_render == "file"
        sub.prop(sc, "gs_z_channel", text = "Render Depth Map")
        col.prop(sc, "gs_draw_params", text = "Draw Parameters")

        col = row.column()
        col.prop(sc, "gs_auto_threads", text = "Auto Threads")
        col.prop(sc, "gs_auto_alpha", text = "Auto Alpha")
        col.prop(sc, "gs_premult", text = "Premultiply")
        col.prop(sc, "gs_clamp_rgb", text = "Clamp RGB")
        col.prop(sc, "gs_show_sam_pix", text = "Show Sam Pix")

        row = layout.row()
        col = row.column()
        col.enabled = sc.gs_draw_params
        col.prop(sc, "gs_custom_string", text = "Custom String")
