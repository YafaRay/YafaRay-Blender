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

# TODO: Use Blender enumerators if any
import bpy
import os
import libyafaray4_bindings
from .. import YAF_ID_NAME

yaf_logger = libyafaray4_bindings.Logger()
yaf_logger.setConsoleVerbosityLevel(yaf_logger.logLevelFromString("debug"))
yaf_logger.setLogVerbosityLevel(yaf_logger.logLevelFromString("debug"))

class RenderEngine(bpy.types.RenderEngine):
    bl_idname = YAF_ID_NAME
    bl_use_preview = True
    bl_label = "YafaRay v4 Render"
    prog = 0.0
    tag = ""

    def __init__(self):
        self.yaf_logger = yaf_logger
        print("__init__", self)

    # callback to export the scene
    def update(self, bl_data, bl_depsgraph):
        self.update_stats("", "Setting up render")
        print("update", self, bl_data, bl_depsgraph)

    # callback to render scene
    def render(self, bl_depsgraph):
        self.update_stats("", "Done!")
        print("render", self, bl_depsgraph)


classes = (
    RenderEngine,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":  # only for live edit.
    import bpy

    bpy.utils.register_module(__name__)
