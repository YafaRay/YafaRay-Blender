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

import math
import bpy
from sys import platform
import traceback
from bpy.props import (IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       BoolProperty,
                       StringProperty,
                       PointerProperty,
                       CollectionProperty)

Scene = bpy.types.Scene

def update_preview(self, context):
    if hasattr(context, "material") and context.material is not None:
        context.material.preview_render_type = context.material.preview_render_type
    elif len(bpy.data.materials) > 0:
        bpy.data.materials[0].preview_render_type = bpy.data.materials[0].preview_render_type

# set fileformat for image saving on same format as in YafaRay, both have default PNG
def call_update_fileformat(self, context):
    scene = context.scene
    render = scene.render
    if scene.img_output is not render.image_settings.file_format:
        render.image_settings.file_format = scene.img_output

class YafaRay4Properties(bpy.types.PropertyGroup):
    pass

class YafaRay4LoggingProperties(bpy.types.PropertyGroup):
    paramsBadgePosition = EnumProperty(
        name="Params Badge position",
        description="Choose the position of the params badge in the exported image file. Inside Blender it may appear incorrect or not at all",
        items=(
            ('top', "Top", "Params badge will appear at the top of the exported image file"),
            ('bottom', "Bottom", "Params badge will appear at the bottom of the exported image file. It may appear cropped in Blender."),
            ('none', "None", "Params badge will not appear")
        ),
        default='none')

    saveLog = BoolProperty(
        name="Save log file",
        description="Save text log file with the exported image files",
        default=False)

    saveHTML = BoolProperty(
        name="Save HTML file",
        description="Save HTML information/log file with the exported image files",
        default=True)

    savePreset = BoolProperty(
        name="Save Preset file",
        description="Save a preset file, with the Render Settings, with the exported image files",
        default=True)

    verbosityLevels=sorted((
            ('mute', "Mute (silent)", "Prints nothing", 0),
            ('error', "Error", "Prints only errors", 1),
            ('warning', "Warning", "Prints also warnings", 2),
            ('params', "Params", "Prints also render param messages", 3),
            ('info', "Info", "Prints also basic info messages", 4),
            ('verbose', "Verbose", "Prints additional info messages", 5),
            ('debug', "Debug", "Prints debug messages (if any)", 6),
        ), key=lambda index: index[3])

    logPrintDateTime = BoolProperty(
        name="Log Date/Time",
        description="Print Date/Time in the logs (enabled by default)",
        default=True)

    consoleVerbosity = EnumProperty(
        name="Console Verbosity",
        description="Select the desired verbosity level for console log output",
        items=(verbosityLevels
        ),
        default="info")

    logVerbosity = EnumProperty(
        name="Log/HTML Verbosity",
        description="Select the desired verbosity level for log and HTML output",
        items=(verbosityLevels
        ),
        default="info")

    drawRenderSettings = BoolProperty(
        name="Draw Render Settings",
        description="Draw Render Settings in the params badge",
        default=True)
        
    drawAANoiseSettings = BoolProperty(
        name="Draw AA/Noise Settings",
        description="Draw AA and Noise Control Settings in the params badge",
        default=True)

    title = StringProperty(
        name="Title",
        description=("Title to be shown in the logs and/or params badge"),
        default="")

    author = StringProperty(
        name="Author",
        description=("Author to be shown in the logs and/or params badge"),
        default="")

    contact = StringProperty(
        name="Contact info",
        description=("Contact information (phone, e-mail, etc) to be shown in the logs and/or params badge"),
        default="")

    comments = StringProperty(
        name="Comments",
        description=("Comments to be added to the logs and/or params badge"),
        default="")

    customIcon = StringProperty(
        name="Custom PNG icon path",
        description=("Path to custom icon for logs and/or params badge."
                     "(recommended around 70x45, black background)."
                     "If blank or wrong, the default YafaRay icon will be shown"),
        subtype="FILE_PATH",
        default="")

    customFont = StringProperty(
        name="Font path",
        description=("Path to params badge TTF font."
                     "If blank or wrong, the default YafaRay font will be used"),
        subtype="FILE_PATH",
        default="")

    fontScale = FloatProperty(
        name="Font scale",
        description=("Font scaling factor."),
        min=0.2, max=5.0, precision=1,
        default=1.0)

    
class YafaRay4NoiseControlProperties(bpy.types.PropertyGroup):
    resampled_floor = FloatProperty(
        name="Resampled floor (%)",
        description=("Noise reduction: when resampled pixels go below this value (% of total pixels),"
                     " the AA threshold will automatically decrease before the next pass"),
        min=0.0, max=100.0, precision=1,
        default=0.0)

    sample_multiplier_factor = FloatProperty(
        name="AA sample multiplier factor",
        description="Factor to increase the AA samples multiplier for next AA pass",
        min=1.0, max=4.0, precision=2,
        default=1.0)

    light_sample_multiplier_factor = FloatProperty(
        name="Light sample multiplier factor",
        description="Factor to increase the light samples multiplier for next AA pass",
        min=1.0, max=4.0, precision=2,
        default=1.0)

    indirect_sample_multiplier_factor = FloatProperty(
        name="Indirect sample multiplier factor",
        description="Factor to increase the indirect samples (FG for example) multiplier for next AA pass",
        min=1.0, max=4.0, precision=2,
        default=1.0)

    detect_color_noise = BoolProperty(
        name="Color noise detection",
        description="Detect noise in RGB components in addidion to pixel brightness",
        default=False)
        
    dark_detection_type = EnumProperty(
        name="Dark areas noise detection",
        items=(
            ('none', "None", "No special dark areas noise detection (default)"),
            ('linear', "Linear", "Linearly change AA threshold depending on pixel brightness and Dark factor"),
            ('curve', "Curve", "Change AA threshold based on a pre-computed curve")
        ),
        default="linear")
        
    dark_threshold_factor = FloatProperty(
        name="Dark factor",
        description=("Factor used to reduce the AA threshold in dark areas."
                     " It will reduce noise in dark areas, but noise in bright areas will take longer."
                     " You probably need to increase the main AA threshold value if you use this parameter" ),
        min=0.0, max=1.0, precision=3,
        default=0.0)

    variance_edge_size = IntProperty(
        name="Variance window",
        description="Window edge size for variance noise detection",
        min=4, max=20,
        default=10)

    variance_pixels = IntProperty(
        name="Variance threshold",
        description="Threshold (in pixels) for variance noise detection. 0 disables variance detection",
        min=0, max=10,
        default=0)

    clamp_samples = FloatProperty(
        name="Clamp samples",
        description="Clamp RGB values in all samples, less noise but less realism. 0.0 disables clamping",
        min=0.0, precision=1,
        default=0.0)

    clamp_indirect = FloatProperty(
        name="Clamp indirect",
        description="Clamp RGB values in the indirect light, less noise but less realism. 0.0 disables clamping",
        min=0.0, precision=1,
        default=0.0)

    background_resampling = BoolProperty(
        update=update_preview, name="Background Resampling",
        description="If disabled, the background will not be resamples in subsequent adaptative AA passes.",
        default=True)

    
