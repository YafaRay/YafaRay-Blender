import bpy
from bpy.props import *


def convertObjects(objects):
    problemList = []

    for object in objects:
        problemList += convertObject(object)

    return problemList


def convertObject(obj):
    problemList = []

    props = obj.get("YafRay", None)
    if not props:
        problemList.append("No properties on object" + obj.name)
        return problemList

    variableDict = dict(
        samples = "ml_samples",
        power = "ml_power",
        double_sided = "ml_double_sided",
        color = "ml_color",
        meshlight = "ml_enable",
        volume = "vol_enable",
        sigma_s = "vol_scatter",
        sigma_a = "vol_absorp",
        density = "vol_density",
        sharpness = "vol_sharpness",
        cover = "vol_cover",
        a = "vol_height",
        b = "vol_steepness",
        bgPortalLight = "bgp_enable",
        with_caustic = "bgp_with_caustic",
        with_diffuse = "bgp_with_diffuse",
        photon_only = "bgp_photon_only"
        )

    for p in props:
        value = props[p]
        # print(p, props[p])

        if p in variableDict:
            p = variableDict[p]

        if value == "ExpDensityVolume":
            obj.vol_region = "ExpDensity Volume"
        elif value == "UniformVolume":
            obj.vol_region = "Uniform Volume"
        elif value == "NoiseVolume":
            obj.vol_region = "Noise Volume"

        try:
            if type(value) in [float, int, bool]:
                exec("obj." + p + " = " + str(value))
            elif type(value) in [str]:
                exec("obj." + p + " = \"" + value + "\"")
            else:
                exec("obj." + p + " = [" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + "]")
        except:
            problemList.append("Object: Problem inserting: " + p)

    return problemList


def convertCameras(cameraObjects):
    problemList = []

    for camera in cameraObjects:
        problemList += convertCamera(camera)

    return problemList


def convertCamera(cameraObj):
    problemList = []

    camera = cameraObj.data

    props = cameraObj.get("YafRay", None)
    if not props:
        problemList.append("No properties on camera" + camera.name)
        return problemList

    variableDict = dict(
        scale = "ortho_scale",
        angle = "angular_angle")

    camera_type = props["type"]

    cameraTypeDict = dict()
    cameraTypeDict["perspective"] = "perspective"
    cameraTypeDict["architect"] = "architect"
    cameraTypeDict["angular"] = "angular"
    cameraTypeDict["orthographic"] = "orthographic"

    camera.camera_type = cameraTypeDict[camera_type]
    print("camera", camera.name, camera.camera_type)

    for p in props:

        value = props[p]
        # print(p, value)
        if p == "dof_object_focus" and value == 1:
            camera.dof_object = bpy.data.objects[props["dof_object"]]

        if p in variableDict:
            p = variableDict[p]

        try:
            if type(value) in [float, int, bool]:
                exec("camera." + p + " = " + str(value))
            elif type(value) in [str]:
                exec("camera." + p + " = \"" + value + "\"")
            else:
                exec("camera." + p + " = [" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + "]")
        except:
            problemList.append("Camera: Problem inserting: " + p)

    return problemList


def convertLights(lightObjects):
    problemList = []

    for light in lightObjects:
        problemList += convertLight(light)

    return problemList


def convertLight(lightObj):
    problemList = []

    light = lightObj.data

    props = lightObj.get("YafRay", None)
    if not props:
        problemList.append("No properties on light" + light.name)
        return problemList

    variableDict = dict(
        samples = "yaf_samples",
        radius = "shadow_soft_size",
        power = "energy",
        createGeometry = "create_geometry")

    # set just the lamp type correctly so the blender type will be also correct
    if props["type"] == "Area":
        light.lamp_type = "area"
    elif props["type"] == "Point":
        light.lamp_type = "point"
    elif props["type"] == "Sphere":
        light.lamp_type = "point"
    elif props["type"] == "IES Light":
        light.lamp_type = "ies"
    elif props["type"] == "Spot":
        light.lamp_type = "spot"
    elif props["type"] == "Sun":
        light.lamp_type = "sun"
    elif props["type"] == "Directional":
        light.lamp_type = "sun"
    else:
        print("No lamp type fits!")

    print("lamp", light.name, light.lamp_type)

    for p in props:
        if p == "type":
            continue

        value = props[p]
        # print(p, value)

        if p in variableDict:
            p = variableDict[p]

        try:
            if type(value) in [float, int, bool]:
                exec("light." + p + " = " + str(value))
            elif type(value) in [str]:
                exec("light." + p + " = \"" + value + "\"")
            else:
                exec("light." + p + " = [" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + "]")
        except:
            problemList.append("Light: Problem inserting: " + p)

    return problemList


