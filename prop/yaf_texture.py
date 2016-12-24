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

import math
import bpy
from bpy.props import (EnumProperty,
                       BoolProperty,
                       FloatProperty)

Texture = bpy.types.Texture

def update_preview(self, context):
    context.texture.saturation = context.texture.saturation

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
        update=update_preview, name="Use map as normal map",
        description="Use image RGB values for normal mapping",
        default=False)
    #test
    Texture.yaf_use_alpha = BoolProperty(
        update=update_preview, name="Use alpha image info",
        description="Use alpha values for image mapping",
        default=False)
        
    Texture.yaf_gamma_input = FloatProperty(
        update=update_preview, name="Gamma input",
        description="Gamma correction applied to input texture",
        min=0, max=5, default=1.0)

    Texture.yaf_tex_interpolate = EnumProperty(
        update=update_preview, name="Interpolation",
        items=(
            ('bilinear', "Bilinear (default)", ""),
            ('bicubic', "Bicubic", ""),
            ('none', "No interpolation", ""),
            ('mipmap_trilinear', "Mipmaps - trilinear", "Mipmaps generation, trilinear interpolation (faster but lower quality)"),
            ('mipmap_ewa', "Mipmaps - EWA", "Mipmaps generation, EWA interpolation (slower but higher quality)")            
        ),
        default='bilinear')
        
    Texture.yaf_tex_optimization = EnumProperty(
        name="Optimization",
        description="Texture optimization to reduce RAM usage",
        items=(
            ('compressed', "Compressed", "Lossy color compression, some color/transparency details will be lost, more RAM improvement"),
            ('optimized', "Optimized", "Lossless optimization, good RAM improvement"),
            ('none', "None", "No optimization, lossless and faster but high RAM usage"),
            ('default', "Default", "Use global texture optimization setting from the Render tab")
        ),
        default='default')

    Texture.yaf_adj_hue = FloatProperty(
        update=update_preview, name="Hue adjustment",
        description="Hue adjustment for the texture",
        min=math.radians(-360), max=math.radians(360),
        subtype="ANGLE", unit="ROTATION",
        default=0.0, precision=1)
        
    Texture.yaf_mipmapleveltest = FloatProperty(
        update=update_preview, name="mipmapleveltest",
        description="mipmapleveltest",
        min=0, default=0.0)

    Texture.yaf_img_grayscale = BoolProperty(
        update=update_preview, name="Use as Grayscale",
        description="Convert internally to Grayscale to reduce memory usage for bump or mask textures, for example",
        default=False)

def unregister():
    Texture.yaf_tex_type
    Texture.yaf_is_normal_map
    Texture.yaf_use_alpha
    Texture.yaf_gamma_input
    Texture.yaf_tex_interpolate
    Texture.yaf_tex_optimization
    Texture.yaf_adj_hue
    Texture.yaf_mipmapleveltest
    Texture.yaf_img_grayscale
