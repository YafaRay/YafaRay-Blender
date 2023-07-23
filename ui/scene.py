# SPDX-License-Identifier: GPL-2.0-or-later

from bl_ui.properties_scene import SceneButtonsPanel
# noinspection PyUnresolvedReferences
from bpy.types import Panel


class ColorManagement(SceneButtonsPanel, Panel):
    bl_idname = "yafaray4.scene_color_management"
    bl_label = "Color Management"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        col = layout.column()
        col.label(text="Display:")
        col.prop(scene.display_settings, "display_device")

        if scene.display_settings.display_device == "sRGB":
            pass
        elif scene.display_settings.display_device == "None":
            row = layout.row(align=True)
            row.prop(scene, "gs_gamma", text="Display device output gamma")
        elif scene.display_settings.display_device == "XYZ":
            row = layout.row(align=True)
            row.label(text="YafaRay 'XYZ' support is experimental and may not give the expected results", icon="ERROR")
        else:
            row = layout.row(align=True)
            row.label(text="YafaRay doesn't support '" + scene.display_settings.display_device + "', assuming sRGB",
                      icon="ERROR")

        col = layout.column()
        col.separator()
        col.label(text="Render:")
        col.template_colormanaged_view_settings(scene, "view_settings")


classes = (
    ColorManagement,
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
