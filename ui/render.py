# SPDX-License-Identifier: GPL-2.0-or-later

import os

import bpy
from bl_ui.properties_render import RenderButtonsPanel
from bpy.path import display_name
# noinspection PyUnresolvedReferences
from bpy.types import Panel, Menu

if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed,
    # before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the
    # "libyafaray4_bindings" compiled module is installed on. Assuming that the YafaRay-Plugin exporter is installed
    # in a folder named "yafaray4" within the addons Blender directory
    # noinspection PyUnresolvedReferences
    import yafaray4.prop.scene

    if hasattr(bpy.types, 'YafaRay4Properties'):
        yafaray4.prop.scene.unregister()
    yafaray4.prop.scene.register()
    # noinspection PyUnresolvedReferences
    import yafaray4.ot.presets

    if hasattr(bpy.types, 'YAFARAY4_OT_render_presets'):
        yafaray4.ot.presets.unregister()
    yafaray4.ot.presets.register()
    # noinspection PyUnresolvedReferences
    from yafaray4.ot import presets
else:
    pass

if bpy.app.version >= (2, 80, 0):
    from bl_ui.properties_output import RenderOutputButtonsPanel  # FIXME BLENDER >= v2.80


    class OutputPanel(RenderOutputButtonsPanel, Panel):
        pass
else:
    from bl_ui.properties_render import RenderButtonsPanel  # FIXME BLENDER >= v2.80


    class OutputPanel(RenderButtonsPanel, Panel):
        pass


def ui_split(ui_item, factor):
    if bpy.app.version >= (2, 80, 0):
        return ui_item.split(factor=factor)
    else:
        return ui_item.split(percentage=factor)


class Render(RenderButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_render"
    bl_label = "Render"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):

        layout = self.layout
        rd = context.scene.render
        scene = context.scene

        row = layout.row()
        row.operator("yafaray4.render_still", text="Image", icon='RENDER_STILL')
        row.operator("yafaray4.render_animation", text="Animation", icon='RENDER_ANIMATION')
        layout.row().operator("yafaray4.render_view", text="Render 3D View", icon='VIEW3D')
        if bpy.app.version >= (2, 80, 0):
            pass  # FIXME BLENDER >= v2.80
        else:
            layout.prop(rd, "display_mode", text="Display")


class RenderPresets(RenderButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_render_presets"
    bl_label = "Render Presets"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}

    # noinspection PyUnusedLocal
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.menu("YAFARAY4_MT_presets_render", text=bpy.types.YAFARAY4_MT_presets_render.bl_label)
        row.operator("yafaray4.render_presets", text="",
                     icon="ADD" if bpy.app.version >= (2, 80, 0) else "ZOOMIN").remove_active = False
        row.operator("yafaray4.render_presets", text="",
                     icon="REMOVE" if bpy.app.version >= (2, 80, 0) else "ZOOMOUT").remove_active = True


class Format(OutputPanel, Panel):
    bl_idname = "YAFARAY4_PT_render_dimensions"
    bl_label = "Format"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        rd = context.scene.render
        row = layout.row(align=True)
        if bpy.app.version >= (2, 80, 0):
            pass  # FIXME BLENDER >= v2.80
        else:
            row.menu("RENDER_MT_presets", text="Dimension Presets")
            row.operator("render.preset_add", text="", icon="ADD" if bpy.app.version >= (2, 80, 0) else "ZOOMIN")
            row.operator("render.preset_add", text="",
                         icon="REMOVE" if bpy.app.version >= (2, 80, 0) else "ZOOMOUT").remove_active = True
        split = layout.split()
        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Resolution:")
        sub.prop(rd, "resolution_x", text="X")
        sub.prop(rd, "resolution_y", text="Y")
        sub.prop(rd, "resolution_percentage", text="")

        row = col.row()
        row.prop(rd, "use_border", text="Border")
        sub = row.row()
        sub.active = rd.use_border
        sub.prop(rd, "use_crop_to_border", text="Crop")


class FrameRange(OutputPanel, Panel):
    bl_idname = "YAFARAY4_PT_render_frame_range"
    bl_label = "Frame Range"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        sub = row.column(align=True)
        sub.label(text="Frame Range:")
        sub.prop(scene, "frame_start", text="Start")
        sub.prop(scene, "frame_end", text="End")
        sub.prop(scene, "frame_step", text="Step")


