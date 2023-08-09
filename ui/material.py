# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bl_ui.properties_material import MaterialButtonsPanel
# noinspection PyUnresolvedReferences
from bpy.types import Panel, Menu

if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed, 
    # before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the 
    # "libyafaray4_bindings" compiled module is installed on. Assuming that the YafaRay-Plugin exporter is installed 
    # in a folder named "yafaray4" within the addons Blender directory
    # noinspection PyUnresolvedReferences
    from yafaray4.ui.ior_values import ior_list
    # noinspection PyUnresolvedReferences
    import yafaray4.prop.material

    yafaray4.prop.material.register()
    # noinspection PyUnresolvedReferences
    import yafaray4.prop.texture

    yafaray4.prop.texture.register()
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
else:
    from .ior_values import ior_list


def ui_split(ui_item, factor):
    if bpy.app.version >= (2, 80, 0):
        return ui_item.split(factor=factor)
    else:
        return ui_item.split(percentage=factor)


def material_from_context(context):
    if bpy.app.version >= (2, 80, 0):
        return context.material
    else:
        # noinspection PyUnresolvedReferences
        from bl_ui.properties_material import active_node_mat
        return active_node_mat(context.material)


def material_check(material):
    if bpy.app.version >= (2, 80, 0):
        return material
    else:
        # noinspection PyUnresolvedReferences
        from bl_ui.properties_material import check_material
        return check_material(material)


def blend_one_draw(layout, mat):
    # noinspection PyBroadException
    try:
        layout.prop_search(mat, "material1name", bpy.data, "materials")
    except Exception:
        return False

    return True


def blend_two_draw(layout, mat):
    # noinspection PyBroadException
    try:
        layout.prop_search(mat, "material2name", bpy.data, "materials")
    except Exception:
        return False
    return True


class Type(MaterialButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_material_type"
    bl_label = ""
    bl_options = {'HIDE_HEADER'}
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):
        yaf_mat = context.material
        engine = context.scene.render.engine
        return material_check(yaf_mat) and (yaf_mat.mat_type in cls.material_type) and (engine in cls.COMPAT_ENGINES)


def find_node(material, node_type):
    if material and material.yafaray_nodes:
        node_tree = material.yafaray_nodes
        active_output_node = None
        for tree_node in node_tree.nodes:
            if getattr(tree_node, "bl_idname", None).startswith(node_type):
                #if getattr(tree_node, "is_active_output", True):
                #    return tree_node
                if not active_output_node:
                    active_output_node = tree_node
        return active_output_node
    return None


def find_node_input(node, name):
    for node_input in node.inputs:
        if node_input.name == name:
            return node_input
    return None


class ContextMaterial(MaterialButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_material_context"
    bl_label = ""
    bl_options = {'HIDE_HEADER'}
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):
        # An exception, don't call the parent poll func because
        # this manages materials for all engine types
        engine = context.scene.render.engine
        return (context.material or context.object) and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        yaf_mat = context.material
        ob = context.object
        slot = context.material_slot
        space = context.space_data

        if ob:
            row = layout.row()
            row.template_list("MATERIAL_UL_matslots", "", ob, "material_slots", ob, "active_material_index", rows=2)

            col = row.column(align=True)
            col.operator("object.material_slot_add", icon="ADD" if bpy.app.version >= (2, 80, 0) else "ZOOMIN", text="")
            col.operator("object.material_slot_remove", icon="REMOVE" if bpy.app.version >= (2, 80, 0) else "ZOOMOUT",
                         text="")

            # TODO: code own operators to copy yaf material settings...
            # FIXME BLENDER >= v2.80 # col.menu("MATERIAL_MT_specials", icon='DOWNARROW_HLT', text="")

            if ob.mode == 'EDIT':
                row = layout.row(align=True)
                row.operator("object.material_slot_assign", text="Assign")
                row.operator("object.material_slot_select", text="Select")
                row.operator("object.material_slot_deselect", text="Deselect")

        split = ui_split(layout, 0.75)

        if ob:
            split.template_ID(ob, "active_material", new="material.new")
            row = split.row()
            if slot:
                row.prop(slot, "link", text="")
            else:
                row.label()

        elif yaf_mat:
            split.template_ID(space, "pin_id")
            split.separator()

        if yaf_mat:
            layout.separator()
            layout.row().prop(yaf_mat, "clay_exclude")
            layout.prop(yaf_mat, "use_nodes", icon='NODETREE')
            layout.separator()
            if not yaf_mat.use_nodes:
                layout.prop(yaf_mat, "mat_type")
            else:
                # layout.prop(yaf_mat, "diffuse_color", text="Viewport color (not used for rendering)")
                layout.template_ID(yaf_mat, "yafaray_nodes", new="yafaray4.new_node_tree")
                op = layout.operator("yafaray4.show_node_tree_window")
                op.node_tree_name = yaf_mat.yafaray_nodes.name
                node_tree = yaf_mat.yafaray_nodes
                node = find_node(yaf_mat, 'YafaRay4Material')
                if not node:
                    layout.label(text="No material node")
                    layout.label(text="Show the Node Editor and add a Material Node, "
                                      "optionally connected to Texture Nodes", icon='INFO')
                else:
                    pass
                    # FIXME BLENDER >= v2.80
                    # default node view panel hardcoded in Blender and unreliable, not working at all in 2.80+
                    # layout.template_node_view(node_tree, node, None)
        layout.separator()


