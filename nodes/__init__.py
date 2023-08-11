# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
import nodeitems_utils
from bpy.props import PointerProperty
from . import material
from . import texture
from . import world
from . import color
from .common import NodeTree

modules = (
    common,
    material,
    texture,
    world,
    color,
)


def register():
    node_categories = []
    for module in modules:
        module.register(node_categories)
    nodeitems_utils.register_node_categories("YAFARAY4_NODES", node_categories)
    bpy.types.Material.yafaray_nodes = PointerProperty(type=NodeTree)
    bpy.types.World.yafaray_nodes = PointerProperty(type=NodeTree)


def unregister():
    del bpy.types.World.yafaray_nodes
    del bpy.types.Material.yafaray_nodes
    nodeitems_utils.unregister_node_categories("YAFARAY4_NODES")
    for module in reversed(modules):
        module.unregister()