class YafaRay4LayersProperties(bpy.types.PropertyGroup):
    pass_enable = BoolProperty(
        name="Enable render passes",
        default=False)

    pass_mask_obj_index = IntProperty(
        name="Mask Object Index",
        description="Object index used for masking in the Mask render passes",
        min=0,
        default=0)
        
    pass_mask_mat_index = IntProperty(
        name="Mask Material Index",
        description="Material index used for masking in the Mask render passes",
        min=0,
        default=0)    
        
    pass_mask_invert = BoolProperty(
        name="Invert Mask selection",
        description="Property to mask-in or mask-out the desired objects/materials in the Mask render passes",
        default=False)
    
    pass_mask_only = BoolProperty(
        name="Mask Only",
        description="Property to show the mask only instead of the masked rendered image",
        default=False)

    objectEdgeThickness = IntProperty(
        name="Object Edge Thickness",
        description="Thickness of the edges used in the Object Edge and Toon Render Passess",
        min=1, max=10,
        default=2)

    facesEdgeThickness = IntProperty(
        name="Faces Edge Thickness",
        description="Thickness of the edges used in the Faces Edge Render Pass",
        min=1, max=10,
        default=1)

    objectEdgeThreshold = FloatProperty(
        name="Object Edge Threshold",
        description=("Threshold for the edge detection process used in the Object Edge and Toon Render Passes"),
        min=0.0, max=1.0, 
        precision=3,
        default=0.3)

    facesEdgeThreshold = FloatProperty(
        name="Faces Edge Threshold",
        description=("Threshold for the edge detection process used in the Faces Edge Render Pass"),
        min=0.0, max=1.0, 
        precision=3,
        default=0.01)

    objectEdgeSmoothness = FloatProperty(
        name="Object Edge Smoothness",
        description=("Smoothness (blur) of the edges used in the Object Edge and Toon Render Passes"),
        min=0.0, max=5.0, 
        precision=2,
        default=0.75)

    facesEdgeSmoothness = FloatProperty(
        name="Faces Edge Smoothness",
        description=("Smoothness (blur) of the edges used in the Faces Edge Render Pass"),
        min=0.0, max=5.0, 
        precision=2,
        default=0.5)

    toonEdgeColor = FloatVectorProperty(
        name="Toon Edge Color",
        description=("Color of the edges used in the Toon Render Pass"),
        subtype='COLOR',
        step=1, precision=2,
        min=0.0, max=1.0,
        soft_min=0.0, soft_max=1.0,
        default=(0.0, 0.0, 0.0))

    toonPreSmooth = FloatProperty(
        name="Toon Pre-Smooth",
        description=("Toon effect: smoothness applied to the original image"),
        min=0.0, 
        precision=2,
        default=3.0)

    toonPostSmooth = FloatProperty(
        name="Toon Post-Smooth",
        description=("Toon effect: smoothness applied to the original image"),
        min=0.0, 
        precision=2,
        default=3.0)

    toonQuantization = FloatProperty(
        name="Toon Color Quantization",
        description=("Toon effect: color Quantization applied to the original image"),
        min=0.0, max=1.0,
        precision=3,
        default=0.1)
        

    #The numbers here MUST NEVER CHANGE to keep backwards compatibility with older scenes. The numbers do not need to match the Core internal pass numbers.
    #The matching between these properties and the YafaRay Core internal passes is done via the first string, for example 'z-depth-abs'. They must match the list of strings for internal passes in the Core: include/core_api/color.h

    renderPassItemsDisabled=sorted((
            ('disabled', "Disabled", "Disable this pass", 999999),
        ), key=lambda index: index[1])

    renderPassItemsBasic=sorted((
            ('combined', "Basic: Combined image", "Basic: Combined standard image", 0),
            ('diffuse', "Basic: Diffuse", "Basic: Diffuse materials", 1),
            ('diffuse-noshadow', "Basic: Diffuse (no shadows)", "Basic: Diffuse materials (without shadows)", 2),
            ('shadow', "Basic: Shadow", "Basic: Shadows", 3),
            ('env', "Basic: Environment", "Basic: Environmental light", 4),
            ('indirect', "Basic: Indirect", "Basic: Indirect light (all, including caustics and diffuse)", 5),
            ('emit', "Basic: Emit", "Basic: Objects emitting light", 6),
            ('reflect', "Basic: Reflection", "Basic: Reflections (all, including perfect and glossy)", 7),
            ('refract', "Basic: Refraction", "Basic: Refractions (all, including perfect and sampled)", 8),
            ('mist', "Basic: Mist", "Basic: Mist", 9),
            ('toon', "Basic: Toon", "Basic: Toon", 10),
        ), key=lambda index: index[1])
        
    renderPassItemsDepth=sorted((
            ('z-depth-abs', "Z-Depth (absolute)", "Z-Depth (absolute values)", 101),
            ('z-depth-norm', "Z-Depth (normalized)", "Z-Depth (normalized values)", 102),
        ), key=lambda index: index[1])
                        
    renderPassItemsIndex=sorted((
            ('obj-index-abs', "Index-Object (absolute)", "Index-Object: Grayscale value = obj.index in the object properties (absolute values)", 201),
            ('obj-index-norm', "Index-Object (normalized)", "Index-Object: Grayscale value = obj.index in the object properties (normalized values)", 202),
            ('obj-index-auto', "Index-Object (auto, color)", "Index-Object: A color automatically generated for each object", 203),
            ('obj-index-mask', "Index-Object Mask", "Index-Object: Masking object based on obj.index.mask setting", 204),
            ('obj-index-mask-shadow', "Index-Object Mask Shadow", "Index-Object: Masking object shadow based on obj.index.mask setting", 205),
            ('obj-index-mask-all', "Index-Object Mask All (Object+Shadow)", "Index-Object: Masking object+shadow based on obj.index.mask setting", 206),
            ('mat-index-abs', "Index-Material (absolute)", "Index-Material: Grayscale value = mat.index in the material properties (absolute values)", 207),
            ('mat-index-norm', "Index-Material (normalized)", "Index-Material: Grayscale value = mat.index in the material properties (normalized values)", 208),
            ('mat-index-auto', "Index-Material (auto, color)", "Index-Material: A color automatically generated for each material", 209),
            ('mat-index-mask', "Index-Material Mask", "Index-Material: Masking material based on mat.index.mask setting", 210),
            ('mat-index-mask-shadow', "Index-Material Mask Shadow", "Index-Material: Masking material shadow based on mat.index.mask setting", 211),
            ('mat-index-mask-all', "Index-Material Mask All (Object+Shadow)", "Index-Material: Masking material+shadow based on mat.index.mask setting", 212),
            ('obj-index-auto-abs', "Index-Object (auto, absolute)", "Index-Object: An absolute value automatically generated for each object", 213),
            ('mat-index-auto-abs', "Index-Material (auto, absolute)", "Index-Material: An absolute value automatically generated for each material", 214)
        ), key=lambda index: index[1])
        
    renderPassItemsDebug=sorted((
            ('debug-aa-samples', "Debug: AA sample count", "Debug: Adaptative AA sample count (estimation), normalized", 301),
            ('debug-uv', "Debug: UV", "Debug: UV coordinates", 302),
            ('debug-dsdv', "Debug: dSdV", "Debug: shading dSdV", 303),
            ('debug-dsdu', "Debug: dSdU", "Debug: shading dSdU", 304),
            ('debug-dpdv', "Debug: dPdV", "Debug: surface dPdV", 305),
            ('debug-dpdu', "Debug: dPdU", "Debug: surface dPdU", 306),
            ('debug-nv', "Debug: NV", "Debug - surface NV", 307),
            ('debug-nu', "Debug: NU", "Debug - surface NU", 308),
            ('debug-normal-geom', "Debug: Normals (geometric)", "Normals (geometric, no smoothness)", 309),
            ('debug-normal-smooth', "Debug: Normals (smooth)", "Normals (including smoothness)", 310),
            ('debug-light-estimation-light-dirac', "Debug: LE Light Dirac", "Light Estimation (Dirac lights)", 311),
            ('debug-light-estimation-light-sampling', "Debug: LE Light Sampling", "Light Estimation (Area lights, light sampling)", 312),
            ('debug-light-estimation-mat-sampling', "Debug: LE Mat Sampling", "Light Estimation (Area lights, material sampling)", 313),
            ('debug-wireframe', "Debug: Wireframe", "Show the objects wireframe (triangles) depending on the material wireframe parameters (except for wireframe amount)", 314),
            ('debug-faces-edges', "Debug: Faces Edges", "Show the faces edges, potentially useful as alternative wireframe pass that can show quads and polygons in a better way", 315),
            ('debug-objects-edges', "Debug: Objects Edges", "Show the objects edges, potentially useful for toon-like shading", 316),
            ('debug-sampling-factor', "Debug: Sampling Factor", "Show the materials sampling factor", 317),
            ('debug-dp-lengths', "Debug: differential dP lengths", "For debugging mipmaps, etc, show differential dPdx and dPdy lengths", 318),
            ('debug-dpdx', "Debug: differential dPdx", "For debugging mipmaps, etc, show differential dPdx X,Y,Z coordinates", 319),
            ('debug-dpdy', "Debug: differential dPdy", "For debugging mipmaps, etc, show differential dPdy X,Y,Z coordinates", 320),
            ('debug-dpdxy', "Debug: differential dPdx+dPdy", "For debugging mipmaps, etc, show differential dPdx+dPdy X,Y,Z coordinates", 321),
            ('debug-dudx-dvdx', "Debug: differential dUdx, dVdx", "For debugging mipmaps, etc, show differential dUdx and dVdx", 322),
            ('debug-dudy-dvdy', "Debug: differential dUdy, dVdy", "For debugging mipmaps, etc, show differential dUdy and dVdy", 323),
            ('debug-dudxy-dvdxy', "Debug: differential dUdx+dUdy, dVdx+dVdy", "For debugging mipmaps, etc, show differential dUdx+dUdy and dVdx+dVdy", 324),
            ('debug-barycentric-uvw', "Debug: Barycentric UVW", "Debug: barycentric UVW coordinates", 325),
        ), key=lambda index: index[1])

    renderInternalPassAdvanced=sorted((
            ('adv-reflect', "Adv: Reflection ", "Advanced: Reflections (perfect only)", 401),
            ('adv-refract', "Adv: Refraction", "Advanced: Refractions (perfect only)", 402),
            ('adv-radiance', "Adv: Photon Radiance map", "Advanced: Radiance map (only for photon mapping)", 403),
            ('adv-volume-transmittance', "Adv: Volume Transmittance", "Advanced: Volume Transmittance", 404),
            ('adv-volume-integration', "Adv: Volume integration", "Advanced: Volume integration", 405),
            ('adv-diffuse-indirect', "Adv: Diffuse Indirect", "Advanced: Diffuse Indirect light", 406),
            ('adv-diffuse-color', "Adv: Diffuse color", "Advanced: Diffuse color", 407),
            ('adv-glossy', "Adv: Glossy", "Advanced: Glossy materials", 408),
            ('adv-glossy-indirect', "Adv: Glossy Indirect", "Advanced: Glossy Indirect light", 409),
            ('adv-glossy-color', "Adv: Glossy color", "Advanced: Glossy color", 410),
            ('adv-trans', "Adv: Transmissive", "Advanced: Transmissive materials", 411),
            ('adv-trans-indirect', "Adv: Trans.Indirect", "Advanced: Transmissive Indirect light", 412),
            ('adv-trans-color', "Adv: Trans.color", "Advanced: Transmissive color", 413),
            ('adv-subsurface', "Adv: SubSurface", "Advanced: SubSurface materials", 414),
            ('adv-subsurface-indirect', "Adv: SubSurf.Indirect", "Advanced: SubSurface Indirect light", 415),
            ('adv-subsurface-color', "Adv: SubSurf.color", "Advanced: SubSurface color", 416),
            ('adv-indirect', "Adv: Indirect", "Adv: Indirect light (depends on the integrator but usually caustics only)", 417),
            ('adv-surface-integration', "Adv: Surface Integration", "Advanced: Surface Integration", 418),
        ), key=lambda index: index[1])

    renderPassItemsAO=sorted((
            ('ao', "AO", "Ambient Occlusion", 501),
            ('ao-clay', "AO clay", "Ambient Occlusion (clay)", 502),
        ), key=lambda index: index[1])

    renderPassAllItems = sorted(renderPassItemsBasic+renderInternalPassAdvanced+renderPassItemsIndex+renderPassItemsDebug+renderPassItemsDepth+renderPassItemsAO, key=lambda index: index[1])

    #This property is not currently used by YafaRay Core, as the combined external pass is always using the internal combined pass. 
    pass_Combined = EnumProperty(
        name="Combined",  #RGBA (4 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassItemsDisabled
        ),
        default="disabled")

    pass_Depth = EnumProperty(
        name="Depth",  #Gray (1 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassItemsDepth
        ),
        default="z-depth-norm")

    pass_Vector = EnumProperty(
        name="Vector",  #RGBA (4 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="obj-index-auto")

    pass_Normal = EnumProperty(
        name="Normal",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="debug-normal-smooth")
        
    pass_UV = EnumProperty(
        name="UV",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="debug-uv")

    pass_Color = EnumProperty(
        name="Color",  #RGBA (4 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="mat-index-auto")

    pass_Emit = EnumProperty(
        name="Emit",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="emit")
        
    pass_Mist = EnumProperty(
        name="Mist",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="mist")

    pass_Diffuse = EnumProperty(
        name="Diffuse",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="diffuse")
        
    pass_Spec = EnumProperty(
        name="Spec",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="adv-reflect")

    pass_AO = EnumProperty(
        name="AO",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassItemsAO
        ),
        default="ao")

    pass_Env = EnumProperty(
        name="Env",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="env")

    pass_Indirect = EnumProperty(
        name="Indirect",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="indirect")

    pass_Shadow = EnumProperty(
        name="Shadow",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="shadow")

    pass_Reflect = EnumProperty(
        name="Reflect",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="reflect")

    pass_Refract = EnumProperty(
        name="Refract",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="refract")

    pass_IndexOB = EnumProperty(
        name="Object Index",  #Gray (1 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassItemsIndex
        ),
        default="obj-index-norm")
        
    pass_IndexMA = EnumProperty(
        name="Material Index",  #Gray (1 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassItemsIndex
        ),
        default="mat-index-norm")

    pass_DiffDir = EnumProperty(
        name="Diff Dir",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="diffuse")
        
    pass_DiffInd = EnumProperty(
        name="Diff Ind",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="adv-diffuse-indirect")

    pass_DiffCol = EnumProperty(
        name="Diff Col",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="adv-diffuse-color")

    pass_GlossDir = EnumProperty(
        name="Gloss Dir",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="adv-glossy")
        
    pass_GlossInd = EnumProperty(
        name="Gloss Ind",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="adv-glossy-indirect")

    pass_GlossCol = EnumProperty(
        name="Gloss Col",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="adv-glossy-color")

    pass_TransDir = EnumProperty(
        name="Trans Dir",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="adv-trans")
        
    pass_TransInd = EnumProperty(
        name="Trans Ind",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="adv-trans-indirect")

    pass_TransCol = EnumProperty(
        name="Trans Col",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="adv-trans-color")

    pass_SubsurfaceDir = EnumProperty(
        name="SubSurface Dir",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="adv-subsurface")
        
    pass_SubsurfaceInd = EnumProperty(
        name="SubSurface Ind",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="adv-subsurface-indirect")

    pass_SubsurfaceCol = EnumProperty(
        name="SubSurface Col",  #RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=(renderPassAllItems
        ),
        default="adv-subsurface-color")

