import bpy
#import types and props ---->
from bpy.props import *
Scene = bpy.types.Scene

Scene.img_output     =  EnumProperty(
                        description = "Image will be saved in this file format",  # yafarays own image output selection, default is open exr
                        items = (
                            ("PNG", " PNG (Portable Network Graphics)", ""),
                            ("TARGA", " TGA (Truevision TARGA)", ""),
                            ("JPEG", " JPEG (Joint Photographic Experts Group)", ""),
                            ("TIFF", " TIFF (Tag Image File Format)", ""),
                            ("OPEN_EXR", " EXR (IL&M OpenEXR)", ""),
                            ("HDR", " HDR (Radiance RGBE)", "")),
                        default = "OPEN_EXR",
                        name = "Image File Type")


class YafarayRenderButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(self, context):
        render = context.scene.render
        return (render.engine in self.COMPAT_ENGINES)


class YAFRENDER_PT_render(YafarayRenderButtonsPanel, bpy.types.Panel):

    bl_label = 'Render'

    def draw(self, context):

        split = self.layout.split()

        split.column().operator("RENDER_OT_render_animation", "Render Image", "RENDER_STILL").animation = False
        split.column().operator("RENDER_OT_render_animation", "Render Animation", "RENDER_ANIMATION").animation = True

        if context.scene.render.engine == "YAFA_RENDER":
            self.layout.row().operator("RENDER_OT_render_view", "Render 3D View", "VIEW3D")

        self.layout.row().prop(context.scene.render, "display_mode")


class YAFRENDER_PT_dimensions(YafarayRenderButtonsPanel, bpy.types.Panel):

    bl_label = "Dimensions"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render

        row = layout.row(align=True)
        row.menu("RENDER_MT_presets", text = bpy.types.RENDER_MT_presets.bl_label)
        row.operator("render.preset_add", text = "", icon = "ZOOMIN")
        row.operator("render.preset_add", text = "", icon = "ZOOMOUT").remove_active = True

        split = layout.split()

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Resolution:")
        sub.prop(rd, "resolution_x", text = "X")
        sub.prop(rd, "resolution_y", text = "Y")
        sub.prop(rd, "resolution_percentage", text = "")

        row = layout.row(align = True)
        row.prop(rd, "use_border", text = "Border", toggle = True)

        col = split.column()
        sub = col.column(align = True)
        sub.label(text="Frame Range:")
        sub.prop(scene, "frame_start", text = "Start")
        sub.prop(scene, "frame_end", text = "End")
        sub.prop(scene, "frame_step", text = "Step")

from yafaray.ui import properties_yaf_general_settings
from yafaray.ui import properties_yaf_integrator
from yafaray.ui import properties_yaf_AA_settings


class YAFRENDER_PT_output(YafarayRenderButtonsPanel, bpy.types.Panel):

    bl_label = "Output Settings"

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render
        sc = context.scene

        layout.prop(rd, "filepath", text = "")

        split = layout.split(percentage = 0.6)
        col = split.column()
        col.prop(sc, "img_output", text = "", icon = "IMAGE_DATA")
        col = split.column()
        col.row().prop(rd, "color_mode", text="Color", expand=True)

class YAFRENDER_PT_post_processing(YafarayRenderButtonsPanel, bpy.types.Panel):

    bl_label = "Post Processing"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render

        split = layout.split()

        col = split.column()
        col.prop(rd, "use_compositing")
        col.prop(rd, "use_sequencer")

        col = split.column()
        col.prop(rd, "dither_intensity", text = "Dither", slider = True)