def convertMaterials(materials):
    problemList = []

    for mat in materials:
        try:
            mat.name = mat.name
        except:
            mat.name = "Problem"
            problemList.append("Renaming mat.name to " + mat.name)

    for mat in materials:
        problemList += convertMaterial(mat)

    return problemList


def convertMaterial(mat):
    problemList = []

    print("convert", mat.name, mat.mat_type)
    props = mat.get("YafRay", None)
    if not props:
        problemList.append("No properties on material " + mat.name)
        return problemList

    materialNames = []
    for item in bpy.data.materials:
        materialNames.append(item.name)
    if props["type"] == "Rough Glass":
        mat.mat_type = 'rough_glass'
    else:
        mat.mat_type = props["type"]

    materialList = []
    for item in [m for m in bpy.data.materials if not m.name == mat.name]:
        materialList.append((item.name, item.name, ""))

    Material = bpy.types.Material
    Material.material1 = EnumProperty(items = materialList, name = "Material One")
    Material.material2 = EnumProperty(items = materialList, name = "Material Two")

    # print("type", props["type"])

    variableDict = dict()

    if mat.mat_type in ["glossy", "coated_glossy"]:
        variableDict["color"] = "glossy_color"
        variableDict["IOR"] = "IOR_reflection"
        variableDict["mirror_color"] = "coat_mir_col"

    elif mat.mat_type == "shinydiffusemat":
        variableDict["color"] = "diffuse_color"
        variableDict["diffuse_color"] = ""
        variableDict["IOR"] = "IOR_reflection"

    elif mat.mat_type in ["glass", "rough_glass"]:
        variableDict["IOR"] = "IOR_refraction"
        variableDict["alpha"] = "refr_roughness"
        variableDict["mirror_color"] = "glass_mir_col"
        variableDict["transmit_filter"] = "glass_transmit"

    for p in props:
        value = props[p]
        # print(p, value)

        if p in variableDict:
            print("p in dict:", p, variableDict[p])
            p = variableDict[p]

        if p == "type":
            continue
        if p == "mask":
            continue
        if p in ["material1", "material2"]:
            if value not in materialNames:
                problemList.append("Broken blend material: " + mat.name + " replacing ...")
                exec("mat." + p + " = \"" + materialList[0][0] + "\"")
                continue

        if p == "brdf_type" or p == "brdfType":
            if value == "Oren-Nayar":
                mat.brdf_type = "oren-nayar"
            continue

        # print("type:", type(value))

        try:
            if type(value) in [float, int, bool]:
                exec("mat." + p + " = " + str(value))
            elif type(value) in [str]:
                exec("mat." + p + " = \"" + value + "\"")
            else:
                exec("mat." + p + " = [" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + "]")
        except:
            problemList.append("Material: Problem inserting: " + p)

    return problemList


def convertWorld(world):
    problemList = []

    props = world.get("YafRay", None)
    if not props:
        problemList.append("No properties on world")
        return problemList

    bg_type = props["bg_type"]

    variableDict = dict(
        zenith_color = "zenith_color",
        horizon_color = "horizon_color",
        horizon_ground_color = "bg_horizon_ground_color",
        zenith_ground_color = "bg_zenith_ground_color",
        color = "bg_single_color",
        ibl = "bg_use_ibl",
        dsturbidity = "bg_turbidity",
        dsadd_sun = "bg_add_sun",
        dssun_power = "bg_sun_power",
        dsbackgroundlight = "bg_background_light",
        dslight_samples = "bg_light_samples",
        dspower = "bg_dsbright",
        dsexposure = "bg_exposure",
        dsgammenc = "bg_gamma_enc",
        volType = "v_int_type",
        stepSize = "v_int_step_size",
        adaptive = "v_int_adaptive",
        optimize = "v_int_optimize",
        attgridScale = "v_int_attgridres")

    bgTypeDict = dict()
    bgTypeDict["Single Color"] = "Single Color"
    bgTypeDict["Gradient"] = "Gradient"
    bgTypeDict["Texture"] = "Texture"
    bgTypeDict["Sunsky"] = "Sunsky"
    bgTypeDict["DarkTide's SunSky"] = "Darktide's Sunsky"

    world.bg_type = bgTypeDict[bg_type]

    for p in props:
        value = props[p]
        # print(p, props[p])

        if p in variableDict:
            p = variableDict[p]

        try:
            if type(value) in [float, int, bool]:
                exec("world." + p + " = " + str(value))
            elif type(value) in [str]:
                exec("world." + p + " = \"" + value + "\"")
            else:
                exec("world." + p + " = [" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + "]")
        except:
            problemList.append("World: Problem inserting: " + p)

    return problemList


