# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bl_ui.properties_render import RenderButtonsPanel
# noinspection PyUnresolvedReferences
from bpy.types import Panel


def ui_split(ui_item, factor):
    if bpy.app.version >= (2, 80, 0):
        return ui_item.split(factor=factor)
    else:
        return ui_item.split(percentage=factor)


class Render(RenderButtonsPanel, Panel):
    bl_idname = "yafaray4.render"
    bl_label = "Render"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):

        layout = self.layout
        rd = context.scene.render

        if context.scene.img_save_with_blend_file:
            row = layout.row()
            row.label(text="Parameter 'Save with Blend file' is enabled in the Output options.", icon="INFO")
            row = layout.row()
            row.label(
                text="Be aware that the first time you render, it will change *automatically* the image output folder",
                icon="INFO")
        if context.scene.gs_secondary_file_output:
            row = layout.row()
            row.label(text="Parameter 'Secondary File Output' is enabled in the General Settings options.", icon="INFO")
            row = layout.row()
            row.label(
                text="Be aware that even when rendering into Blender, it will save images to the image output folder",
                icon="INFO")
        row = layout.row()
        row.operator("yafaray4.render_still", text="Image", icon='RENDER_STILL')
        row.operator("yafaray4.render_animation", text="Animation", icon='RENDER_ANIMATION')
        layout.row().operator("yafaray4.render_view", text="Render 3D View", icon='VIEW3D')
        if bpy.app.version >= (2, 80, 0):
            pass  # FIXME BLENDER 2.80-3.00
        else:
            layout.prop(rd, "display_mode", text="Display")


class Dimensions(RenderButtonsPanel, Panel):
    bl_idname = "yafaray4.render_dimensions"
    bl_label = "Dimensions"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render

        row = layout.row(align=True)
        if bpy.app.version >= (2, 80, 0):
            pass  # FIXME BLENDER 2.80-3.00
        else:
            row.menu("RENDER_MT_presets", text=bpy.types.RENDER_MT_presets.bl_label)
            row.operator("yafaray4.render_presets", text="", icon="ADD" if bpy.app.version >= (2, 80, 0) else "ZOOMIN")
            row.operator("yafaray4.render_presets", text="",
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

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Frame Range:")
        sub.prop(scene, "frame_start", text="Start")
        sub.prop(scene, "frame_end", text="End")
        sub.prop(scene, "frame_step", text="Step")


class Output(RenderButtonsPanel, Panel):
    bl_idname = "yafaray4.render_output"
    bl_label = "Output"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout

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


class PostProcessing(RenderButtonsPanel, Panel):
    bl_idname = "yafaray4.render_post_processing"
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


class ConvertOldSettings(RenderButtonsPanel, Panel):
    bl_idname = "yafaray4.render_convert_old_settings"
    bl_label = "Convert old YafaRay Settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    # noinspection PyUnusedLocal
    def draw(self, context):
        layout = self.layout
        layout.column().operator("yafaray4.data_convert_properties", text="Convert data from 2.4x")


class Advanced(RenderButtonsPanel, Panel):
    bl_idname = "yafaray4.render_advanced"
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


classes = (
    Render,
    Dimensions,
    Output,
    PostProcessing,
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
