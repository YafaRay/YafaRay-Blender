# SPDX-License-Identifier: GPL-2.0-or-later

import nodeitems_utils
from . import material
from . import texture
from . import world
from . import color

modules = (
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


def unregister():
    nodeitems_utils.unregister_node_categories("YAFARAY4_NODES")
    for module in reversed(modules):
        module.unregister()
