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
YAF_ID_NAME = "YAFA_V3_RENDER"

sys.path.append(BIN_PATH)

bl_info = {
    "name": "YafaRay v3 Exporter",
    "description": "YafaRay integration for blender",
    "author": "Shuvro Sarker, Kim Skoglund (Kerbox), Pedro Alcaide (povmaniaco),"
              "Paulo Gomes (tuga3d), Michele Castigliego (subcomandante),"
              "Bert Buchholz, Rodrigo Placencia (DarkTide),"
              "Alexander Smirnov (Exvion), Olaf Arnold (olaf), David Bluecame",
    "version": (3, 0, 0, "ALPHA6"),
    "blender": (2, 7, 7),
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
            if file in {'yafaray_v3_core.dll'}:
                dllArray = ['zlib1', 'libiconv.64.dll', 'zlib.64.dll', 'libpng15', 'libxml2.64.dll', 'yafaray_v3_core', 'yafaray_v3_plugin']
                break
            # load dll's from a MinGW64 installation
            else:
                dllArray = ['libwinpthread-1', 'libgcc_s_seh-1', 'libstdc++-6', 'libiconv-2', 'libzlib1', 'libxml2-2', 'libHalf', 'libIex', 'libImath', 'libIlmThread', 'libIlmImf', 'libjpeg-8', 'libpng16', 'libtiff-5', 'libbz2-1', 'libfreetype-6', 'libboost_system-mt', 'libboost_filesystem-mt', 'libboost_serialization-mt', 'libyafaray_v3_core', 'libyafaray_v3_plugin']

    else:    # Windows 32bit system
        for file in os.listdir(BIN_PATH):
            # load dll's from a MSVC installation
            if file in {'yafaray_v3_core.dll'}:
                dllArray = ['zlib1', 'iconv', 'zlib', 'libpng15', 'libxml2', 'yafaray_v3_core', 'yafaray_v3_plugin']
                break
            # load dll's from a MinGW32 installation
            else:
                dllArray = ['libwinpthread-1', 'libgcc_s_sjlj-1', 'libstdc++-6', 'libiconv-2', 'libzlib1', 'libxml2-2', 'libHalf', 'libIex', 'libImath', 'libIlmThread', 'libIlmImf', 'libjpeg-8', 'libpng16', 'libtiff-5', 'libbz2-1', 'libfreetype-6', 'libboost_system-mt', 'libboost_filesystem-mt', 'libboost_serialization-mt', 'libyafaray_v3_core', 'libyafaray_v3_plugin']

elif sys.platform == 'darwin':
    dllArray = ['libyafaray_v3_core.dylib', 'libyafaray_v3_plugin.dylib']
else:
    if sys.maxsize == 2**63 - 1:    # Linux 64bit system
        dllArray = ['libHalf.so', 'libIex.so', 'libImath.so', 'libIlmThread.so', 'libIlmImf.so', 'libpython3.5m.so', 'libjpeg.so', 'libz.so', 'libpng12.so', 'libjbig.so', 'libtiff.so', 'libfreetype.so', 'libboost_system.so', 'libboost_filesystem.so', 'libboost_serialization.so', 'libyafaray_v3_core.so', 'libyafaray_v3_plugin.so']

    else:   # Linux 32bit system
        dllArray = ['libHalf.so', 'libIex.so', 'libImath.so', 'libIlmThread.so', 'libIlmImf.so', 'libpython3.5m.so', 'libjpeg.so', 'libz.so', 'libpng12.so', 'libjbig.so', 'libtiff.so', 'libfreetype.so', 'libboost_system.so', 'libboost_filesystem.so', 'libboost_serialization.so', 'libyafaray_v3_core.so', 'libyafaray_v3_plugin.so']

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
    from bpy.types import AddonPreferences
    from bpy.props import IntProperty

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

class YafaRay_v3_Preferences(AddonPreferences):
    bl_idname = __name__

    yafaray_computer_node = IntProperty(
        name="YafaRay computer node",
        description='Computer node number in multi-computer render environments / render farms',
        default=0, min=0, max=1000
    )

    def draw(self, context):
        layout = self.layout
        split = layout.split()
        col = split.column()
        col.prop(self, "yafaray_computer_node")
        col = col.column()
        col.label("Click Save User Settings below to store the changes permanently in YafaRay!", icon="INFO")

def register():
    bpy.utils.register_class(YafaRay_v3_Preferences)
    prop.register()
    bpy.utils.register_module(__name__)
    bpy.app.handlers.load_post.append(load_handler)
    # register keys for 'render 3d view', 'render still' and 'render animation'
    if bpy.context.window_manager.keyconfigs.addon is not None:
        km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name='Screen')
        kmi = km.keymap_items.new('render.render_view', 'F12', 'PRESS', False, False, False, True)
        kmi = km.keymap_items.new('render.render_animation', 'F12', 'PRESS', False, False, True, False)
        kmi = km.keymap_items.new('render.render_still', 'F12', 'PRESS', False, False, False, False)


def unregister():
    prop.unregister()
    # unregister keys for 'render 3d view', 'render still' and 'render animation'
    if bpy.context.window_manager.keyconfigs.addon is not None:
        kma = bpy.context.window_manager.keyconfigs.addon.keymaps['Screen']
        for kmi in kma.keymap_items:
            if kmi.idname == 'render.render_view' or kmi.idname == 'render.render_animation' \
            or kmi.idname == 'render.render_still':
                kma.keymap_items.remove(kmi)
    bpy.utils.unregister_module(__name__)
    bpy.app.handlers.load_post.remove(load_handler)
    bpy.utils.unregister_class(YafaRay_v3_Preferences)



if __name__ == '__main__':
    register()
