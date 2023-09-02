# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.props import (
    IntProperty,
    FloatVectorProperty,
    StringProperty,
    BoolProperty,
    FloatProperty,
    EnumProperty,
    PointerProperty,
)

from ..util.properties_annotations import replace_properties_with_annotations


# Class for migrating MaterialTextureSlot from Blender 2.79 into YafaRay, so they can be used in Blender 2.80+
# even after Blender 2.80 has removed the inbuilt MaterialTextureSlot class
# The code from this class is based on the PovRay Blender Add-On

# noinspection PyTypeChecker
@replace_properties_with_annotations
class YafaRay4MaterialTextureSlot(bpy.types.PropertyGroup):

    texture = PointerProperty(
        name="Texture", description="", type=bpy.types.Texture
    )

    alpha_factor = FloatProperty(
        name="Alpha", description="Amount texture affects alpha", default=1.0
    )

    ambient_factor = FloatProperty(
        name="", description="Amount texture affects ambient", default=1.0
    )

    bump_method = EnumProperty(
        name="",
        description="Method to use for bump mapping",
        items=(
            ("BUMP_ORIGINAL", "Bump Original", ""),
            ("BUMP_COMPATIBLE", "Bump Compatible", ""),
            ("BUMP_DEFAULT", "Bump Default", ""),
            ("BUMP_BEST_QUALITY", "Bump Best Quality", ""),
            ("BUMP_LOW_QUALITY", "Bump Low Quality", ""),
        ),
        default="BUMP_ORIGINAL",
    )

    bump_objectspace = EnumProperty(
        name="",
        description="Space to apply bump mapping in",
        items=(
            ("BUMP_VIEWSPACE", "Bump Viewspace", ""),
            ("BUMP_OBJECTSPACE", "Bump Objectspace", ""),
            ("BUMP_TEXTURESPACE", "Bump Texturespace", ""),
        ),
        default="BUMP_VIEWSPACE",
    )

    density_factor = FloatProperty(
        name="", description="Amount texture affects density", default=1.0
    )

    diffuse_color_factor = FloatProperty(
        name="", description="Amount texture affects diffuse color", default=1.0
    )

    diffuse_factor = FloatProperty(
        name="", description="Amount texture affects diffuse reflectivity", default=1.0
    )

    displacement_factor = FloatProperty(
        name="", description="Amount texture displaces the surface", default=0.2
    )

    emission_color_factor = FloatProperty(
        name="", description="Amount texture affects emission color", default=1.0
    )

    emission_factor = FloatProperty(
        name="", description="Amount texture affects emission", default=1.0
    )

    emit_factor = FloatProperty(name="", description="Amount texture affects emission", default=1.0)

    hardness_factor = FloatProperty(
        name="", description="Amount texture affects hardness", default=1.0
    )

    mapping = EnumProperty(
        name="",
        description="",
        items=(
            ("FLAT", "Flat", ""),
            ("CUBE", "Cube", ""),
            ("TUBE", "Tube", ""),
            ("SPHERE", "Sphere", ""),
        ),
        default="FLAT",
    )

    mapping_x = EnumProperty(
        name="",
        description="",
        items=(("NONE", "", ""), ("X", "", ""), ("Y", "", ""), ("Z", "", "")),
        default="NONE",
    )

    mapping_y = EnumProperty(
        name="",
        description="",
        items=(("NONE", "", ""), ("X", "", ""), ("Y", "", ""), ("Z", "", "")),
        default="NONE",
    )

    mapping_z = EnumProperty(
        name="",
        description="",
        items=(("NONE", "", ""), ("X", "", ""), ("Y", "", ""), ("Z", "", "")),
        default="NONE",
    )

    mirror_factor = FloatProperty(
        name="", description="Amount texture affects mirror color", default=1.0
    )

    normal_factor = FloatProperty(
        name="", description="Amount texture affects normal values", default=1.0
    )

    normal_map_space = EnumProperty(
        name="",
        description="Sets space of normal map image",
        items=(
            ("CAMERA", "Camera", ""),
            ("WORLD", "World", ""),
            ("OBJECT", "Object", ""),
            ("TANGENT", "Tangent", ""),
        ),
        default="CAMERA",
    )

    object = PointerProperty(type=bpy.types.Object)

    raymir_factor = FloatProperty(
        name="", description="Amount texture affects ray mirror", default=1.0
    )

    reflection_color_factor = FloatProperty(
        name="", description="Amount texture affects color of out-scattered light", default=1.0
    )

    reflection_factor = FloatProperty(
        name="", description="Amount texture affects brightness of out-scattered light", default=1.0
    )

    scattering_factor = FloatProperty(
        name="", description="Amount texture affects scattering", default=1.0
    )

    specular_color_factor = FloatProperty(
        name="", description="Amount texture affects specular color", default=1.0
    )

    specular_factor = FloatProperty(
        name="", description="Amount texture affects specular reflectivity", default=1.0
    )

    offset = FloatVectorProperty(
        name="Offset",
        description="Fine tune of the texture mapping X, Y and Z locations ",
        precision=4,
        step=0.1,
        soft_min=-100.0,
        soft_max=100.0,
        default=(0.0, 0.0, 0.0),
        options={"ANIMATABLE"},
        subtype="TRANSLATION",
    )

    scale = FloatVectorProperty(
        name="Size",
        subtype="XYZ",
        size=3,
        description="Set scaling for the texture’s X, Y and Z sizes ",
        precision=4,
        step=0.1,
        soft_min=-100.0,
        soft_max=100.0,
        default=(1.0, 1.0, 1.0),
        options={"ANIMATABLE"},
    )

    texture_coords = EnumProperty(
        name="",
        description="",
        items=(
            ("GLOBAL", "Global", ""),
            ("OBJECT", "Object", ""),
            ("UV", "UV", ""),
            ("ORCO", "Original Coordinates", ""),
            ("STRAND", "Strand", ""),
            ("STICKY", "Sticky", ""),
            ("WINDOW", "Window", ""),
            ("NORMAL", "Normal", ""),
            ("REFLECTION", "Reflection", ""),
            ("STRESS", "Stress", ""),
            ("TANGENT", "Tangent", ""),
        ),
        default="GLOBAL",
    )

    translucency_factor = FloatProperty(
        name="", description="Amount texture affects translucency", default=1.0
    )

    transmission_color_factor = FloatProperty(
        name="",
        description="Amount texture affects result color after light has been scattered/absorbed",
        default=1.0,
    )

    use = BoolProperty(name="", description="Enable this material texture slot", default=True)

    use_from_dupli = BoolProperty(
        name="",
        description="Dupli’s instanced from verts, faces or particles, "
                    "inherit texture coordinate from their parent",
        default=False,
    )

    use_from_original = BoolProperty(
        name="",
        description="Dupli’s derive their object coordinates from the "
                    "original objects transformation",
        default=False,
    )

    use_interpolation = BoolProperty(
        name="", description="Interpolates pixels using selected filter ", default=False
    )

    use_map_alpha = BoolProperty(
        name="", description="Causes the texture to affect the alpha value", default=False
    )

    use_map_ambient = BoolProperty(
        name="", description="Causes the texture to affect the value of ambient", default=False
    )

    use_map_color_diffuse = BoolProperty(
        name="",
        description="Causes the texture to affect basic color of the material",
        default=True,
    )

    use_map_color_emission = BoolProperty(
        name="", description="Causes the texture to affect the color of emission", default=False
    )

    use_map_color_reflection = BoolProperty(
        name="",
        description="Causes the texture to affect the color of scattered light",
        default=False,
    )

    use_map_color_spec = BoolProperty(
        name="", description="Causes the texture to affect the specularity color", default=False
    )

    use_map_color_transmission = BoolProperty(
        name="",
        description="Causes the texture to affect the result color after "
                    "other light has been scattered/absorbed",
        default=False,
    )

    use_map_density = BoolProperty(
        name="", description="Causes the texture to affect the volume’s density", default=False
    )

    use_map_diffuse = BoolProperty(
        name="",
        description="Causes the texture to affect the value of the materials diffuse reflectivity",
        default=False,
    )

    use_map_displacement = BoolProperty(
        name="", description="Let the texture displace the surface", default=False
    )

    use_map_emission = BoolProperty(
        name="", description="Causes the texture to affect the volume’s emission", default=False
    )

    use_map_emit = BoolProperty(
        name="", description="Causes the texture to affect the emit value", default=False
    )

    use_map_hardness = BoolProperty(
        name="", description="Causes the texture to affect the hardness value", default=False
    )

    use_map_mirror = BoolProperty(
        name="", description="Causes the texture to affect the mirror color", default=False
    )

    use_map_normal = BoolProperty(
        name="", description="Causes the texture to affect the rendered normal", default=False
    )

    use_map_raymir = BoolProperty(
        name="", description="Causes the texture to affect the ray-mirror value", default=False
    )

    use_map_reflect = BoolProperty(
        name="",
        description="Causes the texture to affect the reflected light’s brightness",
        default=False,
    )

    use_map_scatter = BoolProperty(
        name="", description="Causes the texture to affect the volume’s scattering", default=False
    )

    use_map_specular = BoolProperty(
        name="",
        description="Causes the texture to affect the value of specular reflectivity",
        default=False,
    )

    use_map_translucency = BoolProperty(
        name="", description="Causes the texture to affect the translucency value", default=False
    )

    use_map_warp = BoolProperty(
        name="",
        description="Let the texture warp texture coordinates of next channels",
        default=False,
    )

    uv_layer = StringProperty(
        name="", description="UV layer to use for mapping with UV texture coordinates", default=""
    )

    warp_factor = FloatProperty(
        name="",
        description="Amount texture affects texture coordinates of next channels",
        default=0.0,
    )

    # ---------------------------------------------------------------- #
    # so that its for loop stays one level less nested
    # used_texture_slots generator expression requires :
    def __iter__(self):
        return self

    def __next__(self):
        tex = bpy.data.textures[self.texture]
        while tex.pov.active_texture_index < len(bpy.data.textures):  # XXX should use slots count
            tex.pov.active_texture_index += 1
        raise StopIteration
    # ---------------------------------------------------------------- #
