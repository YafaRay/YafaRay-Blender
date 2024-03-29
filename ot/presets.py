# SPDX-License-Identifier: GPL-2.0-or-later

import os

import bpy
from bpy.path import clean_name, display_name
# noinspection PyUnresolvedReferences
from bpy.types import Operator
from ..util.properties_annotations import replace_properties_with_annotations


# noinspection PyUnusedLocal
def preset_find(name, preset_path, disp_name=False):
    if not name:
        return None

    if disp_name:
        filename = ""
        for fn in os.listdir(preset_path):
            if fn.endswith(".py") and name == display_name(fn):
                filename = fn
                break
    else:
        filename = name + ".py"

    if filename:
        filepath = os.path.join(preset_path, filename)
        if os.path.exists(filepath):
            return filepath


@replace_properties_with_annotations
class RenderPresets(Operator):
    """List of render presets. Also allows to add a Yafaray Render Preset in user home
    folder->yafaray4_user_data/presets/render. To delete or modify presets, modify the .py files directly in that
    folder"""
    bl_idname = "yafaray4.render_presets"
    bl_label = "Yafaray Render Presets"
    bl_options = {'REGISTER'}  # only because invoke_props_popup requires.
    preset_menu = "YAFARAY4_MT_presets_render"
    name = bpy.props.StringProperty(name="Name", description="Name of the preset, used to make the path name",
                                    maxlen=64, default="")
    remove_active = bpy.props.BoolProperty(default=False, options={'HIDDEN'})
    preset_defines = [
        "scene = bpy.context.scene"
    ]
    preset_values = [
        "scene.render.resolution_x",
        "scene.render.resolution_y",
        "scene.render.resolution_percentage",
        "scene.render.border_max_x",
        "scene.render.border_max_y",
        "scene.render.border_min_x",
        "scene.render.border_min_y",
        "scene.render.use_border",
        "scene.render.use_crop_to_border",
        "scene.gs_ray_depth",
        "scene.gs_shadow_depth",
        "scene.gs_threads",
        "scene.display_settings.display_device",
        "scene.gs_gamma",
        "scene.gs_gamma_input",
        "scene.gs_tile_size",
        "scene.gs_tile_order",
        "scene.gs_tex_optimization",
        "scene.gs_auto_threads",
        "scene.gs_clay_render",
        "scene.gs_clay_render_keep_transparency",
        "scene.gs_clay_render_keep_normals",
        "scene.gs_clay_oren_nayar",
        "scene.gs_clay_sigma",
        "scene.gs_clay_col",
        "scene.gs_mask_render",
        "scene.bg_transp",
        "scene.bg_transp_refract",
        "scene.adv_auto_shadow_bias_enabled",
        "scene.adv_shadow_bias_value",
        "scene.adv_auto_min_raydist_enabled",
        "scene.adv_min_raydist_value",
        "scene.gs_premult",
        "scene.gs_transp_shad",
        "scene.gs_show_sam_pix",
        "scene.gs_type_render",
        "scene.gs_tex_optimization",
        "scene.intg_light_method",
        "scene.intg_use_caustics",
        "scene.intg_photons",
        "scene.intg_caustic_mix",
        "scene.intg_caustic_depth",
        "scene.intg_caustic_radius",
        "scene.intg_use_AO",
        "scene.intg_AO_samples",
        "scene.intg_AO_distance",
        "scene.intg_AO_color",
        "scene.intg_photonmap_enable_caustics",
        "scene.intg_photonmap_enable_diffuse",
        "scene.intg_bounces",
        "scene.intg_russian_roulette_min_bounces",
        "scene.intg_diffuse_radius",
        "scene.intg_cPhotons",
        "scene.intg_search",
        "scene.intg_final_gather",
        "scene.intg_fg_bounces",
        "scene.intg_fg_samples",
        "scene.intg_show_map",
        "scene.intg_caustic_method",
        "scene.intg_path_samples",
        "scene.intg_no_recursion",
        "scene.intg_debug_type",
        "scene.intg_show_perturbed_normals",
        "scene.intg_pm_ire",
        "scene.intg_pass_num",
        "scene.intg_times",
        "scene.intg_photon_radius",
        "scene.AA_min_samples",
        "scene.AA_inc_samples",
        "scene.AA_passes",
        "scene.AA_threshold",
        "scene.AA_pixelwidth",
        "scene.AA_filter_type",
        "scene.yafaray4.noise_control.resampled_floor",
        "scene.yafaray4.noise_control.sample_multiplier_factor",
        "scene.yafaray4.noise_control.light_sample_multiplier_factor",
        "scene.yafaray4.noise_control.indirect_sample_multiplier_factor",
        "scene.yafaray4.noise_control.detect_color_noise",
        "scene.yafaray4.noise_control.dark_threshold_factor",
        "scene.yafaray4.noise_control.variance_edge_size",
        "scene.yafaray4.noise_control.variance_pixels",
        "scene.yafaray4.noise_control.clamp_samples",
        "scene.yafaray4.noise_control.clamp_indirect",
        "scene.yafaray4.passes.pass_enable",
        "scene.yafaray4.passes.pass_mask_obj_index",
        "scene.yafaray4.passes.pass_mask_mat_index",
        "scene.yafaray4.passes.pass_mask_invert",
        "scene.yafaray4.passes.pass_mask_only",
        "scene.yafaray4.passes.pass_combined",
        "scene.yafaray4.passes.pass_depth",
        "scene.yafaray4.passes.pass_vector",
        "scene.yafaray4.passes.pass_normal",
        "scene.yafaray4.passes.pass_uV",
        "scene.yafaray4.passes.pass_color",
        "scene.yafaray4.passes.pass_emit",
        "scene.yafaray4.passes.pass_mist",
        "scene.yafaray4.passes.pass_diffuse",
        "scene.yafaray4.passes.pass_spec",
        "scene.yafaray4.passes.pass_aO",
        "scene.yafaray4.passes.pass_env",
        "scene.yafaray4.passes.pass_indirect",
        "scene.yafaray4.passes.pass_shadow",
        "scene.yafaray4.passes.pass_reflect",
        "scene.yafaray4.passes.pass_refract",
        "scene.yafaray4.passes.pass_index_ob",
        "scene.yafaray4.passes.pass_index_ma",
        "scene.yafaray4.passes.pass_diff_dir",
        "scene.yafaray4.passes.pass_diff_ind",
        "scene.yafaray4.passes.pass_diff_col",
        "scene.yafaray4.passes.pass_gloss_dir",
        "scene.yafaray4.passes.pass_gloss_ind",
        "scene.yafaray4.passes.pass_gloss_col",
        "scene.yafaray4.passes.pass_trans_dir",
        "scene.yafaray4.passes.pass_trans_ind",
        "scene.yafaray4.passes.pass_trans_col",
        "scene.yafaray4.passes.pass_subsurface_dir",
        "scene.yafaray4.passes.pass_subsurface_ind",
        "scene.yafaray4.passes.pass_subsurface_col"
    ]
    if bpy.app.version >= (2, 80, 0):
        pass  # FIXME BLENDER >= v2.80
    else:
        preset_values = preset_values + [
            "scene.render.layers[0].use_pass_z",
            "scene.render.layers[0].use_pass_vector",
            "scene.render.layers[0].use_pass_normal",
            "scene.render.layers[0].use_pass_uv",
            "scene.render.layers[0].use_pass_color",
            "scene.render.layers[0].use_pass_emit",
            "scene.render.layers[0].use_pass_mist",
            "scene.render.layers[0].use_pass_diffuse",
            "scene.render.layers[0].use_pass_specular",
            "scene.render.layers[0].use_pass_ambient_occlusion",
            "scene.render.layers[0].use_pass_environment",
            "scene.render.layers[0].use_pass_indirect",
            "scene.render.layers[0].use_pass_shadow",
            "scene.render.layers[0].use_pass_reflection",
            "scene.render.layers[0].use_pass_refraction",
            "scene.render.layers[0].use_pass_object_index",
            "scene.render.layers[0].use_pass_material_index",
            "scene.render.layers[0].use_pass_diffuse_direct",
            "scene.render.layers[0].use_pass_diffuse_indirect",
            "scene.render.layers[0].use_pass_diffuse_color",
            "scene.render.layers[0].use_pass_glossy_direct",
            "scene.render.layers[0].use_pass_glossy_indirect",
            "scene.render.layers[0].use_pass_glossy_color",
            "scene.render.layers[0].use_pass_transmission_direct",
            "scene.render.layers[0].use_pass_transmission_indirect",
            "scene.render.layers[0].use_pass_transmission_color",
            "scene.render.layers[0].use_pass_subsurface_direct",
            "scene.render.layers[0].use_pass_subsurface_indirect",
            "scene.render.layers[0].use_pass_subsurface_color",
        ]
    preset_subdir = "render"

    def execute(self, context):
        if hasattr(self, "pre_cb"):
            self.pre_cb(context)

        preset_menu_class = getattr(bpy.types, self.preset_menu)

        if not self.remove_active:
            if not self.name:
                return {'FINISHED'}

            filename = clean_name(self.name)

            home_dir = os.path.expanduser("~")
            target_path = os.path.join(home_dir, "yafaray4_userdata", "presets", self.preset_subdir)
            if not os.path.exists(target_path):
                os.makedirs(target_path)

            if not target_path:
                self.report({'WARNING'}, "Failed to create presets path")
                return {'CANCELLED'}

            filepath = os.path.join(target_path, filename) + ".py"

            if hasattr(self, "add"):
                self.add(context, filepath)
            else:
                file_preset = open(filepath, 'w')
                file_preset.write("import bpy\n")

                if hasattr(self, "preset_defines"):
                    for rna_path in self.preset_defines:
                        exec(rna_path)
                        file_preset.write("%s\n" % rna_path)
                    file_preset.write("\n")

                self.write_presets_to_file(file_preset)

                file_preset.close()

            preset_menu_class.bl_label = display_name(filename)

        else:
            preset_active = preset_menu_class.bl_label

            home_dir = os.path.expanduser("~")
            target_path = os.path.join(home_dir, "yafaray4_userdata", "presets", self.preset_subdir)
            if not os.path.exists(target_path):
                os.makedirs(target_path)

            filepath = preset_find(preset_active, target_path)

            if not filepath:
                filepath = preset_find(preset_active, target_path, disp_name=True)

            if not filepath:
                return {'CANCELLED'}

            if hasattr(self, "remove"):
                self.remove(context, filepath)
            else:
                # noinspection PyBroadException
                try:
                    os.remove(filepath)
                except Exception:
                    import traceback
                    print("No Preset there to remove...")
            # XXX stupid: Print bl_label on menu selector...
            preset_menu_class.bl_label = self.bl_label

        if hasattr(self, "post_cb"):
            self.post_cb(context)

        return {'FINISHED'}

    # noinspection PyUnusedLocal
    def check(self, context):
        self.name = clean_name(self.name)

    # noinspection PyUnusedLocal
    def invoke(self, context, event):
        if not self.remove_active:
            wm = context.window_manager
            return wm.invoke_props_dialog(self)
        else:
            return self.execute(context)

    def export_to_file(self, filepath):
        filepath += ".preset.py"

        file_preset = open(filepath, 'w')
        file_preset.write("import bpy\n")

        if hasattr(self, "preset_defines"):
            for rna_path in self.preset_defines:
                exec(rna_path)
                file_preset.write("%s\n" % rna_path)
            file_preset.write("\n")

        self.write_presets_to_file(file_preset)

        file_preset.close()

    def write_presets_to_file(self, file_preset):
        for rna_path in self.preset_values:
            value = eval("bpy.context." + rna_path)
            if type(value) == float:  # formatting of the floating point values
                value = round(value, 4)
            if str(value).startswith('Color'):  # formatting of the Color Vectors (r,g,b)
                r, g, b = round(value.r, 3), round(value.g, 3), round(value.b, 3)
                file_preset.write("%s = %r, %r, %r\n" % (rna_path, r, g, b))
            else:
                # noinspection PyBroadException
                try:  # convert thin wrapped sequences to simple lists to repr()
                    value = value[:]
                except Exception:
                    pass
                file_preset.write("%s = %r\n" % (rna_path, value))


classes = (
    RenderPresets,
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