class Preview(MaterialButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_material_preview"
    bl_label = "Preview"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        self.layout.template_preview(context.material)


class PreviewControls(MaterialButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_material_preview_controls"
    bl_label = "Preview Controls"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    # bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.prop(context.scene.yafaray.preview, "enable", text="")

    def draw(self, context):
        if context.scene.yafaray.preview.enable:
            layout = self.layout
            split = layout.split()
            col = split.column()
            col.label(text="Preview dynamic rotation/zoom")
            split = layout.split()
            col = split.column()
            col.prop(context.scene.yafaray.preview, "camRot", text="")
            col = split.column()
            row = col.row()
            row.operator("yafaray4.material_preview_camera_zoom_out", text='Zoom Out', icon='ZOOM_OUT')
            col2 = row.column()
            col2.operator("yafaray4.material_preview_camera_zoom_in", text='Zoom In', icon='ZOOM_IN')
            row = col.row()
            row.label(text="")
            row = col.row()
            row.operator("yafaray4.material_preview_camera_rotation_reset", text='Reset dynamic rotation/zoom')
            split = layout.split()
            col = split.column()
            col.label(text="Preview object control")
            split = layout.split()
            col = split.column()
            col.prop(context.scene.yafaray.preview, "objScale", text="Scale")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "rotZ", text="Z Rotation")
            col = split.column()
            col.prop_search(context.scene.yafaray.preview, "previewObject", bpy.data, "objects", text="")
            split = layout.split()
            col = split.column()
            col.label(text="Preview lights control")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "lightRotZ", text="lights Z Rotation")
            split = layout.split()
            col = split.column()
            col.label(text="Key light:")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "keyLightPowerFactor", text="Power factor")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "keyLightColor", text="")
            split = layout.split()
            col = split.column()
            col.label(text="Fill lights:")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "fillLightPowerFactor", text="Power factor")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "fillLightColor", text="")
            split = layout.split()
            col = split.column()
            col.label(text="Preview scene control")
            split = layout.split()
            col = split.column()
            col.prop(context.scene.yafaray.preview, "previewRayDepth", text="Ray Depth")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "previewAApasses", text="AA samples")
            col = split.column()
            col.prop(context.scene.yafaray.preview, "previewBackground", text="")


def draw_generator(ior):
    # noinspection PyUnusedLocal
    def draw(self, context):
        sl = self.layout
        for values in ior:
            ior_name, ior_index = values
            props = sl.operator('yafaray4.material_preset_ior_list', text=ior_name)
            # two values given to ior preset operator
            props.index = ior_index
            props.name = ior_name

    return draw


submenus = []

for ior_group, ior_n in ior_list:
    submenu_idname = 'YAFARAY4_MT_presets_ior_list_cat%d' % len(submenus)
    submenu = type(
        submenu_idname,
        (Menu,),
        {
            'bl_idname': submenu_idname,
            'bl_label': ior_group,
            'draw': draw_generator(ior_n)
        }
    )
    bpy.utils.register_class(submenu)
    submenus.append(submenu)


class PresetsIorList(Menu):
    bl_idname = "YAFARAY4_MT_presets_ior_list"
    bl_label = "Glass"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    # noinspection PyUnusedLocal
    def draw(self, context):
        sl = self.layout
        for sm in submenus:
            sl.menu(sm.bl_idname)


