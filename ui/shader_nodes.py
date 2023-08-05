# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
import nodeitems_utils
from bl_ui.properties_material import MaterialButtonsPanel
from bpy.props import (FloatProperty,
                       FloatVectorProperty)
from nodeitems_utils import NodeCategory, NodeItem

from ..util.properties_annotations import replace_properties_with_annotations


class ShaderNodeTree(bpy.types.NodeTree):
    bl_idname = "YAFARAY4_SHADER_NODE_TREE"
    bl_label = "YafaRay Nodes"
    bl_icon = 'NODETREE'
    requested_links = set()

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == "YAFARAY4_RENDER"


class ShaderNodeCategory(NodeCategory):
    bl_idname = "YafaRay4ShaderNodeCategory"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "YAFARAY4_SHADER_NODE_TREE"


class ShaderNodeSocket(bpy.types.NodeSocket):
    bl_idname = "YafaRay4ShaderNodeSocket"

    def draw_color(self, context, node):
        return 1.0, 0.4, 0.216, 0.5  # self.socketColor


class ShaderNodeSocketInput(ShaderNodeSocket):
    bl_idname = "YafaRay4ShaderNodeSocketInput"

    def __init__(self, socket_color, slider=False):
        # self.socketColor = socketColor
        # self.slider = slider
        pass

    def draw(self, context, layout, node, text):
        layout.prop(self, "defaultValue", text=text)  # , slider=self.slider)


class ShaderNodeSocketOutput(ShaderNodeSocket):
    bl_idname = "YafaRay4ShaderNodeSocketOutput"

    def __init__(self, socket_color):
        pass  # self.socket_color = socket_color

    def draw(self, context, layout, node, text):
        layout.label(text=text)


@replace_properties_with_annotations
class ShaderNodeSocketInputValue(ShaderNodeSocketInput):
    bl_idname = "YafaRay4ShaderNodeSocketInputValue"
    defaultValue = FloatProperty()

    def __init__(self):
        super().__init__(socket_color=(0.5, 0.3, 0.1, 1.0), slider=True)


@replace_properties_with_annotations
class ShaderNodeSocketInputColorRGB(ShaderNodeSocketInput):
    bl_idname = "YafaRay4ShaderNodeSocketInputColorRGB"
    defaultValue = FloatVectorProperty(
        subtype='COLOR', size=3,  # size=3 for RGB
        min=0.0, max=1.0, default=(1.0, 1.0, 1.0),
    )

    def __init__(self):
        super().__init__(socket_color=(0.1, 0.3, 0.5, 1.0))


@replace_properties_with_annotations
class ShaderNodeSocketInputColorRGBA(ShaderNodeSocketInput):
    bl_idname = "YafaRay4ShaderNodeSocketInputColorRGBA"
    defaultValue = FloatVectorProperty(
        subtype='COLOR', size=4,  # size=4 for RGBA
        min=0.0, max=1.0, default=(1.0, 1.0, 1.0, 1.0),
    )

    def __init__(self):
        super().__init__(socket_color=(0.3, 0.3, 0.5, 1.0))


@replace_properties_with_annotations
class ShaderNodeSocketOutputValue(ShaderNodeSocketOutput):
    bl_idname = "YafaRay4ShaderNodeSocketOutputValue"

    def __init__(self):
        super().__init__(socket_color=(0.5, 0.3, 0.1, 1.0))


@replace_properties_with_annotations
class ShaderNodeSocketOutputColorRGB(ShaderNodeSocketOutput):
    bl_idname = "YafaRay4ShaderNodeSocketOutputColorRGB"

    def __init__(self):
        super().__init__(socket_color=(0.1, 0.3, 0.5, 1.0))


@replace_properties_with_annotations
class ShaderNodeSocketOutputColorRGBA(ShaderNodeSocketOutput):
    bl_idname = "YafaRay4ShaderNodeSocketOutputColorRGBA"

    def __init__(self):
        super().__init__(socket_color=(0.3, 0.3, 0.5, 1.0))


