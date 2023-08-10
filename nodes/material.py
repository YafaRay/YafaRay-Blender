# SPDX-License-Identifier: GPL-2.0-or-later

from bpy.props import FloatVectorProperty
from ..util.properties_annotations import replace_properties_with_annotations
from nodeitems_utils import NodeItem
from .common import GenericNode
from .common import NodeCategory


@replace_properties_with_annotations
class MaterialNode1(GenericNode):
    bl_idname = "YafaRay4MaterialNode1"
    bl_label = "YafaRay Material 1"
    test_var = FloatVectorProperty(
        subtype='COLOR', size=4,  # size=4 for RGBA
        min=0.0, max=1.0, default=(1.0, 1.0, 1.0, 1.0),
    )
    test_var2 = FloatVectorProperty(
        subtype='COLOR', size=4,  # size=4 for RGBA
        min=0.0, max=1.0, default=(1.0, 1.0, 1.0, 1.0),
    )

    def init(self, context):
        self.inputs.new("NodeSocketColor", "Color1").default_value = (1, 0, 1, 0.8)
        self.inputs.new("NodeSocketColor", "Color2").default_value = (0, 1, 0.5, 0.3)
        self.inputs.new("NodeSocketFloat", "Param1").default_value = 11.2
        # self.outputs.new("NodeSocketShader", "Mat")
        self.test_var = (1, 0, 0, 1)
        self.test_var2 = (0, 0.5, 0.7, 0.5)

    def draw_buttons(self, context, layout):
        layout.prop(self, "test_var")
        layout.prop(self, "test_var2")


classes = (
    MaterialNode1,
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