class TypeShinyDiffuse(Type):
    bl_idname = "YAFARAY4_PT_material_shiny_diffuse_diffuse"
    bl_label = "Diffuse reflection"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    material_type = 'shinydiffusemat'

    def draw(self, context):
        if not context.material.use_nodes:
            layout = self.layout
            yaf_mat = material_from_context(context)

            split = layout.split()
            col = split.column()
            col.prop(yaf_mat, "diffuse_color")
            col.prop(yaf_mat, "emit")
            layout.row().prop(yaf_mat, "diffuse_reflect", slider=True)

            col = split.column()
            sub = col.column()
            sub.label(text="Reflectance model:")
            sub.prop(yaf_mat, "brdf_type", text="")
            brdf = sub.column()
            brdf.enabled = yaf_mat.brdf_type == "oren-nayar"
            brdf.prop(yaf_mat, "sigma")

            layout.separator()

            box = layout.box()
            box.label(text="Transparency and translucency:")
            split = box.split()
            col = split.column()
            col.prop(yaf_mat, "transparency", slider=True)
            col = split.column()
            col.prop(yaf_mat, "translucency", slider=True)
            box.row().prop(yaf_mat, "transmit_filter", slider=True)


class TypeShinyDiffuseSpecular(Type):
    bl_idname = "YAFARAY4_PT_material_shiny_diffuse_specular"
    bl_label = "Specular reflection"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    material_type = 'shinydiffusemat'

    def draw(self, context):
        if not context.material.use_nodes:
            layout = self.layout
            yaf_mat = material_from_context(context)

            split = layout.split()
            col = split.column()
            col.label(text="Mirror color:")
            col.prop(yaf_mat, "mirror_color", text="")

            col = split.column()
            col.prop(yaf_mat, "fresnel_effect")
            sub = col.column()
            sub.enabled = yaf_mat.fresnel_effect
            sub.prop(yaf_mat, "IOR_reflection", slider=True)
            layout.row().prop(yaf_mat, "specular_reflect", slider=True)


class TypeGlossyDiffuse(Type):
    bl_idname = "YAFARAY4_PT_material_glossy_diffuse"
    bl_label = "Diffuse reflection"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    material_type = 'glossy', 'coated_glossy'

    def draw(self, context):
        if not context.material.use_nodes:
            layout = self.layout
            yaf_mat = material_from_context(context)

            split = layout.split()
            col = split.column()
            col.prop(yaf_mat, "diffuse_color")

            col = split.column()
            ref = col.column(align=True)
            ref.label(text="Reflectance model:")
            ref.prop(yaf_mat, "brdf_type", text="")
            sig = col.column()
            sig.enabled = yaf_mat.brdf_type == "oren-nayar"
            sig.prop(yaf_mat, "sigma")
            layout.row().prop(yaf_mat, "diffuse_reflect", slider=True)


class TypeGlossySpecular(Type):
    bl_idname = "YAFARAY4_PT_material_glossy_specular"
    bl_label = "Specular reflection"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    material_type = 'glossy', 'coated_glossy'

    def draw(self, context):
        if not context.material.use_nodes:
            layout = self.layout
            yaf_mat = material_from_context(context)

            split = layout.split()
            col = split.column()
            col.prop(yaf_mat, "glossy_color")
            exp = col.column()
            exp.enabled = yaf_mat.anisotropic is False
            exp.prop(yaf_mat, "exponent")

            col = split.column()
            sub = col.column(align=True)
            sub.prop(yaf_mat, "anisotropic")
            ani = sub.column()
            ani.enabled = yaf_mat.anisotropic is True
            ani.prop(yaf_mat, "exp_u")
            ani.prop(yaf_mat, "exp_v")
            layout.row().prop(yaf_mat, "glossy_reflect", slider=True)
            layout.row().prop(yaf_mat, "as_diffuse")

            layout.separator()

            if yaf_mat.mat_type == "coated_glossy":
                box = layout.box()
                box.label(text="Coated layer for glossy:")
                split = box.split()
                col = split.column()
                col.prop(yaf_mat, "coat_mir_col")
                col = split.column(align=True)
                col.label(text="Fresnel reflection:")
                col.prop(yaf_mat, "IOR_reflection")
                col.label()
                layout.row().prop(yaf_mat, "specular_reflect", slider=True)


