import bpy
import sys
from ..ot import yafaray_presets
from bl_ui.properties_render import RenderButtonsPanel
RenderButtonsPanel.COMPAT_ENGINES = {'YAFA_RENDER'}
#import types and props ---->
from bpy.props import (IntProperty,
                       FloatProperty,
                       EnumProperty,
                       BoolProperty,
                       StringProperty)
from bpy.types import Panel, Menu
Scene = bpy.types.Scene

# Default Gamma values for Windows = 2.2, for Linux and MacOS = 1.8
if sys.platform == "win32":
    gamma = 2.20
else:
    gamma = 1.80

Scene.gs_ray_depth = IntProperty(
    name="Ray Depth",
    description="Maximum depth for recursive raytracing",
    min=0, max=64, default=2)

Scene.gs_shadow_depth = IntProperty(
    name="Shadow Depth",
    description="Max. depth for transparent shadows calculation (if enabled)",
    min=0, max=64, default=2)

Scene.gs_threads = IntProperty(
    name="Threads",
    description="Number of threads to use for rendering",
    min=1, default=1)

Scene.gs_gamma = FloatProperty(
    name="Gamma",
    description="Gamma correction applied to final output, inverse correction \
of textures and colors is performed",
    min=0, max=5, default=gamma)

Scene.gs_gamma_input = FloatProperty(
    name="Gamma Input",
    description="Gamma correction applied to input",
    min=0, max=5, default=gamma)

Scene.gs_tile_size = IntProperty(
    name="Tile Size",
    description="Size of the render buckets (tiles)",
    min=0, max=1024, default=32)

Scene.gs_tile_order = EnumProperty(
    name="Tile Order",
    description="Selects tiles order type",
    items=(
        ('linear', "Linear", ""),
        ('random', "Random", "")
    ),
    default='random')

Scene.gs_auto_threads = BoolProperty(
    name="Auto Threads",
    description="Activate thread number auto detection",
    default=True)

Scene.gs_clay_render = BoolProperty(
    name="Clay Render",
    description="Override all materials with a white diffuse material",
    default=False)

Scene.gs_draw_params = BoolProperty(
    name="Draw Parameters",
    description="Write the render parameters below the image",
    default=False)

Scene.gs_custom_string = StringProperty(
    name="Custom String",
    description="Custom string will be added to the info bar, \
use it for CPU, RAM etc.",
    default="")

Scene.gs_premult = BoolProperty(
    name="Premultiply",
    description="Premultipy Alpha channel for renders with transparent background",
    default=False)

Scene.gs_transp_shad = BoolProperty(
    name="Transparent Shadows",
    description="Compute transparent shadows",
    default=False)

Scene.gs_clamp_rgb = BoolProperty(
    name="Clamp RGB",
    description="Reduce the color's brightness to a low dynamic",
    default=False)

Scene.gs_show_sam_pix = BoolProperty(
    name="Show Sample Pixels",
    description="Masks pixels marked for resampling during adaptive passes",
    default=True)

Scene.gs_z_channel = BoolProperty(
    name="Render Depth Map",
    description="Render depth map (Z-Buffer)",
    default=False)

Scene.gs_verbose = BoolProperty(
    name="Log Info in Console",
    description="Print YafaRay engine log messages in console window",
    default=True)

Scene.gs_type_render = EnumProperty(
    name="Render",
    description="Choose the render output method",
    items=(
        ('file', "Image File", "Render the Scene and write it to an Image File when finished"),
        ('into_blender', "Into Blender", "Render the Scene into Blenders Renderbuffer"),
        ('xml', "XML File", "Export the Scene to a XML File")
    ),
    default='into_blender')


class YAFARAY_MT_presets_render(Menu):
    bl_label = "Yafaray Render Presets"
    preset_subdir = "render"
    preset_operator = "script.execute_preset"
    draw = yafaray_presets.Yafaray_Menu.draw_preset


class YAF_PT_general_settings(RenderButtonsPanel, Panel):
    bl_label = "General Settings"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row(align=True)
        row.menu("YAFARAY_MT_presets_render", text=bpy.types.YAFARAY_MT_presets_render.bl_label)
        row.operator("yafaray.preset_add", text="", icon='ZOOMIN')
        row.operator("yafaray.preset_add", text="", icon='ZOOMOUT').remove_active = True

        layout.separator()

        split = layout.split(percentage=0.58)
        col = split.column()
        col.prop(scene, "gs_ray_depth")
        col.prop(scene, "gs_gamma")
        col.prop(scene, "gs_type_render")
        sub = col.column()
        sub.enabled = scene.gs_type_render == "into_blender"
        sub.prop(scene, "gs_tile_order")

        col = split.column()
        sub = col.column()
        sub.enabled = scene.gs_transp_shad
        sub.prop(scene, "gs_shadow_depth")
        col.prop(scene, "gs_gamma_input")
        sub = col.column()
        sub.enabled = scene.gs_auto_threads == False
        sub.prop(scene, "gs_threads")
        sub = col.column()
        sub.enabled = scene.gs_type_render == "into_blender"
        sub.prop(scene, "gs_tile_size")

        layout.separator()

        row = layout.row()
        col = row.column()
        col.prop(scene, "gs_clay_render")
        col.prop(scene, "gs_transp_shad")
        col.prop(scene, "gs_premult")
        sub = col.column()
        sub.enabled = scene.gs_type_render == "file"
        sub.prop(scene, "gs_z_channel")
        col.prop(scene, "gs_draw_params")

        col = row.column()
        col.prop(scene, "gs_auto_threads")
        col.prop(scene, "gs_clamp_rgb")
        col.prop(scene, "gs_show_sam_pix")
        col.prop(scene, "gs_verbose")

        row = layout.row()
        col = row.column()
        col.enabled = scene.gs_draw_params
        col.prop(scene, "gs_custom_string")