class AASettings(RenderButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_aa_settings"
    bl_label = "Anti-Aliasing / Noise control"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

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
        col.column()
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
            col.label(text="")
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


class ConvertOldSettings(RenderButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_render_convert_old_settings"
    bl_label = "Convert old YafaRay Settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    # noinspection PyUnusedLocal
    def draw(self, context):
        layout = self.layout
        layout.column().operator("yafaray4.data_convert_properties", text="Convert data from 2.4x")


class Advanced(RenderButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_render_advanced"
    bl_label = "Advanced Settings - only for experts"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        split = layout.split()
        col = split.column()
        col.prop(scene, "adv_scene_mesh_tesselation")

        split = layout.split()
        col = split.column()
        col.prop(scene, "adv_base_sampling_offset")

        split = layout.split()
        col = split.column()
        col.prop(scene, "adv_auto_shadow_bias_enabled")
        if not scene.adv_auto_shadow_bias_enabled:
            col = split.column()
            sub = col.column()
            sub.prop(scene, "adv_shadow_bias_value")

        split = layout.split()
        col = split.column()
        col.prop(scene, "adv_auto_min_raydist_enabled")
        if not scene.adv_auto_min_raydist_enabled:
            col = split.column()
            sub = col.column()
            sub.prop(scene, "adv_min_raydist_value")

        col = layout.column(align=True)
        col.prop(scene, "intg_motion_blur_time_forced", toggle=True)
        if scene.intg_motion_blur_time_forced:
            col.prop(scene, "intg_motion_blur_time_forced_value")


class PresetsRender(Menu):
    bl_idname = "YAFARAY4_MT_presets_render"
    bl_label = "Yafaray Render Presets"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    preset_subdir = "render"
    preset_operator = "script.execute_preset"

    # noinspection PyUnusedLocal

    def path_menu(self, search_paths, operator, props_default=None):
        if props_default is None:
            props_default = {}
        layout = self.layout

        if not search_paths:
            layout.label(text="* Missing Paths *")

        # collect paths
        files = []
        for directory in search_paths:
            files.extend([(f, os.path.join(directory, f)) for f in os.listdir(directory)])

        files.sort()

        for f, filepath in files:

            if f.startswith(".") or f.startswith("_"):
                continue

            preset_name = display_name(f)
            props = layout.operator(operator, text=preset_name)

            for attr, value in props_default.items():
                setattr(props, attr, value)

            props.filepath = filepath
            if operator == "script.execute_preset":
                props.menu_idname = self.bl_idname

    # noinspection PyUnusedLocal
    def draw(self, context):
        """Define these on the subclass
         - preset_operator
         - preset_subdir
        """
        home_dir = os.path.expanduser("~")
        search_path = [os.path.join(home_dir, "yafaray4_userdata", "presets", self.preset_subdir)]
        if not os.path.exists(search_path[0]):
            os.makedirs(search_path[0])

        self.path_menu(search_path, self.preset_operator)


class GeneralSettings(RenderButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_general_settings"
    bl_label = "General Settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        render = scene.render

        split = ui_split(layout, 0.58)
        col = split.column()
        col.prop(scene, "gs_ray_depth")
        col.prop(scene, "gs_type_render")

        col = split.column()
        sub = col.column()
        sub.enabled = scene.gs_transp_shad
        sub.prop(scene, "gs_shadow_depth")
        sub = col.column()
        sub.enabled = scene.gs_type_render == "into_blender"
        sub.prop(scene, "gs_tile_size")
        sub.prop(scene, "gs_tile_order")

        layout.separator()

        split = layout.split()
        col = split.column()
        col.prop(scene, "gs_tex_optimization")

        split = layout.split()
        col = split.column()
        col.prop(scene, "gs_auto_threads", toggle=True)
        col.prop(scene, "gs_transp_shad", toggle=True)

        col = split.column()
        sub = col.column()
        if not scene.gs_auto_threads:
            sub.prop(scene, "gs_threads")
        else:
            sub.label(text="")
        col.prop(scene, "gs_show_sam_pix", toggle=True)
        col.prop(scene, "use_instances", text="Use instances", toggle=True)

        split = ui_split(layout, 0.5)
        col = split.column()
        col.prop(scene, "bg_transp", toggle=True)
        col = split.column()
        sub = col.column()
        sub.enabled = scene.bg_transp
        sub.prop(scene, "bg_transp_refract", toggle=True)


class Accelerator(RenderButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_accelerator"
    bl_label = "Scene accelerator settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        split = ui_split(layout, 0.43)
        col = split.column()
        col.prop(scene, "gs_accelerator")


class Logging(OutputPanel, Panel):
    bl_idname = "YAFARAY4_PT_logging"
    bl_label = "Logging / Params Badge Settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        split = ui_split(layout, 0.43)
        col = split.column()
        col.prop(scene.yafaray.logging, "paramsBadgePosition")
        col = split.column()
        col.prop(scene.yafaray.logging, "drawRenderSettings")
        col = split.column()
        col.prop(scene.yafaray.logging, "drawAANoiseSettings")

        split = layout.split()
        col = split.column()
        col.prop(scene.yafaray.logging, "logPrintDateTime")
        col = split.column()
        col.prop(scene.yafaray.logging, "consoleVerbosity")
        col = split.column()
        col.prop(scene.yafaray.logging, "logVerbosity")

        split = layout.split()
        col = split.column()
        col.prop(scene.yafaray.logging, "saveLog")
        col = split.column()
        col.prop(scene.yafaray.logging, "saveHTML")
        col = split.column()
        col.prop(scene.yafaray.logging, "savePreset")

        if scene.yafaray.logging.saveLog or scene.yafaray.logging.saveHTML or scene.yafaray.logging.savePreset \
                or scene.yafaray.logging.paramsBadgePosition == "top" \
                or scene.yafaray.logging.paramsBadgePosition == "bottom":
            if scene.gs_type_render == "into_blender" and not scene.gs_secondary_file_output:
                row = layout.row()
                row.label(text="Params badge and saving log/html/preset files only works when exporting to image file.",
                          icon='ERROR')
                row = layout.row()
                row.label(
                    text="To get the badge/logs, render to image or render into Blender+enable Secondary File Output.",
                    icon='ERROR')

            if scene.yafaray.logging.paramsBadgePosition == "bottom" and scene.gs_type_render == "file":
                row = layout.row()
                row.label(text="Image with Params Badge at bottom will appear CROPPED in Blender,", icon='INFO')
                row = layout.row()
                row.label(text="  but will be CORRECT in the exported image file.", icon='INFO')

            row = layout.row()
            row.prop(scene.yafaray.logging, "title")
            row = layout.row()
            row.prop(scene.yafaray.logging, "author")
            row = layout.row()
            row.prop(scene.yafaray.logging, "contact")
            row = layout.row()
            row.prop(scene.yafaray.logging, "comments")
            row = layout.row()
            row.prop(scene.yafaray.logging, "customIcon")
            row = layout.row()
            col = row.column()
            col.prop(scene.yafaray.logging, "customFont")
            col = row.column()
            col.prop(scene.yafaray.logging, "fontScale")


class ClayRender(RenderButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_clay_render"
    bl_label = "Clay Render Settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.row(align=True)
        split = ui_split(layout, 0.5)
        col = split.column()
        col.prop(scene, "gs_clay_render", toggle=True)
        if scene.gs_clay_render:
            col = split.column()
            col.prop(scene, "gs_clay_col", text="")
            layout.separator()
            split = layout.split()
            col = split.column()
            col.prop(scene, "gs_clay_oren_nayar")
            if scene.gs_clay_oren_nayar:
                col = split.column()
                col.prop(scene, "gs_clay_sigma")
            col = layout.column()
            col.prop(scene, "gs_clay_render_keep_transparency")
            # col = split.column()
            col.prop(scene, "gs_clay_render_keep_normals")


class Integrator(RenderButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_integrator_render"
    bl_label = "Integrator"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "intg_light_method")

        if scene.intg_light_method == "Direct Lighting":
            row = layout.row()
            col = row.column(align=True)
            col.prop(scene, "intg_use_caustics", toggle=True)
            if scene.intg_use_caustics:
                col.prop(scene, "intg_caustic_depth")
                col.prop(scene, "intg_photons")
                col.prop(scene, "intg_caustic_radius")
                col.prop(scene, "intg_caustic_mix")

            col = row.column(align=True)
            col.prop(scene, "intg_use_AO", toggle=True)
            if scene.intg_use_AO:
                col.prop(scene, "intg_AO_color")
                col.prop(scene, "intg_AO_samples")
                col.prop(scene, "intg_AO_distance")

        elif scene.intg_light_method == "Photon Mapping":
            row = layout.row()

            row.prop(scene, "intg_bounces")

            row = layout.row()
            col = row.column(align=True)
            col.prop(scene, "intg_photonmap_enable_diffuse", icon='MOD_PHYSICS', toggle=True)
            if scene.intg_photonmap_enable_diffuse:
                col.prop(scene, "intg_photons")
                col.prop(scene, "intg_diffuse_radius")
                col.prop(scene, "intg_search")

            col = row.column(align=True)
            col.prop(scene, "intg_photonmap_enable_caustics", icon='MOD_PARTICLES', toggle=True)
            if scene.intg_photonmap_enable_caustics:
                col.prop(scene, "intg_cPhotons")
                col.prop(scene, "intg_caustic_radius")
                col.prop(scene, "intg_caustic_mix")

            if scene.intg_photonmap_enable_diffuse:
                row = layout.row()
                row.prop(scene, "intg_final_gather", toggle=True, icon='FORCE_FORCE')

                if scene.intg_final_gather:
                    col = layout.row()
                    col.prop(scene, "intg_fg_bounces")
                    col.prop(scene, "intg_fg_samples")
                    col = layout.row()
                    col.prop(scene, "intg_show_map", toggle=True)

        elif scene.intg_light_method == "Pathtracing":
            col = layout.row()
            col.prop(scene, "intg_caustic_method")

            col = layout.row()
            if scene.intg_caustic_method in {"Path+Photon", "Photon"}:
                col.prop(scene, "intg_photons", text="Photons")
                col.prop(scene, "intg_caustic_mix", text="Caus. Mix")
                col = layout.row()
                col.prop(scene, "intg_caustic_depth", text="Caus. Depth")
                col.prop(scene, "intg_caustic_radius", text="Caus. Radius")
                split = layout.split()
                split.column()

            col = layout.row()
            col.prop(scene, "intg_path_samples")
            col.prop(scene, "intg_bounces")
            col.prop(scene, "intg_russian_roulette_min_bounces")
            col = layout.row()
            col.prop(scene, "intg_no_recursion")

        elif scene.intg_light_method == "Debug":
            layout.row().prop(scene, "intg_debug_type")
            layout.row().prop(scene, "intg_show_perturbed_normals")

        elif scene.intg_light_method == "SPPM":
            row = layout.row()
            col = row.column()
            col.prop(scene, "intg_photons", text="Photons")
            col.prop(scene, "intg_pass_num")
            col.prop(scene, "intg_bounces", text="Bounces")
            col = row.column()
            col.prop(scene, "intg_times")
            col.prop(scene, "intg_diffuse_radius")
            col.prop(scene, "intg_search")
            col.prop(scene, "intg_pm_ire")

        elif scene.intg_light_method == "Bidirectional":
            col = layout.column()
            col.label(text="The Bidirectional integrator is UNSTABLE.", icon="ERROR")
            col.label(text="It might give unexpected and perhaps even incorrect render results.")
            col.label(text="Use at your own risk.")


class Output(OutputPanel):
    bl_idname = "YAFARAY4_PT_render_output"
    bl_label = "Output"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if context.scene.img_save_with_blend_file:
            row = layout.row()
            row.label(text="Parameter 'Save with Blend file' is enabled.", icon="INFO")
            row = layout.row()
            row.label(
                text="Be aware that the first time you render, it will change *automatically* the image output folder",
                icon="INFO")
        if context.scene.gs_secondary_file_output:
            row = layout.row()
            row.label(text="Parameter 'Secondary File Output' is enabled.", icon="INFO")
            row = layout.row()
            row.label(
                text="Be aware that even when rendering into Blender, it will save images to the image output folder",
                icon="INFO")

        col = layout.column()

        sub = col.column()
        sub.enabled = scene.gs_type_render == "into_blender"
        sub.prop(scene, "gs_secondary_file_output")

        row = layout.row()
        row.enabled = scene.gs_type_render == "into_blender"
        col = row.column()
        col.prop(scene, "gs_film_save_load")
        if scene.gs_film_save_load == "save" or scene.gs_film_save_load == "load-save":
            row = layout.row()
            col = row.column()
            col.prop(scene, "gs_film_autosave_interval_type")
            col = row.column()
            if scene.gs_film_autosave_interval_type == "pass-interval":
                col.prop(scene, "gs_film_autosave_interval_passes")
            elif scene.gs_film_autosave_interval_type == "time-interval":
                col.prop(scene, "gs_film_autosave_interval_seconds")
            else:
                col.label(text="")

        if scene.gs_film_save_load == "load-save":
            row = layout.row()
            row.label(
                "If the loaded image Film does not match exactly the sceneene, crashes and/or incorrect renders may "
                "happen, USE WITH CARE!",
                icon="INFO")

        if (
                scene.yafaray.logging.saveLog or scene.yafaray.logging.saveHTML or scene.yafaray.logging.savePreset or
                scene.yafaray.logging.paramsBadgePosition == "top"
                or scene.yafaray.logging.paramsBadgePosition == "bottom") \
                and scene.gs_type_render == "into_blender" and not scene.gs_secondary_file_output:
            row = layout.row()
            row.label(text="Params badge and saving log/html/preset files only works when exporting to image file.",
                      icon='INFO')
            row = layout.row()
            row.label(
                text="To get the badge/logs, render to image or render into Blender+enable Secondary File Output.",
                icon='INFO')
            layout.row()

        if scene.yafaray.logging.paramsBadgePosition == "bottom" and scene.gs_type_render == "file":
            row = layout.row()
            row.label(text="Image with Params Badge at bottom will appear CROPPED in Blender,", icon='INFO')
            row = layout.row()
            row.label(text="  but will be CORRECT in the exported image file.", icon='INFO')

        rd = context.scene.render
        sc = context.scene
        image_settings = rd.image_settings

        if sc.gs_type_render == "into_blender" and not sc.gs_secondary_file_output:
            row = layout.row()
            row.label(
                text="To enable file output, enable Secondary File Output or choose"
                     " Render into File or Render into XML",
                icon="INFO")
        else:
            layout.prop(sc, "img_save_with_blend_file")
            if not sc.img_save_with_blend_file:
                layout.row()
                layout.prop(rd, "filepath", text="")
            row = layout.row()
            col = row.column()
            col.prop(sc, "img_add_blend_name")
            col = row.column()
            col.prop(sc, "img_add_datetime")
            row = layout.row()
            col = row.column()
            col.prop(sc, "gs_images_autosave_interval_type")
            col = row.column()
            if sc.gs_images_autosave_interval_type == "pass-interval":
                col.prop(sc, "gs_images_autosave_interval_passes")
            elif sc.gs_images_autosave_interval_type == "time-interval":
                col.prop(sc, "gs_images_autosave_interval_seconds")
            else:
                col.label(text="")

            split = ui_split(layout, 0.6)
            col = split.column()
            col.prop(sc, "img_output", text="", icon='IMAGE_DATA')
            col = split.column()
            col.row().prop(image_settings, "color_mode", text="Color", expand=True)

            if sc.img_output == "OPEN_EXR":
                split = layout.split()
                split.prop(sc, "img_multilayer")

            if sc.img_output == "OPEN_EXR" or sc.img_output == "HDR":
                # If the output file is an HDR/EXR file, we force the render output to Linear
                pass
            elif sc.gs_type_render == "file" or sc.gs_type_render == "xml" or sc.gs_type_render == "c" \
                    or sc.gs_type_render == "python":
                split = ui_split(layout, 0.6)
                col = split.column()
                col.prop(sc.display_settings, "display_device")

                if sc.display_settings.display_device == "None":
                    col = split.column()
                    col.prop(sc, "gs_gamma", text="Gamma")

                if sc.display_settings.display_device == "sRGB":
                    pass
                elif sc.display_settings.display_device == "None":
                    pass
                elif sc.display_settings.display_device == "XYZ":
                    row = layout.row(align=True)
                    row.label(text="YafaRay 'XYZ' support is experimental and may not give the expected results",
                              icon="ERROR")
                else:
                    row = layout.row(align=True)
                    row.label(
                        text="YafaRay doesn't support '" + sc.display_settings.display_device + "', assuming sRGB",
                        icon="ERROR")

            split = ui_split(layout, 0.6)
            col = split.column()
            col.prop(sc, "gs_premult", text="Premultiply Alpha")
            if sc.img_output == "OPEN_EXR" and sc.gs_premult == "no":
                row = layout.row(align=True)
                row.label(text="Typically you should enable Premultiply in EXR files", icon="INFO")
            if sc.img_output == "PNG" and sc.gs_premult == "yes":
                row = layout.row(align=True)
                row.label(text="Typically you should disable Premultiply in PNG files", icon="INFO")
            if sc.img_output != "PNG" and sc.img_output != "OPEN_EXR" and sc.img_output != "JPEG" \
                    and sc.gs_premult == "auto":
                row = layout.row(align=True)
                row.label(
                    text="Can't guess premultiply for " + sc.img_output
                         + " , enabling by default but better select Yes or No",
                    icon="INFO")

            if sc.img_output != "OPEN_EXR" and sc.img_output != "HDR":
                split = layout.split()
                col = split.column()
                col.prop(sc, "img_denoise")
                if sc.img_denoise:
                    col = split.column()
                    col.prop(sc, "img_denoiseMix", text="Mix")
                    col = split.column()
                    col.prop(sc, "img_denoiseHLum", text="h(lum)")
                    col = split.column()
                    col.prop(sc, "img_denoiseHCol", text="h(chrom)")
                    split = layout.split()
                    col = split.column()
                    col.label(text="Denoise will not appear in Blender, only in saved image files", icon="INFO")


class PostProcessing(OutputPanel):
    bl_idname = "YAFARAY4_PT_render_post_processing"
    bl_label = "Post Processing"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render

        split = layout.split()

        col = split.column()
        col.prop(rd, "use_compositing")
        col.prop(rd, "use_sequencer")

        col = split.column()
        col.prop(rd, "dither_intensity", text="Dither", slider=True)


class Views(OutputPanel, Panel):
    bl_idname = "YAFARAY4_PT_views"
    bl_label = "Stereoscopy / Multi-View"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw_header(self, context):
        rd = context.scene.render
        self.layout.prop(rd, "use_multiview", text="")

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render
        rv = rd.views.active

        if rd.use_multiview:
            layout.active = rd.use_multiview
            basic_stereo = rd.views_format == 'STEREO_3D'

            row = layout.row()
            row.prop(rd, "views_format", expand=True)

            if bpy.app.version >= (2, 80, 0):
                renderviews_template_name = "RENDER_UL_renderviews"
            else:
                renderviews_template_name = "RENDERLAYER_UL_renderviews"

            if basic_stereo:
                row = layout.row()
                row.template_list(renderviews_template_name, "name", rd, "stereo_views", rd.views, "active_index",
                                  rows=2)

                row = layout.row()
                row.label(text="File Suffix:")
                row.prop(rv, "file_suffix", text="")

            else:
                row = layout.row()
                row.template_list(renderviews_template_name, "name", rd, "views", rd.views, "active_index", rows=2)

                col = row.column(align=True)
                col.operator("scene.render_view_add", icon="ADD" if bpy.app.version >= (2, 80, 0) else "ZOOMIN",
                             text="")
                col.operator("scene.render_view_remove", icon="REMOVE" if bpy.app.version >= (2, 80, 0) else "ZOOMOUT",
                             text="")

                row = layout.row()
                row.label(text="Camera Suffix:")
                row.prop(rv, "camera_suffix", text="")


classes = (
    PresetsRender,
    RenderPresets,
    Render,
    Format,
    FrameRange,
    GeneralSettings,
    Output,
    Logging,
    Views,
    PostProcessing,
    Integrator,
    Accelerator,
    ClayRender,
    AASettings,
    ConvertOldSettings,
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
