# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from . import object
from . import material
from . import light
from . import scene
from . import camera
from . import texture
from . import world
if bpy.app.version >= (2, 80, 0):
    from . import preferences
    from . import scene_property_groups
else:
    from . import preferences_279
    from . import scene_property_groups_279

modules = (
    object,
    material,
    light,
    scene,
    camera,
    texture,
    world,
)

if bpy.app.version >= (2, 80, 0):
    modules = modules + (preferences, )
    modules = modules + (scene_property_groups, )
else:
    modules = modules + (preferences_279, )
    modules = modules + (scene_property_groups_279, )


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
