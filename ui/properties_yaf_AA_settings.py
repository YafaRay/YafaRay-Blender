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


class YAFA_V3_PT_AA_settings(RenderButtonsPanel, Panel):
    bl_label = "Anti-Aliasing / Noise control"
    COMPAT_ENGINES = {'YAFA_V3_RENDER'}

    def draw(self, context):

        scene = context.scene
        layout = self.layout

        split = layout.split()
        col = split.column()
        col.prop(scene.yafaray.noise_control, "clamp_samples")
        col = split.column()
        col.prop(scene.yafaray.noise_control, "clamp_indirect")

        split = layout.split()
        col = split.column()
        spp = col.column()
        sub = col.column()
        spp.prop(scene, "AA_filter_type")
        spp.prop(scene, "AA_min_samples")
        spp.prop(scene, "AA_pixelwidth")
        spp.enabled = False
        if scene.intg_light_method != "SPPM":
            sub.enabled = scene.AA_passes > 1
            spp.enabled = True
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
        spp.prop(scene, "AA_inc_samples")
        spp.prop(scene.yafaray.noise_control, "background_resampling")

        row = layout.row()
        row.enabled = False

        if scene.AA_passes > 1 and scene.intg_light_method != "SPPM":
            row.enabled = True
        
        row.prop(scene.yafaray.noise_control, "dark_detection_type")
        col = row.column()
        if scene.yafaray.noise_control.dark_detection_type == "curve":
            col.label("")
        elif scene.yafaray.noise_control.dark_detection_type == "linear":
            col.prop(scene, "AA_threshold")
            col.prop(scene.yafaray.noise_control, "dark_threshold_factor")                
        else:
            col.prop(scene, "AA_threshold")

        row = layout.row()
        row.enabled = False

        if scene.AA_passes > 1 and scene.intg_light_method != "SPPM":
            row.enabled = True

        row.prop(scene.yafaray.noise_control, "detect_color_noise")

        row = layout.row()
        row.enabled = False

        if scene.AA_passes > 1 and scene.intg_light_method != "SPPM":
            row.enabled = True

        col = row.column()
        col.prop(scene.yafaray.noise_control, "sample_multiplier_factor")
        col.prop(scene.yafaray.noise_control, "light_sample_multiplier_factor")
        col.prop(scene.yafaray.noise_control, "indirect_sample_multiplier_factor")
        col = row.column()
        col.prop(scene.yafaray.noise_control, "resampled_floor")
        col.prop(scene.yafaray.noise_control, "variance_edge_size")
        col.prop(scene.yafaray.noise_control, "variance_pixels")

if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
