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
from bpy.props import (FloatProperty,
                       BoolProperty,
                       EnumProperty,
                       FloatVectorProperty,
                       StringProperty)

Material = bpy.types.Material


def items_mat1(self, context):
    a = []
    for mat in [m for m in bpy.data.materials if m.name not in self.name]:
        a.append((mat.name, mat.name, "First blend material"))
    return(a)


def items_mat2(self, context):
    a = []
    for mat in [m for m in bpy.data.materials if m.name not in self.name]:
        a.append((mat.name, mat.name, "Second blend material"))
    return(a)


def register():
    Material.mat_type = EnumProperty(
        name="Material type",
        items=(
            ('shinydiffusemat', "Shiny Diffuse", "Assign a material type"),
            ('glossy', "Glossy", "Assign a material type"),
            ('coated_glossy', "Coated Glossy", "Assign a material type"),
            ('glass', "Glass", "Assign a material type"),
            ('rough_glass', "Rough Glass", "Assign a material type"),
            ('blend', "Blend", "Assign a material type")
        ),
        default='shinydiffusemat')

    Material.diffuse_reflect = FloatProperty(
        name="Reflection strength",
        description="Amount of diffuse reflection",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=1.000)

    Material.specular_reflect = FloatProperty(
        name="Reflection strength",
        description="Amount of perfect specular reflection (mirror)",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=0.000)

    Material.transparency = FloatProperty(
        name="Transparency",
        description="Material transparency",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=0.000)

    Material.transmit_filter = FloatProperty(
        name="Transmit filter",
        description="Amount of tinting of light passing through the Material",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=1.000)

    Material.fresnel_effect = BoolProperty(
        name="Fresnel effect",
        description="Apply a fresnel effect to specular reflection",
        default=False)

    Material.brdf_type = EnumProperty(
        name="Reflectance model",
        items=(
            ('oren-nayar', "Oren-Nayar", "Reflectance Model"),
            ('lambert', "Lambert", "Reflectance Model"),
        ),
        default='lambert')

    Material.glossy_color = FloatVectorProperty(
        name="Glossy color",
        description="Glossy Color",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 1.0, 1.0))

    # added mirror col property for coated glossy material
    Material.coat_mir_col = FloatVectorProperty(
        name="Mirror color",
        description="Reflection color of coated layer",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 1.0, 1.0))

    # added mirror color property for glass material
    Material.glass_mir_col = FloatVectorProperty(
        name="Reflection color",
        description="Reflection color of glass material",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 1.0, 1.0))

    Material.glossy_reflect = FloatProperty(
        name="Reflection strength",
        description="Amount of glossy reflection",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=0.000)

    Material.exp_u = FloatProperty(
        name="Exponent U",
        description="Horizontal anisotropic exponent value",
        min=1.0, max=10000.0,
        step=10, precision=2,
        soft_min=1.0, soft_max=10000.0,
        default=50.00)

    Material.exp_v = FloatProperty(
        name="Exponent V",
        description="Vertical anisotropic exponent value",
        min=1.0, max=10000.0,
        step=10, precision=2,
        soft_min=1.0, soft_max=10000.0,
        default=50.00)

    Material.exponent = FloatProperty(
        name="Exponent",
        description="Blur of the glossy reflection, higher exponent = sharper reflections",
        min=1.0, max=10000.0,
        step=10, precision=2,
        soft_min=1.0, soft_max=10000.0,
        default=500.00)

    Material.as_diffuse = BoolProperty(
        name="Use photon map",
        description="Treat glossy component as diffuse",
        default=False)

    Material.anisotropic = BoolProperty(
        name="Anisotropic",
        description="Use anisotropic reflections",
        default=False)

    # added IOR property for refraction
    Material.IOR_refraction = FloatProperty(
        name="IOR",
        description="Index of refraction",
        min=0.0, max=30.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=30.0,
        default=1.520)

    # added IOR property for reflection
    Material.IOR_reflection = FloatProperty(
        name="IOR",
        description="Fresnel reflection strength",
        min=1.0, max=30.0,
        step=1, precision=3,
        soft_min=1.0, soft_max=30.0,
        default=1.800)

    Material.absorption = FloatVectorProperty(
        name="Color and absorption",
        description="Glass volumetric absorption color. White disables absorption",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 1.0, 1.0))

    Material.absorption_dist = FloatProperty(
        name="Abs. distance",
        description="Absorption distance scale",
        min=0.0, max=100.0,
        step=1, precision=4,
        soft_min=0.0, soft_max=100.0,
        default=1.0000)

    # added transmit filter for glass material
    Material.glass_transmit = FloatProperty(
        name="Transmit filter",
        description="Filter strength applied to refracted light",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=1.000)

    Material.filter_color = FloatVectorProperty(
        name="Filter color",
        description="Filter color for refracted light of glass, also tint transparent shadows if enabled",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 1.0, 1.0))

    Material.dispersion_power = FloatProperty(
        name="Disp. power",
        description="Strength of dispersion effect, disabled when 0",
        min=0.0, max=5.0,
        step=1, precision=4,
        soft_min=0.0, soft_max=5.0,
        default=0.0000)

    # added refraction roughness propertie for roughglass material
    Material.refr_roughness = FloatProperty(
        name="Exponent",
        description="Roughness factor for glass material",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=0.200)

    Material.fake_shadows = BoolProperty(
        name="Fake shadows",
        description="Let light straight through for shadow calculation. Not to be used with dispersion",
        default=False)

    Material.blend_value = FloatProperty(
        name="Blend value",
        description="The mixing balance: 0 -> only material 1, 1.0 -> only material 2",
        min=0.0, max=1.0,
        step=3, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=0.500)

    Material.sigma = FloatProperty(
        name="Sigma",
        description="Roughness of the surface",
        min=0.0, max=1.0,
        step=1, precision=5,
        soft_min=0.0, soft_max=1.0,
        default=0.10000)

    Material.rough = BoolProperty(
        name="rough",
        description="",
        default=False)

    Material.coated = BoolProperty(
        name="coated",
        description="",
        default=False)

    Material.material1 = EnumProperty(
        name="Material one",
        description="First blend material",
        items=items_mat1)

    Material.material2 = EnumProperty(
        name="Material two",
        description="Second blend material",
        items=items_mat2)


def unregister():
    del Material.mat_type
    del Material.diffuse_reflect
    del Material.specular_reflect
    del Material.transparency
    del Material.transmit_filter
    del Material.fresnel_effect
    del Material.brdf_type
    del Material.glossy_color
    del Material.coat_mir_col
    del Material.glass_mir_col
    del Material.glossy_reflect
    del Material.exp_u
    del Material.exp_v
    del Material.exponent
    del Material.as_diffuse
    del Material.anisotropic
    del Material.IOR_refraction
    del Material.IOR_reflection
    del Material.absorption
    del Material.absorption_dist
    del Material.glass_transmit
    del Material.filter_color
    del Material.dispersion_power
    del Material.refr_roughness
    del Material.fake_shadows
    del Material.blend_value
    del Material.sigma
    del Material.rough
    del Material.coated
    del Material.material1
    del Material.material2
