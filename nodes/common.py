# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from nodeitems_utils import NodeCategory as BlenderNodeCategory


class NodeTree(bpy.types.NodeTree):
    bl_idname = "YAFARAY4_NODE_TREE"
    bl_label = "YafaRay Node Trees"
    bl_icon = 'NODETREE'

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == "YAFARAY4_RENDER"


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


class NodeCategory(BlenderNodeCategory):
    bl_idname = "YafaRay4NodeCategory"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "YAFARAY4_NODE_TREE"


classes = (
    NodeTree,
)


def register(node_categories):
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
