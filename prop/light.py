# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.props import (EnumProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       StringProperty)

if bpy.app.version >= (2, 80, 0):
    Light = bpy.types.Light
else:
    Light = bpy.types.Lamp


# noinspection PyUnusedLocal
def update_preview(self, context):
    if bpy.app.version >= (2, 80, 0):
        light = context.light
    else:
        light = context.lamp
    light.update_tag()


# noinspection PyUnusedLocal
def call_light_type_update(self, context):
    if bpy.app.version >= (2, 80, 0):
        light = context.light
    else:
        light = context.lamp
    if light is not None:
        switch_light_type = {'area': 'AREA', 'spot': 'SPOT', 'sun': 'SUN', 'point': 'POINT', 'ies': 'SPOT',
                             'directional': 'SUN'}
        light.type = switch_light_type.get(light.lamp_type)


# noinspection PyUnusedLocal
def set_shadow_method(self, context):
    if bpy.app.version >= (2, 80, 0):
        light = context.light
    else:
        light = context.lamp
    if light.yaf_show_dist_clip:
        light.shadow_method = 'BUFFER_SHADOW'
    else:
        light.shadow_method = 'RAY_SHADOW'
    light.type = light.type


# noinspection PyUnusedLocal
def sync_with_distance(self, context):
    if bpy.app.version >= (2, 80, 0):
        light = context.light
    else:
        light = context.lamp
    if light.yaf_sphere_radius != light.distance:
        light.distance = light.yaf_sphere_radius
    light.type = light.type


def register():
    Light.lamp_type = EnumProperty(
        name="Light type",
        description="Type of light",
        items=[
            ('point', "Point", "Omnidirectional point light source"),
            ('sun', "Sun", "Constant direction parallel ray light source"),
            ('spot', "Spot", "Directional cone light source"),
            ('ies', "IES", "Directional cone light source from ies file"),
            ('area', "Area", "Directional area light source"),
            ('directional', "Directional", "Directional Sun light")
        ],
        default="point", update=call_light_type_update)

    Light.yaf_energy = FloatProperty(
        update=update_preview, name="Power",
        description="Intensity multiplier for color",
        min=0.0, max=10000.0,
        default=1.0)

    Light.yaf_sphere_radius = FloatProperty(
        name="Radius",
        description="Radius of the sphere light",
        min=0.01, max=10000.0,
        soft_min=0.01, soft_max=100.0,
        default=1.0, update=sync_with_distance)

    Light.directional = BoolProperty(
        update=update_preview, name="Directional",
        description="Directional sunlight type, like 'spot' (for concentrate photons at area)",
        default=False)

    Light.create_geometry = BoolProperty(
        update=update_preview, name="Create and show geometry",
        description="Creates a visible geometry in the dimensions of the light during the render",
        default=False)

    Light.infinite = BoolProperty(
        update=update_preview, name="Infinite",
        description="Determines if light is infinite or filling a semi-infinite cylinder",
        default=True)

    Light.spot_soft_shadows = BoolProperty(
        update=update_preview, name="Soft shadows",
        description="Use soft shadows",
        default=False)

    Light.shadow_fuzzyness = FloatProperty(
        update=update_preview, name="Shadow fuzzyness",
        description="Fuzzyness of the soft shadows (0 - hard shadow, 1 - fuzzy shadow)",
        min=0.0, max=1.0,
        default=1.0)

    Light.photon_only = BoolProperty(
        update=update_preview, name="Photon only",
        description="This spot will only throw photons not direct light",
        default=False)

    Light.angle = FloatProperty(
        update=update_preview, name="Angle",
        description="Angle of the cone in degrees (shadow softness)",
        min=0.0, max=80.0,
        default=0.5)

    Light.ies_soft_shadows = BoolProperty(
        update=update_preview, name="IES Soft shadows",
        description="Use soft shadows for IES light type",
        default=False)

    Light.ies_file = StringProperty(
        update=update_preview, name="IES File",
        description="File to be used as the light projection",
        subtype='FILE_PATH',
        default="")

    Light.yaf_samples = IntProperty(
        update=update_preview, name="Samples",
        description="Number of samples to be taken for direct lighting",
        min=0, max=512,
        default=16)

    Light.yaf_show_dist_clip = BoolProperty(
        name="Show distance and clipping",
        description="Show distance, clip start and clip end settings for spot light in 3D view",
        default=False, update=set_shadow_method)

    Light.light_enabled = BoolProperty(
        update=update_preview, name="Light enabled",
        description="Enable/Disable light",
        default=True)

    Light.cast_shadows = BoolProperty(
        update=update_preview, name="Cast shadows",
        description="Enable casting shadows. This is the normal and expected behavior."
                    "Disable it only for special cases!",
        default=True)

    Light.caustic_photons = BoolProperty(
        update=update_preview, name="Caustic photons",
        description="Allow light to shoot caustic photons",
        default=True)

    Light.diffuse_photons = BoolProperty(
        update=update_preview, name="Diffuse photons",
        description="Allow light to shoot diffuse photons",
        default=True)


def unregister():
    del Light.lamp_type
    del Light.yaf_energy
    del Light.yaf_sphere_radius
    del Light.directional
    del Light.create_geometry
    del Light.infinite
    del Light.spot_soft_shadows
    del Light.shadow_fuzzyness
    del Light.photon_only
    del Light.angle
    del Light.ies_soft_shadows
    del Light.ies_file
    del Light.yaf_samples
    del Light.yaf_show_dist_clip
    del Light.light_enabled
    del Light.cast_shadows
    del Light.caustic_photons
    del Light.diffuse_photons
