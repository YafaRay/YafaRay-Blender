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

class Integrator:
    def __init__(self, interface):
        self.yi = interface

    def exportIntegrator(self, scene, renderer, logger):
        self.logger = logger
        self.renderer = renderer

        yaf_param_map = libyafaray4_bindings.ParamMap()

        yaf_param_map.setBool("bg_transp", scene.bg_transp)
        if scene.bg_transp:
            yaf_param_map.setBool("bg_transp_refract", scene.bg_transp_refract)
        else:
            yaf_param_map.setBool("bg_transp_refract", False)

        yaf_param_map.setInt("raydepth", scene.gs_ray_depth)
        if scene.name == "preview" and bpy.data.scenes[0].yafaray.preview.enable:
            yaf_param_map.setInt("raydepth", bpy.data.scenes[0].yafaray.preview.previewRayDepth)
        yaf_param_map.setInt("shadowDepth", scene.gs_shadow_depth)
        yaf_param_map.setBool("transpShad", scene.gs_transp_shad)

        light_type = scene.intg_light_method
        self.logger.printInfo("Exporting Integrator: {0}".format(light_type))

        yaf_param_map.setBool("do_AO", scene.intg_use_AO)
        yaf_param_map.setInt("AO_samples", scene.intg_AO_samples)
        yaf_param_map.setFloat("AO_distance", scene.intg_AO_distance)
        c = scene.intg_AO_color
        yaf_param_map.setColor("AO_color", c[0], c[1], c[2])
        yaf_param_map.setBool("time_forced", scene.intg_motion_blur_time_forced)
        yaf_param_map.setFloat("time_forced_value", scene.intg_motion_blur_time_forced_value)

        if light_type == "Direct Lighting":
            yaf_param_map.setString("type", "directlighting")

            yaf_param_map.setBool("caustics", scene.intg_use_caustics)
            yaf_param_map.setString("photon_maps_processing", scene.intg_photon_maps_processing)

            if scene.intg_use_caustics:
                yaf_param_map.setInt("caustic_photons", scene.intg_photons)
                yaf_param_map.setInt("caustic_mix", scene.intg_caustic_mix)
                yaf_param_map.setInt("caustic_depth", scene.intg_caustic_depth)
                yaf_param_map.setFloat("caustic_radius", scene.intg_caustic_radius)

        elif light_type == "Photon Mapping":
            yaf_param_map.setString("type", "photonmapping")
            yaf_param_map.setBool("caustics", scene.intg_photonmap_enable_caustics)
            yaf_param_map.setBool("diffuse", scene.intg_photonmap_enable_diffuse)
            yaf_param_map.setString("photon_maps_processing", scene.intg_photon_maps_processing)
            
            yaf_param_map.setInt("bounces", scene.intg_bounces)
            yaf_param_map.setInt("diffuse_photons", scene.intg_photons)
            yaf_param_map.setInt("caustic_photons", scene.intg_cPhotons)
            yaf_param_map.setFloat("diffuse_radius", scene.intg_diffuse_radius)
            yaf_param_map.setFloat("caustic_radius", scene.intg_caustic_radius)
            yaf_param_map.setInt("diffuse_search", scene.intg_search)
            yaf_param_map.setInt("caustic_mix", scene.intg_caustic_mix)
            #
            yaf_param_map.setBool("finalGather", scene.intg_final_gather)            
            #
            if scene.intg_final_gather:
                yaf_param_map.setInt("fg_bounces", scene.intg_fg_bounces)
                yaf_param_map.setInt("fg_samples", scene.intg_fg_samples)
                yaf_param_map.setBool("show_map", scene.intg_show_map)
                

        elif light_type == "Pathtracing":
            yaf_param_map.setString("type", "pathtracing")
            yaf_param_map.setInt("path_samples", scene.intg_path_samples)
            yaf_param_map.setInt("bounces", scene.intg_bounces)
            yaf_param_map.setInt("russian_roulette_min_bounces", scene.intg_russian_roulette_min_bounces)
            yaf_param_map.setBool("no_recursive", scene.intg_no_recursion)
            yaf_param_map.setString("photon_maps_processing", scene.intg_photon_maps_processing)

            #-- test for simplify code
            causticTypeStr = scene.intg_caustic_method
            switchCausticType = {
                'None': 'none',
                'Path': 'path',
                'Photon': 'photon',
                'Path+Photon': 'both',
            }

            causticType = switchCausticType.get(causticTypeStr)
            yaf_param_map.setString("caustic_type", causticType)

            if causticType not in {'none', 'path'}:
                yaf_param_map.setInt("caustic_photons", scene.intg_photons)
                yaf_param_map.setInt("caustic_mix", scene.intg_caustic_mix)
                yaf_param_map.setInt("caustic_depth", scene.intg_caustic_depth)
                yaf_param_map.setFloat("caustic_radius", scene.intg_caustic_radius)

        elif light_type == "Bidirectional":
            yaf_param_map.setString("type", "bidirectional")

        elif light_type == "Debug":
            yaf_param_map.setString("type", "DebugIntegrator")
            yaf_param_map.setString("debugType", scene.intg_debug_type)
            yaf_param_map.setBool("showPN", scene.intg_show_perturbed_normals)

        elif light_type == "SPPM":
            yaf_param_map.setString("type", "SPPM")
            yaf_param_map.setInt("photons", scene.intg_photons)
            yaf_param_map.setFloat("photonRadius", scene.intg_diffuse_radius)
            yaf_param_map.setInt("searchNum", scene.intg_search)
            yaf_param_map.setFloat("times", scene.intg_times)
            yaf_param_map.setInt("bounces", scene.intg_bounces)
            yaf_param_map.setInt("passNums", scene.intg_pass_num)
            yaf_param_map.setBool("pmIRE", scene.intg_pm_ire)

        self.renderer.defineSurfaceIntegrator()
        return True

    def exportVolumeIntegrator(self, scene):
        
        yaf_param_map = libyafaray4_bindings.ParamMap()

        world = scene.world

        if world:
            vint_type = world.v_int_type
            self.logger.printInfo("Exporting Volume Integrator: {0}".format(vint_type))

            if vint_type == 'Single Scatter':
                yaf_param_map.setString("type", "SingleScatterIntegrator")
                yaf_param_map.setFloat("stepSize", world.v_int_step_size)
                yaf_param_map.setBool("adaptive", world.v_int_adaptive)
                yaf_param_map.setBool("optimize", world.v_int_optimize)

            elif vint_type == 'Sky':
                yaf_param_map.setString("type", "SkyIntegrator")
                yaf_param_map.setFloat("turbidity", world.v_int_dsturbidity)
                yaf_param_map.setFloat("stepSize", world.v_int_step_size)
                yaf_param_map.setFloat("alpha", world.v_int_alpha)
                yaf_param_map.setFloat("sigma_t", world.v_int_scale)

            else:
                yaf_param_map.setString("type", "none")
        else:
            yaf_param_map.setString("type", "none")

        yi.defineVolumeIntegrator()
        return True
