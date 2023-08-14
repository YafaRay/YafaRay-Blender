# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from nodeitems_utils import NodeItem
from .common import NodeCategory
from ..util.properties_annotations import replace_properties_with_annotations


@replace_properties_with_annotations
class WorldNode(bpy.types.Node):
    bl_idname = "YafaRay4WorldNode"
    bl_label = "YafaRay World"

    def init(self, context):
        self.inputs.new("NodeSocketColor", "Background Color", "BackCol").default_value = (1, 1, 1, 1)

    def draw_buttons(self, context, layout):
        pass


classes = (
    WorldNode,
)


def register(node_categories):
    from bpy.utils import register_class
    node_categories_items = []
    for cls in classes:
        register_class(cls)
        node_categories_items.append(NodeItem(cls.bl_idname))
    node_categories.append(NodeCategory("YAFARAY4_WORLD", "YafaRay World", items=node_categories_items))


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