class GenericNode(bpy.types.Node):
    bl_idname = "YafaRay4GenericNode"
    bl_label = "Generic YafaRay node"

    @classmethod
    def poll(cls, tree):
        return tree.bl_idname == "YAFARAY4_SHADER_NODE_TREE"

    def new_input(self, node_input_type, node_input_name, default_value):
        node_input = self.inputs.new(node_input_type, node_input_name)
        node_input.defaultValue = default_value

    def new_output(self, output_type, output_name):
        node_output = self.outputs.new(output_type, output_name)


class MaterialNodeOutput(GenericNode):
    bl_idname = "YafaRay4MaterialNodeOutput"
    bl_label = "YafaRay Material Output"

    def init(self, context):
        self.new_input("YafaRay4ShaderNodeSocketInputColorRGBA", "MatIn", (0.7, 0.7, 0.7, 0.5))


class MaterialNode1(GenericNode):
    bl_idname = "YafaRay4MaterialNode1"
    bl_label = "YafaRay Material 1"

    def init(self, context):
        self.new_input("YafaRay4ShaderNodeSocketInputColorRGB", "Color1", (0.7, 0.7, 0.7))
        self.new_input("YafaRay4ShaderNodeSocketInputColorRGBA", "Color2", (0.7, 0.7, 0.7, 0.5))
        self.new_input("YafaRay4ShaderNodeSocketInputValue", "Param1", 0)
        self.new_output("YafaRay4ShaderNodeSocketOutputColorRGB", "MatOut")


class TextureNode1(GenericNode):
    bl_idname = "YafaRay4TextureNode1"
    bl_label = "YafaRay Texture 1"

    def init(self, context):
        self.new_input("YafaRay4ShaderNodeSocketInputColorRGB", "Color1i", (0.7, 0.7, 0.7))
        self.new_input("YafaRay4ShaderNodeSocketInputColorRGBA", "Color2i", (0.7, 0.7, 0.7, 0.5))
        self.new_input("YafaRay4ShaderNodeSocketInputValue", "Param1i", 0)
        self.new_output("YafaRay4ShaderNodeSocketOutputColorRGB", "Color1o")
        self.new_output("YafaRay4ShaderNodeSocketOutputColorRGBA", "Color2o")
        self.new_output("YafaRay4ShaderNodeSocketOutputValue", "Param1o")


classes = (
    ShaderNodeTree,
    ShaderNodeSocketInputValue,
    ShaderNodeSocketInputColorRGB,
    ShaderNodeSocketInputColorRGBA,
    ShaderNodeSocketOutputValue,
    ShaderNodeSocketOutputColorRGB,
    ShaderNodeSocketOutputColorRGBA,
    MaterialNodeOutput,
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


def register_nodes():
    register_classes()
    shader_node_categories = [
        ShaderNodeCategory("YAFARAY4_SHADER_OUTPUT", "Output", items=[
            NodeItem("YafaRay4MaterialNodeOutput")  # , label="YafaRay Material Output"),
        ]),
        # YafNodeCategory("YAF_TEXTURE", "Texture", items=[
        ShaderNodeCategory("YAFARAY4_SHADER", "Shader", items=[
            NodeItem("YafaRay4MaterialNode1")  # , label="YafaRay Material 1"),
        ]),
        # YafNodeCategory("YAF_TEXTURE", "Texture", items=[
        ShaderNodeCategory("YAFARAY4_SHADER_TEXTURE", "Texture", items=[
            NodeItem("YafaRay4TextureNode1")  # , label="YafaRay Texture 1"),
        ]),
    ]
    nodeitems_utils.register_node_categories("YAFARAY4_SHADER_NODES", shader_node_categories)


def unregister_nodes():
    nodeitems_utils.unregister_node_categories("YAFARAY4_SHADER_NODES")
    unregister_classes()


def register():
    register_nodes()


def unregister():
    unregister_nodes()
