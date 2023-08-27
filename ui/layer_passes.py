# SPDX-License-Identifier: GPL-2.0-or-later

import bpy

if bpy.app.version >= (2, 80, 0):
    from bl_ui.properties_view_layer import ViewLayerButtonsPanel


    class LayersPanel(ViewLayerButtonsPanel):
        pass
else:
    # noinspection PyUnresolvedReferences
    from bl_ui.properties_render_layer import RenderLayerButtonsPanel


    class LayersPanel(RenderLayerButtonsPanel):
        pass

# noinspection PyUnresolvedReferences
from bpy.types import Panel


class Layers(LayersPanel, Panel):
    bl_idname = "YAFARAY4_PT_layers"
    bl_label = "Layers"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    #    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render

        row = layout.row()
        row.template_list("RENDERLAYER_UL_renderlayers", "", rd, "layers", rd.layers, "active_index", rows=2)
        col = row.column(align=True)
        col.operator("scene.render_layer_add", icon="ADD" if bpy.app.version >= (2, 80, 0) else "ZOOMIN", text="")
        col.operator("scene.render_layer_remove",
                     icon="REMOVE" if bpy.app.version >= (2, 80, 0) else "ZOOMOUT", text="")

        row = layout.row()
        # noinspection PyUnresolvedReferences
        view_layer = context.scene.render.layers.active

        row.prop(view_layer, "name")
        row.prop(rd, "use_single_layer", text="", icon_only=True)

        split = layout.split()

        col = split.column()
        col.prop(scene, "layers", text="Scene")
        # TODO: Implement material override
        # col.prop(rl, "material_override", text="Material")

        # noinspection PyUnusedLocal
        col = split.column()
        # TODO: Implement render layers
        # col.prop(rl, "layers", text="Layer")


