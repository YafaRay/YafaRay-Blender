# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.props import (
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
# The code from this class uses as reference:
#   PovRay Blender Add-On
#   Blender 2.79b source code, especially "rna_texture.c" and "rna_material.c"


# noinspection PyUnusedLocal
def update_preview(self, context):
    if context is not None and context.space_data is not None:
        context.space_data.context = context.space_data.context  # To force redrawing the preview panel


# noinspection PyTypeChecker
@replace_properties_with_annotations
class YafaRay4MaterialTextureSlot(bpy.types.PropertyGroup):

    texture = PointerProperty(
        name="Texture", description="Texture data-block used by this texture slot", type=bpy.types.Texture,
        update=update_preview
    )

    # Start, from rna_material.c

    texture_coords = EnumProperty(
        name="Texture Coordinates",
        description="",
        items=(
            ("GLOBAL", "Global", "Use global coordinates for the texture coordinates"),
            ("OBJECT", "Object", "Use linked object's coordinates for texture coordinates"),
            ("UV", "UV", "Use linked object's coordinates for texture coordinates"),
            ("ORCO", "Original Coordinates", "Use the original undeformed coordinates of the object"),
            ("STRAND", "Strand / Particle", "Use normalized strand texture coordinate (1D) or particle age (X) "
                                            "and trail position (Y)"),
            ("WINDOW", "Window", "Use screen coordinates as texture coordinates"),
            ("NORMAL", "Normal", "Use normal vector as texture coordinates"),
            ("REFLECTION", "Reflection", "Use reflection vector as texture coordinates"),
            ("STRESS", "Stress", "Use the difference of edge lengths compared to original coordinates of the mesh"),
            ("TANGENT", "Tangent", "Use the optional tangent vector as texture coordinates"),
        ),
        default="GLOBAL",
    )

    object = PointerProperty(
        type=bpy.types.Object,
        name="Object",
        description="Object to use for mapping with Object texture coordinates",
    )

    uv_layer = StringProperty(
        name="UV Map", description="UV map to use for mapping with UV texture coordinates", default=""
    )

    use_from_dupli = BoolProperty(
        name="From Dupli",
        description="Dupli's instanced from verts, faces or particles, inherit texture coordinate "
                    "from their parent",
        default=False,
    )

    use_map_to_bounds = BoolProperty(
        name="Map to Bounds",
        description="Map coordinates in object bounds",
        default=False,
    )

    use_from_original = BoolProperty(
        name="From Original",
        description="Dupli's derive their object coordinates from the original object's transformation",
        default=False,
    )

    use_map_color_diffuse = BoolProperty(
        name="Diffuse Color",
        description="The texture affects basic color of the material",
        default=True,
    )

    use_map_normal = BoolProperty(
        name="Normal", description="The texture affects the rendered normal", default=False
    )

    use_map_color_spec = BoolProperty(
        name="Specular Color", description="The texture affects the specularity color",
        default=False
    )

    use_map_mirror = BoolProperty(
        name="Mirror", description="The texture affects the mirror color", default=False
    )

    use_map_diffuse = BoolProperty(
        name="Diffuse",
        description="The texture affects the value of diffuse reflectivity",
        default=False,
    )

    use_map_specular = BoolProperty(
        name="Specular",
        description="The texture affects the value of specular reflectivity",
        default=False,
    )

    use_map_ambient = BoolProperty(
        name="Ambient", description="The texture affects the value of ambient", default=False
    )

    use_map_hardness = BoolProperty(
        name="Hardness", description="The texture affects the hardness value", default=False
    )

    use_map_raymir = BoolProperty(
        name="Ray-Mirror", description="The texture affects the ray-mirror value", default=False
    )

    use_map_alpha = BoolProperty(
        name="Alpha", description="The texture affects the alpha value", default=False
    )

    use_map_emit = BoolProperty(
        name="Emit", description="The texture affects the emit value", default=False
    )

    use_map_translucency = BoolProperty(
        name="Translucency", description="The texture affects the translucency value", default=False
    )

    use_map_displacement = BoolProperty(
        name="Displacement", description="Let the texture displace the surface", default=False
    )

    use_map_warp = BoolProperty(
        name="Warp",
        description="Let the texture warp texture coordinates of next channels",
        default=False,
    )

    mapping_x = EnumProperty(
        name="X Mapping",
        description="",
        items=(("NONE", "None", ""), ("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")),
        default="NONE",
    )

    mapping_y = EnumProperty(
        name="Y Mapping",
        description="",
        items=(("NONE", "None", ""), ("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")),
        default="NONE",
    )

    mapping_z = EnumProperty(
        name="Z Mapping",
        description="",
        items=(("NONE", "None", ""), ("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")),
        default="NONE",
    )

    mapping = EnumProperty(
        name="Mapping",
        description="Texture Mapping",
        items=(
            ("FLAT", "Flat", "Map X and Y coordinates directly"),
            ("CUBE", "Cube", "Map using the normal vector"),
            ("TUBE", "Tube", "Map with Z as central axis"),
            ("SPHERE", "Sphere", "Map with Z as central axis"),
        ),
        default="FLAT",
    )

    normal_map_space = EnumProperty(
        name="Normal Map Space",
        description="Sets space of normal map image",
        items=(
            ("CAMERA", "Camera", ""),
            ("WORLD", "World", ""),
            ("OBJECT", "Object", ""),
            ("TANGENT", "Tangent", ""),
        ),
        default="CAMERA",
    )

    normal_factor = FloatProperty(
        name="Normal Factor", description="Amount texture affects normal values", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    displacement_factor = FloatProperty(
        name="Displacement Factor", description="Amount texture displaces the surface", default=0.2,
        soft_min=0.0, soft_max=1.0,
    )

    warp_factor = FloatProperty(
        name="Warp Factor",
        description="Amount texture affects texture coordinates of next channels",
        default=0.0,
        soft_min=0.0, soft_max=1.0,
    )

    specular_color_factor = FloatProperty(
        name="Specular Color Factor", description="Amount texture affects specular color", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    diffuse_color_factor = FloatProperty(
        name="Diffuse Color Factor", description="Amount texture affects diffuse color", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    mirror_factor = FloatProperty(
        name="Mirror Factor", description="Amount texture affects mirror color", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    alpha_factor = FloatProperty(
        name="Alpha Factor", description="Amount texture affects alpha", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    diffuse_factor = FloatProperty(
        name="Diffuse Factor", description="Amount texture affects diffuse reflectivity", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    specular_factor = FloatProperty(
        name="Specular Factor", description="Amount texture affects specular reflectivity", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    emit_factor = FloatProperty(
        name="Emit Factor", description="Amount texture affects emission", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    hardness_factor = FloatProperty(
        name="Hardness Factor", description="Amount texture affects hardness", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    raymir_factor = FloatProperty(
        name="Ray Mirror Factor", description="Amount texture affects ray mirror", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    translucency_factor = FloatProperty(
        name="Translucency Factor", description="Amount texture affects translucency", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    ambient_factor = FloatProperty(
        name="Ambient Factor", description="Amount texture affects ambient", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    # Start volume material

    use_map_color_emission = BoolProperty(
        name="Emission Color", description="The texture affects the color of emission", default=False
    )

    use_map_color_reflection = BoolProperty(
        name="Reflection Color",
        description="The texture affects the color of scattered light",
        default=False,
    )

    use_map_color_transmission = BoolProperty(
        name="Transmission Color",
        description="The texture affects the result color after other light has been scattered/absorbed",
        default=False,
    )

    use_map_density = BoolProperty(
        name="Density", description="The texture affects the volume's density", default=False
    )

    use_map_emission = BoolProperty(
        name="Emission", description="The texture affects the volume's emission", default=False
    )

    use_map_scatter = BoolProperty(
        name="Scattering", description="The texture affects the volume's scattering", default=False
    )

    use_map_reflect = BoolProperty(
        name="Reflection",
        description="The texture affects the reflected light's brightness",
        default=False,
    )

    emission_color_factor = FloatProperty(
        name="Emission Color Factor", description="Amount texture affects emission color", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    reflection_color_factor = FloatProperty(
        name="Reflection Color Factor", description="Amount texture affects color of out-scattered light", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    transmission_color_factor = FloatProperty(
        name="Transmission Color Factor",
        description="Amount texture affects result color after light has been scattered/absorbed",
        default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    density_factor = FloatProperty(
        name="Density Factor", description="Amount texture affects density", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    emission_factor = FloatProperty(
        name="Emission Factor", description="Amount texture affects emission", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    scattering_factor = FloatProperty(
        name="Scattering Factor", description="Amount texture affects scattering", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    reflection_factor = FloatProperty(
        name="Reflection Factor", description="Amount texture affects brightness of out-scattered light", default=1.0,
        soft_min=0.0, soft_max=1.0,
    )

    # End volume material

    use = BoolProperty(
        name="Enabled", description="Enable this material texture slot", default=True
    )

    bump_method = EnumProperty(
        name="Bump Method",
        description="Method to use for bump mapping",
        items=(
            ("BUMP_ORIGINAL", "Original", ""),
            ("BUMP_COMPATIBLE", "Compatible", ""),
            ("BUMP_LOW_QUALITY", "Low Quality", "Use 3 tap filtering"),
            ("BUMP_MEDIUM_QUALITY", "Medium Quality", "Use 5 tap filtering"),
            ("BUMP_BEST_QUALITY", "Best Quality", "Use bicubic filtering (requires OpenGL 3.0+, it will fall back on "
                                                  "medium setting for other systems)"),
        ),
        default="BUMP_ORIGINAL",
    )

    bump_objectspace = EnumProperty(
        name="Bump Object Space",
        description="Space to apply bump mapping in",
        items=(
            ("BUMP_VIEWSPACE", "ViewSpace", ""),
            ("BUMP_OBJECTSPACE", "ObjectSpace", ""),
            ("BUMP_TEXTURESPACE", "TextureSpace", ""),
        ),
        default="BUMP_VIEWSPACE",
    )

    # End, from rna_material.c

    # Start, from rna_texture.c

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

    color = FloatVectorProperty(
        name="Color",
        description="Default color for textures that don't return RGB or when RGB to intensity is enabled",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 0.0, 1.0))

    blend_type = EnumProperty(
        name="Blend Type",
        description="Mode used to apply the texture",
        items=(
            ("MIX", "Mix", ""),
            ("ADD", "Add", ""),
            ("SUBTRACT", "Subtract", ""),
            ("MULTIPLY", "Multiply", ""),
            ("SCREEN", "Screen", ""),
            ("OVERLAY", "Overlay", ""),
            ("DIFFERENCE", "Difference", ""),
            ("DIVIDE", "Divide", ""),
            ("DARKEN", "Darken", ""),
            ("LIGHTEN", "Lighten", ""),
            ("HUE", "Hue", ""),
            ("SATURATION", "Saturation", ""),
            ("VALUE", "Value", ""),
            ("COLOR", "Color", ""),
            ("SOFT_LIGHT", "Soft Light", ""),
            ("LINEAR_LIGHT", "Linear Light", ""),
        ),
        default="MIX",
    )

    use_stencil = BoolProperty(
        name="Stencil", description="Use this texture as a blending value on the next texture", default=False
    )

    invert = BoolProperty(
        name="Negate", description="Invert the values of the texture to reverse its effect", default=False
    )

    use_rgb_to_intensity = BoolProperty(
        name="RGB to Intensity", description="Convert texture RGB values to intensity (gray) values", default=False
    )

    default_value = FloatProperty(
        name="Default Value", description="Value to use for Ref, Spec, Amb, Emit, Alpha, RayMir, TransLu and Hard",
        soft_min=0.0, soft_max=1.0,
        default=1.0
    )

    output_node = EnumProperty(
        name="Output Node",
        description="Which output node to use, for node-based textures",
        items=(
            ("DUMMY", "Dummy", ""),
        ),
        default="DUMMY",
    )

    # End, from rna_texture.c
