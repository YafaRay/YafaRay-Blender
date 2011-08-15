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

Scene.gs_ray_depth =    IntProperty(
                        name = 'Ray Depth',
                        description = 'Maximum depth for recursive raytracing',
                        min = 0, max = 64,
                        default = 2)

Scene.gs_shadow_depth = IntProperty(
                        name = 'Shadow Depth',
                        description = 'Max. depth for transparent shadows calculation (if enabled)',
                        min = 0, max = 64,
                        default = 2)

Scene.gs_threads =      IntProperty(
                        name = 'Threads',
                        description = 'Number of threads to use for rendering',
                        min = 1,
                        default = 1)

Scene.gs_gamma =        FloatProperty(
                        name = 'Gamma',
                        description = 'Gamma correction applied to final output, inverse correction of textures and colors is performed',
                        min = 0, max = 5,
                        default = gamma)

Scene.gs_gamma_input =  FloatProperty(
                        name = 'Gamma Input',
                        description = 'Gamma correction applied to input',
                        min = 0, max = 5,
                        default = gamma)

Scene.gs_tile_size =    IntProperty(
                        name = 'Tile Size',
                        description = 'Size of the render buckets (tiles)',
                        min = 0, max = 1024,
                        default = 32)

Scene.gs_tile_order =   EnumProperty(
                        name = 'Tile Order',
                        description = 'Selects tiles order type',
                        items = (
                            ('linear', 'Linear', ''),
                            ('random', 'Random', '')),
                        default = 'random')

Scene.gs_auto_threads = BoolProperty(
                        name = 'Auto Threads',
                        description = 'Activate thread number auto detection',
                        default = True)

Scene.gs_clay_render =  BoolProperty(
                        name = 'Clay Render',
                        description = 'Override all materials with a white diffuse material',
                        default = False)

Scene.gs_draw_params =  BoolProperty(
                        name = 'Draw Parameters',
                        description = 'Write the render parameters below the image',
                        default = False)

Scene.gs_custom_string = StringProperty(
                        name = 'Custom String',
                        description = 'Custom string will be added to the info bar, use it for CPU, RAM etc.',
                        default = '')

Scene.gs_premult =      BoolProperty(
                        name = 'Premultiply',
                        description = 'Premultipy Alpha channel for renders with transparent background',
                        default = False)

Scene.gs_transp_shad =  BoolProperty(
                        name = 'Transparent Shadows',
                        description = 'Compute transparent shadows',
                        default = False)

Scene.gs_clamp_rgb =    BoolProperty(
                        name = 'Clamp RGB',
                        description = 'Reduce the color\'s brightness to a low dynamic',
                        default = False)

Scene.gs_show_sam_pix = BoolProperty(
                        name = 'Show Sample Pixels',
                        description = 'Masks pixels marked for resampling during adaptive passes',
                        default = True)

Scene.gs_z_channel =    BoolProperty(
                        name = 'Render Depth Map',
                        description = 'Render depth map (Z-Buffer)',
                        default = False)

Scene.gs_verbose =      BoolProperty(
                        name = 'Log Info in Console',
                        description = 'Print YafaRay engine log messages in console window',
                        default = True)

Scene.gs_type_render =  EnumProperty(
                        name = 'Render',
                        description = 'Choose the render output method',
                        items = (
                            ('file', 'Image File', 'Render the Scene and write it to an Image File when finished'),
                            ('into_blender', 'Into Blender', 'Render the Scene into Blenders Renderbuffer'),
                            ('xml', 'XML File', 'Export the Scene to a XML File')),
                        default = 'into_blender')


class YAFARAY_MT_presets_render(bpy.types.Menu):
    bl_label = 'Yafaray Render Presets'
    preset_subdir = 'render'
    preset_operator = 'script.execute_preset'
    draw = yafaray_presets.Yafaray_Menu.draw_preset


class YAF_PT_general_settings(bpy.types.Panel):
    bl_label = 'General Settings'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(cls, context):

        engine = context.scene.render.engine
        return (True  and  (engine in cls.COMPAT_ENGINES))

    def draw(self, context):

        layout = self.layout

        sc = context.scene
        rd = sc.render

        row = layout.row(align = True)
        row.menu('YAFARAY_MT_presets_render', text = bpy.types.YAFARAY_MT_presets_render.bl_label)
        row.operator('yafaray.preset_add', text = '', icon = 'ZOOMIN')
        row.operator('yafaray.preset_add', text = '', icon = 'ZOOMOUT').remove_active = True

        layout.separator()

        split = layout.split(percentage = 0.58)
        col = split.column()
        col.prop(sc, 'gs_ray_depth')
        col.prop(sc, 'gs_gamma')
        col.prop(sc, 'gs_type_render')
        sub = col.column()
        sub.enabled = sc.gs_type_render == 'into_blender'
        sub.prop(sc, 'gs_tile_order')

        col = split.column()
        sub = col.column()
        sub.enabled = sc.gs_transp_shad
        sub.prop(sc, 'gs_shadow_depth')
        col.prop(sc, 'gs_gamma_input')
        sub = col.column()
        sub.enabled = sc.gs_auto_threads == False
        sub.prop(sc, 'gs_threads')
        sub = col.column()
        sub.enabled = sc.gs_type_render == 'into_blender'
        sub.prop(sc, 'gs_tile_size')

        layout.separator()

        row = layout.row()
        col = row.column()
        col.prop(sc, 'gs_clay_render')
        col.prop(sc, 'gs_transp_shad')
        col.prop(sc, 'gs_premult')
        sub = col.column()
        sub.enabled = sc.gs_type_render == 'file'
        sub.prop(sc, 'gs_z_channel')
        col.prop(sc, 'gs_draw_params')

        col = row.column()
        col.prop(sc, 'gs_auto_threads')
        col.prop(sc, 'gs_clamp_rgb')
        col.prop(sc, 'gs_show_sam_pix')
        col.prop(sc, 'gs_verbose')

        row = layout.row()
        col = row.column()
        col.enabled = sc.gs_draw_params
        col.prop(sc, 'gs_custom_string')
