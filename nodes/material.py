# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from ..util.properties_annotations import replace_properties_with_annotations
from nodeitems_utils import NodeItem
from .common import NodeCategory
from ..ui.material import blend_one_draw, blend_two_draw, material_from_context


@replace_properties_with_annotations
class MaterialNodeShinyDiffuse(bpy.types.Node):
    bl_idname = "YafaRay4MaterialShinyDiffuse"
    bl_label = "YafaRay Shiny Diffuse Material"
    yaf_type = "OUTPUT_MATERIAL"
    brdf_type = bpy.types.Material.brdf_type
    fresnel_effect = bpy.types.Material.fresnel_effect

    def init(self, context):
        self.inputs.new(type="NodeSocketColor", name="Diffuse Color", identifier="DiffCol").default_value = (0.8, 0.8, 0.8, 1)
        self.inputs.new(type="NodeSocketFloat", name="Diffuse Amount", identifier="Diff").default_value = 1
        self.inputs.new(type="NodeSocketFloat", name="Oren-Nayar Sigma", identifier="Sigma").default_value = 0.1
        self.inputs.new(type="NodeSocketColor", name="Mirror Color", identifier="MirrCol").default_value = (1, 1, 1, 1)
        self.inputs.new(type="NodeSocketFloat", name="Mirror Amount", identifier="Mirr").default_value = 0.1
        self.inputs.new(type="NodeSocketFloat", name="IOR Additional Amount", identifier="IOR").default_value = 1.8
        self.inputs.new(type="NodeSocketFloat", name="Transparency Amount", identifier="Transp").default_value = 0
        self.inputs.new(type="NodeSocketFloat", name="Translucency Amount", identifier="Transl").default_value = 0
        self.inputs.new(type="NodeSocketFloat", name="Bump Amount", identifier="Bump").default_value = 0
        self.inputs.new(type="NodeSocketFloat", name="Wireframe Amount", identifier="Wireframe").default_value = 0
        self.outputs.new(type="NodeSocketShader", name="BSDF", identifier="BSDF")
        self.brdf_type = 'lambert'
        self.fresnel_effect = False

    def draw_buttons(self, context, layout):
        layout.prop(self, "brdf_type")
        layout.prop(self, "fresnel_effect")