class TypeGlassReal(Type):
    bl_idname = "YAFARAY4_PT_material_glass_real"
    bl_label = "Real glass settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    material_type = 'glass', 'rough_glass'

    def draw(self, context):
        if not context.material.use_nodes:
            layout = self.layout
            yaf_mat = material_from_context(context)

            layout.label(text="Refraction and Reflections:")
            split = layout.split()
            col = split.column()
            col.prop(yaf_mat, "IOR_refraction")

            col = split.column()
            col.menu("YAFARAY4_MT_presets_ior_list", text=bpy.types.YAFARAY4_MT_presets_ior_list.bl_label)

            split = layout.split()
            col = split.column(align=True)
            col.prop(yaf_mat, "absorption")
            col.prop(yaf_mat, "absorption_dist")

            col = split.column(align=True)
            col.label(text="Dispersion:")
            col.prop(yaf_mat, "dispersion_power")

            if yaf_mat.mat_type == "rough_glass":
                box = layout.box()
                box.label(text="Glass roughness:")
                box.row().prop(yaf_mat, "refr_roughness", slider=True)


class TypeGlassFake(Type):
    bl_idname = "YAFARAY4_PT_material_glass_fake"
    bl_label = "Fake glass settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    material_type = 'glass', 'rough_glass'

    def draw(self, context):
        if not context.material.use_nodes:
            layout = self.layout
            yaf_mat = material_from_context(context)

            split = layout.split()
            col = split.column()
            col.prop(yaf_mat, "filter_color")
            col = split.column()
            col.prop(yaf_mat, "glass_mir_col")
            layout.row().prop(yaf_mat, "glass_transmit", slider=True)
            layout.row().prop(yaf_mat, "fake_shadows")


class TypeBlend(Type):
    bl_idname = "YAFARAY4_PT_material_blend"
    bl_label = "Blend material settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    material_type = 'blend'

    def draw(self, context):
        if not context.material.use_nodes:
            layout = self.layout
            yaf_mat = material_from_context(context)

            split = layout.split()
            col = split.column()
            col.label(text="")
            col.prop(yaf_mat, "blend_value", slider=True)

            layout.separator()

            box = layout.box()
            box.label(text="Choose the two materials you wish to blend.")

            blend_one_draw(layout, yaf_mat)
            blend_two_draw(layout, yaf_mat)


class Wireframe(MaterialButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_material_wireframe"
    bl_label = "Wireframe shading options"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        yaf_mat = material_from_context(context)

        split = layout.split()
        col = split.column()
        col.prop(yaf_mat, "wireframe_amount", slider=True, text="Amount")
        col.prop(yaf_mat, "wireframe_color", text="")
        col = split.column()
        col.prop(yaf_mat, "wireframe_thickness", slider=True, text="Thickness")
        col.prop(yaf_mat, "wireframe_exponent", slider=True, text="Softness")


class Advanced(MaterialButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_material_advanced"
    bl_label = "Advanced settings"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        yaf_mat = material_from_context(context)

        layout.prop(yaf_mat, "pass_index")

        split = layout.split()
        split.column()
        layout.row().prop(yaf_mat, "visibility")

        split = layout.split()
        split.column()
        layout.row().prop(yaf_mat, "receive_shadows")

        if yaf_mat.mat_type == "shinydiffusemat":
            split = layout.split()
            split.column()
            layout.row().prop(yaf_mat, "flat_material")
            split = layout.split()
            split.column()
            row = layout.row()
            row.prop(yaf_mat, "transparentbias_factor")
            col = row.column()
            col.prop(yaf_mat, "transparentbias_multiply_raydepth")

        if yaf_mat.mat_type != "blend":
            split = layout.split()
            split.column()
            layout.row().prop(yaf_mat, "additionaldepth")

        split = layout.split()
        split.column()
        layout.row().prop(yaf_mat, "samplingfactor")


classes = (
    ContextMaterial,
    Preview,
    PreviewControls,
    PresetsIorList,
    TypeShinyDiffuse,
    TypeShinyDiffuseSpecular,
    TypeGlossyDiffuse,
    TypeGlossySpecular,
    TypeGlassReal,
    TypeGlassFake,
    TypeBlend,
    Wireframe,
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
