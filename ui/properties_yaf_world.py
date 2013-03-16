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

from bpy.types import Panel
from bl_ui.properties_world import WorldButtonsPanel

WorldButtonsPanel.COMPAT_ENGINES = {'YAFA_RENDER'}

# Inherit World data block
from bl_ui.properties_world import WORLD_PT_context_world
WORLD_PT_context_world.COMPAT_ENGINES.add('YAFA_RENDER')
del WORLD_PT_context_world

# Inherit World Preview Panel
from bl_ui.properties_world import WORLD_PT_preview
WORLD_PT_preview.COMPAT_ENGINES.add('YAFA_RENDER')
del WORLD_PT_preview


class YAFWORLD_PT_world(WorldButtonsPanel, Panel):
    bl_label = "Background Settings"
    ibl = True

    def draw(self, context):
        layout = self.layout
        world = context.world

        split = layout.split()
        col = layout.column()
        col.prop(world, "bg_type", text="Background")

        if world.bg_type == "Gradient":

            split = layout.split(percentage=0.40)
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

            split = layout.split(percentage=0.40)
            col = split.column()
            col.prop(world, "bg_use_ibl")
            col.label(text=" ")

        elif world.bg_type == "Texture":

            tex = context.scene.world.active_texture

            if tex is not None:
                #
                layout.template_ID(context.world, "active_texture")
                #
                if  tex.yaf_tex_type == "IMAGE":  # it allows to change the used image
                    #
                    layout.template_image(tex, "image", tex.image_user, compact=True)
                    #
                else:
                    # TODO: create message about not allow texture type
                    pass
            else:
                #try:
                layout.template_ID(context.world, "active_texture", new="texture.new")
                #except:
                #    pass

            layout.label(text="Background Texture controls")
            layout.prop(world,"bg_rotation")
            # this option is used in YafaRay Core. With more or less effect :)
            layout.prop(world, "bg_exposure")
            layout.prop(world,"yaf_mapworld_type", text="Mapping Coord")
            layout.separator()

            split = layout.split(percentage=0.33)
            col = split.column()
            col.prop(world, "bg_use_ibl")

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

            split = layout.split()
            col = split.column()
            col.label(text="Set sun position:")
            col.prop(world, "bg_from", text="")

            col = split.column()
            col.label(text=" ")
            sub = col.column(align=True)
            sub.operator("world.get_position", text="Get from Location")
            sub.operator("world.get_angle", text="Get from Angle")
            sub.operator("world.update_sun", text="Update Lamp in 3D View")

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
            if world.bg_background_light:
                col.prop(world, "bg_power")
            else:
                col.label(text=" ")

            layout.column().prop(world, "bg_light_samples")

        ## DarkTide Sunsky
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
            sub.operator("world.update_sun", text="Update Lamp in 3D View")
            col.prop(world, "bg_dsaltitude")

            layout.separator()

            split = layout.split()
            col = split.column()
            col.prop(world, "bg_add_sun")
            if world.bg_add_sun:
                col.prop(world, "bg_sun_power")
            else:
                col.label(text=" ")
            if world.bg_background_light:
                col.prop(world, "bg_with_diffuse")
            else:
                col.label(text=" ")

            col = split.column()
            col.prop(world, "bg_background_light")
            if world.bg_background_light:
                col.prop(world, "bg_power")
            else:
                col.label(text=" ")
            if world.bg_background_light:
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

            split = layout.split(percentage=0.33)

            col = split.column()
            col.label("Color:")
            col = split.column()
            col.prop(world, "bg_single_color", text="")

            split = layout.split(percentage=0.33)
            col = split.column()
            col.prop(world, "bg_use_ibl")
            col.label(text=" ")

        if world.bg_use_ibl and self.ibl:
            # for all options that uses IBL
            col = split.column()
            col.prop(world, "bg_ibl_samples")
            col.prop(world, "bg_power", text="Power")


from . import properties_yaf_volume_integrator


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
