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
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       StringProperty)

Lamp = bpy.types.Lamp

def update_preview(self, context):
    context.lamp.type = context.lamp.type


def call_lighttype_update(self, context):
    lamp = context.lamp
    if lamp is not None:
        switchLampType = {'area': 'AREA', 'spot': 'SPOT', 'sun': 'SUN', 'point': 'POINT', 'ies': 'SPOT', 'directional': 'SUN'}
        lamp.type = switchLampType.get(lamp.lamp_type)


def set_shadow_method(self, context):
    lamp = context.lamp
    if lamp.yaf_show_dist_clip:
        lamp.shadow_method = 'BUFFER_SHADOW'
    else:
        lamp.shadow_method = 'RAY_SHADOW'
    context.lamp.type = context.lamp.type
    

def sync_with_distance(self, context):
    lamp = context.lamp
    if lamp.yaf_sphere_radius != lamp.distance:
        lamp.distance = lamp.yaf_sphere_radius
    context.lamp.type = context.lamp.type


def register():
    Lamp.lamp_type = EnumProperty(
        name="Light type",
        description="Type of lamp",
        items=(
            ('point', "Point", "Omnidirectional point light source"),
            ('sun', "Sun", "Constant direction parallel ray light source"),
            ('spot', "Spot", "Directional cone light source"),
            ('ies', "IES", "Directional cone light source from ies file"),
            ('area', "Area", "Directional area light source"),
            ('directional', "Directional", "Directional Sun light")
        ),
        default="point", update=call_lighttype_update)

    Lamp.yaf_energy = FloatProperty(
        update=update_preview, name="Power",
        description="Intensity multiplier for color",
        min=0.0, max=10000.0,
        default=1.0)

    Lamp.yaf_sphere_radius = FloatProperty(
        name="Radius",
        description="Radius of the sphere light",
        min=0.01, max=10000.0,
        soft_min=0.01, soft_max=100.0,
        default=1.0, update=sync_with_distance)

    Lamp.directional = BoolProperty(
        update=update_preview, name="Directional",
        description="Directional sunlight type, like 'spot' (for concentrate photons at area)",
        default=False)

    Lamp.create_geometry = BoolProperty(
        update=update_preview, name="Create and show geometry",
        description="Creates a visible geometry in the dimensions of the light during the render",
        default=False)

    Lamp.infinite = BoolProperty(
        update=update_preview, name="Infinite",
        description="Determines if light is infinite or filling a semi-infinite cylinder",
        default=True)

    Lamp.spot_soft_shadows = BoolProperty(
        update=update_preview, name="Soft shadows",
        description="Use soft shadows",
        default=False)

    Lamp.shadow_fuzzyness = FloatProperty(
        update=update_preview, name="Shadow fuzzyness",
        description="Fuzzyness of the soft shadows (0 - hard shadow, 1 - fuzzy shadow)",
        min=0.0, max=1.0,
        default=1.0)

    Lamp.photon_only = BoolProperty(
        update=update_preview, name="Photon only",
        description="This spot will only throw photons not direct light",
        default=False)

    Lamp.angle = FloatProperty(
        update=update_preview, name="Angle",
        description="Angle of the cone in degrees (shadow softness)",
        min=0.0, max=80.0,
        default=0.5)

    Lamp.ies_soft_shadows = BoolProperty(
        update=update_preview, name="IES Soft shadows",
        description="Use soft shadows for IES light type",
        default=False)

    Lamp.ies_file = StringProperty(
        update=update_preview, name="IES File",
        description="File to be used as the light projection",
        subtype='FILE_PATH',
        default="")

    Lamp.yaf_samples = IntProperty(
        update=update_preview, name="Samples",
        description="Number of samples to be taken for direct lighting",
        min=0, max=512,
        default=16)

    Lamp.yaf_show_dist_clip = BoolProperty(
        name="Show distance and clipping",
        description="Show distance, clip start and clip end settings for spot lamp in 3D view",
        default=False, update=set_shadow_method)

    Lamp.light_enabled = BoolProperty(
        update=update_preview, name="Light enabled",
        description="Enable/Disable light",
        default=True)
        
    Lamp.cast_shadows = BoolProperty(
        update=update_preview, name="Cast shadows",
        description="Enable casting shadows. This is the normal and expected behavior. Disable it only for special cases!",
        default=True)

    Lamp.caustic_photons = BoolProperty(
        update=update_preview, name="Caustic photons",
        description="Allow light to shoot caustic photons",
        default=True)

    Lamp.diffuse_photons = BoolProperty(
        update=update_preview, name="Diffuse photons",
        description="Allow light to shoot diffuse photons",
        default=True)

def unregister():
    del Lamp.lamp_type
    del Lamp.yaf_energy
    del Lamp.yaf_sphere_radius
    del Lamp.directional
    del Lamp.create_geometry
    del Lamp.infinite
    del Lamp.spot_soft_shadows
    del Lamp.shadow_fuzzyness
    del Lamp.photon_only
    del Lamp.angle
    del Lamp.ies_soft_shadows
    del Lamp.ies_file
    del Lamp.yaf_samples
    del Lamp.yaf_show_dist_clip
    del Lamp.light_enabled
    del Lamp.cast_shadows
    del Lamp.caustic_photons
    del Lamp.diffuse_photons
