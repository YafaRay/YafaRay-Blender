# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
import libyafaray4_bindings


def export_integrator(integrator_name, scene_blender, logger):
    param_map = libyafaray4_bindings.ParamMap()

    param_map.set_bool("bg_transp", scene_blender.bg_transp)
    if scene_blender.bg_transp:
        param_map.set_bool("bg_transp_refract", scene_blender.bg_transp_refract)
    else:
        param_map.set_bool("bg_transp_refract", False)

    param_map.set_int("raydepth", scene_blender.gs_ray_depth)
    if scene_blender.name == "preview" and bpy.data.scenes[0].yafaray.preview.enable:
        param_map.set_int("raydepth", bpy.data.scenes[0].yafaray.preview.preview_ray_depth)
    param_map.set_int("shadowDepth", scene_blender.gs_shadow_depth)
    param_map.set_bool("transpShad", scene_blender.gs_transp_shad)

    light_type = scene_blender.intg_light_method
    logger.print_info("Exporting Integrator: {0}".format(light_type))

    param_map.set_bool("do_AO", scene_blender.intg_use_AO)
    param_map.set_int("AO_samples", scene_blender.intg_AO_samples)
    param_map.set_float("AO_distance", scene_blender.intg_AO_distance)
    c = scene_blender.intg_AO_color
    param_map.set_color("AO_color", c[0], c[1], c[2])
    param_map.set_bool("time_forced", scene_blender.intg_motion_blur_time_forced)
    param_map.set_float("time_forced_value", scene_blender.intg_motion_blur_time_forced_value)

    if light_type == "Direct Lighting":
        param_map.set_string("type", "directlighting")

        param_map.set_bool("caustics", scene_blender.intg_use_caustics)

        if scene_blender.intg_use_caustics:
            param_map.set_int("caustic_photons", scene_blender.intg_photons)
            param_map.set_int("caustic_mix", scene_blender.intg_caustic_mix)
            param_map.set_int("caustic_depth", scene_blender.intg_caustic_depth)
            param_map.set_float("caustic_radius", scene_blender.intg_caustic_radius)

    elif light_type == "Photon Mapping":
        param_map.set_string("type", "photonmapping")
        param_map.set_bool("caustics", scene_blender.intg_photonmap_enable_caustics)
        param_map.set_bool("diffuse", scene_blender.intg_photonmap_enable_diffuse)
        param_map.set_int("bounces", scene_blender.intg_bounces)
        param_map.set_int("diffuse_photons", scene_blender.intg_photons)
        param_map.set_int("caustic_photons", scene_blender.intg_cPhotons)
        param_map.set_float("diffuse_radius", scene_blender.intg_diffuse_radius)
        param_map.set_float("caustic_radius", scene_blender.intg_caustic_radius)
        param_map.set_int("diffuse_search", scene_blender.intg_search)
        param_map.set_int("caustic_mix", scene_blender.intg_caustic_mix)
        #
        param_map.set_bool("finalGather", scene_blender.intg_final_gather)
        #
        if scene_blender.intg_final_gather:
            param_map.set_int("fg_bounces", scene_blender.intg_fg_bounces)
            param_map.set_int("fg_samples", scene_blender.intg_fg_samples)
            param_map.set_bool("show_map", scene_blender.intg_show_map)

    elif light_type == "Pathtracing":
        param_map.set_string("type", "pathtracing")
        param_map.set_int("path_samples", scene_blender.intg_path_samples)
        param_map.set_int("bounces", scene_blender.intg_bounces)
        param_map.set_int("russian_roulette_min_bounces", scene_blender.intg_russian_roulette_min_bounces)
        param_map.set_bool("no_recursive", scene_blender.intg_no_recursion)

        # -- test for simplify code
        caustic_type_str = scene_blender.intg_caustic_method
        switch_caustic_type = {
            'None': 'none',
            'Path': 'path',
            'Photon': 'photon',
            'Path+Photon': 'both',
        }

        caustic_type = switch_caustic_type.get(caustic_type_str)
        param_map.set_string("caustic_type", caustic_type)

        if caustic_type not in {'none', 'path'}:
            param_map.set_int("caustic_photons", scene_blender.intg_photons)
            param_map.set_int("caustic_mix", scene_blender.intg_caustic_mix)
            param_map.set_int("caustic_depth", scene_blender.intg_caustic_depth)
            param_map.set_float("caustic_radius", scene_blender.intg_caustic_radius)

    elif light_type == "Bidirectional":
        param_map.set_string("type", "bidirectional")

    elif light_type == "Debug":
        param_map.set_string("type", "DebugIntegrator")
        param_map.set_string("debugType", scene_blender.intg_debug_type)
        param_map.set_bool("showPN", scene_blender.intg_show_perturbed_normals)

    elif light_type == "SPPM":
        param_map.set_string("type", "SPPM")
        param_map.set_int("photons", scene_blender.intg_photons)
        param_map.set_float("photonRadius", scene_blender.intg_diffuse_radius)
        param_map.set_int("searchNum", scene_blender.intg_search)
        param_map.set_float("times", scene_blender.intg_times)
        param_map.set_int("bounces", scene_blender.intg_bounces)
        param_map.set_int("passNums", scene_blender.intg_pass_num)
        param_map.set_bool("pmIRE", scene_blender.intg_pm_ire)

    return libyafaray4_bindings.SurfaceIntegrator(logger, integrator_name, param_map)
