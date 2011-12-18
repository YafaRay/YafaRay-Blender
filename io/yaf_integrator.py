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


class yafIntegrator:
    def __init__(self, interface):
        self.yi = interface

    def exportIntegrator(self, scene):
        yi = self.yi

        yi.paramsClearAll()

        yi.paramsSetInt("raydepth", scene.gs_ray_depth)
        yi.paramsSetInt("shadowDepth", scene.gs_shadow_depth)
        yi.paramsSetBool("transpShad", scene.gs_transp_shad)

        light_type = scene.intg_light_method
        yi.printInfo("Exporting Integrator: {0}".format(light_type))

        if light_type == "Direct Lighting":
            yi.paramsSetString("type", "directlighting")

            yi.paramsSetBool("caustics", scene.intg_use_caustics)

            if scene.intg_use_caustics:
                yi.paramsSetInt("photons", scene.intg_photons)
                yi.paramsSetInt("caustic_mix", scene.intg_caustic_mix)
                yi.paramsSetInt("caustic_depth", scene.intg_caustic_depth)
                yi.paramsSetFloat("caustic_radius", scene.intg_caustic_radius)

            if scene.intg_use_AO:
                yi.paramsSetBool("do_AO", scene.intg_use_AO)
                yi.paramsSetInt("AO_samples", scene.intg_AO_samples)
                yi.paramsSetFloat("AO_distance", scene.intg_AO_distance)

                c = scene.intg_AO_color
                yi.paramsSetColor("AO_color", c[0], c[1], c[2])

        elif light_type == "Photon Mapping":
            yi.paramsSetString("type", "photonmapping")
            yi.paramsSetInt("fg_samples", scene.intg_fg_samples)
            yi.paramsSetInt("photons", scene.intg_photons)
            yi.paramsSetInt("cPhotons", scene.intg_cPhotons)
            yi.paramsSetFloat("diffuseRadius", scene.intg_diffuse_radius)
            yi.paramsSetFloat("causticRadius", scene.intg_caustic_radius)
            yi.paramsSetInt("search", scene.intg_search)
            yi.paramsSetBool("show_map", scene.intg_show_map)
            yi.paramsSetInt("fg_bounces", scene.intg_fg_bounces)
            yi.paramsSetInt("caustic_mix", scene.intg_caustic_mix)
            yi.paramsSetBool("finalGather", scene.intg_final_gather)
            yi.paramsSetInt("bounces", scene.intg_bounces)

        elif light_type == "Pathtracing":
            yi.paramsSetString("type", "pathtracing")
            yi.paramsSetInt("path_samples", scene.intg_path_samples)
            yi.paramsSetInt("bounces", scene.intg_bounces)
            yi.paramsSetBool("no_recursive", scene.intg_no_recursion)

            #-- test for simplify code
            causticTypeStr = scene.intg_caustic_method
            switchCausticType = {
                'None': 'none',
                'Path': 'path',
                'Photon': 'photon',
                'Path+Photon': 'both',
            }

            causticType = switchCausticType.get(causticTypeStr)
            yi.paramsSetString("caustic_type", causticType)

            if causticType != 'none' and causticType != 'path':
                yi.paramsSetInt("photons", scene.intg_photons)
                yi.paramsSetInt("caustic_mix", scene.intg_caustic_mix)
                yi.paramsSetInt("caustic_depth", scene.intg_caustic_depth)
                yi.paramsSetFloat("caustic_radius", scene.intg_caustic_radius)

        elif light_type == "Bidirectional":
            yi.paramsSetString("type", "bidirectional")

        elif light_type == "Debug":
            yi.paramsSetString("type", "DebugIntegrator")

            debugTypeStr = scene.intg_debug_type
            switchDebugType = {
                'N': 1,
                'dPdU': 2,
                'dPdV': 3,
                'NU': 4,
                'NV': 5,
                'dSdU': 6,
                'dSdV': 7,
            }

            debugType = switchDebugType.get(debugTypeStr)
            yi.paramsSetInt("debugType", debugType)
            yi.paramsSetBool("showPN", scene.intg_show_perturbed_normals)

        elif light_type == "SPPM":
            yi.paramsSetString("type", "SPPM")
            yi.paramsSetInt("photons", scene.intg_photons)
            yi.paramsSetFloat("diffuseRadius", scene.intg_diffuse_radius)
            yi.paramsSetInt("search", scene.intg_search)
            yi.paramsSetFloat("times", scene.intg_times)
            yi.paramsSetInt("bounces", scene.intg_bounces)
            yi.paramsSetInt("passNums", scene.intg_pass_num)
            yi.paramsSetBool("pmIRE", scene.intg_pm_ire)

        yi.createIntegrator("default")
        return True

    def exportVolumeIntegrator(self, scene):
        yi = self.yi
        yi.paramsClearAll()

        world = scene.world

        if world:
            vint_type = world.v_int_type
            yi.printInfo("Exporting Volume Integrator: {0}".format(vint_type))

            if vint_type == 'Single Scatter':
                yi.paramsSetString("type", "SingleScatterIntegrator")
                yi.paramsSetFloat("stepSize", world.v_int_step_size)
                yi.paramsSetBool("adaptive", world.v_int_adaptive)
                yi.paramsSetBool("optimize", world.v_int_optimize)

            elif vint_type == 'Sky':
                yi.paramsSetString("type", "SkyIntegrator")
                yi.paramsSetFloat("turbidity", world.v_int_dsturbidity)
                yi.paramsSetFloat("stepSize", world.v_int_step_size)
                yi.paramsSetFloat("alpha", world.v_int_alpha)
                yi.paramsSetFloat("sigma_t", world.v_int_scale)

            else:
                yi.paramsSetString("type", "none")
        else:
            yi.paramsSetString("type", "none")

        yi.createIntegrator("volintegr")
        return True
