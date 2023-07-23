# SPDX-License-Identifier: GPL-2.0-or-later

# Note: variables cannot be used in bl_info, Blender reads it without executing code
bl_info = {
    "name": "YafaRay v4",
    "description": "YafaRay Render Engine for Blender",
    "version": (4, 0, 0, -4),
    "warning": "PRE-ALPHA version, for development only. Do NOT use for real production.",
    "blender": (3, 5, 1),
    "category": "Render",
    "author": "Shuvro Sarker, Kim Skoglund (Kerbox), Pedro Alcaide (povmaniaco), "
              "Paulo Gomes (tuga3d), Michele Castigliego (subcomandante), "
              "Bert Buchholz, Rodrigo Placencia (DarkTide), "
              "Alexander Smirnov (Exvion), Olaf Arnold (olaf), David Bluecame",
    "location": "In Blender 2.79: Info Header > Engine dropdown menu. "
                "In Blender 2.80 and higher: Properties Panel > Render Properties > Render Engine",
    "wiki_url": "https://github.com/YafaRay/YafaRay-Blender",
    "tracker_url": "https://github.com/YafaRay/YafaRay-Blender/issues"
}

YAFARAY_PACKAGE_NAME = __package__
YAFARAY_VERSION_SUFFIX = {
    -4: "PRE-ALPHA",
    -3: "Alpha",
    -2: "Beta",
    -1: "Release Candidate",
    -0: ""  # Normal release
}
YAFARAY_BLENDER_VERSION = str(bl_info['version'][0]) + "." + str(bl_info['version'][1]) + "." + str(
    bl_info['version'][2]) + " " + YAFARAY_VERSION_SUFFIX[bl_info['version'][3]]

import os
import sys

# The path to the system-wide libYafaRay binary libraries can be set in the PYTHONPATH environment variable before
# running Blender. For portable YafaRay-Blender installations, where the libYafaRay binary libraries are
# self-contained in the "bin" folder within the YafaRay-Blender add-on itself, the following code section should set
# the search paths to the "bin" folder
PORTABLE_LIBYAFARAY_PATH = os.path.join(__path__[0], 'bin')
sys.path.append(PORTABLE_LIBYAFARAY_PATH)
if sys.platform == 'win32':  # I think this is the easiest and most flexible way to set the search options for
    # Windows DLL
    os.environ['PATH'] = os.path.dirname(__file__) + '\\bin;' + os.environ['PATH']
# For Linux and MacOSX, set the RPATH in all the .so and .dylib libraries to relative paths respect to their location 


# Importing and registering modules from add-on sub-folders
import bpy
from . import prop
from . import io
from . import ui
from .ot import migration

modules = (
    prop,
    io,
    ui,
    ot,
)


def register():
    for module in modules:
        module.register()
    # noinspection PyTypeChecker
    bpy.app.handlers.load_post.append(migration)
    # register keys for 'render 3d view', 'render still' and 'render animation'
    if bpy.context.window_manager.keyconfigs.addon is not None:
        km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name='Screen')
        km.keymap_items.new(idname='yafaray4.render_view', type='F12', value='PRESS',
                            any=False, shift=False, ctrl=False, alt=True)
        km.keymap_items.new(idname='yafaray4.render_animation', type='F12', value='PRESS',
                            any=False, shift=False, ctrl=True, alt=False)
        km.keymap_items.new(idname='yafaray4.render_still', type='F12', value='PRESS',
                            any=False, shift=False, ctrl=False, alt=False)


def unregister():
    # unregister keys for 'render 3d view', 'render still' and 'render animation'
    if bpy.context.window_manager.keyconfigs.addon is not None:
        kma = bpy.context.window_manager.keyconfigs.addon.keymaps['Screen']
        for kmi in kma.keymap_items:
            if kmi.idname == 'yafaray4.render_view' or kmi.idname == 'yafaray4.render_animation' \
                    or kmi.idname == 'yafaray4.render_still':
                kma.keymap_items.remove(kmi)
    # noinspection PyTypeChecker
    bpy.app.handlers.load_post.remove(migration)
    for module in reversed(modules):
        module.unregister()
