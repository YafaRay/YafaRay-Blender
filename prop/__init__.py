# SPDX-License-Identifier: GPL-2.0-or-later

import bpy

if bpy.app.version >= (2, 80, 0):
    from . import preferences
else:
    from . import preferences_279
# from . import object
# from . import material
# from . import light
# from . import scene
# from . import camera
# from . import texture
# from . import world

if bpy.app.version >= (2, 80, 0):
    modules = (
        preferences,
        #object,
        #material,
        #light,
        #scene,
        #camera,
        #texture,
        #world,
    )
else:
    modules = (
        preferences_279,
        #object,
        #material,
        #light,
        #scene,
        #camera,
        #texture,
        #world,
    )

def register():
    for module in modules:
        module.register()

def unregister():
    for module in reversed(modules):
        module.unregister()