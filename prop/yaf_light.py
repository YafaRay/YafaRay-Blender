import bpy
from bpy.props import (EnumProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       StringProperty)

Lamp = bpy.types.Lamp


def call_lighttype_update(self, context):
        lamp = context.lamp
        switchLampType = {'area': 'AREA', 'spot': 'SPOT', 'sun': 'SUN', 'point': 'POINT', 'ies': 'SPOT'}
        lamp.type = switchLampType.get(lamp.lamp_type)


def register():
    Lamp.lamp_type = EnumProperty(
        name="Light type",
        description="Type of lamp",
        items=(
            ('point', "Point", "Omnidirectional point light source"),
            ('sun', "Sun", "Constant direction parallel ray light source"),
            ('spot', "Spot", "Directional cone light source"),
            ('ies', "IES", "Directional cone light source from ies file"),
            ('area', "Area", "Directional area light source")
        ),
        default="point", update=call_lighttype_update)

    Lamp.yaf_energy = FloatProperty(
        name="Power",
        description="Intensity multiplier for color",
        min=0.0, max=10000.0,
        default=1.0)

    Lamp.directional = BoolProperty(
        name="Directional",
        description="",
        default=False)

    Lamp.create_geometry = BoolProperty(
        name="Create geometry",
        description="Creates a visible geometry in the dimensions of the light during the render",
        default=False)

    Lamp.infinite = BoolProperty(
        name="Infinite",
        description="Determines if light is infinite or filling a semi-infinite cylinder",
        default=True)

    Lamp.spot_soft_shadows = BoolProperty(
        name="Soft shadows",
        description="Use soft shadows",
        default=False)

    Lamp.shadow_fuzzyness = FloatProperty(
        name="Shadow fuzzyness",
        description="Fuzzyness of the soft shadows (0 - hard shadow, 1 - fuzzy shadow)",
        min=0.0, max=1.0,
        default=1.0)

    Lamp.photon_only = BoolProperty(
        name="Photon only",
        description="This spot will only throw photons not direct light",
        default=False)

    Lamp.angle = FloatProperty(
        name="Angle",
        description="Angle of the cone in degrees (shadow softness)",
        min=0.0, max=80.0,
        default=0.5)

    Lamp.ies_soft_shadows = BoolProperty(
        name="IES Soft shadows",
        description="Use soft shadows for IES light type",
        default=False)

    Lamp.ies_file = StringProperty(
        name="IES File",
        description="File to be used as the light projection",
        subtype='FILE_PATH',
        default="")

    Lamp.yaf_samples = IntProperty(
        name="Samples",
        description="Number of samples to be taken for direct lighting",
        min=0, max=512,
        default=16)


def unregister():
    del Lamp.lamp_type
    del Lamp.yaf_energy
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
