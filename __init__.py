# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import sys
import os
import bpy

PLUGIN_NAME = "yafaray_v4"
BIN_PATH = os.path.join(__path__[0], 'bin')
YAF_ID_NAME = "YAFARAY4_RENDER"

# Version to be automatically populated during the cmake build process, getting the version from git tags
YAFARAY_BLENDER_VERSION = "v4-pre-alpha (development)"

sys.path.append(BIN_PATH)

bl_info = {
    "name": "YafaRay v4 Exporter",
    "description": "YafaRay integration for blender",
    "author": "Shuvro Sarker, Kim Skoglund (Kerbox), Pedro Alcaide (povmaniaco),"
              "Paulo Gomes (tuga3d), Michele Castigliego (subcomandante),"
              "Bert Buchholz, Rodrigo Placencia (DarkTide),"
              "Alexander Smirnov (Exvion), Olaf Arnold (olaf), David Bluecame",
    # Version to be automatically populated during the cmake build process, getting the version from git tags
    "version": ("v4-pre-alpha (development)", ""),
    "blender": (3, 5, 1),
    "location": "Info Header > Engine dropdown menu",
    # "wiki_url": "http://www.yafaray.org/community/forum",
    # "tracker_url": "http://www.yafaray.org/development/bugtracker/yafaray",
    "wiki_url": "https://github.com/YafaRay/YafaRay-Blender",
    "tracker_url": "https://github.com/YafaRay/YafaRay-Blender/issues",
    "category": "Render"
}

# Set Library Search options
if sys.platform == 'win32':  # I think this is the easiest and most flexible way to set the search options for Windows DLL
    os.environ['PATH'] = os.path.dirname(__file__) + '\\bin;' + os.environ['PATH']
# For Linux and MacOSX, set the RPATH in all the .so and .dylib libraries to relative paths respect to their location 

#from . import prop
from . import io
#from . import ui
#from . import ot
from .ot import migration

modules = (
    #prop,
    io,
    #ui,
    #ot,
)


def register():
    for module in modules:
        module.register()
    bpy.app.handlers.load_post.append(migration)
    # register keys for 'render 3d view', 'render still' and 'render animation'
    if bpy.context.window_manager.keyconfigs.addon is not None:
        km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name='Screen')
        km.keymap_items.new(idname='render.render_view', type='F12', value='PRESS', any=False, shift=False, ctrl=False,
                            alt=True)
        km.keymap_items.new(idname='render.render_animation', type='F12', value='PRESS', any=False, shift=False,
                            ctrl=True, alt=False)
        km.keymap_items.new(idname='render.render_still', type='F12', value='PRESS', any=False, shift=False, ctrl=False,
                            alt=False)


def unregister():
    # unregister keys for 'render 3d view', 'render still' and 'render animation'
    if bpy.context.window_manager.keyconfigs.addon is not None:
        kma = bpy.context.window_manager.keyconfigs.addon.keymaps['Screen']
        for kmi in kma.keymap_items:
            if kmi.idname == 'render.render_view' or kmi.idname == 'render.render_animation' \
                    or kmi.idname == 'render.render_still':
                kma.keymap_items.remove(kmi)
    bpy.app.handlers.load_post.remove(migration)
    for module in reversed(modules):
        module.unregister()
