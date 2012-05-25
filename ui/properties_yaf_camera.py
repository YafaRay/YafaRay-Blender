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
from bl_ui.properties_data_camera import CameraButtonsPanel

CameraButtonsPanel.COMPAT_ENGINES = {'YAFA_RENDER'}


class YAF_PT_lens(CameraButtonsPanel, Panel):
    bl_label = "Lens"

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

        layout.separator()
        split = layout.split()
        col = split.column(align=True)
        col.label(text="Shift:")
        col.prop(camera, "shift_x", text="X")
        col.prop(camera, "shift_y", text="Y")

        col = split.column(align=True)
        col.prop(camera, "use_clipping")
        sub = col.column()
        sub.active = camera.use_clipping
        sub.prop(camera, "clip_start", text="Start")
        sub.prop(camera, "clip_end", text="End")


class YAF_PT_camera(CameraButtonsPanel, Panel):
    bl_label = "Camera"

    def draw(self, context):
        layout = self.layout

        camera = context.camera

        row = layout.row(align=True)

        row.menu("CAMERA_MT_presets", text=bpy.types.CAMERA_MT_presets.bl_label)
        row.operator("camera.preset_add", text="", icon="ZOOMIN")
        row.operator("camera.preset_add", text="", icon="ZOOMOUT").remove_active = True

        layout.label(text="Sensor:")

        split = layout.split()

        col = split.column(align=True)
        if camera.sensor_fit == 'AUTO':
            col.prop(camera, "sensor_width", text="Size")
        else:
            col.prop(camera, "sensor_width", text="Width")
            col.prop(camera, "sensor_height", text="Height")

        col = split.column(align=True)
        col.prop(camera, "sensor_fit", text="")


class YAF_PT_camera_display(CameraButtonsPanel, Panel):
    bl_label = "Display"

    def draw(self, context):
        layout = self.layout

        camera = context.camera

        split = layout.split()

        col = split.column()
        col.prop(camera, "show_limits", text="Limits")
        col.prop(camera, "show_title_safe", text="Title Safe")
        col.prop(camera, "show_sensor", text="Sensor")
        col.prop(camera, "show_name", text="Name")

        col = split.column()
        col.prop_menu_enum(camera, "show_guide")
        col.prop(camera, "draw_size", text="Size")
        col.prop(camera, "show_passepartout", text="Passepartout")
        sub = col.column()
        sub.active = camera.show_passepartout
        sub.prop(camera, "passepartout_alpha", text="Alpha", slider=True)


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
