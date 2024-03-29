# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bl_ui.properties_data_camera import CameraButtonsPanel
# noinspection PyUnresolvedReferences
from bpy.types import Panel

if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed, 
    # before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the 
    # "libyafaray4_bindings" compiled module is installed on. Assuming that the YafaRay-Plugin exporter is installed 
    # in a folder named "yafaray4" within the addons Blender directory
    # noinspection PyUnresolvedReferences
    import yafaray4.prop.camera

    yafaray4.prop.camera.register()


class Lens(CameraButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_camera_lens"
    bl_label = "Lens"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

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
            layout.prop(camera, "angular_projection")

        elif camera.camera_type == 'orthographic':
            layout.prop(camera, "ortho_scale")

        elif camera.camera_type in {'perspective', 'architect'}:
            layout.prop(camera, "lens")

            layout.separator()

            layout.label(text="Depth of Field:")
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


class Camera(CameraButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_camera"
    bl_label = "Camera"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout

        camera = context.camera

        row = layout.row(align=True)

        if bpy.app.version >= (2, 80, 0):
            pass  # FIXME BLENDER >= v2.80
        else:
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


class CameraDisplay(CameraButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_camera_display"
    bl_label = "Display"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout

        camera = context.camera

        split = layout.split()

        col = split.column()
        col.prop(camera, "show_limits", text="Limits")
        # col.prop(camera, "show_title_safe", text="Title Safe") #FIXME: Disabled it as it's causing error messages
        #  "rna_uiItemR: property not found: Camera.show_title_safe". This line should probably have to be removed
        col.prop(camera, "show_sensor", text="Sensor")
        col.prop(camera, "show_name", text="Name")

        col = split.column()
        if bpy.app.version >= (2, 80, 0):
            pass  # FIXME BLENDER >= v2.80
        else:
            col.prop_menu_enum(camera, "show_guide")
            col.prop(camera, "draw_size", text="Size")
        col.prop(camera, "show_passepartout", text="Passepartout")
        sub = col.column()
        sub.active = camera.show_passepartout
        sub.prop(camera, "passepartout_alpha", text="Alpha", slider=True)


classes = (
    Lens,
    Camera,
    CameraDisplay,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed, 
    # before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the 
    # "libyafaray4_bindings" compiled module is installed on
    register()
