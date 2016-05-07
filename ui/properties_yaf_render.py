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
from bpy.types import Panel
from bl_ui.properties_render import RenderButtonsPanel


class YAFA_V3_PT_Render(RenderButtonsPanel, Panel):
    bl_label = "Render"
    COMPAT_ENGINES = {'YAFA_V3_RENDER'}

    def draw(self, context):

        layout = self.layout
        rd = context.scene.render

        row = layout.row()
        row.operator("render.render_still", text="Image", icon='RENDER_STILL')
        row.operator("render.render_animation", text="Animation", icon='RENDER_ANIMATION')
        layout.row().operator("render.render_view", text="Render 3D View", icon='VIEW3D')
        layout.prop(rd, "display_mode", text="Display")

class YAFA_V3_PT_dimensions(RenderButtonsPanel, Panel):
    bl_label = "Dimensions"
    COMPAT_ENGINES = {'YAFA_V3_RENDER'}
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

        row = col.row()
        row.prop(rd, "use_border", text="Border")
        sub = row.row()
        sub.active = rd.use_border
        sub.prop(rd, "use_crop_to_border", text="Crop")

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Frame Range:")
        sub.prop(scene, "frame_start", text="Start")
        sub.prop(scene, "frame_end", text="End")
        sub.prop(scene, "frame_step", text="Step")

from . import properties_yaf_general_settings
from . import properties_yaf_integrator
from . import properties_yaf_AA_settings


class YAFA_V3_PT_output(RenderButtonsPanel, Panel):
    bl_label = "Output"
    COMPAT_ENGINES = {'YAFA_V3_RENDER'}

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render
        sc = context.scene
        image_settings = rd.image_settings

        layout.prop(sc, "img_save_with_blend_file")
        if not sc.img_save_with_blend_file:
            row = layout.row()
            layout.prop(rd, "filepath", text="")
        row = layout.row()
        col = row.column()
        col.prop(sc, "img_add_blend_name")
        col = row.column()
        col.prop(sc, "img_add_datetime")
        
        split = layout.split(percentage=0.6)
        col = split.column()
        col.prop(sc, "img_output", text="", icon='IMAGE_DATA')
        col = split.column()
        col.row().prop(image_settings, "color_mode", text="Color", expand=True)

        if sc.img_output == "OPEN_EXR":
            split = layout.split()
            split.prop(sc, "img_multilayer")

        if sc.img_output == "OPEN_EXR" or sc.img_output == "HDR":  #If the output file is a HDR/EXR file, we force the render output to Linear
                pass
        elif sc.gs_type_render == "file" or sc.gs_type_render == "xml":
                split = layout.split(percentage=0.6)
                col = split.column()
                col.prop(sc.display_settings, "display_device")
                
                if sc.display_settings.display_device == "None":
                    col = split.column()
                    col.prop(sc, "gs_gamma", text = "Gamma")

                if sc.display_settings.display_device == "sRGB":
                    pass
                elif sc.display_settings.display_device == "None":
                    pass
                elif sc.display_settings.display_device == "XYZ":
                    row = layout.row(align=True)
                    row.label(text="YafaRay 'XYZ' support is experimental and may not give the expected results", icon="ERROR")
                else:
                    row = layout.row(align=True)
                    row.label(text="YafaRay doesn't support '" + sc.display_settings.display_device + "', assuming sRGB", icon="ERROR")
                    
        split = layout.split(percentage=0.6)
        col = split.column()
        col.prop(sc, "gs_premult", text = "Premultiply Alpha")
        if sc.img_output  == "OPEN_EXR" and sc.gs_premult == "no":
            row = layout.row(align=True)
            row.label(text="Typically you should enable Premultiply in EXR files", icon="INFO")
        if sc.img_output  == "PNG" and sc.gs_premult == "yes":
            row = layout.row(align=True)
            row.label(text="Typically you should disable Premultiply in PNG files", icon="INFO")
        if sc.img_output  != "PNG" and sc.img_output  != "OPEN_EXR" and sc.img_output  != "JPEG" and sc.gs_premult == "auto":
            row = layout.row(align=True)
            row.label(text="Can't guess premultiply for " + sc.img_output + " , enabling by default but better select Yes or No", icon="INFO")


class YAFA_V3_PT_post_processing(RenderButtonsPanel, Panel):
    bl_label = "Post Processing"
    COMPAT_ENGINES = {'YAFA_V3_RENDER'}
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


class YAFA_V3_PT_convert(RenderButtonsPanel, Panel):
    bl_label = "Convert old YafaRay Settings"
    COMPAT_ENGINES = {'YAFA_V3_RENDER'}

    def draw(self, context):
        layout = self.layout
        layout.column().operator("data.convert_yafaray_properties", text="Convert data from 2.4x")


class YAFA_V3_PT_Advanced(RenderButtonsPanel, Panel):
    bl_label = "Advanced Settings - only for experts"
    COMPAT_ENGINES = {'YAFA_V3_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        split = layout.split()
        col = split.column()
        col.prop(scene, "adv_auto_shadow_bias_enabled")
        if not scene.adv_auto_shadow_bias_enabled:
            col = split.column()
            sub = col.column()
            sub.prop(scene, "adv_shadow_bias_value")

        split = layout.split()
        col = split.column()
        col.prop(scene, "adv_auto_min_raydist_enabled")
        if not scene.adv_auto_min_raydist_enabled:
            col = split.column()
            sub = col.column()
            sub.prop(scene, "adv_min_raydist_value")
            
if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
