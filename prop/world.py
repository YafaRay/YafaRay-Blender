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
                       FloatProperty,
                       FloatVectorProperty,
                       IntProperty,
                       BoolProperty)

World = bpy.types.World


def update_preview(self, context):
    context.world.use_sky_paper = context.world.use_sky_paper


def register():
    # YafaRay's world background properties
    World.bg_type = EnumProperty(
        update=update_preview, name="Background",
        items=(
            ('Gradient', "Gradient", "Gradient background"),
            ('Texture', "Texture", "Textured background"),
            ('Sunsky1', "Sunsky1", "Sunsky background"),
            ('Sunsky2', "Sunsky2", "New model of Sunsky background"),
            ('Single Color', "Single Color", "Single color background")
        ),
        default="Single Color")

    World.bg_color_space = EnumProperty(
        update=update_preview, name="Color space",
        items=(
            ('CIE (E)', "CIE (E)", "Select color space model"),
            ('CIE (D50)', "CIE (D50)", "Select color space model"),
            ('sRGB (D65)', "sRGB (D65)", "Select color space model"),
            ('sRGB (D50)', "sRGB (D50)", "Select color space model")
        ),
        default="CIE (E)")

    # povman test: create a list of YafaRay mapping modes
    # 
    World.yaf_mapworld_type = EnumProperty(
        update=update_preview, name="Mapping Type",
        items=(
            ('SPHERE', "Spherical", "Spherical mapping"),
            ('ANGMAP', "Angular", "Angular mapping")
        ),
        default='SPHERE')

    World.bg_zenith_color = FloatVectorProperty(
        update=update_preview, name="Zenith color",
        description="Zenith color",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(0.57, 0.65, 1.0))

    World.bg_horizon_color = FloatVectorProperty(
        update=update_preview, name="Horizon color",
        description="Horizon color",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 1.0, 0.5))

    World.bg_zenith_ground_color = FloatVectorProperty(
        update=update_preview, name="Zenith ground color",
        description="Zenith ground color",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 0.9, 0.8))

    World.bg_horizon_ground_color = FloatVectorProperty(
        update=update_preview, name="Horizon ground color",
        description="Horizon ground color",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(0.8, 0.6, 0.3))

    World.bg_single_color = FloatVectorProperty(
        update=update_preview, name="Background color",
        description="Background color",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(0.7, 0.7, 0.7))

    World.bg_use_ibl = BoolProperty(
        update=update_preview, name="Use IBL",
        description="Use the background as the light source for your image",
        default=False)

    World.bg_smartibl_blur = FloatProperty(
        update=update_preview, name="SmartIBL Blur factor",
        description="SmartIBL blur factor to reduce noise. This only blurs the lighting and shadows, keeping the reflections sharp. High values allow less noise but might be less realistic and cause slowdowns",
        min=0.00, max=0.75, precision=2, default=0.00)

    World.ibl_clamp_sampling = FloatProperty(
        update=update_preview, name="IBL clamp sampling",
        description="Trick to reduce light sampling noise at the expense of realism and inexact overall light. The lower, the less noise but worse realism and lighting. 0.f disables clamping (default).",
        min=0.00, precision=2, default=0.00)

    World.bg_with_caustic = BoolProperty(
        update=update_preview, name="Caustic photons",
        description="Allow background light to shoot caustic photons",
        default=True)

    World.bg_with_diffuse = BoolProperty(
        update=update_preview, name="Diffuse photons",
        description="Allow background light to shoot diffuse photons",
        default=True)

    World.bg_ibl_samples = IntProperty(
        update=update_preview, name="IBL Samples",
        description="Number of samples for direct lighting from background",
        min=1, max=512,
        default=16)

    World.bg_rotation = FloatProperty(
        update=update_preview, name="Rotation",
        description="Rotation offset of background texture",
        min=0.0, max=360.0,
        default=0.0)

    World.bg_turbidity = FloatProperty(
        update=update_preview, name="Turbidity",
        description="Turbidity of the atmosphere",
        min=1.0, max=20.0,
        default=2.0)

    World.bg_ds_turbidity = FloatProperty(  # Darktides turbidity has different values
        update=update_preview, name="Turbidity",
        description="Turbidity of the atmosphere",
        min=2.0, max=12.0,
        default=2.0)

    World.bg_a_var = FloatProperty(
        update=update_preview, name="Brightness of horizon gradient",
        description="Darkening or brightening towards horizon",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_b_var = FloatProperty(
        update=update_preview, name="Luminance of horizon",
        description="Luminance gradient near the horizon",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_c_var = FloatProperty(
        update=update_preview, name="Solar region intensity",
        description="Relative intensity of circumsolar region",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_d_var = FloatProperty(
        update=update_preview, name="Width of circumsolor region",
        description="Width of circumsolar region",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_e_var = FloatProperty(
        update=update_preview, name="Backscattered light",
        description="Relative backscattered light",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_from = FloatVectorProperty(
        update=update_preview, name="Set sun position",
        description="Set the position of the sun",
        subtype='DIRECTION',
        step=10, precision=3,
        min=-1.0, max=1.0,
        default=(1.0, 1.0, 1.0))

    World.bg_add_sun = BoolProperty(
        update=update_preview, name="Add sun",
        description="Add a real sun light",
        default=False)

    World.bg_sun_power = FloatProperty(
        update=update_preview, name="Sunlight power",
        description="Sunlight power",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_background_light = BoolProperty(
        update=update_preview, name="Add skylight",
        description="Add skylight",
        default=False)

    World.bg_light_samples = IntProperty(
        update=update_preview, name="Samples",
        description="Set skylight and sunlight samples",
        min=1, max=512,
        default=16)

    World.bg_dsaltitude = FloatProperty(
        update=update_preview, name="Altitude",
        description="Moves the sky dome above or below the camera position",
        min=-1.0, max=2.0,
        default=0.0)

    World.bg_dsnight = BoolProperty(
        update=update_preview, name="Night",
        description="Activate experimental night mode",
        default=False)

    World.bg_dsbright = FloatProperty(
        update=update_preview, name="Sky brightness",
        description="Brightness of the sky",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_power = FloatProperty(
        update=update_preview, name="Skylight power",
        description="Multiplier for background color",
        min=0.0,
        default=1.0)

    World.bg_exposure = FloatProperty(
        update=update_preview, name="Exposure",
        description="Exposure correction for the sky (0 = no correction)",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_clamp_rgb = BoolProperty(
        update=update_preview, name="Clamp RGB",
        description="Clamp RGB values",
        default=False)

    World.bg_gamma_enc = BoolProperty(
        update=update_preview, name="Gamma encoding",
        description="Apply gamma encoding to the sky",
        default=True)

    World.bg_cast_shadows = BoolProperty(
        update=update_preview, name="Background cast shadows",
        description="Enable casting shadows from the Background environmental lighting. This is the normal and expected behavior. Disable it only for special cases!",
        default=True)

    World.bg_cast_shadows_sun = BoolProperty(
        update=update_preview, name="Sun cast shadows",
        description="Enable casting shadows from the Background Sun lighting. This is the normal and expected behavior. Disable it only for special cases!",
        default=True)

    # YafaRay's volume integrator properties
    World.v_int_type = EnumProperty(
        update=update_preview, name="Volume integrator",
        description="Set the volume integrator",
        items=(
            ('None', "None", ""),
            ('Sky', "Sky", ""),
            ('Single Scatter', "Single Scatter", "")
        ),
        default='None')

    World.v_int_step_size = FloatProperty(
        update=update_preview, name="Step size",
        description="Precision of volumetric rendering (in Blender units)",
        min=0.0, max=100.0,
        precision=3,
        default=1.000)

    World.v_int_adaptive = BoolProperty(
        update=update_preview, name="Adaptive",
        description="Optimizes stepping calculations for NoiseVolumes",
        default=False)

    World.v_int_optimize = BoolProperty(
        update=update_preview, name="Optimize",
        description="Precomputing attenuation in the entire volume at a 3d grid of points",
        default=False)

    World.v_int_attgridres = IntProperty(
        update=update_preview, name="Att. grid resolution",
        description="Optimization attenuation grid resolution",
        min=1, max=50,
        default=1)

    # ??? not sure about the following properties ???
    World.v_int_scale = FloatProperty(
        update=update_preview, name="Sigma T",
        min=0.0, precision=3,
        description="",
        default=0.100)

    World.v_int_alpha = FloatProperty(
        update=update_preview, name="Alpha",
        min=0.0, precision=3,
        description="",
        default=0.500)

    World.v_int_dsturbidity = FloatProperty(
        update=update_preview, name="Turbidity",
        description="",
        default=3.0)


def unregister():
    del World.bg_type
    del World.bg_color_space
    del World.bg_zenith_color
    del World.bg_horizon_color
    del World.bg_zenith_ground_color
    del World.bg_horizon_ground_color
    del World.bg_single_color
    del World.bg_use_ibl
    del World.bg_smartibl_blur
    del World.ibl_clamp_sampling
    del World.bg_with_caustic
    del World.bg_with_diffuse
    del World.bg_ibl_samples
    del World.bg_rotation
    del World.bg_turbidity
    del World.bg_ds_turbidity
    del World.bg_a_var
    del World.bg_b_var
    del World.bg_c_var
    del World.bg_d_var
    del World.bg_e_var
    del World.bg_from
    del World.bg_add_sun
    del World.bg_sun_power
    del World.bg_background_light
    del World.bg_light_samples
    del World.bg_dsaltitude
    del World.bg_dsnight
    del World.bg_dsbright
    del World.bg_exposure
    del World.bg_power
    del World.bg_clamp_rgb
    del World.bg_gamma_enc
    del World.bg_cast_shadows
    del World.bg_cast_shadows_sun

    del World.v_int_type
    del World.v_int_step_size
    del World.v_int_adaptive
    del World.v_int_optimize
    del World.v_int_attgridres
    del World.v_int_scale
    del World.v_int_alpha
    del World.v_int_dsturbidity

    # povman test --->
    del World.yaf_mapworld_type
