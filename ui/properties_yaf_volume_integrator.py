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
from bl_ui.properties_world import WorldButtonsPanel

WorldButtonsPanel.COMPAT_ENGINES = {'YAFA_E2_RENDER'}


class YAF_PT_vol_integrator(WorldButtonsPanel, Panel):
    bl_label = "YafaRay Volume Integrator"
    COMPAT_ENGINES = {'YAFA_E2_RENDER'}

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


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
