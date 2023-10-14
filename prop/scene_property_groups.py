import bpy
from bpy.props import (IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       BoolProperty,
                       StringProperty,
                       PointerProperty)

from ..util.properties_annotations import replace_properties_with_annotations


# noinspection PyUnusedLocal
def update_preview(self, context):
    if context is not None and context.space_data is not None:
        context.space_data.context = context.space_data.context  # To force redrawing the preview panel


# noinspection PyTypeChecker
@replace_properties_with_annotations
class YafaRay4SceneProperties(bpy.types.PropertyGroup):
    migrated_to_v4 = BoolProperty(
        name="Migrated to YafaRay v4",
        description="Flag indicating whether the scene has been already migrated to YafaRay v4",
        default=False)
    texture_edition_panel = EnumProperty(
        name="Select Generic Texture Edition Panel",
        description="Property to select the Texture Edition Panel to be shown",
        items=[
            ('MATERIAL', "Material", "Shows the Material Texture Slots Properties panel"),
            ('WORLD', "World",
             "Shows the World Texture Properties panel"),
            ('TEXTURE', "Texture", "Shows a generic Texture Properties panel")
        ],
        default='MATERIAL')


# noinspection PyTypeChecker
@replace_properties_with_annotations
class YafaRay4TexturePropertiesEdition(bpy.types.PropertyGroup):
    texture_selected = PointerProperty(name="Texture selected",
                                       description="Texture selected for properties edition",
                                       type=bpy.types.Texture,
                                       update=update_preview)


# noinspection PyTypeChecker
@replace_properties_with_annotations
class YafaRay4LoggingProperties(bpy.types.PropertyGroup):
    params_badge_position = EnumProperty(
        name="Params Badge position",
        description="Choose the position of the params badge in the exported image file. Inside Blender it may appear "
                    "incorrect or not at all",
        items=[
            ('top', "Top", "Params badge will appear at the top of the exported image file"),
            ('bottom', "Bottom",
             "Params badge will appear at the bottom of the exported image file. It may appear cropped in Blender."),
            ('none', "None", "Params badge will not appear")
        ],
        default='none')

    save_log = BoolProperty(
        name="Save log file",
        description="Save text log file with the exported image files",
        default=False)

    save_html = BoolProperty(
        name="Save HTML file",
        description="Save HTML information/log file with the exported image files",
        default=True)

    save_preset = BoolProperty(
        name="Save Preset file",
        description="Save a preset file, with the Render Settings, with the exported image files",
        default=True)

    __verbosity_levels = sorted((
        ('mute', "Mute (silent)", "Prints nothing", 0),
        ('error', "Error", "Prints only errors", 1),
        ('warning', "Warning", "Prints also warnings", 2),
        ('params', "Params", "Prints also render param messages", 3),
        ('info', "Info", "Prints also basic info messages", 4),
        ('verbose', "Verbose", "Prints additional info messages", 5),
        ('debug', "Debug", "Prints debug messages (if any)", 6),
    ), key=lambda index: index[3])

    log_print_date_time = BoolProperty(
        name="Log Date/Time",
        description="Print Date/Time in the logs (enabled by default)",
        default=True)

    console_verbosity = EnumProperty(
        name="Console Verbosity",
        description="Select the desired verbosity level for console log output",
        items=__verbosity_levels,
        default="info")

    log_verbosity = EnumProperty(
        name="Log/HTML Verbosity",
        description="Select the desired verbosity level for log and HTML output",
        items=__verbosity_levels,
        default="info")

    draw_render_settings = BoolProperty(
        name="Draw Render Settings",
        description="Draw Render Settings in the params badge",
        default=True)

    draw_aa_noise_settings = BoolProperty(
        name="Draw AA/Noise Settings",
        description="Draw AA and Noise Control Settings in the params badge",
        default=True)

    title = StringProperty(
        name="Title",
        description="Title to be shown in the logs and/or params badge",
        default="")

    author = StringProperty(
        name="Author",
        description="Author to be shown in the logs and/or params badge",
        default="")

    contact = StringProperty(
        name="Contact info",
        description="Contact information (phone, e-mail, etc) to be shown in the logs and/or params badge",
        default="")

    comments = StringProperty(
        name="Comments",
        description="Comments to be added to the logs and/or params badge",
        default="")

    custom_icon = StringProperty(
        name="Custom PNG icon path",
        description=("Path to custom icon for logs and/or params badge."
                     "(recommended around 70x45, black background)."
                     "If blank or wrong, the default YafaRay icon will be shown"),
        subtype="FILE_PATH",
        default="")

    custom_font = StringProperty(
        name="Font path",
        description=("Path to params badge TTF font."
                     "If blank or wrong, the default YafaRay font will be used"),
        subtype="FILE_PATH",
        default="")

    font_scale = FloatProperty(
        name="Font scale",
        description="Font scaling factor.",
        min=0.2, max=5.0, precision=1,
        default=1.0)


