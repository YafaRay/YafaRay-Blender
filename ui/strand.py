# SPDX-License-Identifier: GPL-2.0-or-later

# noinspection PyUnresolvedReferences
from bpy.types import Panel


class StrandSettings(Panel):
    bl_idname = "yafaray4.strand_settings"
    bl_label = "Strand Settings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "particle"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):

        psys = context.object.particle_systems
        engine = context.scene.render.engine
        return psys and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        yaf_mat = context.object.active_material
        if yaf_mat:
            tan = yaf_mat.strand

            split = layout.split()

            col = split.column()
            sub = col.column(align=True)
            sub.label(text="Size:")
            sub.prop(tan, "root_size", text="Root")
            sub.prop(tan, "tip_size", text="Tip")
            col.column()
            col.prop(tan, "shape")
            col.prop(tan, "use_blender_units")

            col = split.column()
            col.label(text="Shading:")
            col.prop(tan, "width_fade")
            ob = context.object
            if ob and ob.type == 'MESH':
                col.prop_search(tan, "uv_layer", ob.data, "uv_textures", text="")
            else:
                col.prop(tan, "uv_layer", text="")


classes = (
    StrandSettings,
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
