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
from bpy.types import Operator
import os
import sys
from bpy.path import clean_name, display_name
from bpy_types import StructRNA, _GenericUI, RNAMeta


def preset_find(name, preset_path, disp_name=False):
    if not name:
        return None

    if display_name:
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


class AddPresetBase():
    bl_options = {'REGISTER'}  # only because invoke_props_popup requires.
    name = bpy.props.StringProperty(name="Name", description="Name of the preset, used to make the path name", maxlen=64, default="")
    remove_active = bpy.props.BoolProperty(default=False, options={'HIDDEN'})

    def execute(self, context):

        if hasattr(self, "pre_cb"):
            self.pre_cb(context)

        preset_menu_class = getattr(bpy.types, self.preset_menu)

        if not self.remove_active:

            if not self.name:
                return {'FINISHED'}

            filename = clean_name(self.name)

            home_dir = os.path.expanduser("~")
            target_path = os.path.join(home_dir, "yafaray_userdata", "presets", self.preset_subdir)
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

                for rna_path in self.preset_values:
                    value = eval(rna_path)
                    if type(value) == float:  # formatting of the floating point values
                        value = round(value, 4)
                    if str(value).startswith('Color'):  # formatting of the Color Vectors (r,g,b)
                        r, g, b = round(value.r, 3), round(value.g, 3), round(value.b, 3)
                        file_preset.write("%s = %r, %r, %r\n" % (rna_path, r, g, b))
                    else:
                        try:  # convert thin wrapped sequences to simple lists to repr()
                            value = value[:]
                        except:
                            pass
                        file_preset.write("%s = %r\n" % (rna_path, value))

                file_preset.close()

            preset_menu_class.bl_label = display_name(filename)

        else:
            preset_active = preset_menu_class.bl_label

            home_dir = os.path.expanduser("~")
            target_path = os.path.join(home_dir, "yafaray_userdata", "presets", self.preset_subdir)
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
                try:
                    os.remove(filepath)
                except:
                    import traceback
                    print("No Preset there to remove...")
            # XXX stupid: Print bl_label on menu selector...
            preset_menu_class.bl_label = self.bl_label

        if hasattr(self, "post_cb"):
            self.post_cb(context)

        return {'FINISHED'}

    def check(self, context):
        self.name = clean_name(self.name)

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

        if bpy.app.version >= (2, 80, 0):
            pass  # FIXME BLENDER 2.80-3.00
        else:
            for rna_path in self.preset_values:
                value = eval(rna_path)
                if type(value) == float:  # formatting of the floating point values
                    value = round(value, 4)
                if str(value).startswith('Color'):  # formatting of the Color Vectors (r,g,b)
                    r, g, b = round(value.r, 3), round(value.g, 3), round(value.b, 3)
                    file_preset.write("%s = %r, %r, %r\n" % (rna_path, r, g, b))
                else:
                    try:  # convert thin wrapped sequences to simple lists to repr()
                        value = value[:]
                    except:
                        pass
                    file_preset.write("%s = %r\n" % (rna_path, value))

        file_preset.close()


class YAFARAY_OT_presets_renderset(AddPresetBase, Operator):
    '''Add a Yafaray Render Preset in user home folder->yafaray_user_data/presets/render'''
    '''To delete or modify presets, modify the .py files directly in that folder'''
    bl_idname = "yafaray.preset_add"
    bl_label = "Yafaray Render Presets"
    preset_menu = "YAFARAY4_MT_presets_render"
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
        "scene.yafaray.noise_control.resampled_floor",
        "scene.yafaray.noise_control.sample_multiplier_factor",
        "scene.yafaray.noise_control.light_sample_multiplier_factor",
        "scene.yafaray.noise_control.indirect_sample_multiplier_factor",
        "scene.yafaray.noise_control.detect_color_noise",
        "scene.yafaray.noise_control.dark_threshold_factor",
        "scene.yafaray.noise_control.variance_edge_size",
        "scene.yafaray.noise_control.variance_pixels",
        "scene.yafaray.noise_control.clamp_samples",
        "scene.yafaray.noise_control.clamp_indirect",
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
        "scene.yafaray.passes.pass_enable",
        "scene.yafaray.passes.pass_mask_obj_index",
        "scene.yafaray.passes.pass_mask_mat_index",
        "scene.yafaray.passes.pass_mask_invert",
        "scene.yafaray.passes.pass_mask_only",
        "scene.yafaray.passes.pass_Combined",
        "scene.yafaray.passes.pass_Depth",
        "scene.yafaray.passes.pass_Vector",
        "scene.yafaray.passes.pass_Normal",
        "scene.yafaray.passes.pass_UV",
        "scene.yafaray.passes.pass_Color",
        "scene.yafaray.passes.pass_Emit",
        "scene.yafaray.passes.pass_Mist",
        "scene.yafaray.passes.pass_Diffuse",
        "scene.yafaray.passes.pass_Spec",
        "scene.yafaray.passes.pass_AO",
        "scene.yafaray.passes.pass_Env",
        "scene.yafaray.passes.pass_Indirect",
        "scene.yafaray.passes.pass_Shadow",
        "scene.yafaray.passes.pass_Reflect",
        "scene.yafaray.passes.pass_Refract",
        "scene.yafaray.passes.pass_IndexOB",
        "scene.yafaray.passes.pass_IndexMA",
        "scene.yafaray.passes.pass_DiffDir",
        "scene.yafaray.passes.pass_DiffInd",
        "scene.yafaray.passes.pass_DiffCol",
        "scene.yafaray.passes.pass_GlossDir",
        "scene.yafaray.passes.pass_GlossInd",
        "scene.yafaray.passes.pass_GlossCol",
        "scene.yafaray.passes.pass_TransDir",
        "scene.yafaray.passes.pass_TransInd",
        "scene.yafaray.passes.pass_TransCol",
        "scene.yafaray.passes.pass_SubsurfaceDir",
        "scene.yafaray.passes.pass_SubsurfaceInd",
        "scene.yafaray.passes.pass_SubsurfaceCol"
    ]

    preset_subdir = "render"


class Yafaray_Menu(StructRNA, _GenericUI, metaclass=RNAMeta):  # Yafaray's own Preset Menu drawing: search method for files changed
    __slots__ = ()

    def path_menu(self, searchpaths, operator, props_default={}):
        layout = self.layout
        # hard coded to set the operators 'filepath' to the filename.

        import os
        import bpy.utils

        layout = self.layout

        if not searchpaths:
            layout.label(text="* Missing Paths *")

        # collect paths
        files = []
        for directory in searchpaths:
            files.extend([(f, os.path.join(directory, f)) for f in os.listdir(directory)])

        files.sort()

        for f, filepath in files:

            if f.startswith("."):
                continue

            preset_name = display_name(f)
            props = layout.operator(operator, text=preset_name)

            for attr, value in props_default.items():
                setattr(props, attr, value)

            props.filepath = filepath
            if operator == "script.execute_preset":
                props.menu_idname = self.bl_idname

    def draw_preset(self, context):
        """Define these on the subclass
         - preset_operator
         - preset_subdir
        """
        home_dir = os.path.expanduser("~")
        search_path = [os.path.join(home_dir, "yafaray_userdata", "presets", self.preset_subdir)]
        if not os.path.exists(search_path[0]):
            os.makedirs(search_path[0])
       
        self.path_menu(search_path, self.preset_operator)


classes = (
    YAFARAY_OT_presets_renderset,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
