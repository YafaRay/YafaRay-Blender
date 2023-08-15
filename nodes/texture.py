# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from nodeitems_utils import NodeItem
from .common import NodeCategory
from ..util.properties_annotations import replace_properties_with_annotations


@replace_properties_with_annotations
class TextureNode1(bpy.types.Node):
    bl_idname = "YafaRay4TextureNode1"
    bl_label = "YafaRay Texture 1"

    def init(self, context):
        self.inputs.new("NodeSocketColor", "Color 1", "Color1").default_value = (0, 1, 1, 0.2)
        self.inputs.new("NodeSocketColor", "Color 2", "Color2").default_value = (0, 1, 0, 0.5)
        self.inputs.new("NodeSocketFloat", "Param 1", "Param1").default_value = 13.5
        self.outputs.new("NodeSocketColor", "Color", "OutColor")


@replace_properties_with_annotations
class TextureNodeVoronoi(bpy.types.ShaderNodeTexVoronoi):
    bl_idname = "YafaRay4TextureNodeVoronoi"
    bl_label = "YafaRay Voronoi Texture"
    tex = bpy.props.PointerProperty(type=bpy.types.Texture)
    coll = bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    def init(self, context):
        super().__init__(context)
        print(dir(super))
        self.inputs.new("NodeSocketColor", "Color 3", "Color3").default_value = (0, 1, 1, 0.2)
        self.outputs.new("NodeSocketColor", "Color", "OutColor")

    def draw_buttons(self, context, layout):
        layout.template_ID_preview(self, "tex")
        layout.prop(self, "coll")
        layout.operator("yafaray4.show_texture_window")
        bpy.types.YAFARAY4_PT_texture_type_voronoi.draw2(None, self.tex, layout)


classes = (
    TextureNode1,
    TextureNodeVoronoi,
)


def register(node_categories):
    from bpy.utils import register_class
    node_categories_items = []
    for cls in classes:
        register_class(cls)
        node_categories_items.append(NodeItem(cls.bl_idname))
    node_categories_items.append(NodeItem("ShaderNodeTexVoronoi", "YafaRay Voronoi Native Texture"))
    node_categories.append(NodeCategory("YAFARAY4_TEXTURE", "YafaRay Texture", items=node_categories_items))


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
