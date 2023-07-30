# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
# Inherit World data block
from bl_ui.properties_world import WORLD_PT_context_world
from bl_ui.properties_world import WorldButtonsPanel
# noinspection PyUnresolvedReferences
from bpy.types import Panel

WORLD_PT_context_world.COMPAT_ENGINES.add('YAFARAY4_RENDER')
del WORLD_PT_context_world

if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed, 
    # before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the 
    # "libyafaray4_bindings" compiled module is installed on. Assuming that the YafaRay-Plugin exporter is installed 
    # in a folder named "yafaray4" within the addons Blender directory
    # noinspection PyUnresolvedReferences
    import yafaray4.prop.world

    yafaray4.prop.world.register()


def ui_split(ui_item, factor):
    if bpy.app.version >= (2, 80, 0):
        return ui_item.split(factor=factor)
    else:
        return ui_item.split(percentage=factor)


# Inherit World Preview Panel
if bpy.app.version >= (2, 80, 0):
    pass  # FIXME BLENDER >= v2.80
else:
    # noinspection PyUnresolvedReferences
    from bl_ui.properties_world import WORLD_PT_preview

    WORLD_PT_preview.COMPAT_ENGINES.add('YAFARAY4_RENDER')
    del WORLD_PT_preview


class World(WorldButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_world"
    bl_label = "Background Settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    ibl = True

    def draw(self, context):
        layout = self.layout
        world = context.world

        split = layout.split()
        col = layout.column()
        col.prop(world, "bg_type", text="Background")

        if world.bg_type == "Gradient":

            split = ui_split(layout, 0.40)
            col = split.column()
            col.label(text="Zenith:")
            col.label(text="Horizon:")
            col.label(text="Horizon ground:")
            col.label(text="Zenith ground:")

            col = split.column()
            col.prop(world, "bg_zenith_color", text="")
            col.prop(world, "bg_horizon_color", text="")
            col.prop(world, "bg_horizon_ground_color", text="")
            col.prop(world, "bg_zenith_ground_color", text="")
            col.prop(world, "bg_power")

            split = ui_split(layout, 0.40)
            col = split.column()
            col.prop(world, "bg_use_ibl")
            col.label(text=" ")

            if world.bg_use_ibl:
                row = layout.row()
                row.prop(world, "bg_with_diffuse")
                row.prop(world, "bg_with_caustic")

        elif world.bg_type == "Texture":
            if bpy.app.version >= (2, 80, 0):
                return  # FIXME BLENDER >= v2.80

            tex = context.scene.world.active_texture
            if tex is not None:
                #
                layout.template_ID(context.world, "active_texture")
                #
                if tex.yaf_tex_type == "IMAGE":  # it allows to change the used image
                    #
                    layout.template_image(tex, "image", tex.image_user, compact=True)

                    if tex.image.colorspace_settings.name == "sRGB" \
                            or tex.image.colorspace_settings.name == "Linear" \
                            or tex.image.colorspace_settings.name == "Non-Color":
                        pass

                    elif tex.image.colorspace_settings.name == "XYZ":
                        row = layout.row(align=True)
                        row.label(text="YafaRay 'XYZ' support is experimental and may not give the expected results",
                                  icon="ERROR")

                    elif tex.image.colorspace_settings.name == "Linear ACES":
                        row = layout.row(align=True)
                        row.label(
                            text="YafaRay doesn't support '" + tex.image.colorspace_settings.name
                                 + "', assuming linear RGB",
                            icon="ERROR")

                    elif tex.image.colorspace_settings.name == "Raw":
                        row = layout.row(align=True)
                        row.prop(tex, "yaf_gamma_input", text="Texture gamma input correction")

                    else:
                        row = layout.row(align=True)
                        row.label(
                            text="YafaRay doesn't support '" + tex.image.colorspace_settings.name + "', assuming sRGB",
                            icon="ERROR")

                    #
                else:
                    # TODO: create message about not allow texture type
                    pass
            else:
                layout.template_ID(context.world, "active_texture", new="texture.new")

            layout.label(text="Background Texture controls")
            layout.prop(world, "bg_rotation")
            layout.prop(world, "yaf_mapworld_type", text="Mapping Coord")
            layout.separator()
            layout.prop(world, "bg_power")

            split = ui_split(layout, 0.33)
            col = split.column()
            col.prop(world, "bg_use_ibl")
            col = split.column()
            col.prop(world, "bg_smartibl_blur")
            # col = split.column()
            # col.prop(world, "ibl_clamp_sampling") #No longer needed after this issue was solved in Core
            # (http://www.yafaray.org/node/752#comment-1621), but I will leave it here for now just in case...

            if world.bg_use_ibl:
                row = layout.row()
                row.prop(world, "bg_with_diffuse")
                row.prop(world, "bg_with_caustic")
            else:
                col = layout.column()
                col.label(text=" ")
                col.label(text=" ")

        elif world.bg_type == "Sunsky1":
            self.ibl = False
            layout.separator()
            sub = layout.column(align=True)
            sub.prop(world, "bg_turbidity")
            sub.prop(world, "bg_a_var")
            sub.prop(world, "bg_b_var")
            sub.prop(world, "bg_c_var")
            sub.prop(world, "bg_d_var")
            sub.prop(world, "bg_e_var")
            sub.prop(world, "bg_power")

            split = layout.split()
            col = split.column()
            col.label(text="Set sun position:")
            col.prop(world, "bg_from", text="")

            col = split.column()
            col.label(text=" ")
            sub = col.column(align=True)
            sub.operator("world.get_position", text="Get from Location")
            sub.operator("world.get_angle", text="Get from Angle")
            sub.operator("world.update_sun", text="Update Light in 3D View")

            layout.separator()

            split = layout.split()
            col = split.column()
            col.prop(world, "bg_add_sun")
            if world.bg_add_sun:
                col.prop(world, "bg_sun_power")

            else:
                col.label(text=" ")

            col = split.column()
            col.prop(world, "bg_background_light")

            layout.column().prop(world, "bg_light_samples")

            if world.bg_add_sun or world.bg_background_light:
                row = layout.row()
                row.prop(world, "bg_with_diffuse")
                row.prop(world, "bg_with_caustic")

        # DarkTide Sunsky
        elif world.bg_type == "Sunsky2":
            self.ibl = False
            layout.separator()
            sub = layout.column(align=True)
            sub.prop(world, "bg_ds_turbidity")
            sub.prop(world, "bg_a_var")
            sub.prop(world, "bg_b_var")
            sub.prop(world, "bg_c_var")
            sub.prop(world, "bg_d_var")
            sub.prop(world, "bg_e_var")

            split = layout.split()
            col = split.column()
            col.label(text="Set sun position:")
            col.prop(world, "bg_from", text="")
            col.prop(world, "bg_dsnight")

            col = split.column()
            col.label(text=" ")
            sub = col.column(align=True)
            sub.operator("world.get_position", text="Get from Location")
            sub.operator("world.get_angle", text="Get from Angle")
            sub.operator("world.update_sun", text="Update Light in 3D View")
            col.prop(world, "bg_dsaltitude")

            layout.separator()

            split = layout.split()
            col = split.column()
            col.prop(world, "bg_add_sun")
            if world.bg_add_sun:
                col.prop(world, "bg_sun_power")
            else:
                col.label(text=" ")
            if world.bg_add_sun or world.bg_background_light:
                col.prop(world, "bg_with_diffuse")
            else:
                col.label(text=" ")

            col = split.column()
            col.prop(world, "bg_background_light")
            if world.bg_background_light:
                col.prop(world, "bg_power")
            else:
                col.label(text=" ")
            if world.bg_add_sun or world.bg_background_light:
                col.prop(world, "bg_with_caustic")
            else:
                col.label(text=" ")

            split = layout.split()
            col = split.column()
            col.prop(world, "bg_exposure")
            col = split.column()
            col.prop(world, "bg_dsbright")

            layout.column().prop(world, "bg_light_samples")
            layout.column().prop(world, "bg_color_space")

        elif world.bg_type == "Single Color":

            split = ui_split(layout, 0.33)

            col = split.column()
            col.label(text="Color:")
            col = split.column()
            col.prop(world, "bg_single_color", text="")
            col.prop(world, "bg_power", text="Power")

            split = ui_split(layout, 0.33)
            col = split.column()
            col.prop(world, "bg_use_ibl")
            col.label(text=" ")

            if world.bg_use_ibl and self.ibl:
                row = layout.row()
                row.prop(world, "bg_with_diffuse")
                row.prop(world, "bg_with_caustic")

        if world.bg_use_ibl and self.ibl:
            # for all options that uses IBL
            col = split.column()
            col.prop(world, "bg_ibl_samples")


class Advanced(WorldButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_world_advanced"
    bl_label = "Advanced settings"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout
        world = context.world

        split = layout.split()
        col = split.column()
        col.prop(world, "bg_cast_shadows")
        if world.bg_type == "Sunsky1" or world.bg_type == "Sunsky2":
            col = split.column()
            col.prop(world, "bg_cast_shadows_sun")


classes = (
    World,
    Advanced,
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
