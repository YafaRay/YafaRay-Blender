# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.props import EnumProperty, BoolProperty
from nodeitems_utils import NodeItem
from .common import NodeCategory
from ..util.properties_annotations import replace_properties_with_annotations


@replace_properties_with_annotations
class ColorBlendNode(bpy.types.Node):
    bl_idname = "YafaRay4ColorBlendNode"
    bl_label = "YafaRay Color Blend Node"
    blend_type = EnumProperty(
        name="Blend Type",
        items=[
            ('MIX', "MIX", "MIX"),
            ('ADD', "ADD", "ADD"),
            ('MULTIPLY', "MULTIPLY", "MULTIPLY"),
            ('SUBTRACT', "SUBTRACT", "SUBTRACT"),
            ('SCREEN', "SCREEN", "SCREEN"),
            ('DIVIDE', "DIVIDE", "DIVIDE"),
            ('DIFFERENCE', "DIFFERENCE", "DIFFERENCE"),
            ('DARKEN', "DARKEN", "DARKEN"),
            ('LIGHTEN', "LIGHTEN", "LIGHTEN"),
        ],
        default="MIX")
    invert = BoolProperty(name="Negative", default=False)
    use_stencil = BoolProperty(name="Stencil", default=False)
    use_rgb_to_intensity = BoolProperty(name="No RGB", default=False)

    # default_color = FloatVectorProperty(name="Default Color", subtype='COLOR', size=4, default=(1, 0, 1, 1))
    # default_value = FloatProperty(name="Default Value", default=1)

    def init(self, context):
        self.inputs.new("NodeSocketColor", "Color 1", "Color1").default_value = (1, 1, 1, 1)
        self.inputs.new("NodeSocketColor", "Color 2", "Color2").default_value = (1, 1, 1, 1)
        self.outputs.new("NodeSocketColor", "Color", "OutColor")
        self.blend_type = 'MIX'
        self.invert = False
        self.use_stencil = False
        self.use_rgb_to_intensity = False
        # self.default_color = (1, 0, 1, 1)
        # self.default_value = 1

    def draw_buttons(self, context, layout):
        layout.prop(self, "blend_type")
        layout.prop(self, "invert")
        layout.prop(self, "use_stencil")
        layout.prop(self, "use_rgb_to_intensity")
        # layout.prop(self, "default_color")
        # layout.prop(self, "default_value")


classes = (
    ColorBlendNode,
)


def register(node_categories):
    from bpy.utils import register_class
    node_categories_items = []
    for cls in classes:
        register_class(cls)
        node_categories_items.append(NodeItem(cls.bl_idname))
    node_categories.append(NodeCategory("YAFARAY4_COLOR", "YafaRay Color", items=node_categories_items))


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
