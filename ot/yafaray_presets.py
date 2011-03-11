import bpy
import os
from bpy.utils import script_paths
from bpy.path import clean_name, display_name


def yaf_script_path():
    for yaf_path in script_paths(os.path.join("addons", "yafaray")):
        if yaf_path:
            return yaf_path
    return ''


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
            target_path = os.path.normpath(os.path.join(yaf_script_path(), "presets", self.preset_subdir))

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
                    # convert thin wrapped sequences to simple lists to repr()
                    try:
                        value = value[:]
                    except:
                        pass

                    file_preset.write("%s = %r\n" % (rna_path, value))

                file_preset.close()

            preset_menu_class.bl_label = display_name(filename)

        else:
            preset_active = clean_name(preset_menu_class.bl_label)
            filepath = os.path.join(yaf_script_path(), "presets", self.preset_subdir, preset_active + ".py")

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


class YAFARAY_OT_presets_renderset(YAF_AddPresetBase, bpy.types.Operator):
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
        "scene.gs_auto_save",
        "scene.gs_auto_alpha",
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
        "scene.intg_use_bg",
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
