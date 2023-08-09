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
    bl_label = "YafaRay Shader Nodes"
    bl_icon = 'NODETREE'

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == "YAFARAY4_RENDER"


class NodeCategory(BlenderNodeCategory):
    bl_idname = "YafaRay4NodeCategory"

    @classmethod
    def poll(cls, context):
        return True # context.space_data.tree_type == "YAFARAY4_NODE_TREE"


class NodeSocketInput(bpy.types.NodeSocket):
    bl_idname = "YafaRay4NodeSocketInput"

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text)  # , slider=self.slider)


class NodeSocketOutput(bpy.types.NodeSocket):
    bl_idname = "YafaRay4NodeSocketOutput"

    def draw(self, context, layout, node, text):
        layout.label(text=text)


@replace_properties_with_annotations
class NodeSocketInputValue(NodeSocketInput):
    bl_idname = "YafaRay4NodeSocketInputValue"
    default_value = FloatProperty()

    def draw_color(self, context, node):
        return 1.0, 0.4, 0.216, 0.5


@replace_properties_with_annotations
class NodeSocketInputColorRGB(NodeSocketInput):
    bl_idname = "YafaRay4NodeSocketInputColorRGB"
    default_value = FloatVectorProperty(
        subtype='COLOR', size=3,  # size=3 for RGB
        min=0.0, max=1.0, default=(1.0, 1.0, 1.0),
    )

    def draw_color(self, context, node):
        return 0.1, 0.3, 0.5, 1.0


@replace_properties_with_annotations
class NodeSocketInputColorRGBA(NodeSocketInput):
    bl_idname = "YafaRay4NodeSocketInputColorRGBA"
    default_value = FloatVectorProperty(
        subtype='COLOR', size=4,  # size=4 for RGBA
        min=0.0, max=1.0, default=(1.0, 1.0, 1.0, 1.0),
    )

    def draw_color(self, context, node):
        return 0.3, 0.3, 0.5, 1.0


class NodeSocketOutputValue(NodeSocketOutput):
    bl_idname = "YafaRay4NodeSocketOutputValue"

    def draw_color(self, context, node):
        return 1.0, 0.4, 0.216, 0.5


class NodeSocketOutputColorRGB(NodeSocketOutput):
    bl_idname = "YafaRay4NodeSocketOutputColorRGB"

    def draw_color(self, context, node):
        return 0.1, 0.3, 0.5, 1.0


class NodeSocketOutputColorRGBA(NodeSocketOutput):
    bl_idname = "YafaRay4NodeSocketOutputColorRGBA"

    def draw_color(self, context, node):
        return 0.3, 0.3, 0.5, 1.0


class GenericNode(bpy.types.Node):
    bl_idname = "YafaRay4Node"
    bl_label = "YafaRay Generic Node"

    @classmethod
    def poll(cls, tree):
        return True #tree.bl_idname == "YAFARAY4_NODE_TREE"

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
        self.new_input("YafaRay4NodeSocketInputColorRGB", "Color1", (0.7, 0.7, 0.7))
        self.new_input("YafaRay4NodeSocketInputColorRGBA", "Color2", (0.7, 0.7, 0.7, 0.5))
        self.new_input("YafaRay4NodeSocketInputValue", "Param1", 0)

    def draw_buttons(self, context, layout):
        layout.prop(self, "test_var")


@replace_properties_with_annotations
class TextureNode1(GenericNode):
    bl_idname = "YafaRay4TextureNode1"
    bl_label = "YafaRay Texture 1"
    type = 'TEXTURE'
    bl_static_type = type

    def init(self, context):
        self.new_input("YafaRay4NodeSocketInputColorRGB", "Color1i", (0.7, 0.7, 0.7))
        self.new_input("YafaRay4NodeSocketInputColorRGBA", "Color2i", (0.7, 0.7, 0.7, 0.5))
        self.new_input("YafaRay4NodeSocketInputValue", "Param1i", 0)
        self.new_output("YafaRay4NodeSocketOutputColorRGB", "Color1o")
        self.new_output("YafaRay4NodeSocketOutputColorRGBA", "Color2o")
        self.new_output("YafaRay4NodeSocketOutputValue", "Param1o")


classes = (
    NodeTree,
    NodeSocketInputValue,
    NodeSocketInputColorRGB,
    NodeSocketInputColorRGBA,
    NodeSocketOutputValue,
    NodeSocketOutputColorRGB,
    NodeSocketOutputColorRGBA,
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
            NodeItem("YafaRay4MaterialNode1")
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
