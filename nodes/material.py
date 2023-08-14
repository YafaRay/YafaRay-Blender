# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from ..util.properties_annotations import replace_properties_with_annotations
from nodeitems_utils import NodeItem
from .common import NodeCategory
from ..ui.material import blend_one_draw, blend_two_draw, material_from_context


@replace_properties_with_annotations
class MaterialNodeShinyDiffuse(bpy.types.Node):
    bl_idname = "YafaRay4MaterialShinyDiffuse"
    bl_label = "Shiny Diffuse Material"
    brdf_type = bpy.types.Material.brdf_type
    fresnel_effect = bpy.types.Material.fresnel_effect

    def init(self, context):
        self.inputs.new("NodeSocketColor", "Diffuse Color", "DiffCol").default_value = (0.8, 0.8, 0.8, 1)
        self.inputs.new("NodeSocketFloat", "Diffuse Amount", "Diff").default_value = 1
        self.inputs.new("NodeSocketFloat", "Oren-Nayar Sigma", "Sigma").default_value = 0.1
        self.inputs.new("NodeSocketColor", "Mirror Color", "MirrCol").default_value = (1, 1, 1, 1)
        self.inputs.new("NodeSocketFloat", "Mirror Amount", "Mirr").default_value = 0.1
        self.inputs.new("NodeSocketFloat", "IOR Additional Amount", "IOR").default_value = 1.8
        self.inputs.new("NodeSocketFloat", "Transparency Amount", "Transp").default_value = 0
        self.inputs.new("NodeSocketFloat", "Translucency Amount", "Transl").default_value = 0
        self.inputs.new("NodeSocketFloat", "Bump Amount", "Bump").default_value = 0
        self.inputs.new("NodeSocketFloat", "Wireframe Amount", "Wireframe").default_value = 0
        self.outputs.new("NodeSocketShader", "BSDF", "BSDF")
        self.brdf_type = 'lambert'
        self.fresnel_effect = False

    def draw_buttons(self, context, layout):
        layout.prop(self, "brdf_type")
        layout.prop(self, "fresnel_effect")


@replace_properties_with_annotations
class MaterialNodeGlossy(bpy.types.Node):
    bl_idname = "YafaRay4MaterialGlossy"
    bl_label = "Glossy Material"
    brdf_type = bpy.types.Material.brdf_type
    anisotropic = bpy.types.Material.anisotropic
    as_diffuse = bpy.types.Material.as_diffuse

    def init(self, context):
        self.inputs.new("NodeSocketColor", "Diffuse Color", "DiffCol").default_value = (0.8, 0.8, 0.8, 1)
        self.inputs.new("NodeSocketFloat", "Diffuse Amount", "Diff").default_value = 1
        self.inputs.new("NodeSocketFloat", "Oren-Nayar Sigma", "Sigma").default_value = 0.1
        self.inputs.new("NodeSocketColor", "Glossy Color", "GlossyCol").default_value = (1, 1, 1, 1)
        self.inputs.new("NodeSocketFloat", "Glossy Amount", "Glossy").default_value = 0
        self.inputs.new("NodeSocketFloat", "Glossy Exponent", "Exp").default_value = 500
        self.inputs.new("NodeSocketFloat", "Glossy Aniso.Exp.U", "ExpU").default_value = 50
        self.inputs.new("NodeSocketFloat", "Glossy Aniso.Exp.V", "ExpV").default_value = 50
        self.inputs.new("NodeSocketFloat", "Bump Amount", "Bump").default_value = 0
        self.inputs.new("NodeSocketFloat", "Wireframe Amount", "Wireframe").default_value = 0
        self.outputs.new("NodeSocketShader", "BSDF", "BSDF")
        self.brdf_type = 'lambert'
        self.anisotropic = False
        self.as_diffuse = False

    def draw_buttons(self, context, layout):
        layout.prop(self, "brdf_type")
        layout.prop(self, "anisotropic")
        layout.prop(self, "as_diffuse")


@replace_properties_with_annotations
class MaterialNodeCoatedGlossy(bpy.types.Node):
    bl_idname = "YafaRay4MaterialCoatedGlossy"
    bl_label = "Coated Glossy Material"
    brdf_type = bpy.types.Material.brdf_type
    anisotropic = bpy.types.Material.anisotropic
    as_diffuse = bpy.types.Material.as_diffuse

    def init(self, context):
        self.inputs.new("NodeSocketColor", "Diffuse Color", "DiffCol").default_value = (0.8, 0.8, 0.8, 1)
        self.inputs.new("NodeSocketFloat", "Diffuse Amount", "Diff").default_value = 1
        self.inputs.new("NodeSocketFloat", "Oren-Nayar Sigma", "Sigma").default_value = 0.1
        self.inputs.new("NodeSocketColor", "Glossy Color", "GlossyCol").default_value = (1, 1, 1, 1)
        self.inputs.new("NodeSocketFloat", "Glossy Amount", "Glossy").default_value = 0
        self.inputs.new("NodeSocketFloat", "Glossy Exponent", "Exp").default_value = 500
        self.inputs.new("NodeSocketFloat", "Glossy Aniso.Exp.U", "ExpU").default_value = 50
        self.inputs.new("NodeSocketFloat", "Glossy Aniso.Exp.V", "ExpV").default_value = 50
        self.inputs.new("NodeSocketColor", "Mirror Color", "MirrCol").default_value = (1, 1, 1, 1)
        self.inputs.new("NodeSocketFloat", "Mirror Amount", "Mirr").default_value = 0.1
        self.inputs.new("NodeSocketFloat", "IOR Additional Amount", "IOR").default_value = 1.8
        self.inputs.new("NodeSocketFloat", "Bump Amount", "Bump").default_value = 0
        self.inputs.new("NodeSocketFloat", "Wireframe Amount", "Wireframe").default_value = 0
        self.outputs.new("NodeSocketShader", "BSDF", "BSDF")
        self.brdf_type = 'lambert'
        self.anisotropic = False
        self.as_diffuse = False

    def draw_buttons(self, context, layout):
        layout.prop(self, "brdf_type")
        layout.prop(self, "anisotropic")
        layout.prop(self, "as_diffuse")