@replace_properties_with_annotations
class MaterialNodeGlossy(bpy.types.Node):
    bl_idname = "YafaRay4MaterialGlossy"
    bl_label = "YafaRay Glossy Material"
    yaf_type = "OUTPUT_MATERIAL"
    brdf_type = bpy.types.Material.brdf_type
    anisotropic = bpy.types.Material.anisotropic
    as_diffuse = bpy.types.Material.as_diffuse

    def init(self, context):
        self.inputs.new(type="NodeSocketColor", name="Diffuse Color", identifier="DiffCol").default_value = (0.8, 0.8, 0.8, 1)
        self.inputs.new(type="NodeSocketFloat", name="Diffuse Amount", identifier="Diff").default_value = 1
        self.inputs.new(type="NodeSocketFloat", name="Oren-Nayar Sigma", identifier="Sigma").default_value = 0.1
        self.inputs.new(type="NodeSocketColor", name="Glossy Color", identifier="GlossyCol").default_value = (1, 1, 1, 1)
        self.inputs.new(type="NodeSocketFloat", name="Glossy Amount", identifier="Glossy").default_value = 0
        self.inputs.new(type="NodeSocketFloat", name="Glossy Exponent", identifier="Exp").default_value = 500
        self.inputs.new(type="NodeSocketFloat", name="Glossy Aniso.Exp.U", identifier="ExpU").default_value = 50
        self.inputs.new(type="NodeSocketFloat", name="Glossy Aniso.Exp.V", identifier="ExpV").default_value = 50
        self.inputs.new(type="NodeSocketFloat", name="Bump Amount", identifier="Bump").default_value = 0
        self.inputs.new(type="NodeSocketFloat", name="Wireframe Amount", identifier="Wireframe").default_value = 0
        self.outputs.new(type="NodeSocketShader", name="BSDF", identifier="BSDF")
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
    bl_label = "YafaRay Coated Glossy Material"
    yaf_type = "OUTPUT_MATERIAL"
    brdf_type = bpy.types.Material.brdf_type
    anisotropic = bpy.types.Material.anisotropic
    as_diffuse = bpy.types.Material.as_diffuse

    def init(self, context):
        self.inputs.new(type="NodeSocketColor", name="Diffuse Color", identifier="DiffCol").default_value = (0.8, 0.8, 0.8, 1)
        self.inputs.new(type="NodeSocketFloat", name="Diffuse Amount", identifier="Diff").default_value = 1
        self.inputs.new(type="NodeSocketFloat", name="Oren-Nayar Sigma", identifier="Sigma").default_value = 0.1
        self.inputs.new(type="NodeSocketColor", name="Glossy Color", identifier="GlossyCol").default_value = (1, 1, 1, 1)
        self.inputs.new(type="NodeSocketFloat", name="Glossy Amount", identifier="Glossy").default_value = 0
        self.inputs.new(type="NodeSocketFloat", name="Glossy Exponent", identifier="Exp").default_value = 500
        self.inputs.new(type="NodeSocketFloat", name="Glossy Aniso.Exp.U", identifier="ExpU").default_value = 50
        self.inputs.new(type="NodeSocketFloat", name="Glossy Aniso.Exp.V", identifier="ExpV").default_value = 50
        self.inputs.new(type="NodeSocketColor", name="Mirror Color", identifier="MirrCol").default_value = (1, 1, 1, 1)
        self.inputs.new(type="NodeSocketFloat", name="Mirror Amount", identifier="Mirr").default_value = 0.1
        self.inputs.new(type="NodeSocketFloat", name="IOR Additional Amount", identifier="IOR").default_value = 1.8
        self.inputs.new(type="NodeSocketFloat", name="Bump Amount", identifier="Bump").default_value = 0
        self.inputs.new(type="NodeSocketFloat", name="Wireframe Amount", identifier="Wireframe").default_value = 0
        self.outputs.new(type="NodeSocketShader", name="BSDF", identifier="BSDF")
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
    bl_label = "YafaRay Glass Material"
    yaf_type = "OUTPUT_MATERIAL"
    absorption_color = bpy.types.Material.absorption
    absorption_dist = bpy.types.Material.absorption_dist
    dispersion_power = bpy.types.Material.dispersion_power
    fake_shadows = bpy.types.Material.fake_shadows

    def init(self, context):
        self.inputs.new(type="NodeSocketColor", name="Filter Color", identifier="FiltCol").default_value = (1, 1, 1, 1)
        self.inputs.new(type="NodeSocketFloat", name="Filter Amount", identifier="Filt").default_value = 1
        self.inputs.new(type="NodeSocketColor", name="Mirror Color", identifier="MirrCol").default_value = (1, 1, 1, 1)
        self.inputs.new(type="NodeSocketFloat", name="Mirror Amount", identifier="Mirr").default_value = 0.1
        self.inputs.new(type="NodeSocketFloat", name="IOR Additional Amount", identifier="IOR").default_value = 1.8
        self.inputs.new(type="NodeSocketFloat", name="Bump Amount", identifier="Bump").default_value = 0
        self.inputs.new(type="NodeSocketFloat", name="Wireframe Amount", identifier="Wireframe").default_value = 0
        self.outputs.new(type="NodeSocketShader", name="BSDF", identifier="BSDF")
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
    bl_label = "YafaRay Rough Glass Material"
    yaf_type = "OUTPUT_MATERIAL"
    absorption_color = bpy.types.Material.absorption
    absorption_dist = bpy.types.Material.absorption_dist
    dispersion_power = bpy.types.Material.dispersion_power
    fake_shadows = bpy.types.Material.fake_shadows

    def init(self, context):
        self.inputs.new(type="NodeSocketColor", name="Filter Color", identifier="FiltCol").default_value = (1, 1, 1, 1)
        self.inputs.new(type="NodeSocketFloat", name="Filter Amount", identifier="Filt").default_value = 1
        self.inputs.new(type="NodeSocketColor", name="Mirror Color", identifier="MirrCol").default_value = (1, 1, 1, 1)
        self.inputs.new(type="NodeSocketFloat", name="Mirror Amount", identifier="Mirr").default_value = 0.1
        self.inputs.new(type="NodeSocketFloat", name="IOR Additional Amount", identifier="IOR").default_value = 1.8
        self.inputs.new(type="NodeSocketFloat", name="Roughness Exponent", identifier="Roughness").default_value = 0.2
        self.inputs.new(type="NodeSocketFloat", name="Bump Amount", identifier="Bump").default_value = 0
        self.inputs.new(type="NodeSocketFloat", name="Wireframe Amount", identifier="Wireframe").default_value = 0
        self.outputs.new(type="NodeSocketShader", name="BSDF", identifier="BSDF")
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
    bl_label = "YafaRay Blend Material"
    yaf_type = "OUTPUT_MATERIAL"
    material1name = bpy.types.Material.material1name
    material2name = bpy.types.Material.material2name

    def init(self, context):
        self.inputs.new(type="NodeSocketFloat", name="Blend Amount", identifier="Blend").default_value = 0.5
        self.outputs.new(type="NodeSocketShader", name="BSDF", identifier="BSDF")

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
