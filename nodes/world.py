# SPDX-License-Identifier: GPL-2.0-or-later

from bpy.props import FloatVectorProperty
from nodeitems_utils import NodeItem
from .common import GenericNode
from .common import NodeCategory
from ..util.properties_annotations import replace_properties_with_annotations


@replace_properties_with_annotations
class WorldNode(GenericNode):
    bl_idname = "YafaRay4WorldNode"
    bl_label = "YafaRay World"
    test_var = FloatVectorProperty(name="Test Variable", subtype='COLOR', size=4, min=0.0, max=1.0)

    def init(self, context):
        self.inputs.new("NodeSocketColor", "Color1").default_value = (1, 0, 1, 0.8)
        self.inputs.new("NodeSocketColor", "Color2").default_value = (0, 1, 0.5, 0.3)
        self.inputs.new("NodeSocketFloat", "Param1").default_value = 11.2
        self.test_var = (1, 0, 0, 1)

    def draw_buttons(self, context, layout):
        layout.prop(self, "test_var")


classes = (
    WorldNode,
)


def register(node_categories):
    from bpy.utils import register_class
    node_categories_items = []
    for cls in classes:
        register_class(cls)
        node_categories_items.append(NodeItem(cls.bl_idname))
    node_categories.append(NodeCategory("YAFARAY4_WORLD", "World", items=node_categories_items))


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
