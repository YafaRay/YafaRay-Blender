# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.props import FloatVectorProperty
from ..util.properties_annotations import replace_properties_with_annotations
from nodeitems_utils import NodeItem
from .common import GenericNode
from .common import NodeCategory


@replace_properties_with_annotations
class MaterialNodeShinyDiffuse(GenericNode):
    bl_idname = "YafaRay4MaterialShinyDiffuse"
    bl_label = "Shiny Diffuse Material"
    brdf_type = bpy.types.Material.brdf_type
    fresnel_effect = bpy.types.Material.fresnel_effect

    def init(self, context):
        self.inputs.new("NodeSocketColor", "Diffuse Color").default_value = (0.8, 0.8, 0.8, 1)
        self.inputs.new("NodeSocketFloat", "Diffuse Amount").default_value = 1
        self.inputs.new("NodeSocketFloat", "Oren-Nayar Sigma").default_value = 0.1
        self.inputs.new("NodeSocketColor", "Mirror Color").default_value = (1, 1, 1, 1)
        self.inputs.new("NodeSocketFloat", "Mirror Amount").default_value = 0.1
        self.inputs.new("NodeSocketFloat", "IOR").default_value = 1.8
        self.inputs.new("NodeSocketFloat", "Transparency Amount").default_value = 0
        self.inputs.new("NodeSocketFloat", "Translucency Amount").default_value = 0
        self.inputs.new("NodeSocketFloat", "Bump Amount").default_value = 0
        self.inputs.new("NodeSocketFloat", "Wireframe Amount").default_value = 0
        # self.outputs.new("NodeSocketShader", "Mat")
        self.brdf_type = 'lambert'
        self.fresnel_effect = False

    def draw_buttons(self, context, layout):
        layout.prop(self, "brdf_type")
        layout.prop(self, "fresnel_effect")


classes = (
    MaterialNodeShinyDiffuse,
)


def register(node_categories):
    from bpy.utils import register_class
    node_categories_items = []
    for cls in classes:
        register_class(cls)
        node_categories_items.append(NodeItem(cls.bl_idname))
    node_categories.append(NodeCategory("YAFARAY4_MATERIAL", "Material", items=node_categories_items))


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
