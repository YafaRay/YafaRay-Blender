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

class yafIntegrator:
    def __init__(self, interface):
        self.yi = interface

    def exportIntegrator(self, scene, renderer, logger):
        self.logger = logger
        self.renderer = renderer

        param_map = libyafaray4_bindings.ParamMap()

        param_map.setBool("bg_transp", scene.bg_transp)
        if scene.bg_transp:
            param_map.setBool("bg_transp_refract", scene.bg_transp_refract)
        else:
            param_map.setBool("bg_transp_refract", False)

        param_map.setInt("raydepth", scene.gs_ray_depth)
        if scene.name == "preview" and bpy.data.scenes[0].yafaray.preview.enable:
            param_map.setInt("raydepth", bpy.data.scenes[0].yafaray.preview.previewRayDepth)
        param_map.setInt("shadowDepth", scene.gs_shadow_depth)
        param_map.setBool("transpShad", scene.gs_transp_shad)

        light_type = scene.intg_light_method
        self.logger.printInfo("Exporting Integrator: {0}".format(light_type))

        param_map.setBool("do_AO", scene.intg_use_AO)
        param_map.setInt("AO_samples", scene.intg_AO_samples)
        param_map.setFloat("AO_distance", scene.intg_AO_distance)
        c = scene.intg_AO_color
        param_map.setColor("AO_color", c[0], c[1], c[2])
        param_map.setBool("time_forced", scene.intg_motion_blur_time_forced)
        param_map.setFloat("time_forced_value", scene.intg_motion_blur_time_forced_value)

        if light_type == "Direct Lighting":
            param_map.setString("type", "directlighting")

            param_map.setBool("caustics", scene.intg_use_caustics)
            param_map.setString("photon_maps_processing", scene.intg_photon_maps_processing)

            if scene.intg_use_caustics:
                param_map.setInt("caustic_photons", scene.intg_photons)
                param_map.setInt("caustic_mix", scene.intg_caustic_mix)
                param_map.setInt("caustic_depth", scene.intg_caustic_depth)
                param_map.setFloat("caustic_radius", scene.intg_caustic_radius)

        elif light_type == "Photon Mapping":
            param_map.setString("type", "photonmapping")
            param_map.setBool("caustics", scene.intg_photonmap_enable_caustics)
            param_map.setBool("diffuse", scene.intg_photonmap_enable_diffuse)
            param_map.setString("photon_maps_processing", scene.intg_photon_maps_processing)
            
            param_map.setInt("bounces", scene.intg_bounces)
            param_map.setInt("diffuse_photons", scene.intg_photons)
            param_map.setInt("caustic_photons", scene.intg_cPhotons)
            param_map.setFloat("diffuse_radius", scene.intg_diffuse_radius)
            param_map.setFloat("caustic_radius", scene.intg_caustic_radius)
            param_map.setInt("diffuse_search", scene.intg_search)
            param_map.setInt("caustic_mix", scene.intg_caustic_mix)
            #
            param_map.setBool("finalGather", scene.intg_final_gather)            
            #
            if scene.intg_final_gather:
                param_map.setInt("fg_bounces", scene.intg_fg_bounces)
                param_map.setInt("fg_samples", scene.intg_fg_samples)
                param_map.setBool("show_map", scene.intg_show_map)
                

        elif light_type == "Pathtracing":
            param_map.setString("type", "pathtracing")
            param_map.setInt("path_samples", scene.intg_path_samples)
            param_map.setInt("bounces", scene.intg_bounces)
            param_map.setInt("russian_roulette_min_bounces", scene.intg_russian_roulette_min_bounces)
            param_map.setBool("no_recursive", scene.intg_no_recursion)
            param_map.setString("photon_maps_processing", scene.intg_photon_maps_processing)

            #-- test for simplify code
            causticTypeStr = scene.intg_caustic_method
            switchCausticType = {
                'None': 'none',
                'Path': 'path',
                'Photon': 'photon',
                'Path+Photon': 'both',
            }

            causticType = switchCausticType.get(causticTypeStr)
            param_map.setString("caustic_type", causticType)

            if causticType not in {'none', 'path'}:
                param_map.setInt("caustic_photons", scene.intg_photons)
                param_map.setInt("caustic_mix", scene.intg_caustic_mix)
                param_map.setInt("caustic_depth", scene.intg_caustic_depth)
                param_map.setFloat("caustic_radius", scene.intg_caustic_radius)

        elif light_type == "Bidirectional":
            param_map.setString("type", "bidirectional")

        elif light_type == "Debug":
            param_map.setString("type", "DebugIntegrator")
            param_map.setString("debugType", scene.intg_debug_type)
            param_map.setBool("showPN", scene.intg_show_perturbed_normals)

        elif light_type == "SPPM":
            param_map.setString("type", "SPPM")
            param_map.setInt("photons", scene.intg_photons)
            param_map.setFloat("photonRadius", scene.intg_diffuse_radius)
            param_map.setInt("searchNum", scene.intg_search)
            param_map.setFloat("times", scene.intg_times)
            param_map.setInt("bounces", scene.intg_bounces)
            param_map.setInt("passNums", scene.intg_pass_num)
            param_map.setBool("pmIRE", scene.intg_pm_ire)

        self.renderer.defineSurfaceIntegrator()
        return True

    def exportVolumeIntegrator(self, scene):
        
        param_map = libyafaray4_bindings.ParamMap()

        world = scene.world

        if world:
            vint_type = world.v_int_type
            self.logger.printInfo("Exporting Volume Integrator: {0}".format(vint_type))

            if vint_type == 'Single Scatter':
                param_map.setString("type", "SingleScatterIntegrator")
                param_map.setFloat("stepSize", world.v_int_step_size)
                param_map.setBool("adaptive", world.v_int_adaptive)
                param_map.setBool("optimize", world.v_int_optimize)

            elif vint_type == 'Sky':
                param_map.setString("type", "SkyIntegrator")
                param_map.setFloat("turbidity", world.v_int_dsturbidity)
                param_map.setFloat("stepSize", world.v_int_step_size)
                param_map.setFloat("alpha", world.v_int_alpha)
                param_map.setFloat("sigma_t", world.v_int_scale)

            else:
                param_map.setString("type", "none")
        else:
            param_map.setString("type", "none")

        yi.defineVolumeIntegrator()
        return True
