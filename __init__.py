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

import sys
import os
import threading
import time

PLUGIN_PATH = os.path.join(__path__[0], 'bin', 'plugins')
BIN_PATH = os.path.join(__path__[0], 'bin')
YAF_ID_NAME = "YAFA_RENDER"

sys.path.append(BIN_PATH)

bl_info = {
    "name": "YafaRay Exporter",
    "author": "Shuvro Sarker, Kim Skoglund (Kerbox), \
Pedro Alcaide (povmaniaco), Paulo Gomes (tuga3d), \
Michele Castigliego (subcomandante), Bert Buchholz, \
Rodrigo Placencia (DarkTide), Alexander Smirnov (Exvion)",
    "version": (0, 1, 2, 'alpha'),
    "blender": (2, 5, 6),
    "api": 37389,
    "location": "Info Header (engine dropdown)",
    "description": "YafaRay integration for blender",
    "warning": "Alpha state",
    "wiki_url": "http://www.yafaray.org/community/forum",
    "tracker_url": "http://www.yafaray.org/development/bugtracker/yafaray",
    "category": "Render"
    }

# Preload needed libraries

if sys.platform == 'win32':
    # Loading order of the dlls is sensible please do not alter it
    dllArray = ['zlib1', 'libxml2-2', 'libgcc_s_sjlj-1', 'Half', 'Iex', 'IlmThread', 'IlmImf', 'libjpeg-8', 'libpng14', 'libtiff-3', 'libfreetype-6', 'libyafaraycore', 'libyafarayplugin']
elif sys.platform == 'darwin':
    dllArray = ['libyafaraycore.dylib', 'libyafarayplugin.dylib']
else:
    dllArray = ['libyafaraycore.so', 'libyafarayplugin.so']

import ctypes
for dll in dllArray:
    try:
        ctypes.cdll.LoadLibrary(os.path.join(BIN_PATH, dll))
    except Exception as e:
        print("ERROR: Failed to load library " + dll + ", " + repr(e))

if "bpy" in locals():
    import imp
    imp.reload(prop)
    imp.reload(io)
    imp.reload(ui)
    imp.reload(ot)
else:
    import bpy
    from yafaray import prop, io, ui, ot


def register():
    prop.register()
    bpy.utils.register_module(__name__)

    kitems = bpy.context.window_manager.keyconfigs.active.keymaps["Screen"]
    kitems.keymap_items.new("RENDER_OT_render_view", 'F12', 'RELEASE', False, False, False, True)
    kitems.keymap_items.new("RENDER_OT_render_animation", 'F12', 'RELEASE', False, False, True, False)



def unregister():
    print("unregister called")
    bpy.utils.unregister_module(__name__, True)
    prop.unregister()

if __name__ == '__main__':
    register()
