# SPDX-License-Identifier: GPL-2.0-or-later

import bpy


def convert_objects(objects):
    problem_list = []

    for obj in objects:
        problem_list += convert_object(obj)

    return problem_list


def convert_object(obj):
    problem_list = []

    props = obj.get("YafRay", None)
    if not props:
        problem_list.append("No properties on object {0}".format(obj.name))
        return problem_list

    variable_dict = dict(samples="ml_samples", power="ml_power", double_sided="ml_double_sided", color="ml_color",
                         meshlight="ml_enable", volume="vol_enable", sigma_s="vol_scatter", sigma_a="vol_absorp",
                         density="vol_density", sharpness="vol_sharpness", cover="vol_cover", a="vol_height",
                         b="vol_steepness", bgPortalLight="bgp_enable", with_caustic="bgp_with_caustic",
                         with_diffuse="bgp_with_diffuse", photon_only="bgp_photon_only")

    for p in props:
        value = props[p]

        if p in variable_dict:
            p = variable_dict[p]

        if value == "ExpDensityVolume":
            obj.vol_region = "ExpDensity Volume"
        elif value == "UniformVolume":
            obj.vol_region = "Uniform Volume"
        elif value == "NoiseVolume":
            obj.vol_region = "Noise Volume"

        # noinspection PyBroadException
        try:
            if type(value) in {float, int, bool}:
                exec("obj.{0} = {1}".format(p, value))
            elif type(value) in {str}:
                exec("obj.{0} = \"{1}\"".format(p, value))
            else:
                exec("obj.{0} = [{1}, {2}, {3}]".format(p, round(value[0], 3), round(value[1], 3), round(value[2], 3)))
        except Exception:
            problem_list.append("Object: Problem inserting: {0}".format(p))

    return problem_list


def convert_cameras(camera_objects):
    problem_list = []

    for camera in camera_objects:
        problem_list += convert_camera(camera)

    return problem_list


def convert_camera(camera_obj):
    problem_list = []
    camera = camera_obj.data
    props = camera_obj.get("YafRay", None)
    if not props:
        problem_list.append("No properties on camera {0}".format(camera.name))
        return problem_list

    camera.camera_type = props["type"]

    variable_dict = dict(scale="ortho_scale", angle="angular_angle")

    for p in props:
        if p == "type":
            continue
        value = props[p]

        if p == "dof_object_focus" and value == 1:
            camera.dof_object = bpy.data.objects[props["dof_object"]]

        if p in variable_dict:
            p = variable_dict[p]

        # noinspection PyBroadException
        try:
            if type(value) in {float, int, bool}:
                exec("camera.{0} = {1}".format(p, value))
            elif type(value) in {str}:
                exec("camera.{0} = \"{1}\"".format(p, value))
            else:
                exec("camera.{0} = [{1}, {2}, {3}]".format(p, round(value[0], 3), round(value[1], 3),
                                                           round(value[2], 3)))
        except Exception:
            problem_list.append("Camera: Problem inserting: {0}".format(p))

    return problem_list


def convert_lights(light_objects):
    problem_list = []

    for light in light_objects:
        problem_list += convert_light(light)

    return problem_list


def convert_light(light_obj):
    problem_list = []

    light = light_obj.data

    props = light_obj.get("YafRay", None)
    if not props:
        problem_list.append("No properties on light {0}".format(light.name))
        return problem_list

    switch_light_type = {"Area": "area", "Spot": "spot", "Sun": "sun", "Point": "point", "IES LIGHT": "ies",
                         "Directional": "sun", "Sphere": "point"}
    light.lamp_type = switch_light_type.get(props["type"], "point")

    variable_dict = dict(samples="yaf_samples", radius="shadow_soft_size", power="yaf_energy",
                         createGeometry="create_geometry", iesfile="ies_file", iesSamples="yaf_samples",
                         iesSoftShadows="ies_soft_shadows", SpotSoftShadows="spot_soft_shadows",
                         SpotShadowFuzzyness="shadow_fuzzyness", SpotSamples="yaf_samples",
                         SpotPhotonOnly="photon_only")

    for p in props:
        if p == "type":
            continue

        value = props[p]

        if p in variable_dict:
            p = variable_dict[p]

        # noinspection PyBroadException
        try:
            if type(value) in {float, int, bool}:
                exec("light.{0} = {1}".format(p, value))
            elif type(value) in {str}:
                exec("light.{0} = \"{1}\"".format(p, value))
            else:
                exec(
                    "light.{0} = [{1}, {2}, {3}]".format(p, round(value[0], 3), round(value[1], 3), round(value[2], 3)))
        except Exception:
            problem_list.append("Light: Problem inserting: {0}".format(p))

    return problem_list


