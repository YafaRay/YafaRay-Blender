# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.props import (IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       BoolProperty,
                       PointerProperty)
from .scene_property_groups import YafaRay4LayersProperties, YafaRay4MaterialPreviewControlProperties, \
    YafaRay4NoiseControlProperties, YafaRay4LoggingProperties, YafaRay4MigrationProperties

Scene = bpy.types.Scene


# set file format for image saving on same format as in YafaRay, both have default PNG
# noinspection PyUnusedLocal
def call_update_file_format(self, context):
    scene = context.scene
    render = scene.render
    if scene.img_output is not render.image_settings.file_format:
        render.image_settings.file_format = scene.img_output


class YafaRay4Properties(bpy.types.PropertyGroup):
    pass


def register():
    # YafaRay's general settings properties
    Scene.gs_accelerator = EnumProperty(
        name="Scene accelerator",
        description="Selects the scene accelerator algorithm",
        items=[
            ('yafaray-kdtree-original', "KDTree single-thread",
             "KDTree single-thread (original/default, faster but single threaded)"),
            ('yafaray-kdtree-multi-thread', "KDTree multi-thread",
             "KDTree multi-thread (slower per thread, but might be faster for >= 8 cores)"),
            ('yafaray-simpletest', "Simple/Test", "Simple (for development TESTING ONLY, very slow renders!)"),
        ],
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
        min=0, max=5, default=1.0)

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
        items=[
            ('linear', "Linear", "Render tiles appear in succesive lines until all render is complete."),
            ('random', "Random", "Render tiles appear at random locations until all render is complete."),
            ('centre', "Centre",
             "Render tiles appear around the centre of the image expanding until all render is complete.")
        ],
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
        description="Color of clay render material - default value Middle Gray (sRGB 50% reflectance)",
        # as defined at https://en.wikipedia.org/wiki/Middle_gray
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
        description="Shadow Bias Automatic Calculation (recommended). Disable ONLY if artifacts or black dots due to "
                    "bad self-shadowing, otherwise LEAVE THIS ENABLED FOR NORMAL SCENES",
        default=True)

    Scene.adv_shadow_bias_value = FloatProperty(
        name="Shadow Bias Factor",
        description="Shadow Bias (default 0.0005). Change ONLY if artifacts or black dots due to bad self-shadowing. "
                    "Increasing this value can led to artifacts and incorrect renders",
        min=0.00000001, max=10000, default=0.0005)

    Scene.adv_auto_min_raydist_enabled = BoolProperty(
        name="Min Ray Dist Automatic",
        description="Min Ray Dist Automatic Calculation (recommended), based on the Shadow Bias factor. Disable ONLY "
                    "if artifacts or light leaks due to bad ray intersections, otherwise LEAVE THIS ENABLED FOR "
                    "NORMAL SCENES",
        default=True)

    Scene.adv_min_raydist_value = FloatProperty(
        name="Min Ray Dist Factor",
        description="Min Ray Dist (default 0.00005). Change ONLY if artifacts or light leaks due to bad ray "
                    "intersections. Increasing this value can led to artifacts and incorrect renders",
        min=0.00000001, max=10000, default=0.00005)

    Scene.adv_base_sampling_offset = IntProperty(
        name="Base Sampling Offset",
        description="For multi-computer film generation, set a different sampling offset in each computer so they"
                    "don't \"repeat\" the same samples. Separate them enough (at least the number of samples each "
                    "computer is supposed to calculate)",
        min=0, max=2000000000,
        default=0)

    Scene.adv_scene_type = EnumProperty(
        name="Scene Type/Renderer",
        description="Selects the scene type/renderer, 'yafaray' by default. Other scene types/renderers might be "
                    "added in the future.",
        items=[
            ('yafaray', "yafaray", "(default) YafaRay scene type/renderer will be used.")
        ],
        default='yafaray')

    Scene.adv_scene_mesh_tesselation = EnumProperty(
        name="Mesh Tesselation",
        description="Selects the way that meshes are tesselated before being rendered by YafaRay.",
        items=[
            ('triangles_quads', "Triangles + Quads",
             "(default) Meshes are internally tesselated as a mix of triangles and quads."),
            ('triangles_only', "Triangles Only", "Meshes are internally tesselated as triangles only."),
        ],
        default='triangles_quads')

    Scene.gs_premult = EnumProperty(
        name="Premultiply",
        description="Premultipy Alpha channel for renders with transparent background",
        items=[
            ('yes', "Yes", "Apply Alpha channel Premultiply"),
            ('no', "No", "Don't apply Alpha channel Premultiply"),
            ('auto', "Auto",
             "Automatically try to guess if Alpha channel Premultiply is needed depending on the file type ("
             "recommended)")
        ],
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
        items=[
            ('file', "Image file", "Render the Scene and write it to an Image File when finished"),
            ('into_blender', "Into Blender", "Render the Scene into Blenders Renderbuffer"),
            ('xml', "Export to XML file", "Export the Scene to a XML File"),
            ('c', "Export to C file", "Export the Scene to an ANSI C89/C90 File"),
            ('python', "Export to Python file", "Export the Scene to a Python3 File"),
        ],
        default='into_blender')

    Scene.gs_secondary_file_output = BoolProperty(
        name="Secondary file output",
        description="Enable saving YafaRay render results at the same time as importing into Blender",
        default=True)

    Scene.gs_tex_optimization = EnumProperty(
        name="Textures optimization",
        description="Textures optimization to reduce RAM usage, can be overriden by per-texture setting",
        items=[
            ('compressed', "Compressed",
             "Lossy color compression, some color/transparency details will be lost, more RAM improvement"),
            ('optimized', "Optimized", "Lossless optimization, good RAM improvement"),
            ('none', "None", "No optimization, lossless and faster but high RAM usage")
        ],
        default='optimized')

    Scene.gs_images_autosave_interval_seconds = FloatProperty(
        name="Interval (s)",
        description="Images AutoSave Interval (in seconds) to autosave partially rendered images. WARNING: short "
                    "intervals can increase significantly render time.",
        min=5.0, default=300.0, precision=1)

    Scene.gs_images_autosave_interval_passes = IntProperty(
        name="Interval (passes)",
        description="Images AutoSave Interval (every X passes) to autosave partially rendered images.",
        min=1, default=1)

    Scene.gs_images_autosave_interval_type = EnumProperty(
        name="Autosave interval",
        description="Images AutoSave: type of interval",
        items=[
            ('pass-interval', "Passes interval", "Autosaves the image every X render AA passes"),
            ('time-interval', "Time interval", "Autosaves the image every X seconds"),
            ('none', "Disabled", "Image autosave will be disabled")
        ],
        default="none")

    Scene.gs_film_save_load = EnumProperty(
        name="Internal ImageFilm save/load",
        description="Option to save / load the imageFilm, may be useful to continue interrupted renders. The "
                    "ImageFilm file can be BIG and SLOW, especially when enabling many render passes.",
        items=[
            ('load-save', "Load and Save",
             "Loads the internal ImageFilm files at start. USE WITH CARE! It will also save the ImageFilm with the "
             "images"),
            ('save', "Save", "Saves the internal ImageFilm with the images"),
            ('none', "Disabled", "Image autosave will be disabled")
        ],
        default="none")

    Scene.gs_film_autosave_interval_seconds = FloatProperty(
        name="Interval (s)",
        description="Internal ImageFilm AutoSave Interval (in seconds). WARNING: short intervals can increase"
                    "significantly render time.",
        min=5.0, default=300.0, precision=1)

    Scene.gs_film_autosave_interval_passes = IntProperty(
        name="Interval (passes)",
        description="Internal ImageFilm AutoSave Interval (every X passes).",
        min=1, default=1)

    Scene.gs_film_autosave_interval_type = EnumProperty(
        name="Autosave interval",
        description="Internal ImageFilm AutoSave: type of interval",
        items=[
            ('pass-interval', "Passes interval", "Autosaves the image every X render AA passes"),
            ('time-interval', "Time interval", "Autosaves the image every X seconds"),
            ('none', "Disabled", "Image autosave will be disabled")
        ],
        default="none")

    # YafaRay's own image output property
    Scene.img_output = EnumProperty(
        name="Image File Type",
        description="Image will be saved in this file format",
        items=[
            ('PNG', " PNG (Portable Network Graphics)", ""),
            ('TARGA', " TGA (Truevision TARGA)", ""),
            ('JPEG', " JPEG (Joint Photographic Experts Group)", ""),
            ('TIFF', " TIFF (Tag Image File Format)", ""),
            ('OPEN_EXR', " EXR (IL&M OpenEXR)", ""),
            ('HDR', " HDR (Radiance RGBE)", "")
        ],
        default='PNG', update=call_update_file_format)

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
        description="Denoise h (luminance) property. Increase it to reduce brightness noise"
                    " (but could blur the image!)",
        min=1, max=40, default=5)

    Scene.img_denoiseHCol = IntProperty(
        name="Denoise hCol",
        description="Denoise h (chrominance) property. Increase it to reduce color noise (but could blur the colors "
                    "in the image!)",
        min=1, max=40, default=5)

    Scene.img_denoiseMix = FloatProperty(
        name="Denoise Mix",
        description="Proportion of denoised and original image. Recommended approx 0.8 (80% denoised + 20% original) "
                    "to avoid banding artifacts in fully denoised images",
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

    # YafaRay's integrator properties
    Scene.intg_light_method = EnumProperty(
        name="Lighting Method",
        items=[
            ('Direct Lighting', "Direct Lighting", ""),
            ('Photon Mapping', "Photon Mapping", ""),
            ('Pathtracing', "Pathtracing", ""),
            ('Debug', "Debug", ""),
            ('Bidirectional', "Bidirectional (unstable)", ""),
            ('SPPM', "SPPM", "")
        ],
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

    Scene.intg_motion_blur_time_forced = BoolProperty(
        name="Force time for testing Motion Blur",
        description="For testing purposes only, for testing Motion Blur",
        default=False)

    Scene.intg_motion_blur_time_forced_value = FloatProperty(
        name="Forced time value for testing Motion Blur",
        description="For testing purposes only, for testing Motion Blur",
        min=0.0, max=1.0,
        default=0.0)

    Scene.intg_photonmap_enable_caustics = BoolProperty(
        name="Caustic Photons",
        description="Enable caustic photons processing in Photon Map integrator",
        default=True)

    Scene.intg_photonmap_enable_diffuse = BoolProperty(
        name="Diffuse Photons",
        description="Enable diffuse photons processing in Photon Map integrator",
        default=True)

    Scene.intg_bounces = IntProperty(
        name="Depth",
        description="",
        min=1,
        default=4)

    Scene.intg_russian_roulette_min_bounces = IntProperty(
        name="Min bounces",
        description="After this number of bounces, start using russian roulette to speed up path tracing. The lower "
                    "this value, the faster but possibly noisier, especially in darker areas. To disable russian "
                    "roulette, set Min bounces = Depth.",
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
        items=[
            ('None', "None", ""),
            ('Path', "Path", ""),
            ('Path+Photon', "Path+Photon", ""),
            ('Photon', "Photon", "")],
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
        items=[
            ('N', "N", ""),
            ('dPdU', "dPdU", ""),
            ('dPdV', "dPdV", ""),
            ('NU', "NU", ""),
            ('NV', "NV", ""),
            ('dSdU', "dSdU", ""),
            ('dSdV', "dSdV", "")],
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
        description="Initial radius times",
        default=1.0)

    Scene.intg_photon_radius = FloatProperty(
        name="Search radius",
        min=0.0,
        default=1.0)

    # YafaRay's antialiasing/noise properties
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
        items=[
            ('box', "Box", "AA filter type"),
            ('mitchell', "Mitchell", "AA filter type"),
            ('gauss', "Gauss", "AA filter type"),
            ('lanczos', "Lanczos", "AA filter type")
        ],
        default="gauss")

    Scene.use_instances = BoolProperty(
        name="Use Instances for Rendering",
        description="Use Instances during rendering for instanced objects."
                    "If disabled it generates internally full copies of the "
                    "base object in memory instead of instances.",
        default=True)

    Scene.active_texture = PointerProperty(name="YafaRay Generic Texture Editor", type=bpy.types.Texture)

    bpy.utils.register_class(YafaRay4Properties)
    bpy.types.Scene.yafaray4 = PointerProperty(type=YafaRay4Properties)

    bpy.utils.register_class(YafaRay4LayersProperties)
    YafaRay4Properties.passes = PointerProperty(type=YafaRay4LayersProperties)

    bpy.utils.register_class(YafaRay4NoiseControlProperties)
    YafaRay4Properties.noise_control = PointerProperty(type=YafaRay4NoiseControlProperties)

    bpy.utils.register_class(YafaRay4LoggingProperties)
    YafaRay4Properties.logging = PointerProperty(type=YafaRay4LoggingProperties)

    bpy.utils.register_class(YafaRay4MaterialPreviewControlProperties)
    YafaRay4Properties.preview = PointerProperty(type=YafaRay4MaterialPreviewControlProperties)

    bpy.utils.register_class(YafaRay4MigrationProperties)
    YafaRay4Properties.migration = PointerProperty(type=YafaRay4MigrationProperties)


def unregister():
    del YafaRay4Properties.migration
    bpy.utils.unregister_class(YafaRay4MigrationProperties)
    del YafaRay4Properties.preview
    bpy.utils.unregister_class(YafaRay4MaterialPreviewControlProperties)
    del YafaRay4Properties.logging
    bpy.utils.unregister_class(YafaRay4LoggingProperties)
    del YafaRay4Properties.noise_control
    bpy.utils.unregister_class(YafaRay4NoiseControlProperties)
    del YafaRay4Properties.passes
    bpy.utils.unregister_class(YafaRay4LayersProperties)
    del bpy.types.Scene.yafaray4
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
    del Scene.adv_scene_mesh_tesselation

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
    del Scene.intg_motion_blur_time_forced
    del Scene.intg_motion_blur_time_forced_value
    del Scene.intg_photonmap_enable_caustics
    del Scene.intg_photonmap_enable_diffuse
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
    del Scene.use_instances
    del Scene.active_texture
