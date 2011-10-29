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


def yaf_preset_find(name, preset_path, disp_name=False):
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


class YAF_AddPresetBase():
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
            target_path = os.path.join(sys.path[0], "yafaray", "presets", self.preset_subdir)

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
            target_path = os.path.join(sys.path[0], "yafaray", "presets", self.preset_subdir)
            filepath = yaf_preset_find(preset_active, target_path)

            if not filepath:
                filepath = yaf_preset_find(preset_active, target_path, disp_name=True)

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


class YAFARAY_OT_presets_renderset(YAF_AddPresetBase, Operator):
    '''Add a Yafaray Render Preset'''
    bl_idname = "yafaray.preset_add"
    bl_label = "Yafaray Render Presets"
    preset_menu = "YAFARAY_MT_presets_render"
    preset_defines = [
        "scene = bpy.context.scene"
    ]
    preset_values = [
        "scene.render.use_color_management",
        "scene.gs_ray_depth",
        "scene.gs_shadow_depth",
        "scene.gs_threads",
        "scene.gs_gamma",
        "scene.gs_gamma_input",
        "scene.gs_tile_size",
        "scene.gs_tile_order",
        "scene.gs_auto_threads",
        "scene.gs_clay_render",
        "scene.gs_draw_params",
        "scene.gs_custom_string",
        "scene.gs_premult",
        "scene.gs_transp_shad",
        "scene.gs_clamp_rgb",
        "scene.gs_show_sam_pix",
        "scene.gs_z_channel",
        "scene.gs_type_render",
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
        "scene.intg_bounces",
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
        "scene.AA_filter_type"
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
            layout.label("* Missing Paths *")

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
        search_path = [os.path.join(sys.path[0], "yafaray", "presets", self.preset_subdir)]
        self.path_menu(search_path, self.preset_operator)
