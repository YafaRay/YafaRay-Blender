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
from bpy.props import (EnumProperty,
                       BoolProperty)

Texture = bpy.types.Texture


# try to update blender propertie texture.type to YafaRay's texture.yaf_tex_type
def call_tex_type_update(self, context):
    try:
        tex = context.texture
        if tex is not None:
            tex.type = tex.yaf_tex_type
    except:
        pass


def register():
    Texture.yaf_tex_type = EnumProperty(
        name="Type",
        items=(
            ('NONE', "None", ""),
            ('BLEND', "Blend", ""),
            ('CLOUDS', "Clouds", ""),
            ('WOOD', "Wood", ""),
            ('MARBLE', "Marble", ""),
            ('VORONOI', "Voronoi", ""),
            ('MUSGRAVE', "Musgrave", ""),
            ('DISTORTED_NOISE', "Distorted Noise", ""),
            ('IMAGE', "Image", "")
        ),
        update=call_tex_type_update,
        default='NONE')

    Texture.yaf_is_normal_map = BoolProperty(
        name="Use map as normal map",
        description="Use image RGB values for normal mapping",
        default=False)


def unregister():
    Texture.yaf_tex_type
    Texture.yaf_is_normal_map
