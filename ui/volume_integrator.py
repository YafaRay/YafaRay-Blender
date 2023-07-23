# SPDX-License-Identifier: GPL-2.0-or-later

from bl_ui.properties_world import WorldButtonsPanel
# noinspection PyUnresolvedReferences
from bpy.types import Panel


class VolumeIntegrator(WorldButtonsPanel, Panel):
    bl_idname = "yafaray4.vol_integrator"
    bl_label = "YafaRay Volume Integrator"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout
        world = context.world

        layout.prop(world, "v_int_type")
        layout.separator()

        if world.v_int_type == "Single Scatter":
            layout.prop(world, "v_int_step_size")
            layout.prop(world, "v_int_adaptive")
            layout.prop(world, "v_int_optimize")
            if world.v_int_optimize:
                layout.prop(world, "v_int_attgridres")

        if world.v_int_type == "Sky":
            layout.prop(world, "v_int_step_size")
            layout.prop(world, "v_int_dsturbidity")
            split = layout.split()
            split.prop(world, "v_int_scale")
            split.prop(world, "v_int_alpha")


classes = (
    VolumeIntegrator,
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
