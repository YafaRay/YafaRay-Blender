# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
import nodeitems_utils
from bpy.props import (FloatProperty,
                       FloatVectorProperty,
                       PointerProperty)
from nodeitems_utils import NodeCategory as BlenderNodeCategory, NodeItem
from ..util.properties_annotations import replace_properties_with_annotations


class NodeTree(bpy.types.NodeTree):
    bl_idname = "YAFARAY4_NODE_TREE"
    bl_label = "YafaRay Node Trees"
    bl_icon = 'NODETREE'

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == "YAFARAY4_RENDER"


class NodeCategory(BlenderNodeCategory):
    bl_idname = "YafaRay4NodeCategory"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "YAFARAY4_NODE_TREE"


class GenericNode(bpy.types.Node):
    bl_idname = "YafaRay4Node"
    bl_label = "YafaRay Generic Node"

    @classmethod
    def poll(cls, tree):
        return tree.bl_idname == "YAFARAY4_NODE_TREE"

    def new_input(self, node_input_type, node_input_name, default_value):
        node_input = self.inputs.new(node_input_type, node_input_name)
        node_input.default_value = default_value

    def new_output(self, output_type, output_name):
        self.outputs.new(output_type, output_name)


@replace_properties_with_annotations
class MaterialNode1(GenericNode):
    bl_idname = "YafaRay4MaterialNode1"
    bl_label = "YafaRay Material 1"
    test_var = FloatVectorProperty(
        subtype='COLOR', size=4,  # size=4 for RGBA
        min=0.0, max=1.0, default=(1.0, 1.0, 1.0, 1.0),
    )

    def init(self, context):
        self.inputs.new("NodeSocketColor", "Color1").default_value = (1,0,1,0.8)
        self.inputs.new("NodeSocketColor", "Color2").default_value = (0,1,0.5,0.3)
        self.inputs.new("NodeSocketFloat", "Param1").default_value = 11.2
        # self.outputs.new("NodeSocketShader", "Mat")

    def draw_buttons(self, context, layout):
        layout.prop(self, "test_var")


@replace_properties_with_annotations
class TextureNode1(GenericNode):
    bl_idname = "YafaRay4TextureNode1"
    bl_label = "YafaRay Texture 1"

    def init(self, context):
        self.inputs.new("NodeSocketColor", "Color1").default_value = (0,1,1,0.2)
        self.inputs.new("NodeSocketColor", "Color2").default_value = (0,1,0,0.5)
        self.inputs.new("NodeSocketFloat", "Param1").default_value = 13.5
        self.outputs.new("NodeSocketColor", "Color1")
        self.outputs.new("NodeSocketColor", "Color2")
        self.outputs.new("NodeSocketFloat", "Param1")


classes = (
    NodeTree,
    MaterialNode1,
    TextureNode1,
)


def register_classes():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_classes():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


def register():
    register_classes()
    shader_node_categories = [
        NodeCategory("YAFARAY4_MATERIAL", "Material", items=[
            NodeItem("YafaRay4MaterialNode1", settings={
                "test_var": repr((1,0,0,1)),
            })
        ]),
        NodeCategory("YAFARAY4_TEXTURE", "Texture", items=[
            NodeItem("YafaRay4TextureNode1")
        ]),
    ]
    nodeitems_utils.register_node_categories("YAFARAY4_NODES", shader_node_categories)
    bpy.types.Material.yafaray_nodes = PointerProperty(type=NodeTree)


def unregister():
    del bpy.types.Material.yafaray_nodes
    nodeitems_utils.unregister_node_categories("YAFARAY4_NODES")
    unregister_classes()