class YafaRay4MaterialPreviewControlProperties(bpy.types.PropertyGroup):

    enable = BoolProperty(
        update=update_preview,
        name="Material Preview Controls enabled",
        description="Enable/Disable material preview controls",
        default=False)

    objScale = FloatProperty(
        update=update_preview,
        name="objScale",
        description=("Material Preview object scaling factor"),
        min=0.0, #max=10.0, 
        precision=2, step=10,
        default=1.0)

    rotZ = FloatProperty(
        update=update_preview,
        name="rotZ",
        description=("Material Preview object rotation Z axis"),
        precision=1, step=1000,
        #min=math.radians(-360), max=math.radians(360),
        subtype="ANGLE", unit="ROTATION",
        default=0.0)

    lightRotZ = FloatProperty(
        update=update_preview,
        name="lightRotZ",
        description=("Material Preview light rotation Z axis"),
        precision=1, step=1000,
        #min=math.radians(-360), max=math.radians(360),
        subtype="ANGLE", unit="ROTATION",
        default=0.0)

    keyLightPowerFactor = FloatProperty(
        update=update_preview,
        name="keyLightPowerFactor",
        description=("Material Preview power factor for the key light"),
        min=0.0, max=10.0, precision=2, step=10,
        default=1.0)

    fillLightPowerFactor = FloatProperty(
        update=update_preview,
        name="lightPowerFactor",
        description=("Material Preview power factor for the fill lights"),
        min=0.0, max=10.0, precision=2, step=10,
        default=0.5)

    keyLightColor = FloatVectorProperty(
        update=update_preview,
        name="keyLightColor",
        description=("Material Preview color for key light"),
        subtype='COLOR',
        step=1, precision=2,
        min=0.0, max=1.0,
        soft_min=0.0, soft_max=1.0,
        default=(1.0, 1.0, 1.0))

    fillLightColor = FloatVectorProperty(
        update=update_preview,
        name="fillLightColor",
        description=("Material Preview color for fill lights"),
        subtype='COLOR',
        step=1, precision=2,
        min=0.0, max=1.0,
        soft_min=0.0, soft_max=1.0,
        default=(1.0, 1.0, 1.0))

    previewRayDepth = IntProperty(
        update=update_preview,
        name="previewRayDepth",
        description=("Material Preview max ray depth, set higher for better (slower) glass preview"),
        min=0, max=20, default=2)

    previewAApasses = IntProperty(
        update=update_preview,
        name="previewAApasses",
        description=("Material Preview AA passes, set higher for better (slower) preview"),
        min=1, max=20, default=1)

    previewBackground = EnumProperty(
        update=update_preview,
        name="previewBackground",
        description=("Material Preview background type"),
        items=(
            ('none', "None", "No background", 0),
            ('checker', "Checker", "Checker background (default)", 1),
            ('world', "Scene World", "Scene world background (can be slow!)", 2)
        ),
        default="checker")

    previewObject = StringProperty(
        update=update_preview,
        name="previewObject",
        description=("Material Preview custom object to be shown, if empty will use default preview objects"),
        default="")

    camDist = FloatProperty(
        update=update_preview,
        name="camDist",
        description=("Material Preview Camera distance to object"),
        min=0.1, max=22.0, precision=2, step=100,
        default=12.0)
        
    camRot = FloatVectorProperty(
        update=update_preview,
        name="camRot",
        description=("Material Preview camera rotation"),
        subtype='DIRECTION',
        #step=10, precision=3,
        #min=-1.0, max=1.0,
        default=(0.0, 0.0, 1.0)
        )        

    class OBJECT_OT_CamRotReset(bpy.types.Operator):
        """ Reset camera rotation/zoom to initial values. """
        bl_idname = "preview.camrotreset"
        bl_label = "reset camera rotation/distance values to defaults"
        country = bpy.props.StringProperty()
     
        def execute(self, context):
            bpy.data.scenes[0].yafaray.preview.camRot = (0,0,1)
            bpy.data.scenes[0].yafaray.preview.camDist = 12
            return{'FINISHED'}    

    class OBJECT_OT_CamZoomIn(bpy.types.Operator):
        """ Camera zoom in (reduces distance between camera and object) """
        bl_idname = "preview.camzoomin"
        bl_label = "reset camera rotation/distance values to defaults"
        country = bpy.props.StringProperty()
     
        def execute(self, context):
            bpy.data.scenes[0].yafaray.preview.camDist -= 0.5;
            return{'FINISHED'}    

    class OBJECT_OT_CamZoomOut(bpy.types.Operator):
        """ Camera zoom out (increases distance between camera and object) """
        bl_idname = "preview.camzoomout"
        bl_label = "reset camera rotation/distance values to defaults"
        country = bpy.props.StringProperty()
     
        def execute(self, context):
            bpy.data.scenes[0].yafaray.preview.camDist += 0.5;
            return{'FINISHED'}    


