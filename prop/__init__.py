# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from . import object
from . import material
from . import light
from . import scene
from . import camera
from . import texture
from . import world
from . import preferences

modules = (
    object,
    material,
    light,
    scene,
    camera,
    texture,
    world,
    preferences,
)


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