def convert_materials(materials):
    problem_list = []

    for mat in materials:
        # noinspection PyBroadException
        try:
            mat.name = mat.name
        except Exception:
            mat.name = "Problem"
            problem_list.append("Renaming mat.name to {0}".format(mat.name))

    for mat in materials:
        problem_list += convert_material(mat)

    return problem_list


def convert_material(mat):
    problem_list = []

    props = mat.get("YafRay", None)
    if not props:
        problem_list.append("No properties on material {0}".format(mat.name))
        return problem_list

    material_names = []
    for item in bpy.data.materials:
        material_names.append(item.name)

    if props["type"] == "Rough Glass":
        mat.mat_type = "rough_glass"
    else:
        mat.mat_type = props["type"]

    material_list = []
    for item in [m for m in bpy.data.materials if not m.name == mat.name]:
        material_list.append((item.name, item.name, ""))

    variable_dict = dict()

    if mat.mat_type in {"glossy", "coated_glossy"}:
        variable_dict["color"] = "glossy_color"
        variable_dict["IOR"] = "IOR_reflection"
        variable_dict["mirror_color"] = "coat_mir_col"

    elif mat.mat_type == "shinydiffusemat":
        variable_dict["color"] = "diffuse_color"
        variable_dict["diffuse_color"] = ""
        variable_dict["IOR"] = "IOR_reflection"

    elif mat.mat_type in {"glass", "rough_glass"}:
        variable_dict["color"] = "diffuse_color"
        variable_dict["IOR"] = "IOR_refraction"
        variable_dict["alpha"] = "refr_roughness"
        variable_dict["mirror_color"] = "glass_mir_col"
        variable_dict["transmit_filter"] = "glass_transmit"

    for p in props:
        value = props[p]

        if p in variable_dict:
            p = variable_dict[p]

        if p in {"type", "blend_shader", ""}:
            continue

        if p in {"brdf_type", "brdfType"}:
            if value == "Oren-Nayar":
                mat.brdf_type = "oren-nayar"
            continue

        # noinspection PyBroadException
        try:
            if type(value) in {float, int, bool}:
                exec("mat.{0} = {1}".format(p, value))
            elif type(value) in {str}:
                exec("mat.{0} = \"{1}\"".format(p, value))
            else:
                exec("mat.{0} = [{1}, {2}, {3}]".format(p, round(value[0], 3), round(value[1], 3), round(value[2], 3)))
        except Exception:
            problem_list.append("Material: Problem inserting: {0}".format(p))

    return problem_list


