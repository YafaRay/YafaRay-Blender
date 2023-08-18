# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from nodeitems_utils import NodeItem

from .common import NodeCategory
from ..util.properties_annotations import replace_properties_with_annotations
from bpy.props import PointerProperty


@replace_properties_with_annotations
class TextureNode1(bpy.types.Node):
    bl_idname = "YafaRay4TextureNode1"
    bl_label = "YafaRay Texture 1"
    yafaray_type = 'TEXTURE'
    texture = PointerProperty(type=bpy.types.Texture)

    def init(self, context):
        self.inputs.new(type="NodeSocketColor", name="Color 1", identifier="Color1").default_value = (0, 1, 1, 0.2)
        self.inputs.new(type="NodeSocketColor", name="Color 2", identifier="Color2").default_value = (0, 1, 0, 0.5)
        self.inputs.new(type="NodeSocketFloat", name="Param 1", identifier="Param1").default_value = 13.5
        self.outputs.new(type="NodeSocketColor", name="Color", identifier="OutColor")

    def draw_buttons(self, context, layout):
        layout.template_ID(self, "texture", new="texture.new")
        op = layout.operator("yafaray4.show_texture_window")
        if self.texture is not None:
            op.texture_name = self.texture.name
        layout.label(text="If a new Properties window appears, click again to show the editor for the selected texture", icon="INFO")


classes = (
    TextureNode1,
)


def register(node_categories):
    from bpy.utils import register_class
    node_categories_items = []
    for cls in classes:
        register_class(cls)
        node_categories_items.append(NodeItem(cls.bl_idname))
    # node_categories_items.append(NodeItem("ShaderNodeTexVoronoi", "YafaRay Voronoi Native Texture"))
    node_categories.append(NodeCategory("YAFARAY4_TEXTURE", "YafaRay Texture", items=node_categories_items))


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
