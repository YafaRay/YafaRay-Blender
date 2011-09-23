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
from bpy.types import Panel
from bl_ui.properties_data_camera import CameraButtonsPanel

CameraButtonsPanel.COMPAT_ENGINES = {'YAFA_RENDER'}


class YAF_PT_camera(CameraButtonsPanel, Panel):
    bl_label = "Camera"

    def draw(self, context):
        layout = self.layout

        camera = context.camera

        layout.prop(camera, "camera_type", expand=True)

        layout.separator()

        if camera.camera_type == 'angular':
            layout.prop(camera, "angular_angle")
            layout.prop(camera, "max_angle")
            layout.prop(camera, "mirrored")
            layout.prop(camera, "circular")

        elif camera.camera_type == 'orthographic':
            layout.prop(camera, "ortho_scale")

        elif camera.camera_type in {'perspective', 'architect'}:
            layout.prop(camera, "lens")

            layout.separator()

            layout.label("Depth of Field:")
            layout.prop(camera, "aperture")
            split = layout.split()
            split.prop(camera, "dof_object", text="")
            col = split.column()
            if camera.dof_object is not None:
                col.enabled = False
            col.prop(camera, "dof_distance", text="Distance")

            layout.prop(camera, "bokeh_type")
            layout.prop(camera, "bokeh_bias")
            layout.prop(camera, "bokeh_rotation")


class YAF_PT_camera_display(CameraButtonsPanel, Panel):
    bl_label = "Display"

    def draw(self, context):
        layout = self.layout

        camera = context.camera

        split = layout.split()

        col = split.column()
        col.prop(camera, "show_limits")
        col.prop(camera, "show_title_safe")
        col.prop(camera, "show_name")

        col = split.column()
        col.prop(camera, "draw_size", text="Size")
        col.prop(camera, "show_passepartout", text="Passepartout")
        sub = col.column()
        sub.active = camera.show_passepartout
        sub.prop(camera, "passepartout_alpha", text="Alpha", slider=True)

        layout.separator()
        layout.prop(camera, "use_clipping")

        split = layout.split()
        col = split.column(align=True)
        clip = col.column()
        clip.active = camera.use_clipping
        clip.prop(camera, "clip_start", text="Start")
        clip.prop(camera, "clip_end", text="End")

        col = split.column()
        col.prop_menu_enum(camera, "show_guide")
