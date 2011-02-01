import bpy
from bpy.props import *


def convertLights(lights):
    problemList = []

    for light in lights:
        problemList += convertLight(light)

    return problemList


def convertLight(light):
    problemList = []

    lightObj = bpy.data.objects.get(light.name)

    if not lightObj:
        problemList.append("Light " + light.name + " not found as object.")
        return problemList

    props = lightObj.get("YafRay", None)
    if not props:
        problemList.append("No properties on light" + light.name)
        return problemList

    variableDict = dict(
        samples = "yaf_samples",
        radius = "shadow_soft_size",
        power = "energy",
        createGeometry = "create_geometry")


    for p in props:
        value = props[p]
        print(p, props[p])

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

    values = [("Material One", "Material One", "")]
    for item in materials:
        values.append((item.name, item.name, ""))

    materialList1 = tuple(values)

    values = [("Material Two", "Material Two", "")]
    for item in materials:
        values.append((item.name, item.name, ""))

    materialList2 = tuple(values)

    Material = bpy.types.Material
    Material.material1 = EnumProperty(items = materialList1)
    Material.material2 = EnumProperty(items = materialList2)

    for mat in materials:
        problemList += convertMaterial(mat)

    return problemList



def convertMaterial(mat):
    problemList = []

    # print("convert", mat.name)
    props = mat.get("YafRay", None)
    if not props:
        problemList.append("No properties on material " + mat.name)
        return problemList

    materialNames = []
    for item in bpy.data.materials:
        materialNames.append(item.name)

    mat.mat_type = props["type"]

    # print("type", props["type"])

    for p in props:
        value = props[p]
        # print(p, props[p])

        if p == "type": continue
        if p == "mask": continue
        if p in ["material1", "material2"]:
            if value not in materialNames:
                problemList.append("Broken blend material: " + mat.name + " replacing ...")
                exec("mat." + p + " = \"" + materialNames[0] + "\"")
                continue

        if p == "brdf_type" or p == "brdfType":
            if value == "Oren-Nayar":
                mat.brdf_type = "oren-nayar"
            continue

        # print("type:", type(value))

        if type(value) in [float, int, bool]:
            exec("mat." + p + " = " + str(value))
        elif type(value) in [str]:
            exec("mat." + p + " = \"" + value + "\"")
        else:
            exec("mat." + p + " = [" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + "]")

    return problemList


def convertWorld(world):
    problemList = []

    # print("convert", mat.name)
    props = world.get("YafRay", None)
    if not props:
        problemList.append("No properties on world")
        return problemList

    bg_type = props["bg_type"]

    bgTypeDict = dict()
    bgTypeDict["Constant"]= "Single Color"
    bgTypeDict["Gradient"]= "Gradient"
    bgTypeDict["Texture"]= "Texture"
    bgTypeDict["Sunsky"]= "Sunsky"
    bgTypeDict["DarkTide's SunSky"]= "Darktide's Sunsky"

    world.bg_type = bgTypeDict[bg_type]

    for p in props:
        value = props[p]
        # print(p, props[p])

        if p in ['zenith_color', 'horizon_color']:
            exec("world." + p + " = [" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + "]")
            continue
        if p in ['horizon_ground_color']:
            exec("world.ambient_color = [" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + "]")
            continue
        if p in ['color']:
            exec("world.horizon_color = [" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + "]")
            continue
        if p in ['ibl']:
            exec("world.bg_use_ibl = " + str(value))
            continue
        if p in ['dsturbidity']:
            exec("world.bg_turbidity = " + str(value))
            continue
        if p in ['dsadd_sun']:
            exec("world.bg_add_sun = " + str(value))
            continue
        if p in ['dssun_power']:
            exec("world.bg_sun_power = " + str(value))
            continue
        if p in ['dsbackground_light']:
            exec("world.bg_background_light = " + str(value))
            continue
        if p in ['dslight_samples']:
            exec("world.bg_light_samples = " + str(value))
            continue
        if p in ['dspower']:
            exec("world.bg_power = " + str(value))
            continue
        if p in ['dsexposure']:
            exec("world.bg_exposure = " + str(value))
            continue
        if p in ['dsgammaenc']:
            exec("world.bg_gamma_enc = " + str(value))
            continue
        if p in ['alpha', 'sigma_t', 'attgridScale', 'optimize', 'adaptive', 'stepSize', 'volType', 'dscolorspace', 'with_caustic', 'with_diffuse', 'bg_type', 'dsa', 'dsb', 'dsc', 'dsd', 'dse', 'dsf']: continue

        if type(value) in [float, int, bool]:
            exec("world.bg_" + p + " = " + str(value))
        elif type(value) in [str]:
            exec("world.bg_" + p + " = \"" + value + "\"")
        else:
            exec("world.bg_" + p + " = [" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + "]")  


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
        minsamples = "AA_filter_type")

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
        gammeInput = "gamma_input",
        clayRender = "clay_render",
        drawPArams = "draw_params",
        customString = "custom_string",
        autoalpha = "auto_alpha",
        transpShad = "transp_shad")

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
        diffuseRadiu = "diffuse_radius",
        finalGather = "final_gather",
        use_background = "use_bg",
        debugType = "debug_type")

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
        problemList += convertLights(data.lamps)
        problemList += convertWorld(data.worlds[0])
        problemList += convertSceneSettings(scene)

        print("Problems:")
        for p in problemList:
            print(p)

        return {'FINISHED'}


