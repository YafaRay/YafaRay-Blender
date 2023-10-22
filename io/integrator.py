# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
import libyafaray4_bindings


class Integrator:
    def __init__(self, logger):
        self.yaf_integrator = None
        self.logger = logger

    def export_integrator(self, scene, is_preview):
        param_map = libyafaray4_bindings.ParamMap()

        param_map.set_bool("bg_transp", scene.bg_transp)
        if scene.bg_transp:
            param_map.set_bool("bg_transp_refract", scene.bg_transp_refract)
        else:
            param_map.set_bool("bg_transp_refract", False)

        param_map.set_int("raydepth", scene.gs_ray_depth)
        if scene.name == "preview" and bpy.data.scenes[0].yafaray.preview.enable:
            param_map.set_int("raydepth", bpy.data.scenes[0].yafaray.preview.preview_ray_depth)
        param_map.set_int("shadowDepth", scene.gs_shadow_depth)
        param_map.set_bool("transpShad", scene.gs_transp_shad)

        light_type = scene.intg_light_method
        self.logger.print_info("Exporting Integrator: {0}".format(light_type))

        param_map.set_bool("do_AO", scene.intg_use_AO)
        param_map.set_int("AO_samples", scene.intg_AO_samples)
        param_map.set_float("AO_distance", scene.intg_AO_distance)
        c = scene.intg_AO_color
        param_map.set_color("AO_color", c[0], c[1], c[2])
        param_map.set_bool("time_forced", scene.intg_motion_blur_time_forced)
        param_map.set_float("time_forced_value", scene.intg_motion_blur_time_forced_value)

        if light_type == "Direct Lighting":
            param_map.set_string("type", "directlighting")

            param_map.set_bool("caustics", scene.intg_use_caustics)

            if scene.intg_use_caustics:
                param_map.set_int("caustic_photons", scene.intg_photons)
                param_map.set_int("caustic_mix", scene.intg_caustic_mix)
                param_map.set_int("caustic_depth", scene.intg_caustic_depth)
                param_map.set_float("caustic_radius", scene.intg_caustic_radius)

        elif light_type == "Photon Mapping":
            param_map.set_string("type", "photonmapping")
            param_map.set_bool("caustics", scene.intg_photonmap_enable_caustics)
            param_map.set_bool("diffuse", scene.intg_photonmap_enable_diffuse)
            param_map.set_int("bounces", scene.intg_bounces)
            param_map.set_int("diffuse_photons", scene.intg_photons)
            param_map.set_int("caustic_photons", scene.intg_cPhotons)
            param_map.set_float("diffuse_radius", scene.intg_diffuse_radius)
            param_map.set_float("caustic_radius", scene.intg_caustic_radius)
            param_map.set_int("diffuse_search", scene.intg_search)
            param_map.set_int("caustic_mix", scene.intg_caustic_mix)
            #
            param_map.set_bool("finalGather", scene.intg_final_gather)
            #
            if scene.intg_final_gather:
                param_map.set_int("fg_bounces", scene.intg_fg_bounces)
                param_map.set_int("fg_samples", scene.intg_fg_samples)
                param_map.set_bool("show_map", scene.intg_show_map)

        elif light_type == "Pathtracing":
            param_map.set_string("type", "pathtracing")
            param_map.set_int("path_samples", scene.intg_path_samples)
            param_map.set_int("bounces", scene.intg_bounces)
            param_map.set_int("russian_roulette_min_bounces", scene.intg_russian_roulette_min_bounces)
            param_map.set_bool("no_recursive", scene.intg_no_recursion)

            # -- test for simplify code
            caustic_type_str = scene.intg_caustic_method
            switch_caustic_type = {
                'None': 'none',
                'Path': 'path',
                'Photon': 'photon',
                'Path+Photon': 'both',
            }

            caustic_type = switch_caustic_type.get(caustic_type_str)
            param_map.set_string("caustic_type", caustic_type)

            if caustic_type not in {'none', 'path'}:
                param_map.set_int("caustic_photons", scene.intg_photons)
                param_map.set_int("caustic_mix", scene.intg_caustic_mix)
                param_map.set_int("caustic_depth", scene.intg_caustic_depth)
                param_map.set_float("caustic_radius", scene.intg_caustic_radius)

        elif light_type == "Bidirectional":
            param_map.set_string("type", "bidirectional")

        elif light_type == "Debug":
            param_map.set_string("type", "DebugIntegrator")
            param_map.set_string("debugType", scene.intg_debug_type)
            param_map.set_bool("showPN", scene.intg_show_perturbed_normals)

        elif light_type == "SPPM":
            param_map.set_string("type", "SPPM")
            param_map.set_int("photons", scene.intg_photons)
            param_map.set_float("photonRadius", scene.intg_diffuse_radius)
            param_map.set_int("searchNum", scene.intg_search)
            param_map.set_float("times", scene.intg_times)
            param_map.set_int("bounces", scene.intg_bounces)
            param_map.set_int("passNums", scene.intg_pass_num)
            param_map.set_bool("pmIRE", scene.intg_pm_ire)

        if is_preview:
            integrator_name = "Blender Main SurfaceIntegrator"
        else:
            integrator_name = "Blender Preview SurfaceIntegrator"

        self.yaf_integrator = libyafaray4_bindings.SurfaceIntegrator(self.logger, integrator_name, param_map)
        return True

    def export_volume_integrator(self, scene_blender, scene_yafaray):
        param_map = libyafaray4_bindings.ParamMap()
        world = scene_blender.world
        if world:
            vint_type = world.v_int_type
            self.logger.print_info("Exporting Volume Integrator: {0}".format(vint_type))

            if vint_type == 'Single Scatter':
                param_map.set_string("type", "SingleScatterIntegrator")
                param_map.set_float("stepSize", world.v_int_step_size)
                param_map.set_bool("adaptive", world.v_int_adaptive)
                param_map.set_bool("optimize", world.v_int_optimize)

            elif vint_type == 'Sky':
                param_map.set_string("type", "SkyIntegrator")
                param_map.set_float("turbidity", world.v_int_dsturbidity)
                param_map.set_float("stepSize", world.v_int_step_size)
                param_map.set_float("alpha", world.v_int_alpha)
                param_map.set_float("sigma_t", world.v_int_scale)

            else:
                param_map.set_string("type", "none")
        else:
            param_map.set_string("type", "none")

        self.yaf_integrator.defineVolumeIntegrator(scene_yafaray, param_map)
        return True
