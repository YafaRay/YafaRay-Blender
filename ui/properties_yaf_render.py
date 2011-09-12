import bpy
#import types and props ---->
from bpy.props import EnumProperty
from bpy.types import Panel
from bl_ui.properties_render import RenderButtonsPanel
RenderButtonsPanel.COMPAT_ENGINES = {'YAFA_RENDER'}
Scene = bpy.types.Scene


# set fileformat for image saving on same format as in YafaRay, both have default PNG
def call_update_fileformat(self, context):
    sc = context.scene
    rd = sc.render
    if sc.img_output != rd.file_format:
        rd.file_format = sc.img_output
        if rd.file_format == "OPEN_EXR" and sc.gs_z_channel:
            rd.exr_zbuf = True


# YafaRays own image output selection, default is PNG
Scene.img_output = EnumProperty(
    name="Image File Type",
    description="Image will be saved in this file format",
    items=(
        ('PNG', " PNG (Portable Network Graphics)", ""),
        ('TARGA', " TGA (Truevision TARGA)", ""),
        ('JPEG', " JPEG (Joint Photographic Experts Group)", ""),
        ('TIFF', " TIFF (Tag Image File Format)", ""),
        ('OPEN_EXR', " EXR (IL&M OpenEXR)", ""),
        ('HDR', " HDR (Radiance RGBE)", "")
    ),
    default='PNG', update=call_update_fileformat)


class YAFRENDER_PT_render(RenderButtonsPanel, Panel):
    bl_label = "Render"

    def draw(self, context):

        layout = self.layout
        rd = context.scene.render

        row = layout.row()
        row.operator("render.render_still", text="Image", icon='RENDER_STILL')
        row.operator("render.render_animation", text="Animation", icon='RENDER_ANIMATION')
        layout.row().operator("render.render_view", text="Render 3D View", icon='VIEW3D')
        layout.prop(rd, "display_mode", text="Display")


class YAFRENDER_PT_dimensions(RenderButtonsPanel, Panel):
    bl_label = "Dimensions"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render

        row = layout.row(align=True)
        row.menu("RENDER_MT_presets", text=bpy.types.RENDER_MT_presets.bl_label)
        row.operator("render.preset_add", text="", icon='ZOOMIN')
        row.operator("render.preset_add", text="", icon='ZOOMOUT').remove_active = True

        split = layout.split()

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Resolution:")
        sub.prop(rd, "resolution_x", text="X")
        sub.prop(rd, "resolution_y", text="Y")
        sub.prop(rd, "resolution_percentage", text="")

        # Border render disabled in UI, has to be solved in YafaRay engine first...
        # layout.row().prop(rd, "use_border", text="Border", toggle=True)

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Frame Range:")
        sub.prop(scene, "frame_start", text="Start")
        sub.prop(scene, "frame_end", text="End")
        sub.prop(scene, "frame_step", text="Step")

from . import properties_yaf_general_settings
from . import properties_yaf_integrator
from . import properties_yaf_AA_settings


class YAFRENDER_PT_output(RenderButtonsPanel, Panel):
    bl_label = "Output Settings"

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render
        sc = context.scene

        layout.prop(rd, "filepath", text="")

        split = layout.split(percentage=0.6)
        col = split.column()
        col.prop(sc, "img_output", text="", icon='IMAGE_DATA')
        col = split.column()
        col.row().prop(rd, "color_mode", text="Color", expand=True)


class YAFRENDER_PT_post_processing(RenderButtonsPanel, Panel):
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
        col.prop(rd, "dither_intensity", text="Dither", slider=True)


class YAF_PT_convert(RenderButtonsPanel, Panel):
    bl_label = "Convert old YafaRay Settings"

    def draw(self, context):
        layout = self.layout
        layout.column().operator("data.convert_yafaray_properties", text="Convert data from 2.4x")
