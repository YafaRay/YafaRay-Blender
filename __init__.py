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
import ctypes

PLUGIN_PATH = os.path.join(__path__[0], 'bin', 'plugins')
BIN_PATH = os.path.join(__path__[0], 'bin')
YAF_ID_NAME = "YAFA_RENDER"

sys.path.append(BIN_PATH)

bl_info = {
    "name": "YafaRay Exporter",
    "description": "YafaRay integration for blender",
    "author": "Shuvro Sarker, Kim Skoglund (Kerbox), Pedro Alcaide (povmaniaco),"
              "Paulo Gomes (tuga3d), Michele Castigliego (subcomandante),"
              "Bert Buchholz, Rodrigo Placencia (DarkTide),"
              "Alexander Smirnov (Exvion), Olaf Arnold (olaf), David Bluecame",
    "version": ('Experimental', 2, 0, 0),
    "blender": (2, 7, 6),
    "location": "Info Header > Engine dropdown menu",
    "wiki_url": "http://www.yafaray.org/community/forum",
    "tracker_url": "http://www.yafaray.org/development/bugtracker/yafaray",
    "category": "Render"
    }

# Preload needed libraries
# Loading order of the dlls is sensible please do not alter it
if sys.platform == 'win32':
    if sys.maxsize == 2**63 - 1:    # Windows 64bit system
        for file in os.listdir(BIN_PATH):
            # load dll's from a MSVC installation
            if file in {'yafaraycore.dll'}:
                dllArray = ['zlib1', 'iconv', 'zlib', 'libpng15', 'libxml2', 'yafaraycore', 'yafarayplugin']
                break
            # load dll's from a MinGW64 installation
            else:
                dllArray = ['libwinpthread-1', 'libgcc_s_seh-1', 'libstdc++-6', 'libiconv-2', 'libzlib1', 'libxml2-2', 'libHalf', 'libIex', 'libImath', 'libIlmThread', 'libIlmImf', 'libjpeg-8', 'libpng16', 'libtiff-5', 'libbz2-1', 'libfreetype-6', 'libyafaraycore', 'libyafarayplugin']

    else:    # Windows 32bit system
        for file in os.listdir(BIN_PATH):
            # load dll's from a MSVC installation
            if file in {'yafaraycore.dll'}:
                dllArray = ['zlib1', 'iconv', 'zlib', 'libpng15', 'libxml2', 'yafaraycore', 'yafarayplugin']
                break
            # load dll's from a MinGW32 installation
            else:
                dllArray = ['libwinpthread-1', 'libgcc_s_sjlj-1', 'libstdc++-6', 'libiconv-2', 'libzlib1', 'libxml2-2', 'libHalf', 'libIex', 'libImath', 'libIlmThread', 'libIlmImf', 'libjpeg-8', 'libpng16', 'libtiff-5', 'libbz2-1', 'libfreetype-6', 'libyafaraycore', 'libyafarayplugin']

elif sys.platform == 'darwin':
    dllArray = ['libyafaraycore.dylib', 'libyafarayplugin.dylib']
else:
    if sys.maxsize == 2**63 - 1:    # Linux 64bit system
        dllArray = ['libHalf.so.6.0.0', 'libIex.so.6.0.0', 'libImath.so.6.0.0', 'libIlmThread.so.6.0.0', 'libIlmImf.so.6.0.0', 'libpython3.4m.so.1.0', 'libjpeg.so.62.0.0', 'libz.so.1.2.3.4', 'libpng12.so.0.44.0', 'libtiff.so.4.3.3', 'libfreetype.so.6.6.0', 'libyafaraycore.so', 'libyafarayplugin.so']

    else:   # Linux 32bit system
        dllArray = ['libHalf.so.6.0.0', 'libIex.so.6.0.0', 'libImath.so.6.0.0', 'libIlmThread.so.6.0.0', 'libIlmImf.so.6.0.0', 'libpython3.4m.so.1.0', 'libjpeg.so.62.0.0', 'libz.so.1.2.3.4', 'libpng12.so.0.44.0', 'libtiff.so.4.3.3', 'libfreetype.so.6.6.0', 'libyafaraycore.so', 'libyafarayplugin.so']

for dll in dllArray:
    try:
        ctypes.cdll.LoadLibrary(os.path.join(BIN_PATH, dll))
    except Exception as e:
        print("ERROR: Failed to load library {0}, {1}".format(dll, repr(e)))

if "bpy" in locals():
    import imp
    imp.reload(prop)
    imp.reload(io)
    imp.reload(ui)
    imp.reload(ot)
else:
    import bpy
    from bpy.app.handlers import persistent
    from . import prop
    from . import io
    from . import ui
    from . import ot


@persistent
def load_handler(dummy):
    for tex in bpy.data.textures:
        if tex is not None:
            # set the correct texture type on file load....
            # converts old files, where propertie yaf_tex_type wasn't defined
            print("Load Handler: Convert Yafaray texture \"{0}\" with texture type: \"{1}\" to \"{2}\"".format(tex.name, tex.yaf_tex_type, tex.type))
            tex.yaf_tex_type = tex.type
    for mat in bpy.data.materials:
        if mat is not None:
            # from old scenes, convert old blend material Enum properties into the new string properties
            if mat.mat_type == "blend":
                if not mat.is_property_set("material1name") or not mat.material1name:
                    mat.material1name = mat.material1
                if not mat.is_property_set("material2name") or not mat.material2name:
                    mat.material2name = mat.material2
    # convert image output file type setting from blender to yafaray's file type setting on file load, so that both are the same...
    if bpy.context.scene.render.image_settings.file_format is not bpy.context.scene.img_output:
        bpy.context.scene.img_output = bpy.context.scene.render.image_settings.file_format


def register():
    prop.register()
    bpy.utils.register_module(__name__)
    bpy.app.handlers.load_post.append(load_handler)
    # register keys for 'render 3d view', 'render still' and 'render animation'
    km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name='Screen')
    kmi = km.keymap_items.new('render.render_view', 'F12', 'PRESS', False, False, False, True)
    kmi = km.keymap_items.new('render.render_animation', 'F12', 'PRESS', False, False, True, False)
    kmi = km.keymap_items.new('render.render_still', 'F12', 'PRESS', False, False, False, False)


def unregister():
    prop.unregister()
    # unregister keys for 'render 3d view', 'render still' and 'render animation'
    kma = bpy.context.window_manager.keyconfigs.addon.keymaps['Screen']
    for kmi in kma.keymap_items:
        if kmi.idname == 'render.render_view' or kmi.idname == 'render.render_animation' \
        or kmi.idname == 'render.render_still':
            kma.keymap_items.remove(kmi)
    bpy.utils.unregister_module(__name__)
    bpy.app.handlers.load_post.remove(load_handler)


if __name__ == '__main__':
    register()
