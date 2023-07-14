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
import libyafaray4_bindings

class Integrator:
    def __init__(self, yaf_logger):
        self.yaf_integrator = None
        self.yaf_logger = yaf_logger

    def exportIntegrator(self, scene, is_preview):

        yaf_param_map = libyafaray4_bindings.ParamMap()

        yaf_param_map.set_bool("bg_transp", scene.bg_transp)
        if scene.bg_transp:
            yaf_param_map.set_bool("bg_transp_refract", scene.bg_transp_refract)
        else:
            yaf_param_map.set_bool("bg_transp_refract", False)

        yaf_param_map.set_int("raydepth", scene.gs_ray_depth)
        if scene.name == "preview" and bpy.data.scenes[0].yafaray.is_preview.enable:
            yaf_param_map.set_int("raydepth", bpy.data.scenes[0].yafaray.is_preview.previewRayDepth)
        yaf_param_map.set_int("shadowDepth", scene.gs_shadow_depth)
        yaf_param_map.set_bool("transpShad", scene.gs_transp_shad)

        light_type = scene.intg_light_method
        self.yaf_logger.printInfo("Exporting Integrator: {0}".format(light_type))

        yaf_param_map.set_bool("do_AO", scene.intg_use_AO)
        yaf_param_map.set_int("AO_samples", scene.intg_AO_samples)
        yaf_param_map.set_float("AO_distance", scene.intg_AO_distance)
        c = scene.intg_AO_color
        yaf_param_map.set_color("AO_color", c[0], c[1], c[2])
        yaf_param_map.set_bool("time_forced", scene.intg_motion_blur_time_forced)
        yaf_param_map.set_float("time_forced_value", scene.intg_motion_blur_time_forced_value)

        if light_type == "Direct Lighting":
            yaf_param_map.set_string("type", "directlighting")

            yaf_param_map.set_bool("caustics", scene.intg_use_caustics)

            if scene.intg_use_caustics:
                yaf_param_map.set_int("caustic_photons", scene.intg_photons)
                yaf_param_map.set_int("caustic_mix", scene.intg_caustic_mix)
                yaf_param_map.set_int("caustic_depth", scene.intg_caustic_depth)
                yaf_param_map.set_float("caustic_radius", scene.intg_caustic_radius)

        elif light_type == "Photon Mapping":
            yaf_param_map.set_string("type", "photonmapping")
            yaf_param_map.set_bool("caustics", scene.intg_photonmap_enable_caustics)
            yaf_param_map.set_bool("diffuse", scene.intg_photonmap_enable_diffuse)
            yaf_param_map.set_int("bounces", scene.intg_bounces)
            yaf_param_map.set_int("diffuse_photons", scene.intg_photons)
            yaf_param_map.set_int("caustic_photons", scene.intg_cPhotons)
            yaf_param_map.set_float("diffuse_radius", scene.intg_diffuse_radius)
            yaf_param_map.set_float("caustic_radius", scene.intg_caustic_radius)
            yaf_param_map.set_int("diffuse_search", scene.intg_search)
            yaf_param_map.set_int("caustic_mix", scene.intg_caustic_mix)
            #
            yaf_param_map.set_bool("finalGather", scene.intg_final_gather)            
            #
            if scene.intg_final_gather:
                yaf_param_map.set_int("fg_bounces", scene.intg_fg_bounces)
                yaf_param_map.set_int("fg_samples", scene.intg_fg_samples)
                yaf_param_map.set_bool("show_map", scene.intg_show_map)
                

        elif light_type == "Pathtracing":
            yaf_param_map.set_string("type", "pathtracing")
            yaf_param_map.set_int("path_samples", scene.intg_path_samples)
            yaf_param_map.set_int("bounces", scene.intg_bounces)
            yaf_param_map.set_int("russian_roulette_min_bounces", scene.intg_russian_roulette_min_bounces)
            yaf_param_map.set_bool("no_recursive", scene.intg_no_recursion)

            #-- test for simplify code
            causticTypeStr = scene.intg_caustic_method
            switchCausticType = {
                'None': 'none',
                'Path': 'path',
                'Photon': 'photon',
                'Path+Photon': 'both',
            }

            causticType = switchCausticType.get(causticTypeStr)
            yaf_param_map.set_string("caustic_type", causticType)

            if causticType not in {'none', 'path'}:
                yaf_param_map.set_int("caustic_photons", scene.intg_photons)
                yaf_param_map.set_int("caustic_mix", scene.intg_caustic_mix)
                yaf_param_map.set_int("caustic_depth", scene.intg_caustic_depth)
                yaf_param_map.set_float("caustic_radius", scene.intg_caustic_radius)

        elif light_type == "Bidirectional":
            yaf_param_map.set_string("type", "bidirectional")

        elif light_type == "Debug":
            yaf_param_map.set_string("type", "DebugIntegrator")
            yaf_param_map.set_string("debugType", scene.intg_debug_type)
            yaf_param_map.set_bool("showPN", scene.intg_show_perturbed_normals)

        elif light_type == "SPPM":
            yaf_param_map.set_string("type", "SPPM")
            yaf_param_map.set_int("photons", scene.intg_photons)
            yaf_param_map.set_float("photonRadius", scene.intg_diffuse_radius)
            yaf_param_map.set_int("searchNum", scene.intg_search)
            yaf_param_map.set_float("times", scene.intg_times)
            yaf_param_map.set_int("bounces", scene.intg_bounces)
            yaf_param_map.set_int("passNums", scene.intg_pass_num)
            yaf_param_map.set_bool("pmIRE", scene.intg_pm_ire)

        if is_preview:
            integrator_name = "Blender Main SurfaceIntegrator"
        else:
            integrator_name = "Blender Preview SurfaceIntegrator"

        self.yaf_integrator = libyafaray4_bindings.SurfaceIntegrator(self.yaf_logger, "Blender Main SurfaceIntegrator", yaf_param_map)
        return True

    def exportVolumeIntegrator(self, bl_scene, yaf_scene):
        
        yaf_param_map = libyafaray4_bindings.ParamMap()

        bl_world = bl_scene.world

        if bl_world:
            vint_type = bl_world.v_int_type
            self.yaf_logger.printInfo("Exporting Volume Integrator: {0}".format(vint_type))

            if vint_type == 'Single Scatter':
                yaf_param_map.set_string("type", "SingleScatterIntegrator")
                yaf_param_map.set_float("stepSize", bl_world.v_int_step_size)
                yaf_param_map.set_bool("adaptive", bl_world.v_int_adaptive)
                yaf_param_map.set_bool("optimize", bl_world.v_int_optimize)

            elif vint_type == 'Sky':
                yaf_param_map.set_string("type", "SkyIntegrator")
                yaf_param_map.set_float("turbidity", bl_world.v_int_dsturbidity)
                yaf_param_map.set_float("stepSize", bl_world.v_int_step_size)
                yaf_param_map.set_float("alpha", bl_world.v_int_alpha)
                yaf_param_map.set_float("sigma_t", bl_world.v_int_scale)

            else:
                yaf_param_map.set_string("type", "none")
        else:
            yaf_param_map.set_string("type", "none")

        self.yaf_integrator.defineVolumeIntegrator(yaf_scene, yaf_param_map)
        return True
