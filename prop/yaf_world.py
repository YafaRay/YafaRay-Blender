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


def register():
    ########### YafaRays world background properties #############
    World.bg_type = EnumProperty(
        name="Background",
        items=(
            ('Gradient', "Gradient", "Gradient background"),
            ('Texture', "Texture", "Textured background"),
            ('Sunsky1', "Sunsky1", "Sunsky background"),
            ('Sunsky2', "Sunsky2", "New model of Sunsky background"),
            ('Single Color', "Single Color", "Single color background")
        ),
        default="Single Color")

    World.bg_color_space = EnumProperty(
        name="Color space",
        items=(
            ('CIE (E)', "CIE (E)", "Select color space model"),
            ('CIE (D50)', "CIE (D50)", "Select color space model"),
            ('sRGB (D65)', "sRGB (D65)", "Select color space model"),
            ('sRGB (D50)', "sRGB (D50)", "Select color space model")
        ),
        default="CIE (E)")

    World.bg_zenith_color = FloatVectorProperty(
        name="Zenith color",
        description="Zenith color",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(0.57, 0.65, 1.0))

    World.bg_horizon_color = FloatVectorProperty(
        name="Horizon color",
        description="Horizon color",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 1.0, 0.5))

    World.bg_zenith_ground_color = FloatVectorProperty(
        name="Zenith ground color",
        description="Zenith ground color",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 0.9, 0.8))

    World.bg_horizon_ground_color = FloatVectorProperty(
        name="Horizon ground color",
        description="Horizon ground color",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(0.8, 0.6, 0.3))

    World.bg_single_color = FloatVectorProperty(
        name="Background color",
        description="Background color",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(0.7, 0.7, 0.7))

    World.bg_use_ibl = BoolProperty(
        name="Use IBL",
        description="Use the background as the light source for your image",
        default=False)

    World.bg_with_caustic = BoolProperty(
        name="Caustic photons",
        description="Allow background light to shoot caustic photons",
        default=True)

    World.bg_with_diffuse = BoolProperty(
        name="Diffuse photons",
        description="Allow background light to shoot diffuse photons",
        default=True)

    World.bg_ibl_samples = IntProperty(
        name="IBL Samples",
        description="Number of samples for direct lighting from background",
        min=1, max=512,
        default=16)

    World.bg_rotation = FloatProperty(
        name="Rotation",
        description="Rotation offset of background texture",
        min=0.0, max=360.0,
        default=0.0)

    World.bg_turbidity = FloatProperty(
        name="Turbidity",
        description="Turbidity of the atmosphere",
        min=1.0, max=20.0,
        default=2.0)

    World.bg_ds_turbidity = FloatProperty(  # Darktides turbidity has different values
        name="Turbidity",
        description="Turbidity of the atmosphere",
        min=2.0, max=12.0,
        default=2.0)

    World.bg_a_var = FloatProperty(
        name="Brightness of horizon gradient",
        description="Darkening or brightening towards horizon",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_b_var = FloatProperty(
        name="Luminance of horizon",
        description="Luminance gradient near the horizon",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_c_var = FloatProperty(
        name="Solar region intensity",
        description="Relative intensity of circumsolar region",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_d_var = FloatProperty(
        name="Width of circumsolor region",
        description="Width of circumsolar region",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_e_var = FloatProperty(
        name="Backscattered light",
        description="Relative backscattered light",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_from = FloatVectorProperty(
        name="Set sun position",
        description="Set the position of the sun",
        subtype='DIRECTION',
        step=10, precision=3,
        min=-1.0, max=1.0,
        default=(1.0, 1.0, 1.0))

    World.bg_add_sun = BoolProperty(
        name="Add sun",
        description="Add a real sun light",
        default=False)

    World.bg_sun_power = FloatProperty(
        name="Sunlight power",
        description="Sunlight power",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_background_light = BoolProperty(
        name="Add skylight",
        description="Add skylight",
        default=False)

    World.bg_light_samples = IntProperty(
        name="Samples",
        description="Set skylight and sunlight samples",
        min=1, max=512,
        default=16)

    World.bg_dsaltitude = FloatProperty(
        name="Altitude",
        description="Moves the sky dome above or below the camera position",
        min=-1.0, max=2.0,
        default=0.0)

    World.bg_dsnight = BoolProperty(
        name="Night",
        description="Activate experimental night mode",
        default=False)

    World.bg_dsbright = FloatProperty(
        name="Sky brightness",
        description="Brightness of the sky",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_power = FloatProperty(
        name="Skylight power",
        description="Multiplier for background color",
        min=0.0,
        default=1.0)

    World.bg_exposure = FloatProperty(
        name="Exposure",
        description="Exposure correction for the sky (0 = no correction)",
        min=0.0, max=10.0,
        default=1.0)

    World.bg_clamp_rgb = BoolProperty(
        name="Clamp RGB",
        description="Clamp RGB values",
        default=False)

    World.bg_gamma_enc = BoolProperty(
        name="Gamma encoding",
        description="Apply gamma encoding to the sky",
        default=True)

    ########### YafaRays volume integrator properties #############
    World.v_int_type = EnumProperty(
        name="Volume integrator",
        description="Set the volume integrator",
        items=(
            ('None', "None", ""),
            ('Sky', "Sky", ""),
            ('Single Scatter', "Single Scatter", "")
        ),
        default='None')

    World.v_int_step_size = FloatProperty(
        name="Step size",
        description="Precision of volumetric rendering (in Blender units)",
        min=0.0, max=100.0,
        precision=3,
        default=1.000)

    World.v_int_adaptive = BoolProperty(
        name="Adaptive",
        description="Optimizes stepping calculations for NoiseVolumes",
        default=False)

    World.v_int_optimize = BoolProperty(
        name="Optimize",
        description="Precomputing attenuation in the entire volume at a 3d grid of points",
        default=False)

    World.v_int_attgridres = IntProperty(
        name="Att. grid resolution",
        description="Optimization attenuation grid resolution",
        min=1, max=50,
        default=1)

    # ??? not sure about the following properties ???
    World.v_int_scale = FloatProperty(
        name="Sigma T",
        min=0.0, precision=3,
        description="",
        default=0.100)

    World.v_int_alpha = FloatProperty(
        name="Alpha",
        min=0.0, precision=3,
        description="",
        default=0.500)

    World.v_int_dsturbidity = FloatProperty(
        name="Turbidity",
        description="",
        default=3.0)


def unregister():
    World.bg_type
    World.bg_color_space
    World.bg_zenith_color
    World.bg_horizon_color
    World.bg_zenith_ground_color
    World.bg_horizon_ground_color
    World.bg_single_color
    World.bg_use_ibl
    World.bg_with_caustic
    World.bg_with_diffuse
    World.bg_ibl_samples
    World.bg_rotation
    World.bg_turbidity
    World.bg_ds_turbidity
    World.bg_a_var
    World.bg_b_var
    World.bg_c_var
    World.bg_d_var
    World.bg_e_var
    World.bg_from
    World.bg_add_sun
    World.bg_sun_power
    World.bg_background_light
    World.bg_light_samples
    World.bg_dsaltitude
    World.bg_dsnight
    World.bg_dsbright
    World.bg_power
    World.bg_exposure
    World.bg_clamp_rgb
    World.bg_gamma_enc

    World.v_int_type
    World.v_int_step_size
    World.v_int_adaptive
    World.v_int_optimize
    World.v_int_attgridres
    World.v_int_scale
    World.v_int_alpha
    World.v_int_dsturbidity
