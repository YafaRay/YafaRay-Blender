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

sys.path.append(BIN_PATH)



bl_addon_info = {
    "name": "YafaRay Integration",
    "author": "Shuvro Sarker",
    "version": "0.1.2 alpha",
    "blender": (2, 5, 5),
    "category": "Render",
    "warning" : "VERY ALPHA!",
    "description": "YafaRay integration for blender 2.5. When activated, YafaRay will be available in the Render Engine dropdown"
    }
if sys.platform == 'win32':
    # preload some dlls so users do not have to mess about with path
    import ctypes
    for dll in ['zlib1','libxml2-2','libgcc_s_sjlj-1','Half','Iex','IlmThread',# in some rev of Blender, Half before Iex
                'IlmImf','libjpeg-8','libpng14','libtiff-3','libfreetype-6',
                'libyafaraycore','libyafarayplugin']:
    # load order of libraries is very important, not altered
        try:
            ctypes.cdll.LoadLibrary(os.path.join(BIN_PATH, dll))
        except Exception as e:
            print("ERROR: Failed to load library " + dll + ", " + repr(e));



import bpy


def register():

    from yafaray import io, ui, op

    io.register()
    for submodule in [ui, op]:
        for element in dir(submodule):
            try:
                getattr(getattr(submodule, element), 'register')()
            except  AttributeError as e:
               pass

    return

    try:
        import io, ui, op
    except:
        print("Could not import subpackages, delay loading...")
        def delayload():
            time.sleep(1)
            print("trying to register again...")
            register()
        t = threading.Thread(target=delayload)
        t.start()
        return

    io.register()
    for submodule in [ui, op]:
        for element in dir(submodule):
            try:
                getattr(getattr(submodule, element), 'register')()
            except AttributeError as e:
                pass


def unregister():
    #import bpy
    from yafaray import io, ui, op # neccesary? double import?

    io.unregister()
    for submodule in [ui, op]:
        for element in dir(submodule):
            try:
                getattr(getattr(submodule, element), 'unregister')()
            except AttributeError:
                pass

if __name__ == '__main__':
    register()
