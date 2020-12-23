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

# <pep8 compliant>

import bpy
from ..ot import yafaray_presets
from bl_ui.properties_render import RenderButtonsPanel
from bpy.types import Panel, Menu


class YAFARAY4_MT_presets_render(Menu):
    bl_label = "Yafaray Render Presets"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    
    preset_subdir = "render"
    preset_operator = "script.execute_preset"
    draw = yafaray_presets.Yafaray_Menu.draw_preset


class YAFARAY4_PT_general_settings(RenderButtonsPanel, Panel):
    bl_label = "General Settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        render = scene.render

        row = layout.row(align=True)
        row.menu("YAFARAY4_MT_presets_render", text=bpy.types.YAFARAY4_MT_presets_render.bl_label)
        row.operator("yafaray.preset_add", text="", icon='ZOOMIN')
        #row.operator("yafaray.preset_add", text="", icon='ZOOMOUT').remove_active = True  #Does not work as expected, possibly better that the user deletes the presets manually himself to avoid deleting the wrong one by mistake anyway?

        layout.separator()

        split = layout.split(percentage=0.58)
        col = split.column()
        col.prop(scene, "gs_ray_depth")
        col.prop(scene, "gs_type_render")

        sub = col.column()
        sub.enabled = scene.gs_type_render == "into_blender"
        sub.prop(scene, "gs_secondary_file_output")
        
        if (scene.yafaray.logging.saveLog or scene.yafaray.logging.saveHTML or scene.yafaray.logging.savePreset or scene.yafaray.logging.paramsBadgePosition == "top" or scene.yafaray.logging.paramsBadgePosition == "bottom") and scene.gs_type_render == "into_blender" and not scene.gs_secondary_file_output:
                row = layout.row()
                row.label("Params badge and saving log/html/preset files only works when exporting to image file.", icon='ERROR')
                row = layout.row()
                row.label("To get the badge/logs, render to image or render into Blender+enable Secondary File Output.", icon='ERROR')
                row = layout.row()

        if scene.yafaray.logging.paramsBadgePosition == "bottom" and scene.gs_type_render == "file":
                row = layout.row()
                row.label("Image with Params Badge at bottom will appear CROPPED in Blender,", icon='INFO')
                row = layout.row()
                row.label("  but will be CORRECT in the exported image file.", icon='INFO')

        col = split.column()
        sub = col.column()
        sub.enabled = scene.gs_transp_shad
        sub.prop(scene, "gs_shadow_depth")
        sub = col.column()
        sub.enabled = scene.gs_type_render == "into_blender"
        sub.prop(scene, "gs_tile_size")
        sub.prop(scene, "gs_tile_order")

        layout.separator()

        split = layout.split()
        col = split.column()
        col.prop(scene, "gs_tex_optimization")

        split = layout.split()
        col = split.column()
        col.prop(scene, "gs_auto_threads", toggle=True)
        col.prop(scene, "gs_transp_shad", toggle=True)

        col = split.column()
        sub = col.column()
        if not scene.gs_auto_threads:
                sub.prop(scene, "gs_threads")
        else:
                sub.label("")
        col.prop(scene, "gs_show_sam_pix", toggle=True)
        col.prop(render, "use_instances", text="Use instances", toggle=True)

        split = layout.split(percentage=0.5)
        col = split.column()
        col.prop(scene, "bg_transp", toggle=True)
        col = split.column()
        sub = col.column()
        sub.enabled = scene.bg_transp
        sub.prop(scene, "bg_transp_refract", toggle=True)


class YAFARAY4_MT_logging(RenderButtonsPanel, Panel):
    bl_label = "Logging / Params Badge Settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        render = scene.render

        split = layout.split(percentage=0.43)
        col = split.column()
        col.prop(scene.yafaray.logging, "paramsBadgePosition")
        col = split.column()
        col.prop(scene.yafaray.logging, "drawRenderSettings")
        col = split.column()
        col.prop(scene.yafaray.logging, "drawAANoiseSettings")

        split = layout.split()
        col = split.column()
        col.prop(scene.yafaray.logging, "logPrintDateTime")
        col = split.column()
        col.prop(scene.yafaray.logging, "consoleVerbosity")
        col = split.column()
        col.prop(scene.yafaray.logging, "logVerbosity")

        split = layout.split()
        col = split.column()
        col.prop(scene.yafaray.logging, "saveLog")
        col = split.column()
        col.prop(scene.yafaray.logging, "saveHTML")
        col = split.column()
        col.prop(scene.yafaray.logging, "savePreset")

        if scene.yafaray.logging.saveLog or scene.yafaray.logging.saveHTML or scene.yafaray.logging.savePreset or scene.yafaray.logging.paramsBadgePosition == "top" or scene.yafaray.logging.paramsBadgePosition == "bottom":
                if scene.gs_type_render == "into_blender" and not scene.gs_secondary_file_output:
                        row = layout.row()
                        row.label("Params badge and saving log/html/preset files only works when exporting to image file.", icon='ERROR')
                        row = layout.row()
                        row.label("To get the badge/logs, render to image or render into Blender+enable Secondary File Output.", icon='ERROR')

                if scene.yafaray.logging.paramsBadgePosition == "bottom" and scene.gs_type_render == "file":
                        row = layout.row()
                        row.label("Image with Params Badge at bottom will appear CROPPED in Blender,", icon='INFO')
                        row = layout.row()
                        row.label("  but will be CORRECT in the exported image file.", icon='INFO')

                row = layout.row()
                row.prop(scene.yafaray.logging, "title")
                row = layout.row()
                row.prop(scene.yafaray.logging, "author")
                row = layout.row()
                row.prop(scene.yafaray.logging, "contact")
                row = layout.row()
                row.prop(scene.yafaray.logging, "comments")
                row = layout.row()
                row.prop(scene.yafaray.logging, "customIcon")
                row = layout.row()
                col = row.column()
                col.prop(scene.yafaray.logging, "customFont")
                col = row.column()
                col.prop(scene.yafaray.logging, "fontScale")


class YAFARAY4_MT_clay_render(RenderButtonsPanel, Panel):
    bl_label = "Clay Render Settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        render = scene.render

        row = layout.row(align=True)
        split = layout.split(percentage=0.5)
        col = split.column()
        col.prop(scene, "gs_clay_render", toggle=True)
        if scene.gs_clay_render:
            col = split.column()
            col.prop(scene, "gs_clay_col", text="")
            layout.separator()
            split = layout.split()
            col = split.column()
            col.prop(scene, "gs_clay_oren_nayar")
            if scene.gs_clay_oren_nayar:
                col = split.column()
                col.prop(scene, "gs_clay_sigma")            
            col = layout.column()
            col.prop(scene, "gs_clay_render_keep_transparency")
            #col = split.column()
            col.prop(scene, "gs_clay_render_keep_normals")



if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