def convert_world(world):
    problem_list = []

    props = world.get("YafRay", None)
    if not props:
        problem_list.append("No properties on world")
        return problem_list

    switch_bg_type = {"Single Color": "Single Color", "Gradient": "Gradient", "Texture": "Texture", "Sunsky": "Sunsky1",
                      "DarkTide's SunSky": "Sunsky2"}
    world.bg_type = switch_bg_type.get(props["bg_type"], "Single Color")
    world.bg_from = props["from"]

    # check for Volume Integrator settings...
    if props.get("volType"):
        world.v_int_type = props["volType"]
        world.v_int_step_size = props["stepSize"]
        world.v_int_adaptive = props["adaptive"]
        world.v_int_optimize = props["optimize"]
        world.v_int_attgridres = props["attgridScale"]

    variable_dict = dict(color="single_color", ibl="use_ibl", dsturbidity="ds_turbidity", dsadd_sun="add_sun",
                         dssun_power="sun_power", dsbackground_light="background_light",
                         dslight_samples="light_samples", dsa="a_var", dsb="b_var", dsc="c_car", dsd="d_var",
                         dse="e_var", dscolorspace="color_space", dspower="power", dsexposure="exposure",
                         dsgammaenc="gamma_enc")

    for p in props:
        value = props[p]

        if p in {"bg_type", "from", "volType", "stepSize", "adaptive", "optimize", "attgridScale"}:
            continue

        if p in variable_dict:
            p = variable_dict[p]

        # noinspection PyBroadException
        try:
            if type(value) in {float, int, bool}:
                exec("world.bg_{0} = {1}".format(p, value))
            elif type(value) in {str}:
                exec("world.bg_{0} = \"{1}\"".format(p, value))
            else:
                exec("world.bg_{0} = [{1}, {2}, {3}]".format(p, round(value[0], 3), round(value[1], 3),
                                                             round(value[2], 3)))
        except Exception:
            problem_list.append("World: Problem inserting: {0}".format(p))

    return problem_list


def convert_aa_settings(scene):
    problem_list = []

    props_dummy = scene.get("YafRay", None)
    if not props_dummy:
        problem_list.append("No properties on scene")
        return problem_list

    props = props_dummy.get("Renderer", None)

    variable_dict = dict(filter_type="AA_filter_type", AA_minsamples="AA_min_samples")

    for p in props:
        # ignore general and integrator settings
        if p in {"premult", "file_type", "transpShad", "clayRender", "show_perturbed_normals", "fg_samples",
                 "finalGather", "output_method", "customString", "caustic_radius", "tiles_order", "photons",
                 "z_channel", "debugType", "autoSave", "cPhotons", "tile_size", "fg_bounces", "AO_samples", "do_AO",
                 "auto_threads", "clamp_rgb", "diffuseRadius", "autoalpha", "caustics", "search", "no_recursive",
                 "AO_distance", "threads", "show_sam_pix", "raydepth", "caustic_depth", "path_samples", "shadowDepth",
                 "drawParams", "bounces", "lightType", "use_background", "causticRadius", "caustic_mix", "AO_color",
                 "gammaInput", "caustic_type", "show_map", "gamma"}:
            continue

        value = props[p]

        if p in variable_dict:
            p = variable_dict[p]

        # noinspection PyBroadException
        try:
            if type(value) in {float, int, bool}:
                exec("scene.{0} = {1}".format(p, value))
            elif type(value) in {str}:
                exec("scene.{0} = \"{1}\"".format(p, value))
            else:
                exec(
                    "scene.{0} = [{1}, {2}, {3}]".format(p, round(value[0], 3), round(value[1], 3), round(value[2], 3)))
        except Exception:
            problem_list.append("AA: Problem inserting: {0}".format(p))

    return problem_list