def register():
    ########### YafaRay's general settings properties #############
    Scene.gs_accelerator = EnumProperty(
        name="Scene accelerator",
        description="Selects the scene accelerator algorithm",
        items=(
            ('yafaray-kdtree-original', "KDTree single-thread", "KDTree single-thread (original/default, faster but single threaded)"),
            ('yafaray-kdtree-multi-thread', "KDTree multi-thread", "KDTree multi-thread (slower per thread, but might be faster for >= 8 cores)"),
            ('yafaray-simpletest', "Simple/Test", "Simple (for development TESTING ONLY, very slow renders!)"),
        ),
        default='yafaray-kdtree-original')

    Scene.gs_ray_depth = IntProperty(
        name="Ray depth",
        description="Maximum depth for recursive raytracing",
        min=0, max=64, default=2)

    Scene.gs_shadow_depth = IntProperty(
        name="Shadow depth",
        description="Max. depth for transparent shadows calculation (if enabled)",
        min=0, max=64, default=2)

    Scene.gs_threads = IntProperty(
        name="Threads",
        description="Number of threads to use for rendering",
        min=1, default=1)

    Scene.gs_gamma = FloatProperty(
        name="Gamma",
        description="Gamma correction applied to final output, inverse correction "
                    "of textures and colors is performed",
        min=0, max=5, default= 1.0)

    Scene.gs_gamma_input = FloatProperty(
        name="Gamma input",
        description="Gamma correction applied to input",
        min=0, max=5, default=1.0)

    Scene.gs_tile_size = IntProperty(
        name="Tile size",
        description="Size of the render buckets (tiles)",
        min=0, max=1024, default=32)

    Scene.gs_tile_order = EnumProperty(
        name="Tile order",
        description="Selects tiles order type",
        items=(
            ('linear', "Linear", "Render tiles appear in succesive lines until all render is complete."),
            ('random', "Random", "Render tiles appear at random locations until all render is complete."),
            ('centre', "Centre", "Render tiles appear around the centre of the image expanding until all render is complete.")
        ),
        default='centre')

    Scene.gs_auto_threads = BoolProperty(
        name="Auto threads",
        description="Activate thread number auto detection",
        default=True)

    Scene.gs_clay_render = BoolProperty(
        name="Render clay",
        description="Override all materials with a white diffuse material",
        default=False)

    Scene.gs_clay_render_keep_transparency = BoolProperty(
        name="Keep transparency",
        description="Keep transparency during clay render",
        default=False)

    Scene.gs_clay_render_keep_normals = BoolProperty(
        name="Keep normal/bump maps",
        description="Keep normal and bump maps during clay render",
        default=False)

    Scene.gs_clay_oren_nayar = BoolProperty(
        name="Oren-Nayar",
        description="Use Oren-Nayar shader for a more realistic diffuse clay render",
        default=True)

    Scene.gs_clay_sigma = FloatProperty(
        name="Sigma",
        description="Roughness of the clay surfaces when rendering with Clay-Oren Nayar",
        min=0.0, max=1.0,
        step=1, precision=5,
        soft_min=0.0, soft_max=1.0,
        default=0.30000)


    # added clay color property
    Scene.gs_clay_col = FloatVectorProperty(
        name="Clay color",
        description="Color of clay render material - default value Middle Gray (sRGB 50% reflectance)", #as defined at https://en.wikipedia.org/wiki/Middle_gray
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(0.216, 0.216, 0.216))

    Scene.gs_mask_render = BoolProperty(
        name="Render mask",
        description="Renders an object mask pass with different colors",
        default=False)

    Scene.bg_transp = BoolProperty(
        name="Transp.background",
        description="Render the background as transparent",
        default=False)

    Scene.bg_transp_refract = BoolProperty(
        name="Materials transp. refraction",
        description="Materials refract the background as transparent",
        default=True)

    Scene.adv_auto_shadow_bias_enabled = BoolProperty(
        name="Shadow Bias Automatic",
        description="Shadow Bias Automatic Calculation (recommended). Disable ONLY if artifacts or black dots due to bad self-shadowing, otherwise LEAVE THIS ENABLED FOR NORMAL SCENES",
        default=True)

    Scene.adv_shadow_bias_value = FloatProperty(
        name="Shadow Bias Factor",
        description="Shadow Bias (default 0.0005). Change ONLY if artifacts or black dots due to bad self-shadowing. Increasing this value can led to artifacts and incorrect renders",
        min=0.00000001, max=10000, default=0.0005)

    Scene.adv_auto_min_raydist_enabled = BoolProperty(
        name="Min Ray Dist Automatic",
        description="Min Ray Dist Automatic Calculation (recommended), based on the Shadow Bias factor. Disable ONLY if artifacts or light leaks due to bad ray intersections, otherwise LEAVE THIS ENABLED FOR NORMAL SCENES",
        default=True)

    Scene.adv_min_raydist_value = FloatProperty(
        name="Min Ray Dist Factor",
        description="Min Ray Dist (default 0.00005). Change ONLY if artifacts or light leaks due to bad ray intersections. Increasing this value can led to artifacts and incorrect renders",
        min=0.00000001, max=10000, default=0.00005)

    Scene.adv_base_sampling_offset = IntProperty(
        name="Base Sampling Offset",
        description="For multi-computer film generation, set a different sampling offset in each computer so they don't \"repeat\" the same samples. Separate them enough (at least the number of samples each computer is supposed to calculate)",
        min=0, max=2000000000,
        default=0)

    Scene.adv_scene_type = EnumProperty(
        name="Scene Type/Renderer",
        description="Selects the scene type/renderer, 'yafaray' by default. Other scene types/renderers might be added in the future.",
        items=(
            ('yafaray', "yafaray", "(default) YafaRay scene type/renderer will be used."),
        ),
        default='yafaray')

    Scene.gs_premult = EnumProperty(
        name="Premultiply",
        description="Premultipy Alpha channel for renders with transparent background",
        items=(
            ('yes', "Yes", "Apply Alpha channel Premultiply"),
            ('no', "No", "Don't apply Alpha channel Premultiply"),
            ('auto', "Auto", "Automatically try to guess if Alpha channel Premultiply is needed depending on the file type (recommended)")
        ),
        default='auto')

    Scene.gs_transp_shad = BoolProperty(
        name="Transparent shadows",
        description="Compute transparent shadows",
        default=False)

    Scene.gs_show_sam_pix = BoolProperty(
        name="Show sample pixels",
        description="Masks pixels marked for resampling during adaptive passes",
        default=True)
    
    Scene.gs_type_render = EnumProperty(
        name="Render",
        description="Choose the render output method",
        items=(
            ('file', "Image file", "Render the Scene and write it to an Image File when finished"),
            ('into_blender', "Into Blender", "Render the Scene into Blenders Renderbuffer"),
            ('xml', "Export to XML file", "Export the Scene to a XML File"),
            ('c', "Export to C file", "Export the Scene to an ANSI C89/C90 File"),
            ('python', "Export to Python file", "Export the Scene to a Python3 File"),
        ),
        default='into_blender')

    Scene.gs_secondary_file_output = BoolProperty(
        name="Secondary file output",
        description="Enable saving YafaRay render results at the same time as importing into Blender",
        default=True)

    Scene.gs_tex_optimization = EnumProperty(
        name="Textures optimization",
        description="Textures optimization to reduce RAM usage, can be overriden by per-texture setting",
        items=(
            ('compressed', "Compressed", "Lossy color compression, some color/transparency details will be lost, more RAM improvement"),
            ('optimized', "Optimized", "Lossless optimization, good RAM improvement"),
            ('none', "None", "No optimization, lossless and faster but high RAM usage")
        ),
        default='optimized')

    Scene.gs_images_autosave_interval_seconds = FloatProperty(
        name="Interval (s)",
        description="Images AutoSave Interval (in seconds) to autosave partially rendered images. WARNING: short intervals can increase significantly render time.",
        min=5.0, default=300.0, precision=1)

    Scene.gs_images_autosave_interval_passes = IntProperty(
        name="Interval (passes)",
        description="Images AutoSave Interval (every X passes) to autosave partially rendered images.",
        min=1, default=1)

    Scene.gs_images_autosave_interval_type = EnumProperty(
        name="Autosave interval",
        description="Images AutoSave: type of interval",
        items=(
            ('pass-interval', "Passes interval", "Autosaves the image every X render AA passes"),
            ('time-interval', "Time interval", "Autosaves the image every X seconds"),
            ('none', "Disabled", "Image autosave will be disabled")
        ),
        default="none")

    Scene.gs_film_save_load = EnumProperty(
        name="Internal ImageFilm save/load",
        description="Option to save / load the imageFilm, may be useful to continue interrupted renders. The ImageFilm file can be BIG and SLOW, especially when enabling many render passes.",
        items=(
            ('load-save', "Load and Save", "Loads the internal ImageFilm files at start. USE WITH CARE! It will also save the ImageFilm with the images"),
            ('save', "Save", "Saves the internal ImageFilm with the images"),
            ('none', "Disabled", "Image autosave will be disabled")
        ),
        default="none")

    Scene.gs_film_autosave_interval_seconds = FloatProperty(
        name="Interval (s)",
        description="Internal ImageFilm AutoSave Interval (in seconds). WARNING: short intervals can increase significantly render time.",
        min=5.0, default=300.0, precision=1)

    Scene.gs_film_autosave_interval_passes = IntProperty(
        name="Interval (passes)",
        description="Internal ImageFilm AutoSave Interval (every X passes).",
        min=1, default=1)

    Scene.gs_film_autosave_interval_type = EnumProperty(
        name="Autosave interval",
        description="Internal ImageFilm AutoSave: type of interval",
        items=(
            ('pass-interval', "Passes interval", "Autosaves the image every X render AA passes"),
            ('time-interval', "Time interval", "Autosaves the image every X seconds"),
            ('none', "Disabled", "Image autosave will be disabled")
        ),
        default="none")

    ######### YafaRays own image output property ############
    Scene.img_output = EnumProperty(
        name="Image File Type",
        description="Image will be saved in this file format",
        items=(
            ('PNG', " PNG (Portable Network Graphics)", ""),
            ('TARGA', " TGA (Truevision TARGA)", ""),
            ('JPEG', " JPEG (Joint Photographic Experts Group)", ""),
            ('TIFF', " TIFF (Tag Image File Format)", ""),
            ('OPEN_EXR', " EXR (IL&M OpenEXR)", ""),
            ('HDR', " HDR (Radiance RGBE)", "")
        ),
        default='PNG', update=call_update_fileformat)

    Scene.img_multilayer = BoolProperty(
        name="MultiLayer",
        description="Enable MultiLayer image export, only available in certain formats as EXR",
        default=False)

    Scene.img_denoise = BoolProperty(
        name="Denoise",
        description="Enable Denoise for image export. Not available for HDR / EXR formats",
        default=False)

    Scene.img_denoiseHLum = IntProperty(
        name="Denoise hLum",
        description="Denoise h (luminance) property. Increase it to reduce brightness noise (but could blur the image!)",
        min=1, max=40, default=5)

    Scene.img_denoiseHCol = IntProperty(
        name="Denoise hCol",
        description="Denoise h (chrominance) property. Increase it to reduce color noise (but could blur the colors in the image!)",
        min=1, max=40, default=5)

    Scene.img_denoiseMix = FloatProperty(
        name="Denoise Mix",
        description="Proportion of denoised and original image. Recommended approx 0.8 (80% denoised + 20% original) to avoid banding artifacts in fully denoised images",
        min=0.0, max=1.0, default=0.8, precision=2)

    Scene.img_save_with_blend_file = BoolProperty(
        name="Save with .blend file",
        description="Save image/logs in a folder with same name as the .blend file plus suffix ""_render""",
        default=True)

    Scene.img_add_blend_name = BoolProperty(
        name="Include .blend name",
        description="Include .blend name in the image filename",
        default=True)
        
    Scene.img_add_datetime = BoolProperty(
        name="Include date/time",
        description="Include current date/time in the image filename",
        default=False)

    ########### YafaRays integrator properties #############
    Scene.intg_light_method = EnumProperty(
        name="Lighting Method",
        items=(
            ('Direct Lighting', "Direct Lighting", ""),
            ('Photon Mapping', "Photon Mapping", ""),
            ('Pathtracing', "Pathtracing", ""),
            ('Debug', "Debug", ""),
            ('Bidirectional', "Bidirectional (unstable)", ""),
            ('SPPM', "SPPM", "")
        ),
        default='Direct Lighting')

    Scene.intg_use_caustics = BoolProperty(
        name="Caustic Photons",
        description="Enable caustic photons processing in Direct Light integrator",
        default=False)

    Scene.intg_photons = IntProperty(
        name="Photons",
        description="Number of photons to be shot",
        min=1, max=100000000,
        default=500000)

    Scene.intg_caustic_mix = IntProperty(
        name="Caustic Mix",
        description="Max. number of photons to mix (blur)",
        min=1, max=10000,
        default=100)

    Scene.intg_caustic_depth = IntProperty(
        name="Caustic Depth",
        description="Max. number of scatter events for photons",
        min=0, max=50,
        default=10)

    Scene.intg_caustic_radius = FloatProperty(
        name="Caustic Radius",
        description="Max. radius to search for photons",
        min=0.0001, max=100.0,
        default=1.0)

    Scene.intg_use_AO = BoolProperty(
        name="Ambient Occlusion",
        description="Enable ambient occlusion",
        default=False)

    Scene.intg_AO_samples = IntProperty(
        name="Samples",
        description="Number of samples for ambient occlusion",
        min=1, max=1000,
        default=32)

    Scene.intg_AO_distance = FloatProperty(
        name="Distance",
        description=("Max. occlusion distance,"
                     " Surfaces further away do not occlude ambient light"),
        min=0.0, max=10000.0,
        default=1.0)

    Scene.intg_AO_color = FloatVectorProperty(
        name="AO Color",
        description="Color Settings", subtype='COLOR',
        min=0.0, max=1.0,
        default=(0.9, 0.9, 0.9))

    Scene.intg_photonmap_enable_caustics = BoolProperty(
        name="Caustic Photons",
        description="Enable caustic photons processing in Photon Map integrator",
        default=True)

    Scene.intg_photonmap_enable_diffuse = BoolProperty(
        name="Diffuse Photons",
        description="Enable diffuse photons processing in Photon Map integrator",
        default=True)

    Scene.intg_photon_maps_processing = EnumProperty(
        name="Photon Maps processing",
        items=(
            ('generate-only', 'Generate only', "Generate the Photon Maps in each render (default and RECOMMENDED)"),
            ('generate-save', 'Generate and save', "Generate the Photon Maps and save them to files so they can be reloaded later"),
            ('load', 'Load', "Load the Photon Maps from files. USE WITH CARE, only for scenes where ONLY the camera changes, like fly-through scenes"),
            ('reuse-previous', 'Reuse previous', "Reuse previously generated Photon Maps from memory. USE WITH CARE, only for scenes where ONLY the camera changes, like fly-through scenes")            
        ),
        default='generate-only')

    Scene.intg_bounces = IntProperty(
        name="Depth",
        description="",
        min=1,
        default=4)

    Scene.intg_russian_roulette_min_bounces = IntProperty(
        name="Min bounces",
        description="After this number of bounces, start using russian roulette to speed up path tracing. The lower this value, the faster but possibly noisier, especially in darker areas. To disable russian roulette, set Min bounces = Depth.",
        min=0,
        default=2)

    Scene.intg_diffuse_radius = FloatProperty(
        name="Search radius",
        description="Radius to search for diffuse photons",
        min=0.001,
        default=1.0)

    Scene.intg_cPhotons = IntProperty(
        name="Count",
        description="Number of caustic photons to be shot",
        min=1, default=500000)

    Scene.intg_search = IntProperty(
        name="Search count",
        description="Maximum number of diffuse photons to be filtered",
        min=1, max=10000,
        default=100)

    Scene.intg_final_gather = BoolProperty(
        name="Final Gather",
        description="Use final gathering (recommended)",
        default=True)

    Scene.intg_fg_bounces = IntProperty(
        name="Bounces",
        description="Allow gather rays to extend to paths of this length",
        min=1, max=20,
        default=3)

    Scene.intg_fg_samples = IntProperty(
        name="Samples",
        description="Number of samples for final gathering",
        min=1,
        default=16)

    Scene.intg_show_map = BoolProperty(
        name="Show radiance map",
        description="Directly show radiance map, useful to calibrate the photon map (disables final gathering step)",
        default=False)

    Scene.intg_caustic_method = EnumProperty(
        name="Caustic Method",
        items=(
            ('None', "None", ""),
            ('Path', "Path", ""),
            ('Path+Photon', "Path+Photon", ""),
            ('Photon', "Photon", "")),
        description="Choose caustic rendering method",
        default='None')

    Scene.intg_path_samples = IntProperty(
        name="Path Samples",
        description="Number of path samples per pixel sample",
        min=1,
        default=32)

    Scene.intg_no_recursion = BoolProperty(
        name="No Recursion",
        description="No recursive raytracing, only pure path tracing",
        default=False)

    Scene.intg_debug_type = EnumProperty(
        name="Debug type",
        items=(
            ('N', "N", ""),
            ('dPdU', "dPdU", ""),
            ('dPdV', "dPdV", ""),
            ('NU', "NU", ""),
            ('NV', "NV", ""),
            ('dSdU', "dSdU", ""),
            ('dSdV', "dSdV", "")),
        default='dSdV')

    Scene.intg_show_perturbed_normals = BoolProperty(
        name="Show perturbed normals",
        description="Show the normals perturbed by bump and normal maps",
        default=False)

    Scene.intg_pm_ire = BoolProperty(
        name="PM Initial Radius Estimate",
        default=False)

    Scene.intg_pass_num = IntProperty(
        name="Passes",
        min=1,
        default=1000)

    Scene.intg_times = FloatProperty(
        name="Radius factor",
        min=0.0,
        description= "Initial radius times",
        default=1.0)

    Scene.intg_photon_radius = FloatProperty(
        name="Search radius",
        min=0.0,
        default=1.0)

    ######### YafaRays anti-aliasing/noise properties ###########
    Scene.AA_min_samples = IntProperty(
        name="Samples",
        description="Number of samples for first AA pass",
        min=1,
        default=1)

    Scene.AA_inc_samples = IntProperty(
        name="Additional Samples",
        description="Number of samples for additional AA passes",
        min=1,
        default=1)

    Scene.AA_passes = IntProperty(
        name="Passes",
        description=("Number of anti-aliasing passes,"
                     " Adaptive sampling (passes > 1) uses different pattern"),
        min=1,
        default=1)

    Scene.AA_threshold = FloatProperty(
        name="Threshold",
        description="Color threshold for additional AA samples in next pass",
        min=0.0, max=1.0, precision=4,
        default=0.05)

    Scene.AA_pixelwidth = FloatProperty(
        name="Pixelwidth",
        description="AA filter size",
        min=1.0, max=20.0, precision=3,
        default=1.5)

    Scene.AA_filter_type = EnumProperty(
        name="Filter",
        items=(
            ('box', "Box", "AA filter type"),
            ('mitchell', "Mitchell", "AA filter type"),
            ('gauss', "Gauss", "AA filter type"),
            ('lanczos', "Lanczos", "AA filter type")
        ),
        default="gauss")

    bpy.utils.register_class(YafaRay4Properties)
    bpy.types.Scene.yafaray = PointerProperty(type=YafaRay4Properties)

    bpy.utils.register_class(YafaRay4LayersProperties)
    YafaRay4Properties.passes = PointerProperty(type=YafaRay4LayersProperties)

    bpy.utils.register_class(YafaRay4NoiseControlProperties)
    YafaRay4Properties.noise_control = PointerProperty(type=YafaRay4NoiseControlProperties)

    bpy.utils.register_class(YafaRay4LoggingProperties)
    YafaRay4Properties.logging = PointerProperty(type=YafaRay4LoggingProperties)

    bpy.utils.register_class(YafaRay4MaterialPreviewControlProperties)
    YafaRay4Properties.preview = PointerProperty(type=YafaRay4MaterialPreviewControlProperties)


