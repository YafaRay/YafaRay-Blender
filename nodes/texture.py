# SPDX-License-Identifier: GPL-2.0-or-later

from nodeitems_utils import NodeItem
from .common import GenericNode
from .common import NodeCategory
from ..util.properties_annotations import replace_properties_with_annotations


@replace_properties_with_annotations
class TextureNode1(GenericNode):
    bl_idname = "YafaRay4TextureNode1"
    bl_label = "YafaRay Texture 1"

    def init(self, context):
        self.inputs.new("NodeSocketColor", "Color1").default_value = (0, 1, 1, 0.2)
        self.inputs.new("NodeSocketColor", "Color2").default_value = (0, 1, 0, 0.5)
        self.inputs.new("NodeSocketFloat", "Param1").default_value = 13.5
        self.outputs.new("NodeSocketColor", "Color1")
        self.outputs.new("NodeSocketColor", "Color2")
        self.outputs.new("NodeSocketFloat", "Param1")


classes = (
    TextureNode1,
)


def register(node_categories):
    from bpy.utils import register_class
    node_categories_items = []
    for cls in classes:
        register_class(cls)
        node_categories_items.append(NodeItem(cls.bl_idname))
    node_categories.append(NodeCategory("YAFARAY4_TEXTURE", "Texture", items=node_categories_items))


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
