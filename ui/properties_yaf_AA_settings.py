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
        sub_always = col.column()
        sub_nosppm = col.column()
        sub_nosppm.enabled = scene.intg_light_method != "SPPM"
        sub_morethan1pass = col.column()
        sub_morethan1pass.enabled = scene.AA_passes > 1
        sub_nosppm_morethan1pass = col.column()
        sub_nosppm_morethan1pass.enabled = scene.intg_light_method != "SPPM" and scene.AA_passes > 1
        sub_always.prop(scene, "AA_filter_type")
        sub_nosppm.prop(scene, "AA_min_samples")
        sub_always.prop(scene, "AA_pixelwidth")

        col = split.column()
        sub_always = col.column()
        sub_nosppm = col.column()
        sub_nosppm.enabled = scene.intg_light_method != "SPPM"
        sub_morethan1pass = col.column()
        sub_morethan1pass.enabled = scene.AA_passes > 1
        sub_nosppm_morethan1pass = col.column()
        sub_nosppm_morethan1pass.enabled = scene.intg_light_method != "SPPM" and scene.AA_passes > 1
        sub_nosppm.prop(scene, "AA_passes")
        sub_nosppm_morethan1pass.prop(scene, "AA_inc_samples")
        sub_nosppm_morethan1pass.prop(scene.yafaray.noise_control, "background_resampling")

        row = layout.row()
        row.enabled = scene.intg_light_method != "SPPM" and scene.AA_passes > 1
        
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
        row.enabled = scene.intg_light_method != "SPPM" and scene.AA_passes > 1

        row.prop(scene.yafaray.noise_control, "detect_color_noise")

        row = layout.row()
        row.enabled = scene.intg_light_method != "SPPM" and scene.AA_passes > 1

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