def unregister():
    bpy.utils.unregister_class(YafaRay4MaterialPreviewControlProperties)
    bpy.utils.unregister_class(YafaRay4LoggingProperties)
    bpy.utils.unregister_class(YafaRay4NoiseControlProperties)
    bpy.utils.unregister_class(YafaRay4LayersProperties)
    bpy.utils.unregister_class(YafaRay4Properties)

    del Scene.gs_accelerator
    del Scene.gs_ray_depth
    del Scene.gs_shadow_depth
    del Scene.gs_threads
    del Scene.gs_gamma
    del Scene.gs_gamma_input
    del Scene.gs_tile_size
    del Scene.gs_tile_order
    del Scene.gs_auto_threads
    del Scene.gs_clay_render
    del Scene.gs_clay_render_keep_transparency
    del Scene.gs_clay_render_keep_normals
    del Scene.gs_clay_oren_nayar
    del Scene.gs_clay_sigma
    del Scene.gs_clay_col
    del Scene.gs_mask_render
    del Scene.bg_transp
    del Scene.bg_transp_refract
    del Scene.adv_auto_shadow_bias_enabled
    del Scene.adv_shadow_bias_value
    del Scene.adv_auto_min_raydist_enabled
    del Scene.adv_min_raydist_value
    del Scene.adv_base_sampling_offset
    del Scene.adv_scene_type

    del Scene.gs_premult
    del Scene.gs_transp_shad
    del Scene.gs_show_sam_pix
    del Scene.gs_type_render
    del Scene.gs_secondary_file_output
    del Scene.gs_tex_optimization
    del Scene.gs_images_autosave_interval_seconds
    del Scene.gs_images_autosave_interval_passes
    del Scene.gs_images_autosave_interval_type
    del Scene.gs_film_save_load
    del Scene.gs_film_autosave_interval_seconds
    del Scene.gs_film_autosave_interval_passes
    del Scene.gs_film_autosave_interval_type

    del Scene.img_output
    del Scene.img_multilayer
    del Scene.img_denoise
    del Scene.img_denoiseHLum
    del Scene.img_denoiseHCol
    del Scene.img_denoiseMix
    del Scene.img_save_with_blend_file
    del Scene.img_add_blend_name
    del Scene.img_add_datetime

    del Scene.intg_light_method
    del Scene.intg_use_caustics
    del Scene.intg_photons
    del Scene.intg_caustic_mix
    del Scene.intg_caustic_depth
    del Scene.intg_caustic_radius
    del Scene.intg_use_AO
    del Scene.intg_AO_samples
    del Scene.intg_AO_distance
    del Scene.intg_AO_color
    del Scene.intg_photonmap_enable_caustics
    del Scene.intg_photonmap_enable_diffuse
    del Scene.intg_photon_maps_processing
    del Scene.intg_bounces
    del Scene.intg_russian_roulette_min_bounces
    del Scene.intg_diffuse_radius
    del Scene.intg_cPhotons
    del Scene.intg_search
    del Scene.intg_final_gather
    del Scene.intg_fg_bounces
    del Scene.intg_fg_samples
    del Scene.intg_show_map
    del Scene.intg_caustic_method
    del Scene.intg_path_samples
    del Scene.intg_no_recursion
    del Scene.intg_debug_type
    del Scene.intg_show_perturbed_normals
    del Scene.intg_pm_ire
    del Scene.intg_pass_num
    del Scene.intg_times
    del Scene.intg_photon_radius

    del Scene.AA_min_samples
    del Scene.AA_inc_samples
    del Scene.AA_passes
    del Scene.AA_threshold
    del Scene.AA_pixelwidth
    del Scene.AA_filter_type