@replace_properties_with_annotations
class MaterialNodeGlass(bpy.types.Node):
    bl_idname = "YafaRay4MaterialGlass"
    bl_label = "Glass Material"
    absorption_color = bpy.types.Material.absorption
    absorption_dist = bpy.types.Material.absorption_dist
    dispersion_power = bpy.types.Material.dispersion_power
    fake_shadows = bpy.types.Material.fake_shadows

    def init(self, context):
        self.inputs.new("NodeSocketColor", "Filter Color", "FiltCol").default_value = (1, 1, 1, 1)
        self.inputs.new("NodeSocketFloat", "Filter Amount", "Filt").default_value = 1
        self.inputs.new("NodeSocketColor", "Mirror Color", "MirrCol").default_value = (1, 1, 1, 1)
        self.inputs.new("NodeSocketFloat", "Mirror Amount", "Mirr").default_value = 0.1
        self.inputs.new("NodeSocketFloat", "IOR Additional Amount", "IOR").default_value = 1.8
        self.inputs.new("NodeSocketFloat", "Bump Amount", "Bump").default_value = 0
        self.inputs.new("NodeSocketFloat", "Wireframe Amount", "Wireframe").default_value = 0
        self.outputs.new("NodeSocketShader", "BSDF", "BSDF")
        self.absorption_color = (1, 1, 1)
        self.absorption_dist = 1
        self.dispersion_power = 0
        self.fake_shadows = False

    def draw_buttons(self, context, layout):
        layout.prop(self, "absorption_color")
        layout.prop(self, "absorption_dist")
        layout.prop(self, "dispersion_power")
        layout.prop(self, "fake_shadows")


@replace_properties_with_annotations
class MaterialNodeRoughGlass(bpy.types.Node):
    bl_idname = "YafaRay4MaterialRoughGlass"
    bl_label = "Rough Glass Material"
    absorption_color = bpy.types.Material.absorption
    absorption_dist = bpy.types.Material.absorption_dist
    dispersion_power = bpy.types.Material.dispersion_power
    fake_shadows = bpy.types.Material.fake_shadows

    def init(self, context):
        self.inputs.new("NodeSocketColor", "Filter Color", "FiltCol").default_value = (1, 1, 1, 1)
        self.inputs.new("NodeSocketFloat", "Filter Amount", "Filt").default_value = 1
        self.inputs.new("NodeSocketColor", "Mirror Color", "MirrCol").default_value = (1, 1, 1, 1)
        self.inputs.new("NodeSocketFloat", "Mirror Amount", "Mirr").default_value = 0.1
        self.inputs.new("NodeSocketFloat", "IOR Additional Amount", "IOR").default_value = 1.8
        self.inputs.new("NodeSocketFloat", "Roughness Exponent", "Roughness").default_value = 0.2
        self.inputs.new("NodeSocketFloat", "Bump Amount", "Bump").default_value = 0
        self.inputs.new("NodeSocketFloat", "Wireframe Amount", "Wireframe").default_value = 0
        self.outputs.new("NodeSocketShader", "BSDF", "BSDF")
        self.absorption_color = (1, 1, 1)
        self.absorption_dist = 1
        self.dispersion_power = 0
        self.fake_shadows = False

    def draw_buttons(self, context, layout):
        layout.prop(self, "absorption_color")
        layout.prop(self, "absorption_dist")
        layout.prop(self, "dispersion_power")
        layout.prop(self, "fake_shadows")


@replace_properties_with_annotations
class MaterialNodeBlend(bpy.types.Node):
    bl_idname = "YafaRay4MaterialBlend"
    bl_label = "Blend Material"
    material1name = bpy.types.Material.material1name
    material2name = bpy.types.Material.material2name

    def init(self, context):
        self.inputs.new("NodeSocketFloat", "Blend Amount", "Blend").default_value = 0.5
        self.outputs.new("NodeSocketShader", "BSDF", "BSDF")

    def draw_buttons(self, context, layout):
        box = layout.box()
        box.label(text="Choose the two materials you wish to blend.")
        blend_one_draw(layout, self)
        blend_two_draw(layout, self)


classes = (
    MaterialNodeShinyDiffuse,
    MaterialNodeGlossy,
    MaterialNodeCoatedGlossy,
    MaterialNodeGlass,
    MaterialNodeRoughGlass,
    MaterialNodeBlend
)


def register(node_categories):
    from bpy.utils import register_class
    node_categories_items = []
    for cls in classes:
        register_class(cls)
        node_categories_items.append(NodeItem(cls.bl_idname))
    node_categories.append(NodeCategory("YAFARAY4_MATERIAL", "YafaRay Material", items=node_categories_items))


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
