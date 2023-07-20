# SPDX-License-Identifier: GPL-2.0-or-later

from bpy.types import Panel


class YAFARAY4_PT_object_light(Panel):
    bl_label = "YafaRay Object Properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):

        engine = context.scene.render.engine
        return (context.object.type == "MESH" and (engine in cls.COMPAT_ENGINES))

    def draw(self, context):
        layout = self.layout
        ob = context.object

        layout.prop(ob, "motion_blur_bezier", toggle=True)
        layout.prop(ob, "ml_enable", toggle=True)
        if ob.ml_enable:
            col = layout.column(align=True)
            col.prop(ob, "ml_color")
            col.prop(ob, "ml_power")
            layout.prop(ob, "ml_samples")
            layout.prop(ob, "ml_double_sided")

        layout.prop(ob, "bgp_enable", toggle=True)

        if ob.bgp_enable:
            layout.prop(ob, "bgp_power")
            layout.prop(ob, "bgp_samples")
            split = layout.split()
            split.prop(ob, "bgp_with_diffuse")
            split.prop(ob, "bgp_with_caustic")
            layout.prop(ob, "bgp_photon_only")

        layout.prop(ob, "vol_enable", toggle=True)

        if ob.vol_enable:
            layout.separator()
            layout.prop(ob, "vol_region")
            layout.separator()
            col = layout.column(align=True)
            col.prop(ob, "vol_absorp", text="Absorption")
            col.prop(ob, "vol_scatter", text="Scatter")

            if ob.vol_region == "ExpDensity Volume":
                col = layout.column(align=True)
                col.prop(ob, "vol_height")
                col.prop(ob, "vol_steepness")

            if ob.vol_region == "Noise Volume":
                col = layout.column(align=True)
                col.prop(ob, "vol_sharpness")
                col.prop(ob, "vol_cover")
                col.prop(ob, "vol_density")

        #layout.prop(ob, "pass_index")  #no need for this, there is a pass_index field by default in the object properties panel, but just in case I'm leaving this here.

classes = (
    YAFARAY4_PT_object_light,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed, before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the "libyafaray4_bindings" compiled module is installed on
    register()