class LayerPasses(LayersPanel, Panel):
    bl_idname = "YAFARAY4_PT_layer_passes"
    bl_label = "Render Passes"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw_header(self, context):
        scene = context.scene
        self.layout.prop(scene.yafaray4.passes, "pass_enable", text="")

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        if bpy.app.version >= (2, 80, 0):
            view_layer = context.view_layer
        else:
            # noinspection PyUnresolvedReferences
            view_layer = context.scene.render.layers.active

        if scene.yafaray4.passes.pass_enable:
            layout.row()  # (align=True)
            row = layout.row()  # (align=True)
            row.prop(view_layer, "use_pass_z")  # , "Z-depth")
            if view_layer.use_pass_z:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_depth", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_vector")
            if view_layer.use_pass_vector:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_vector", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_normal")
            if view_layer.use_pass_normal:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_normal", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_uv")
            if view_layer.use_pass_uv:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_uv", text="")

            if bpy.app.version < (2, 80, 0):
                row = layout.row()
                row.prop(view_layer, "use_pass_color")
                if view_layer.use_pass_color:
                    sub = row.column(align=True)
                    sub.prop(scene.yafaray4.passes, "pass_color", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_emit")
            if view_layer.use_pass_emit:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_emit", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_mist")
            if view_layer.use_pass_mist:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_mist", text="")

            if bpy.app.version < (2, 80, 0):
                row = layout.row()
                row.prop(view_layer, "use_pass_diffuse")
                if view_layer.use_pass_diffuse:
                    sub = row.column(align=True)
                    sub.prop(scene.yafaray4.passes, "pass_diffuse", text="")

                row = layout.row()
                row.prop(view_layer, "use_pass_specular")
                if view_layer.use_pass_specular:
                    sub = row.column(align=True)
                    sub.prop(scene.yafaray4.passes, "pass_spec", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_ambient_occlusion")
            if view_layer.use_pass_ambient_occlusion:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_ao", text="")
                row = layout.row()
                col = row.column()
                col.prop(scene, "intg_AO_color")
                col.prop(scene, "intg_AO_samples")
                col.prop(scene, "intg_AO_distance")

            row = layout.row()
            row.prop(view_layer, "use_pass_environment")
            if view_layer.use_pass_environment:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_env", text="")

            if bpy.app.version < (2, 80, 0):
                row = layout.row()
                row.prop(view_layer, "use_pass_indirect")
                if view_layer.use_pass_indirect:
                    sub = row.column(align=True)
                    sub.prop(scene.yafaray4.passes, "pass_indirect", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_shadow")
            if view_layer.use_pass_shadow:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_shadow", text="")

            if bpy.app.version < (2, 80, 0):
                row = layout.row()
                row.prop(view_layer, "use_pass_reflection")
                if view_layer.use_pass_reflection:
                    sub = row.column(align=True)
                    sub.prop(scene.yafaray4.passes, "pass_reflect", text="")

                row = layout.row()
                row.prop(view_layer, "use_pass_refraction")
                if view_layer.use_pass_refraction:
                    sub = row.column(align=True)
                    sub.prop(scene.yafaray4.passes, "pass_refract", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_object_index")
            if view_layer.use_pass_object_index:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_index_ob", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_material_index")
            if view_layer.use_pass_material_index:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_index_ma", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_diffuse_direct")
            if view_layer.use_pass_diffuse_direct:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_diff_dir", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_diffuse_indirect")
            if view_layer.use_pass_diffuse_indirect:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_diff_ind", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_diffuse_color")
            if view_layer.use_pass_diffuse_color:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_diff_col", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_glossy_direct")
            if view_layer.use_pass_glossy_direct:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_gloss_dir", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_glossy_indirect")
            if view_layer.use_pass_glossy_indirect:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_gloss_ind", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_glossy_color")
            if view_layer.use_pass_glossy_color:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_gloss_col", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_transmission_direct")
            if view_layer.use_pass_transmission_direct:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_trans_dir", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_transmission_indirect")
            if view_layer.use_pass_transmission_indirect:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_trans_ind", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_transmission_color")
            if view_layer.use_pass_transmission_color:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_trans_col", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_subsurface_direct")
            if view_layer.use_pass_subsurface_direct:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_subsurface_dir", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_subsurface_indirect")
            if view_layer.use_pass_subsurface_indirect:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_subsurface_ind", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_subsurface_color")
            if view_layer.use_pass_subsurface_color:
                sub = row.column(align=True)
                sub.prop(scene.yafaray4.passes, "pass_subsurface_col", text="")

            box = layout.box()
            box.label(text="Masking Passes settings:")

            row = box.row()
            row.prop(scene.yafaray4.passes, "pass_mask_obj_index")
            sub = row.column(align=True)
            sub.prop(scene.yafaray4.passes, "pass_mask_mat_index")

            row = box.row()
            row.prop(scene.yafaray4.passes, "pass_mask_invert")
            sub = row.column(align=True)
            sub.prop(scene.yafaray4.passes, "pass_mask_only")

            box = layout.box()
            box.label(text="Toon and Object Edge Passes settings:")

            row = box.row()
            row.prop(scene.yafaray4.passes, "object_edge_thickness")
            sub = row.column(align=True)
            sub.prop(scene.yafaray4.passes, "toon_edge_color", text="")
            sub = row.column(align=True)
            sub.prop(scene.yafaray4.passes, "object_edge_smoothness")
            sub = row.column(align=True)
            sub.prop(scene.yafaray4.passes, "object_edge_threshold")

            row = box.row()
            row.prop(scene.yafaray4.passes, "toon_pre_smooth")
            sub = row.column(align=True)
            sub.prop(scene.yafaray4.passes, "toon_quantization")
            sub = row.column(align=True)
            sub.prop(scene.yafaray4.passes, "toon_post_smooth")

            box = layout.box()
            box.label(text="Faces Edge Pass settings:")

            row = box.row()
            row.prop(scene.yafaray4.passes, "faces_edge_thickness")
            sub = row.column(align=True)
            sub.prop(scene.yafaray4.passes, "faces_edge_smoothness")
            sub = row.column(align=True)
            sub.prop(scene.yafaray4.passes, "faces_edge_threshold")


classes = (
    LayerPasses,
)

if bpy.app.version < (2, 80, 0):
    classes = (Layers, ) + classes


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