# noinspection PyTypeChecker
@replace_properties_with_annotations
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
        items=[
            ('none', "None", "No special dark areas noise detection (default)"),
            ('linear', "Linear", "Linearly change AA threshold depending on pixel brightness and Dark factor"),
            ('curve', "Curve", "Change AA threshold based on a pre-computed curve")
        ],
        default="linear")

    dark_threshold_factor = FloatProperty(
        name="Dark factor",
        description=("Factor used to reduce the AA threshold in dark areas."
                     " It will reduce noise in dark areas, but noise in bright areas will take longer."
                     " You probably need to increase the main AA threshold value if you use this parameter"),
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


# noinspection PyTypeChecker
@replace_properties_with_annotations
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

    object_edge_thickness = IntProperty(
        name="Object Edge Thickness",
        description="Thickness of the edges used in the Object Edge and Toon Render Passess",
        min=1, max=10,
        default=2)

    faces_edge_thickness = IntProperty(
        name="Faces Edge Thickness",
        description="Thickness of the edges used in the Faces Edge Render Pass",
        min=1, max=10,
        default=1)

    object_edge_threshold = FloatProperty(
        name="Object Edge Threshold",
        description="Threshold for the edge detection process used in the Object Edge and Toon Render Passes",
        min=0.0, max=1.0,
        precision=3,
        default=0.3)

    faces_edge_threshold = FloatProperty(
        name="Faces Edge Threshold",
        description="Threshold for the edge detection process used in the Faces Edge Render Pass",
        min=0.0, max=1.0,
        precision=3,
        default=0.01)

    object_edge_smoothness = FloatProperty(
        name="Object Edge Smoothness",
        description="Smoothness (blur) of the edges used in the Object Edge and Toon Render Passes",
        min=0.0, max=5.0,
        precision=2,
        default=0.75)

    faces_edge_smoothness = FloatProperty(
        name="Faces Edge Smoothness",
        description="Smoothness (blur) of the edges used in the Faces Edge Render Pass",
        min=0.0, max=5.0,
        precision=2,
        default=0.5)

    toon_edge_color = FloatVectorProperty(
        name="Toon Edge Color",
        description="Color of the edges used in the Toon Render Pass",
        subtype='COLOR',
        step=1, precision=2,
        min=0.0, max=1.0,
        soft_min=0.0, soft_max=1.0,
        default=(0.0, 0.0, 0.0))

    toon_pre_smooth = FloatProperty(
        name="Toon Pre-Smooth",
        description="Toon effect: smoothness applied to the original image",
        min=0.0,
        precision=2,
        default=3.0)

    toon_post_smooth = FloatProperty(
        name="Toon Post-Smooth",
        description="Toon effect: smoothness applied to the original image",
        min=0.0,
        precision=2,
        default=3.0)

    toon_quantization = FloatProperty(
        name="Toon Color Quantization",
        description="Toon effect: color Quantization applied to the original image",
        min=0.0, max=1.0,
        precision=3,
        default=0.1)

    # The numbers here MUST NEVER CHANGE to keep backwards compatibility with older scenes. The numbers do not need
    # to match the Core internal pass numbers. The matching between these properties and the YafaRay Core internal
    # passes is done via the first string, for example 'z-depth-abs'. They must match the list of strings for
    # internal passes in the Core: include/core_api/color.h

    __render_pass_items_disabled = sorted((
        ('disabled', "Disabled", "Disable this pass", 999999),
    ), key=lambda index: index[1])

    __render_pass_items_basic = sorted((
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

    __render_pass_items_depth = sorted((
        ('z-depth-abs', "Z-Depth (absolute)", "Z-Depth (absolute values)", 101),
        ('z-depth-norm', "Z-Depth (normalized)", "Z-Depth (normalized values)", 102),
    ), key=lambda index: index[1])

    __render_pass_items_index = sorted((
        ('obj-index-abs', "Index-Object (absolute)",
         "Index-Object: Grayscale value = obj.index in the object properties (absolute values)", 201),
        ('obj-index-norm', "Index-Object (normalized)",
         "Index-Object: Grayscale value = obj.index in the object properties (normalized values)", 202),
        (
            'obj-index-auto', "Index-Object (auto, color)",
            "Index-Object: A color automatically generated for each object",
            203),
        ('obj-index-mask', "Index-Object Mask", "Index-Object: Masking object based on obj.index.mask setting", 204),
        ('obj-index-mask-shadow', "Index-Object Mask Shadow",
         "Index-Object: Masking object shadow based on obj.index.mask setting", 205),
        ('obj-index-mask-all', "Index-Object Mask All (Object+Shadow)",
         "Index-Object: Masking object+shadow based on obj.index.mask setting", 206),
        ('mat-index-abs', "Index-Material (absolute)",
         "Index-Material: Grayscale value = mat.index in the material properties (absolute values)", 207),
        ('mat-index-norm', "Index-Material (normalized)",
         "Index-Material: Grayscale value = mat.index in the material properties (normalized values)", 208),
        ('mat-index-auto', "Index-Material (auto, color)",
         "Index-Material: A color automatically generated for each material", 209),
        ('mat-index-mask', "Index-Material Mask", "Index-Material: Masking material based on mat.index.mask setting",
         210),
        ('mat-index-mask-shadow', "Index-Material Mask Shadow",
         "Index-Material: Masking material shadow based on mat.index.mask setting", 211),
        ('mat-index-mask-all', "Index-Material Mask All (Object+Shadow)",
         "Index-Material: Masking material+shadow based on mat.index.mask setting", 212),
        ('obj-index-auto-abs', "Index-Object (auto, absolute)",
         "Index-Object: An absolute value automatically generated for each object", 213),
        ('mat-index-auto-abs', "Index-Material (auto, absolute)",
         "Index-Material: An absolute value automatically generated for each material", 214)
    ), key=lambda index: index[1])

    __render_pass_items_debug = sorted((
        ('debug-aa-samples', "Debug: AA sample count", "Debug: Adaptative AA sample count (estimation), normalized",
         301),
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
        ('debug-light-estimation-light-sampling', "Debug: LE Light Sampling",
         "Light Estimation (Area lights, light sampling)", 312),
        ('debug-light-estimation-mat-sampling', "Debug: LE Mat Sampling",
         "Light Estimation (Area lights, material sampling)", 313),
        ('debug-wireframe', "Debug: Wireframe",
         "Show the objects wireframe (triangles) depending on the material wireframe parameters (except for wireframe "
         "amount)",
         314),
        ('debug-faces-edges', "Debug: Faces Edges",
         "Show the faces edges, potentially useful as alternative wireframe pass that can show quads and polygons in "
         "a better way",
         315),
        ('debug-objects-edges', "Debug: Objects Edges",
         "Show the objects edges, potentially useful for toon-like shading", 316),
        ('debug-sampling-factor', "Debug: Sampling Factor", "Show the materials sampling factor", 317),
        ('debug-dp-lengths', "Debug: differential dP lengths",
         "For debugging mipmaps, etc, show differential dPdx and dPdy lengths", 318),
        ('debug-dpdx', "Debug: differential dPdx",
         "For debugging mipmaps, etc, show differential dPdx X,Y,Z coordinates", 319),
        ('debug-dpdy', "Debug: differential dPdy",
         "For debugging mipmaps, etc, show differential dPdy X,Y,Z coordinates", 320),
        ('debug-dpdxy', "Debug: differential dPdx+dPdy",
         "For debugging mipmaps, etc, show differential dPdx+dPdy X,Y,Z coordinates", 321),
        ('debug-dudx-dvdx', "Debug: differential dUdx, dVdx",
         "For debugging mipmaps, etc, show differential dUdx and dVdx", 322),
        ('debug-dudy-dvdy', "Debug: differential dUdy, dVdy",
         "For debugging mipmaps, etc, show differential dUdy and dVdy", 323),
        ('debug-dudxy-dvdxy', "Debug: differential dUdx+dUdy, dVdx+dVdy",
         "For debugging mipmaps, etc, show differential dUdx+dUdy and dVdx+dVdy", 324),
        ('debug-barycentric-uvw', "Debug: Barycentric UVW", "Debug: barycentric UVW coordinates", 325),
        ('debug-object-time', "Debug: Object Time",
         "Debug: Time of Object samples. Samples of non-motion blur objects are green. Samples of motion blur objects "
         "are blue for t=0.0 towards red for t=1.0",
         326),
    ), key=lambda index: index[1])

    __render_internal_pass_advanced = sorted((
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
        ('adv-indirect', "Adv: Indirect", "Adv: Indirect light (depends on the integrator but usually caustics only)",
         417),
        ('adv-surface-integration', "Adv: Surface Integration", "Advanced: Surface Integration", 418),
    ), key=lambda index: index[1])

    __render_pass_items_ao = sorted((
        ('ao', "AO", "Ambient Occlusion", 501),
        ('ao-clay', "AO clay", "Ambient Occlusion (clay)", 502),
    ), key=lambda index: index[1])

    __render_pass_all_items = sorted(
        __render_pass_items_basic + __render_internal_pass_advanced + __render_pass_items_index
        + __render_pass_items_debug + __render_pass_items_depth + __render_pass_items_ao,
        key=lambda index: index[1])

    # This property is not currently used by YafaRay Core, as the combined external pass is always using the internal
    # combined pass.
    pass_combined = EnumProperty(
        name="Combined",  # RGBA (4 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_items_disabled,
        default="disabled")

    pass_depth = EnumProperty(
        name="Depth",  # Gray (1 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_items_depth,
        default="z-depth-norm")

    pass_vector = EnumProperty(
        name="Vector",  # RGBA (4 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="obj-index-auto")

    pass_normal = EnumProperty(
        name="Normal",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="debug-normal-smooth")

    pass_uv = EnumProperty(
        name="UV",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="debug-uv")

    pass_color = EnumProperty(
        name="Color",  # RGBA (4 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="mat-index-auto")

    pass_emit = EnumProperty(
        name="Emit",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="emit")

    pass_mist = EnumProperty(
        name="Mist",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="mist")

    pass_diffuse = EnumProperty(
        name="Diffuse",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="diffuse")

    pass_spec = EnumProperty(
        name="Spec",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="adv-reflect")

    pass_ao = EnumProperty(
        name="AO",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_items_ao,
        default="ao")

    pass_env = EnumProperty(
        name="Env",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="env")

    pass_indirect = EnumProperty(
        name="Indirect",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="indirect")

    pass_shadow = EnumProperty(
        name="Shadow",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="shadow")

    pass_reflect = EnumProperty(
        name="Reflect",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="reflect")

    pass_refract = EnumProperty(
        name="Refract",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="refract")

    pass_index_ob = EnumProperty(
        name="Object Index",  # Gray (1 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_items_index,
        default="obj-index-norm")

    pass_index_ma = EnumProperty(
        name="Material Index",  # Gray (1 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_items_index,
        default="mat-index-norm")

    pass_diff_dir = EnumProperty(
        name="Diff Dir",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="diffuse")

    pass_diff_ind = EnumProperty(
        name="Diff Ind",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="adv-diffuse-indirect")

    pass_diff_col = EnumProperty(
        name="Diff Col",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="adv-diffuse-color")

    pass_gloss_dir = EnumProperty(
        name="Gloss Dir",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="adv-glossy")

    pass_gloss_ind = EnumProperty(
        name="Gloss Ind",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="adv-glossy-indirect")

    pass_gloss_col = EnumProperty(
        name="Gloss Col",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="adv-glossy-color")

    pass_trans_dir = EnumProperty(
        name="Trans Dir",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="adv-trans")

    pass_trans_ind = EnumProperty(
        name="Trans Ind",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="adv-trans-indirect")

    pass_trans_col = EnumProperty(
        name="Trans Col",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="adv-trans-color")

    pass_subsurface_dir = EnumProperty(
        name="SubSurface Dir",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="adv-subsurface")

    pass_subsurface_ind = EnumProperty(
        name="SubSurface Ind",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="adv-subsurface-indirect")

    pass_subsurface_col = EnumProperty(
        name="SubSurface Col",  # RGB (3 x float)
        description="Select the type of image you want to be displayed in this pass",
        items=__render_pass_all_items,
        default="adv-subsurface-color")


# noinspection PyTypeChecker
@replace_properties_with_annotations
class YafaRay4MaterialPreviewControlProperties(bpy.types.PropertyGroup):
    enable = BoolProperty(
        update=update_preview,
        name="Material Preview Controls enabled",
        description="Enable/Disable material preview controls",
        default=False)

    obj_scale = FloatProperty(
        update=update_preview,
        name="objScale",
        description="Material Preview object scaling factor",
        min=0.0,  # max=10.0,
        precision=2, step=10,
        default=1.0)

    rot_z = FloatProperty(
        update=update_preview,
        name="rotZ",
        description="Material Preview object rotation Z axis",
        precision=1, step=1000,
        # min=math.radians(-360), max=math.radians(360),
        subtype="ANGLE", unit="ROTATION",
        default=0.0)

    light_rot_z = FloatProperty(
        update=update_preview,
        name="lightRotZ",
        description="Material Preview light rotation Z axis",
        precision=1, step=1000,
        # min=math.radians(-360), max=math.radians(360),
        subtype="ANGLE", unit="ROTATION",
        default=0.0)

    key_light_power_factor = FloatProperty(
        update=update_preview,
        name="keyLightPowerFactor",
        description="Material Preview power factor for the key light",
        min=0.0, max=10.0, precision=2, step=10,
        default=1.0)

    fill_light_power_factor = FloatProperty(
        update=update_preview,
        name="lightPowerFactor",
        description="Material Preview power factor for the fill lights",
        min=0.0, max=10.0, precision=2, step=10,
        default=0.5)

    key_light_color = FloatVectorProperty(
        update=update_preview,
        name="keyLightColor",
        description="Material Preview color for key light",
        subtype='COLOR',
        step=1, precision=2,
        min=0.0, max=1.0,
        soft_min=0.0, soft_max=1.0,
        default=(1.0, 1.0, 1.0))

    fill_light_color = FloatVectorProperty(
        update=update_preview,
        name="fillLightColor",
        description="Material Preview color for fill lights",
        subtype='COLOR',
        step=1, precision=2,
        min=0.0, max=1.0,
        soft_min=0.0, soft_max=1.0,
        default=(1.0, 1.0, 1.0))

    preview_ray_depth = IntProperty(
        update=update_preview,
        name="previewRayDepth",
        description="Material Preview max ray depth, set higher for better (slower) glass preview",
        min=0, max=20, default=2)

    preview_aa_passes = IntProperty(
        update=update_preview,
        name="previewAApasses",
        description="Material Preview AA passes, set higher for better (slower) preview",
        min=1, max=20, default=1)

    preview_background = EnumProperty(
        update=update_preview,
        name="previewBackground",
        description="Material Preview background type",
        items=[
            ('none', "None", "No background"),
            ('checker', "Checker", "Checker background (default)"),
            ('world', "Scene World", "Scene world background (can be slow!)")
        ],
        default="checker")

    preview_object = StringProperty(
        update=update_preview,
        name="previewObject",
        description="Material Preview custom object to be shown, if empty will use default preview objects",
        default="")

    cam_dist = FloatProperty(
        update=update_preview,
        name="camDist",
        description="Material Preview Camera distance to object",
        min=0.1, max=22.0, precision=2, step=100,
        default=12.0)

    cam_rot = FloatVectorProperty(
        update=update_preview,
        name="camRot",
        description="Material Preview camera rotation",
        subtype='DIRECTION',
        # step=10, precision=3,
        # min=-1.0, max=1.0,
        default=(0.0, 0.0, 1.0)
    )
