# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import AddonPreferences
from bpy.props import IntProperty

if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed, before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the "libyafaray4_bindings" compiled module is installed on.
    # Assuming that the YafaRay-Plugin exporter is installed in a folder named "yafaray4" within the addons Blender directory
    from yafaray4 import YAFARAY_PACKAGE_NAME
else:
    from .. import YAFARAY_PACKAGE_NAME


class Preferences(AddonPreferences):
    bl_idname = YAFARAY_PACKAGE_NAME

    yafaray_computer_node = IntProperty(
        name="YafaRay computer node",
        description='Computer node number in multi-computer render environments / render farms',
        default=0, min=0, max=1000
    )

    def draw(self, bl_context):
        layout = self.layout
        split = layout.split()
        col = split.column()
        col.prop(self, "yafaray_computer_node")
        col = col.column()
        col.label(text="Click bottom left \"Save & Load\"->\"Save Preferences\" to apply changes permanently!",
                  icon="INFO")


classes = (
    Preferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
