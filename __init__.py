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

# Version to be automatically populated during the build process, getting the version from git tags
# for example:
# sed -i "s/(devel)/$(git --git-dir=/yafaray/src/Blender-Exporter/.git --work-tree=/yafaray/src/Blender-Exporter describe --dirty --always --tags)/g" "/yafaray/linux/build/yafaray_v3/__init__.py"
YAFARAY_EXPORTER_VERSION = "(devel)"

sys.path.append(BIN_PATH)

bl_info = {
    "name": "YafaRay v3 Exporter",
    "description": "YafaRay integration for blender",
    "author": "Shuvro Sarker, Kim Skoglund (Kerbox), Pedro Alcaide (povmaniaco),"
              "Paulo Gomes (tuga3d), Michele Castigliego (subcomandante),"
              "Bert Buchholz, Rodrigo Placencia (DarkTide),"
              "Alexander Smirnov (Exvion), Olaf Arnold (olaf), David Bluecame",
    # Version to be automatically populated during the build process, getting the version from git tags
    # for example:
    # sed -i "s/(devel)/$(git --git-dir=/yafaray/src/Blender-Exporter/.git --work-tree=/yafaray/src/Blender-Exporter describe --dirty --always --tags)/g" "/yafaray/linux/build/yafaray_v3/__init__.py"
    "version": ("(devel)", ""),
    "blender": (2, 7, 8),
    "location": "Info Header > Engine dropdown menu",
    "wiki_url": "http://www.yafaray.org/community/forum",
    "tracker_url": "http://www.yafaray.org/development/bugtracker/yafaray",
    "category": "Render"
    }

# Set Library Search options
if sys.platform == 'win32':   #I think this is the easiest and most flexible way to set the search options for Windows DLL
    os.environ['PATH'] = os.path.dirname(__file__) + '\\bin;' + os.environ['PATH']
# For Linux and MacOSX, set the RPATH in all the .so and .dylib libraries to relative paths respect to their location 


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

class YafaRay_Preferences(AddonPreferences):
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
    bpy.utils.register_class(YafaRay_Preferences)
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


if __name__ == '__main__':
    register()
