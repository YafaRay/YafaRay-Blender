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

if bpy.app.version >= (2, 80, 0):
    icon_add = "ADD"
    icon_remove = "REMOVE"
else:
    icon_add = "ZOOMIN"
    icon_remove = "ZOOMOUT"

def ui_split(ui_item, factor):
    if bpy.app.version >= (2, 80, 0):
        return ui_item.split(factor=factor)
    else:
        return ui_item.split(percentage=factor)

def light_from_context(context):
    if bpy.app.version >= (2, 80, 0):
        return context.light
    else:
        return context.lamp

def material_from_context(context):
    if bpy.app.version >= (2, 80, 0):
        return context.material
    else:
        from bl_ui.properties_material import active_node_mat
        return active_node_mat(context.material)

def material_check(material):
    if bpy.app.version >= (2, 80, 0):
        return material
    else:
        from bl_ui.properties_material import check_material
        return check_material(material)