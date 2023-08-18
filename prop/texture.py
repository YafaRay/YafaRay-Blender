# SPDX-License-Identifier: GPL-2.0-or-later

import math

import bpy
from bpy.props import (EnumProperty,
                       BoolProperty,
                       FloatProperty)

Texture = bpy.types.Texture


# noinspection PyUnusedLocal
def update_preview(self, context):
    context.texture.update_tag()


# try to update Blender property texture.type to YafaRay's texture.yaf_tex_type
# noinspection PyUnusedLocal,PyBroadException
def call_tex_type_update(self, context):
    try:
        if context.space_data.texture_context == 'MATERIAL':
            tex = context.active_object.active_material.active_texture
        elif context.space_data.texture_context == 'WORLD':
            tex = context.scene.world.active_texture
        elif context.space_data.texture_context == 'OTHER':
            tex = context.scene.active_texture
        else:
            tex = None
        if tex is not None:
            tex.type = tex.yaf_tex_type
    except Exception:
        pass


def register():
    Texture.yaf_tex_type = EnumProperty(
        name="Type",
        items=[
            ('NONE', "None", ""),
            ('BLEND', "Blend", ""),
            ('CLOUDS', "Clouds", ""),
            ('WOOD', "Wood", ""),
            ('MARBLE', "Marble", ""),
            ('VORONOI', "Voronoi", ""),
            ('MUSGRAVE', "Musgrave", ""),
            ('DISTORTED_NOISE', "Distorted Noise", ""),
            ('IMAGE', "Image", "")
        ],
        update=call_tex_type_update,
        default='NONE')

    Texture.yaf_is_normal_map = BoolProperty(
        update=update_preview, name="Use map as normal map",
        description="Use image RGB values for normal mapping",
        default=False)
    # test
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
        items=[
            ('bilinear', "Bilinear (default)", ""),
            ('bicubic', "Bicubic", ""),
            ('none', "No interpolation", ""),
            ('mipmap_trilinear', "Mipmaps - trilinear",
             "Mipmaps generation, trilinear interpolation (faster but lower quality)"),
            ('mipmap_ewa', "Mipmaps - EWA", "Mipmaps generation, EWA interpolation (slower but higher quality)")
        ],
        default='bilinear')

    Texture.yaf_tex_optimization = EnumProperty(
        name="Optimization",
        description="Texture optimization to reduce RAM usage",
        items=[
            ('compressed', "Compressed",
             "Lossy color compression, some color/transparency details will be lost, more RAM improvement"),
            ('optimized', "Optimized", "Almost lossless optimization, good RAM improvement"),
            ('none', "None", "No optimization, lossless and faster but high RAM usage"),
            ('default', "Default", "Use global texture optimization setting from the Render tab")
        ],
        default='default')

    Texture.yaf_adj_hue = FloatProperty(
        update=update_preview, name="Hue adjustment",
        description="Hue adjustment for the texture",
        min=math.radians(-360), max=math.radians(360),
        subtype="ANGLE", unit="ROTATION",
        default=0.0, precision=1)

    Texture.yaf_trilinear_level_bias = FloatProperty(
        update=update_preview, name="Trilinear level bias",
        description="Negative values will choose higher resolution mipmaps than calculated, reducing the blurry "
                    "artifacts at the cost of increasing texture noise. Positive values will choose lower resolution "
                    "mipmaps than calculated. Default (and recommended) is 0.0 to use the calculated mipmaps as-is.",
        min=-1.0, max=1.0, default=0.0)

    Texture.yaf_ewa_max_anisotropy = FloatProperty(
        update=update_preview, name="EWA max anisotropy",
        description="Maximum anisotropy allowed for mipmap EWA algorithm. Higher values give better quality in "
                    "textures seen from an angle, but render will be slower. Lower values will give more speed but "
                    "lower quality in textures seen in an angle.",
        min=1.0, max=100.0, default=8.0)

    Texture.yaf_img_grayscale = BoolProperty(
        update=update_preview, name="Use as Grayscale",
        description="Convert internally to Grayscale to reduce memory usage for bump or mask textures, for example",
        default=False)


def unregister():
    del Texture.yaf_tex_type
    del Texture.yaf_is_normal_map
    del Texture.yaf_use_alpha
    del Texture.yaf_gamma_input
    del Texture.yaf_tex_interpolate
    del Texture.yaf_tex_optimization
    del Texture.yaf_adj_hue
    del Texture.yaf_trilinear_level_bias
    del Texture.yaf_ewa_max_anisotropy
    del Texture.yaf_img_grayscale
