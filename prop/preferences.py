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

import bpy
from bpy.types import AddonPreferences
from bpy.props import IntProperty
from .. import BASE_PACKAGE_NAME

class Preferences(AddonPreferences):
    bl_idname = BASE_PACKAGE_NAME

    yafaray_computer_node = IntProperty(
        name="YafaRay computer node",
        description='Computer node number in multi-computer render environments / render farms',
        default=0, min=0, max=1000
    )

    def draw(self, bl_context):
        layout = self.layout
        split = layout.split()
        col = split.column()
        col.prop(self, "yafaray_computer_node")
        col = col.column()
        col.label(text="Click bottom left \"Save & Load\"->\"Save Preferences\" to apply changes permanently!", icon="INFO")


classes = (
    Preferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
