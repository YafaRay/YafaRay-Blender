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

import sys, os, threading, time

PLUGIN_PATH = os.path.join(__path__[0], 'bin', 'plugins')
BIN_PATH = os.path.join(__path__[0], 'bin')
YAF_ID_NAME = "YAFARAY_RENDER"

sys.path.append(BIN_PATH)

bl_info = {
    "name": "YafaRay Exporter",
    "author": "Shuvro Sarker, Kim Skoglund (Kerbox), Pedro Alcaide (povmaniaco), Paulo Gomes (tuga3d), Michele Castigliego (subcomandante), Bert Bucholtz, Rodrigo Placencia (DarkTide)",
    "version": (0, 1, 2, 'alpha'),
    "blender": (2, 5, 6),
    "location": "Info Header (engine dropdown)",
    "description": "YafaRay integration for blender",
    "warning" : "Alpha state",
    "wiki_url": "http://www.yafaray.org/community/forum",
    "tracker_url": "http://www.yafaray.org/development/bugtracker/yafaray",
    "category": "Render"
    }

# Preload needed libraries

if sys.platform == 'win32':
    # Loading order of the dlls is sensible please do not alter it
    dllArray = ['zlib1','libxml2-2','libgcc_s_sjlj-1','Half','Iex','IlmThread','IlmImf','libjpeg-8','libpng14','libtiff-3','libfreetype-6','libyafaraycore','libyafarayplugin']
elif sys.platform == 'darwin':
    dllArray = ['libyafaraycore.dylib','libyafarayplugin.dylib']
else:
    dllArray = ['libyafaraycore.so','libyafarayplugin.so']

import ctypes
for dll in dllArray:
    try:
        ctypes.cdll.LoadLibrary(os.path.join(BIN_PATH, dll))
    except Exception as e:
        print("ERROR: Failed to load library " + dll + ", " + repr(e));

if "bpy" in locals():
    import imp
    imp.reload(io)
    imp.reload(ui)
    imp.reload(ot)
else:
    import bpy
    from yafaray import io, ui, ot

def register():
    pass

def unregister():
    pass

if __name__ == '__main__':
    register()

