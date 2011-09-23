# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from ..ot import yafaray_presets
from bl_ui.properties_render import RenderButtonsPanel
from bpy.types import Panel, Menu

RenderButtonsPanel.COMPAT_ENGINES = {'YAFA_RENDER'}


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

        split = layout.split()
        col = split.column()
        sub = col.split(percentage=0.7)
        sub.prop(scene, "gs_clay_render")
        if scene.gs_clay_render:
            sub.prop(scene, "gs_clay_col", text="")
        # col.prop(scene, "gs_mask_render")
        sub = col.column()
        sub.enabled = scene.gs_type_render == "file"
        sub.prop(scene, "gs_z_channel")
        col.prop(scene, "gs_transp_shad")
        col.prop(scene, "gs_premult")
        col.prop(scene, "gs_draw_params")

        col = split.column()
        col.prop(scene, "gs_auto_threads")
        col.prop(scene, "gs_clamp_rgb")
        col.prop(scene, "gs_show_sam_pix")
        col.prop(scene, "gs_verbose")

        col = layout.column()
        col.enabled = scene.gs_draw_params
        col.prop(scene, "gs_custom_string")