def convertAASettings(scene):
    problemList = []

    propsDummy = scene.get("YafRay", None)
    if not propsDummy:
        problemList.append("No properties on scene")
        return problemList

    props = propsDummy.get("Renderer", None)

    variableDict = dict(
        filter_type = "AA_filter_type",
        AA_minsamples = "AA_min_samples")

    for p in props:
        value = props[p]
        # print(p, props[p])

        if p in variableDict:
            p = variableDict[p]

        try:
            if type(value) in [float, int, bool]:
                exec("scene." + p + " = " + str(value))
            elif type(value) in [str]:
                exec("scene." + p + " = \"" + value + "\"")
            else:
                exec("scene." + p + " = [" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + "]")
        except:
            problemList.append("AA: Problem inserting: " + p)

    return problemList


def convertGeneralSettings(scene):
    problemList = []

    propsDummy = scene.get("YafRay", None)
    if not propsDummy:
        problemList.append("No properties on scene")
        return problemList

    props = propsDummy.get("Renderer", None)

    variableDict = dict(
        raydepth = "ray_depth",
        shadowDepth = "shadow_depth",
        gammaInput = "gamma_input",
        clayRender = "clay_render",
        drawParams = "draw_params",
        customString = "custom_string",
        autoalpha = "auto_alpha",
        transpShad = "transp_shad")

    try:  # not for old 0.1.1 yafaray
        tileOrder = props["tiles_order"]
        tileOrderDict = dict()
        tileOrderDict["Linear"] = "linear"
        tileOrderDict["Random"] = "random"
        scene.gs_tile_order = tileOrderDict[tileOrder]
    except:
        print("No tile order propertie found, file from old yafaray 0.1.1 exporter")

    for p in props:
        value = props[p]
        # print(p, props[p])

        if p in variableDict:
            p = variableDict[p]

        try:
            if type(value) in [float, int, bool]:
                exec("scene.gs_" + p + " = " + str(value))
            elif type(value) in [str]:
                exec("scene.gs_" + p + " = \"" + value + "\"")
            else:
                exec("scene.gs_" + p + " = [" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + "]")
        except:
            problemList.append("GS: Problem inserting: " + p)

    return problemList


def convertIntegratorSettings(scene):
    problemList = []

    propsDummy = scene.get("YafRay", None)
    if not propsDummy:
        problemList.append("No properties on scene")
        return problemList

    props = propsDummy.get("Renderer", None)

    variableDict = dict(
        cautics = "use_caustics",
        do_AO = "use_AO",
        diffuseRadius = "diffuse_radius",
        finalGather = "final_gather",
        use_background = "use_bg",
        debugType = "debug_type")

    lightType = props["lightType"]

    lightTypeDict = dict()
    lightTypeDict["Photon mapping"] = "Photon Mapping"
    lightTypeDict["Direct lighting"] = "Direct Lighting"
    lightTypeDict["Pathtracing"] = "Pathtracing"
    lightTypeDict["Debug"] = "Debug"
    scene.intg_light_method = lightTypeDict[lightType]

    for p in props:
        value = props[p]
        # print(p, props[p])

        if p in variableDict:
            p = variableDict[p]

        try:
            if type(value) in [float, int, bool]:
                exec("scene.intg_" + p + " = " + str(value))
            elif type(value) in [str]:
                exec("scene.intg_." + p + " = \"" + value + "\"")
            else:
                exec("scene.intg_" + p + " = [" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + "]")
        except:
            problemList.append("Intg: Problem inserting: " + p)

    return problemList


def convertSceneSettings(scene):
    problemList = []
    problemList += convertAASettings(scene)
    problemList += convertGeneralSettings(scene)
    problemList += convertIntegratorSettings(scene)
    return problemList


class ConvertYafarayProperties(bpy.types.Operator):
    bl_idname = "data.convert_yafaray_properties"
    bl_label = ""

    def execute(self, context):
        scene = context.scene
        data = context.blend_data

        problemList = []

        problemList += convertMaterials(data.materials)
        problemList += convertLights([l for l in data.objects if l.type == "LAMP"])
        problemList += convertCameras([c for c in data.objects if c.type == "CAMERA"])
        problemList += convertWorld(data.worlds[0])
        problemList += convertSceneSettings(scene)
        problemList += convertObjects([o for o in data.objects if o.type == "MESH"])

        print("Problems:")
        for p in problemList:
            print(p)

        return {'FINISHED'}
