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

RenderButtonsPanel.COMPAT_ENGINES = {'YAFA_RENDER'}


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


class YAFRENDER_PT_layers(RenderButtonsPanel, Panel):
    bl_label = "Layers"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render

        row = layout.row()
        row.template_list("RENDER_UL_renderlayers", "", rd, "layers", rd.layers, "active_index", rows=2)

        col = row.column(align=True)
        col.operator("scene.render_layer_add", icon='ZOOMIN', text="")
        col.operator("scene.render_layer_remove", icon='ZOOMOUT', text="")

        row = layout.row()
        rl = rd.layers.active
        row.prop(rl, "name")
        row.prop(rd, "use_single_layer", text="", icon_only=True)

        split = layout.split()

        col = split.column()
        col.prop(scene, "layers", text="Scene")
        # TODO: Implement material override
        #col.prop(rl, "material_override", text="Material")

        col = split.column()
        # TODO: Implement render layers
        #col.prop(rl, "layers", text="Layer")


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


class YAFRENDER_PT_output(RenderButtonsPanel, Panel):
    bl_label = "Output"

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render
        sc = context.scene
        image_settings = rd.image_settings

        layout.prop(rd, "filepath", text="")

        split = layout.split(percentage=0.6)
        col = split.column()
        col.prop(sc, "img_output", text="", icon='IMAGE_DATA')
        col = split.column()
        col.row().prop(image_settings, "color_mode", text="Color", expand=True)


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


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