def convert_general_settings(scene):
    problem_list = []

    props_dummy = scene.get("YafRay", None)
    if not props_dummy:
        problem_list.append("No properties on scene")
        return problem_list

    props = props_dummy.get("Renderer", None)

    switch_output_method = {"GUI": "into_blender", "Image": "file", "XML": "xml"}
    if props.get("output_method"):
        scene.gs_type_render = switch_output_method.get(props["output_method"], "into_blender")
        if props["output_method"] == "Image":
            switch_file_type = {"TIFF [Tag Image File Format]": "TIFF", "TGA [Truevision TARGA]": "TARGA",
                                "PNG [Portable Network Graphics]": "PNG",
                                "JPEG [Joint Photographic Experts Group]": "JPEG", "HDR [Radiance RGBE]": "HDR",
                                "EXR [IL&M OpenEXR]": "OPEN_EXR"}
            scene.img_output = switch_file_type.get(props["file_type"], "PNG")

    variable_dict = dict(raydepth="ray_depth", shadowDepth="shadow_depth", gammaInput="gamma_input",
                         clayRender="clay_render", drawParams="draw_params", customString="custom_string",
                         transpShad="transp_shad")

    for p in props:
        if p in {"tiles_order", "AA_minsamples", "show_perturbed_normals", "fg_samples", "AA_pixelwidth",
                 "AA_inc_samples", "finalGather", "output_method", "caustic_radius", "photons", "debugType", "autoSave",
                 "cPhotons", "AA_threshold", "fg_bounces", "AO_samples", "do_AO", "diffuseRadius", "auto_alpha",
                 "caustics", "search", "filter_type", "no_recursive", "AO_distance", "AO_passes", "caustic_depth",
                 "path_samples", "bounces", "lightType", "use_background", "caustic_mix", "AO_color", "caustic_type",
                 "show_map", "causticRadius", "AA_passes", "file_type", "autoalpha"}:
            continue
        value = props[p]

        if p in variable_dict:
            p = variable_dict[p]

        # noinspection PyBroadException
        try:
            if type(value) in {float, int, bool}:
                exec("scene.gs_{0} = {1}".format(p, value))
            elif type(value) in {str}:
                exec("scene.gs_{0} = \"{1}\"".format(p, value))
            else:
                exec("scene.gs_{0} = [{1}, {2}, {3}]".format(p, round(value[0], 3), round(value[1], 3),
                                                             round(value[2], 3)))
        except Exception:
            problem_list.append("GS: Problem inserting: {0}".format(p))

    return problem_list


def convert_integrator_settings(scene):
    problem_list = []

    props_dummy = scene.get("YafRay", None)
    if not props_dummy:
        problem_list.append("No properties on scene")
        return problem_list

    props = props_dummy.get("Renderer", None)

    switch_light_type = {"Photon mapping": "Photon Mapping", "Direct lighting": "Direct Lighting",
                         "Pathtracing": "Pathtracing", "Debug": "Debug",
                         "Bidirectional (EXPERIMENTAL)": "Bidirectional"}

    scene.intg_light_method = switch_light_type.get(props["lightType"], "Direct Lighting")

    variable_dict = dict(cautics="use_caustics", do_AO="use_AO", diffuseRadius="diffuse_radius",
                         finalGather="final_gather", use_background="use_bg", debugType="debug_type")

    for p in props:
        if p == "lighType":
            continue
        value = props[p]

        if p in variable_dict:
            p = variable_dict[p]

        # noinspection PyBroadException
        try:
            if type(value) in {float, int, bool}:
                exec("scene.intg_{0} = {1}".format(p, value))
            elif type(value) in {str}:
                exec("scene.intg_{0} = \"{1}\"".format(p, value))
            else:
                exec("scene.intg_{0} = [{1}, {2}, {3}]".format(p, round(value[0], 3), round(value[1], 3),
                                                               round(value[2], 3)))
        except Exception:
            problem_list.append("Intg: Problem inserting: {0}".format(p))

    return problem_list


def convert_scene_settings(scene):
    problem_list = []
    problem_list += convert_aa_settings(scene)
    problem_list += convert_general_settings(scene)
    problem_list += convert_integrator_settings(scene)
    return problem_list


class ConvertYafarayProperties(bpy.types.Operator):
    bl_idname = "yafaray4.data_convert_properties"
    bl_label = ""

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        scene = context.scene
        data = context.blend_data

        problem_list = []
        problem_list += convert_materials(data.materials)
        problem_list += convert_lights(
            [light for light in data.objects if (light.type == "LAMP" or light.type == "LIGHT")])
        problem_list += convert_cameras([camera for camera in data.objects if camera.type == "CAMERA"])
        problem_list += convert_world(scene.world)
        problem_list += convert_scene_settings(scene)
        problem_list += convert_objects([o for o in data.objects if o.type == "MESH"])

        print("Problems:")
        for p in problem_list:
            print(p)

        return {'FINISHED'}


classes = (ConvertYafarayProperties,)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed, 
    # before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the 
    # "libyafaray4_bindings" compiled module is installed on
    register()
