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
                       IntProperty,                       
                       BoolProperty,
                       EnumProperty,
                       FloatVectorProperty,
                       StringProperty)

Material = bpy.types.Material

# This code is irrelevant after the change in the blend material to convert it from EnumProperty to StringProperty. I'm keeping this as a reference in case a better solution can be found for the blend material component materials references
def items_mat1(self, context):
    a = []
    for mat in [m for m in bpy.data.materials if m.name not in self.name]:
        a.append((mat.name, mat.name, "First blend material"))
    return(a)

# This code is irrelevant after the change in the blend material to convert it from EnumProperty to StringProperty. I'm keeping this as a reference in case a better solution can be found for the blend material component materials references
def items_mat2(self, context):
    a = []
    for mat in [m for m in bpy.data.materials if m.name not in self.name]:
        a.append((mat.name, mat.name, "Second blend material"))
    return(a)

def update_preview(self, context):
    context.material.preview_render_type = context.material.preview_render_type


def register():
    Material.mat_type = EnumProperty(
        update=update_preview, name="Material type",
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
        update=update_preview, name="Reflection strength",
        description="Amount of diffuse reflection",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=1.000)

    Material.specular_reflect = FloatProperty(
        update=update_preview, name="Reflection strength",
        description="Amount of perfect specular reflection (mirror)",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=0.000)

    Material.transparency = FloatProperty(
        update=update_preview, name="Transparency",
        description="Material transparency",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=0.000)

    Material.transmit_filter = FloatProperty(
        update=update_preview, name="Transmit filter",
        description="Amount of tinting of light passing through the Material",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=1.000)

    Material.fresnel_effect = BoolProperty(
        update=update_preview, name="Fresnel effect",
        description="Apply a fresnel effect to specular reflection",
        default=False)

    Material.brdf_type = EnumProperty(
        update=update_preview, name="Reflectance model",
        items=(
            ('oren-nayar', "Oren-Nayar", "Reflectance Model"),
            ('lambert', "Lambert", "Reflectance Model"),
        ),
        default='lambert')

    Material.wireframe_amount = FloatProperty(
        update=update_preview, name="Wireframe amount",
        description="Amount of wireframe shading",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=0.000)

    Material.wireframe_thickness = FloatProperty(
        update=update_preview, name="Wireframe thickness",
        description="Thickness of wireframe shading",
        min=0.0,
        step=1, precision=3,
        soft_min=0.0001, soft_max=0.10,
        default=0.01)

    Material.wireframe_exponent = FloatProperty(
        update=update_preview, name="Wireframe softness",
        description="Softness of wireframe shading",
        min=0.0, max=2.0,
        step=1, precision=2,
        default=0.0)

    Material.wireframe_color = FloatVectorProperty(
        update=update_preview, name="Wireframe color",
        description="Wireframe Color",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 1.0, 1.0))

    Material.glossy_color = FloatVectorProperty(
        update=update_preview, name="Glossy color",
        description="Glossy Color",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 1.0, 1.0))

    # added mirror col property for coated glossy material
    Material.coat_mir_col = FloatVectorProperty(
        update=update_preview, name="Mirror color",
        description="Reflection color of coated layer",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 1.0, 1.0))

    # added mirror color property for glass material
    Material.glass_mir_col = FloatVectorProperty(
        update=update_preview, name="Reflection color",
        description="Reflection color of glass material",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 1.0, 1.0))

    Material.glossy_reflect = FloatProperty(
        update=update_preview, name="Reflection strength",
        description="Amount of glossy reflection",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=0.000)

    Material.exp_u = FloatProperty(
        update=update_preview, name="Exponent U",
        description="Horizontal anisotropic exponent value",
        min=1.0, max=10000.0,
        step=10, precision=2,
        soft_min=1.0, soft_max=10000.0,
        default=50.00)

    Material.exp_v = FloatProperty(
        update=update_preview, name="Exponent V",
        description="Vertical anisotropic exponent value",
        min=1.0, max=10000.0,
        step=10, precision=2,
        soft_min=1.0, soft_max=10000.0,
        default=50.00)

    Material.exponent = FloatProperty(
        update=update_preview, name="Exponent",
        description="Blur of the glossy reflection, higher exponent = sharper reflections",
        min=1.0, max=10000.0,
        step=10, precision=2,
        soft_min=1.0, soft_max=10000.0,
        default=500.00)

    Material.as_diffuse = BoolProperty(
        update=update_preview, name="Use photon map",
        description="Treat glossy component as diffuse",
        default=False)

    Material.anisotropic = BoolProperty(
        update=update_preview, name="Anisotropic",
        description="Use anisotropic reflections",
        default=False)

    # added IOR property for refraction
    Material.IOR_refraction = FloatProperty(
        update=update_preview, name="IOR",
        description="Index of refraction",
        min=0.0, max=30.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=30.0,
        default=1.520)

    # added IOR property for reflection
    Material.IOR_reflection = FloatProperty(
        update=update_preview, name="IOR",
        description="Fresnel reflection strength",
        min=1.0, max=30.0,
        step=1, precision=3,
        soft_min=1.0, soft_max=30.0,
        default=1.800)

    Material.absorption = FloatVectorProperty(
        update=update_preview, name="Color and absorption",
        description="Glass volumetric absorption color. White disables absorption",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 1.0, 1.0))

    Material.absorption_dist = FloatProperty(
        update=update_preview, name="Abs. distance",
        description="Absorption distance scale",
        min=0.0, max=100.0,
        step=1, precision=4,
        soft_min=0.0, soft_max=100.0,
        default=1.0000)

    # added transmit filter for glass material
    Material.glass_transmit = FloatProperty(
        update=update_preview, name="Transmit filter",
        description="Filter strength applied to refracted light",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=1.000)

    Material.filter_color = FloatVectorProperty(
        update=update_preview, name="Filter color",
        description="Filter color for refracted light of glass, also tint transparent shadows if enabled",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(1.0, 1.0, 1.0))

    Material.dispersion_power = FloatProperty(
        update=update_preview, name="Disp. power",
        description="Strength of dispersion effect, disabled when 0",
        min=0.0, max=5.0,
        step=1, precision=4,
        soft_min=0.0, soft_max=5.0,
        default=0.0000)

    # added refraction roughness propertie for roughglass material
    Material.refr_roughness = FloatProperty(
        update=update_preview, name="Exponent",
        description="Roughness factor for glass material",
        min=0.0, max=1.0,
        step=1, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=0.200)

    Material.fake_shadows = BoolProperty(
        update=update_preview, name="Fake shadows",
        description="Let light straight through for shadow calculation. Not to be used with dispersion",
        default=False)

    Material.clay_exclude = BoolProperty(
        update=update_preview, name="Exclude from Clay render",
        description="Exclude from Clay render mode: this material will be rendered normally even in Clay render mode",
        default=False)

    Material.blend_value = FloatProperty(
        update=update_preview, name="Blend value",
        description="The mixing balance: 0 -> only material 1, 1.0 -> only material 2",
        min=0.0, max=1.0,
        step=3, precision=3,
        soft_min=0.0, soft_max=1.0,
        default=0.500)

    Material.sigma = FloatProperty(
        update=update_preview, name="Sigma",
        description="Roughness of the surface",
        min=0.0, max=1.0,
        step=1, precision=5,
        soft_min=0.0, soft_max=1.0,
        default=0.10000)

    Material.rough = BoolProperty(
        update=update_preview, name="rough",
        description="",
        default=False)

    Material.coated = BoolProperty(
        update=update_preview, name="coated",
        description="",
        default=False)

    #Deprecated blend material component Enum references, only to keep compatibility with old scenes
    Material.material1 = EnumProperty(
        update=update_preview, name="Material one",
        description="First blend material",
        items=items_mat1)

    Material.material2 = EnumProperty(
        update=update_preview, name="Material two",
        description="Second blend material",
        items=items_mat2)

    #New blend material component String references, when opening old scenes it should copy the old Enum Property materials to the new String Properties
    Material.material1name = StringProperty(
        update=update_preview, name="Material one",
        description="First blend material")
        #,        get=get_blend_mat1_old_scenes)

    Material.material2name = StringProperty(
        update=update_preview, name="Material two",
        description="Second blend material")
        #,        get=get_blend_mat2_old_scenes)

    Material.visibility = EnumProperty(
        update=update_preview, name="Visibility",
        items=(
            ('invisible', "Invisible", "Totally invisible"),
            ('shadow_only', "Shadows only", "Invisible but casting shadows"),
            ('no_shadows', "No shadows", "Visible but not casting shadows"),
            ('normal', "Normal", "Normal visibility - visible casting shadows"),
            
        ),
        default='normal')
        
    Material.receive_shadows = BoolProperty(
        update=update_preview, name="Receive Shadows",
        description="If this parameter is set to false, the material will not receive shadows from other objects",
        default=True)

    Material.flat_material = BoolProperty(
        update=update_preview, name="Flat Material",
        description="Flat Material is a special non-photorealistic material that does not multiply the surface color by the cosine of the angle with the light, as happens in real life. For special applications only",
        default=False)

    Material.additionaldepth = IntProperty(
        update=update_preview, name="Additional Ray Depth",
        description="Additional per-material Ray depth to be added to the general Ray Depth setting",
        min=0, max=20,
        default=0)

    Material.transparentbias_factor = FloatProperty(
        update=update_preview, name="Transparent Bias",
        description="If this value is >0.0 an additional (non-realistic) 'bias' will be added to each ray when it hits a transparent surface. This could be useful to render many stacked transparent surfaces and avoid black artifacts in some cases BUT COULD CAUSE EASILY OTHER WEIRD ARTIFACTS, USE WITH CARE!!. If the ray hits a transparent surface, the next secondary ray will not start exactly after that surface but after this bias factor. So, subsequent transparent surfaces can be skipped and not rendered, but the objects behind will be rendered (unless they are too close, in that case they might not be rendered!).",
        min=0.0,
        default=0.0)

    Material.transparentbias_multiply_raydepth = BoolProperty(
        update=update_preview, name="Multiply Bias by Ray Depth",
        description="If the Transparent Bias is used and this is disabled, the bias will be just added to each secondary ray initial position. If this parameter is enabled, the bias for each ray will be multiplied by the ray depth. That way, the first few surfaces will be rendered giving a better density but the further the secondary rays are generated, the bigger the bias will be.",
        default=False)
        
    Material.samplingfactor = FloatProperty(
        update=update_preview, name="Sampling Factor",
        description="The number of samples in the adaptative AA passes are multiplied by this per-material factor. This does not affect the first pass.",
        min=1.0,
        default=1.0)

    if bpy.app.version >= (2, 80, 0):
        Material.translucency = FloatProperty(
            update=update_preview, name="Translucency",
            description="Material translucency",
            min=0.0, max=1.0,
            step=1, precision=3,
            soft_min=0.0, soft_max=1.0,
            default=0.000)

        Material.mirror_color = FloatVectorProperty(
            update=update_preview, name="Mirror color",
            description="Mirror Color",
            subtype='COLOR',
            min=0.0, max=1.0,
            default=(1.0, 1.0, 1.0))

        Material.emit = BoolProperty(
            update=update_preview, name="emit",
            description="",
            default=False)

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
    del Material.clay_exclude
    del Material.blend_value
    del Material.sigma
    del Material.rough
    del Material.coated
    del Material.material1
    del Material.material2
    del Material.material1name
    del Material.material2name
    del Material.visibility
    del Material.receive_shadows
    del Material.flat_material
    del Material.additionaldepth
    del Material.transparentbias_factor
    del Material.transparentbias_multiply_raydepth
    del Material.wireframe_amount
    del Material.wireframe_thickness
    del Material.wireframe_exponent
    del Material.wireframe_color
    del Material.samplingfactor
    if bpy.app.version >= (2, 80, 0):
        del Material.emit
        del Material.translucency
        del Material.mirror_color
