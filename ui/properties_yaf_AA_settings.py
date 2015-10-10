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
from bl_ui.properties_render import RenderButtonsPanel

RenderButtonsPanel.COMPAT_ENGINES = {'YAFA_RENDER'}


class YAF_PT_AA_settings(RenderButtonsPanel, Panel):
    bl_label = "Anti-Aliasing"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):

        scene = context.scene
        layout = self.layout

        split = layout.split()
        col = split.column()
        col.prop(scene, "AA_filter_type")
        col.prop(scene, "AA_min_samples")
        col.prop(scene, "AA_pixelwidth")
        # fix suggest by 'samo' in http://www.yafaray.org/node/581
        col = split.column()
        spp = col.column()
        sub = col.column()
        spp.enabled = False
        if scene.intg_light_method != "SPPM":
            sub.enabled = scene.AA_passes > 1
            spp.enabled = True
        #
        spp.prop(scene, "AA_passes")
        sub.prop(scene, "AA_inc_samples")
        sub.prop(scene, "AA_threshold")


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
