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

        if bpy.app.version >= (2, 80, 0):
            row = layout.row() # FIXME BLENDER >= v2.80
        else:
            row = layout.row()
            row.template_list("RENDERLAYER_UL_renderlayers", "", rd, "layers", rd.layers, "active_index", rows=2)

        col = row.column(align=True)
        col.operator("scene.render_layer_add", icon="ADD" if bpy.app.version >= (2, 80, 0) else "ZOOMIN", text="")
        col.operator("scene.render_layer_remove",
                     icon="REMOVE" if bpy.app.version >= (2, 80, 0) else "ZOOMOUT", text="")

        row = layout.row()
        if bpy.app.version >= (2, 80, 0):
            view_layer = context.view_layer
        else:
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
        self.layout.prop(scene.yafaray.passes, "pass_enable", text="")

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        if bpy.app.version >= (2, 80, 0):
            view_layer = context.view_layer
        else:
            # noinspection PyUnresolvedReferences
            view_layer = context.scene.render.layers.active

        if scene.yafaray.passes.pass_enable:
            layout.row()  # (align=True)
            row = layout.row()  # (align=True)
            row.prop(view_layer, "use_pass_z")  # , "Z-depth")
            if view_layer.use_pass_z:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_Depth", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_vector")
            if view_layer.use_pass_vector:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_Vector", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_normal")
            if view_layer.use_pass_normal:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_Normal", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_uv")
            if view_layer.use_pass_uv:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_UV", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_color")
            if view_layer.use_pass_color:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_Color", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_emit")
            if view_layer.use_pass_emit:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_Emit", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_mist")
            if view_layer.use_pass_mist:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_Mist", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_diffuse")
            if view_layer.use_pass_diffuse:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_Diffuse", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_specular")
            if view_layer.use_pass_specular:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_Spec", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_ambient_occlusion")
            if view_layer.use_pass_ambient_occlusion:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_AO", text="")
                row = layout.row()
                col = row.column()
                col.prop(scene, "intg_AO_color")
                col.prop(scene, "intg_AO_samples")
                col.prop(scene, "intg_AO_distance")

            row = layout.row()
            row.prop(view_layer, "use_pass_environment")
            if view_layer.use_pass_environment:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_Env", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_indirect")
            if view_layer.use_pass_indirect:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_Indirect", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_shadow")
            if view_layer.use_pass_shadow:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_Shadow", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_reflection")
            if view_layer.use_pass_reflection:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_Reflect", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_refraction")
            if view_layer.use_pass_refraction:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_Refract", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_object_index")
            if view_layer.use_pass_object_index:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_IndexOB", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_material_index")
            if view_layer.use_pass_material_index:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_IndexMA", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_diffuse_direct")
            if view_layer.use_pass_diffuse_direct:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_DiffDir", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_diffuse_indirect")
            if view_layer.use_pass_diffuse_indirect:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_DiffInd", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_diffuse_color")
            if view_layer.use_pass_diffuse_color:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_DiffCol", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_glossy_direct")
            if view_layer.use_pass_glossy_direct:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_GlossDir", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_glossy_indirect")
            if view_layer.use_pass_glossy_indirect:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_GlossInd", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_glossy_color")
            if view_layer.use_pass_glossy_color:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_GlossCol", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_transmission_direct")
            if view_layer.use_pass_transmission_direct:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_TransDir", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_transmission_indirect")
            if view_layer.use_pass_transmission_indirect:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_TransInd", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_transmission_color")
            if view_layer.use_pass_transmission_color:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_TransCol", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_subsurface_direct")
            if view_layer.use_pass_subsurface_direct:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_SubsurfaceDir", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_subsurface_indirect")
            if view_layer.use_pass_subsurface_indirect:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_SubsurfaceInd", text="")

            row = layout.row()
            row.prop(view_layer, "use_pass_subsurface_color")
            if view_layer.use_pass_subsurface_color:
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_SubsurfaceCol", text="")

            box = layout.box()
            box.label(text="Masking Passes settings:")

            row = box.row()
            row.prop(scene.yafaray.passes, "pass_mask_obj_index")
            sub = row.column(align=True)
            sub.prop(scene.yafaray.passes, "pass_mask_mat_index")

            row = box.row()
            row.prop(scene.yafaray.passes, "pass_mask_invert")
            sub = row.column(align=True)
            sub.prop(scene.yafaray.passes, "pass_mask_only")

            box = layout.box()
            box.label(text="Toon and Object Edge Passes settings:")

            row = box.row()
            row.prop(scene.yafaray.passes, "objectEdgeThickness")
            sub = row.column(align=True)
            sub.prop(scene.yafaray.passes, "toonEdgeColor", text="")
            sub = row.column(align=True)
            sub.prop(scene.yafaray.passes, "objectEdgeSmoothness")
            sub = row.column(align=True)
            sub.prop(scene.yafaray.passes, "objectEdgeThreshold")

            row = box.row()
            row.prop(scene.yafaray.passes, "toonPreSmooth")
            sub = row.column(align=True)
            sub.prop(scene.yafaray.passes, "toonQuantization")
            sub = row.column(align=True)
            sub.prop(scene.yafaray.passes, "toonPostSmooth")

            box = layout.box()
            box.label(text="Faces Edge Pass settings:")

            row = box.row()
            row.prop(scene.yafaray.passes, "facesEdgeThickness")
            sub = row.column(align=True)
            sub.prop(scene.yafaray.passes, "facesEdgeSmoothness")
            sub = row.column(align=True)
            sub.prop(scene.yafaray.passes, "facesEdgeThreshold")


class Views(LayersPanel, Panel):
    bl_idname = "YAFARAY4_PT_views"
    bl_label = "Views"
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

            if basic_stereo:
                row = layout.row()
                row.template_list("RENDERLAYER_UL_renderviews", "name", rd, "stereo_views", rd.views, "active_index",
                                  rows=2)

                row = layout.row()
                row.label(text="File Suffix:")
                row.prop(rv, "file_suffix", text="")

            else:
                row = layout.row()
                row.template_list("RENDERLAYER_UL_renderviews", "name", rd, "views", rd.views, "active_index", rows=2)

                col = row.column(align=True)
                col.operator("scene.render_view_add", icon="ADD" if bpy.app.version >= (2, 80, 0) else "ZOOMIN",
                             text="")
                col.operator("scene.render_view_remove", icon="REMOVE" if bpy.app.version >= (2, 80, 0) else "ZOOMOUT",
                             text="")

                row = layout.row()
                row.label(text="Camera Suffix:")
                row.prop(rv, "camera_suffix", text="")


classes = (
    Layers,
    LayerPasses,
    Views,
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
