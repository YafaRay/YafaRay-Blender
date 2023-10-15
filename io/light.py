# SPDX-License-Identifier: GPL-2.0-or-later

import os
from math import degrees, pi, sin, cos

import bpy
import libyafaray4_bindings
import mathutils
from bpy.path import abspath
from mathutils import Vector

from ..util.io import scene_from_depsgraph


def multiplyMatrix4x4Vector4(matrix, vector):
    result = mathutils.Vector((0.0, 0.0, 0.0, 0.0))
    if bpy.app.version >= (2, 80, 0):
        for i in range(4):
            result[i] = vector @ matrix[i]  # use reverse vector multiply order, API changed with rev. 38674
    else:
        for i in range(4):
            result[i] = vector * matrix[i]  # use reverse vector multiply order, API changed with rev. 38674
    return result


class LightControl:
    def __init__(self, depsgraph, scene_yafaray, logger, is_preview):
        self.depsgraph = depsgraph
        self.scene = scene_from_depsgraph(depsgraph)
        self.scene_yafaray = scene_yafaray
        self.logger = logger
        self.lightMatName = None
        self.is_preview = is_preview

    def makeSphere(self, nu, nv, x, y, z, rad, mat):

        # get next free id from interface
        object_name = "SphereLight::" + mat
        param_map = libyafaray4_bindings.ParamMap()
        param_map.set_string("type", "mesh")
        param_map.set_int("num_vertices", 2 + (nu - 1) * nv)
        param_map.set_int("num_faces", 2 * (nu - 1) * nv)
        object_id = self.scene_yafaray.create_object(object_name, param_map)

        self.scene_yafaray.add_vertex(object_id, x, y, z + rad)
        self.scene_yafaray.add_vertex(object_id, x, y, z - rad)
        for v in range(0, nv):
            t = v / float(nv)
            sin_v = sin(2.0 * pi * t)
            cos_v = cos(2.0 * pi * t)
            for u in range(1, nu):
                s = u / float(nu)
                sin_u = sin(pi * s)
                cos_u = cos(pi * s)
                self.scene_yafaray.add_vertex(object_id, x + cos_v * sin_u * rad, y + sin_v * sin_u * rad,
                                             z + cos_u * rad)
        material_id = self.scene_yafaray.get_material_id(mat)
        for v in range(0, nv):
            self.scene_yafaray.add_triangle(object_id, 0, 2 + v * (nu - 1), 2 + ((v + 1) % nv) * (nu - 1), material_id)
            self.scene_yafaray.add_triangle(object_id, 1, ((v + 1) % nv) * (nu - 1) + nu, v * (nu - 1) + nu, material_id)
            for u in range(object_id, 0, nu - 2):
                self.scene_yafaray.add_triangle(object_id, 2 + v * (nu - 1) + u, 2 + v * (nu - 1) + u + 1,
                                               2 + ((v + 1) % nv) * (nu - 1) + u, material_id)
                self.scene_yafaray.add_triangle(object_id, 2 + v * (nu - 1) + u + 1,
                                               2 + ((v + 1) % nv) * (nu - 1) + u + 1, 2 + ((v + 1) % nv) * (nu - 1) + u,
                                               material_id)

        return object_name

    def create_light(self, yi, light_object, matrix=None):

        light = light_object.data
        name = light_object.name

        if matrix is None:
            matrix = light_object.matrix_world.copy()
        # matrix indexing (row, colums) changed in Blender rev.42816, for explanation see also:
        # http://wiki.blender.org/index.php/User:TrumanBlending/Matrix_Indexing
        pos = matrix.col[3]
        direct = matrix.col[2]  # msg 'Assignment to reserved built-in symbol: dir' ( change to direct)
        # up = matrix[1]  /* UNUSED */
        to = pos - direct

        lightType = light.lamp_type
        power = light.yaf_energy
        color = light.color

        if self.is_preview:
            if name == "Light" or name == "Lamp":
                pos = (-6, -4, 8, 1.0)
                power = 5
                if bpy.data.scenes[0].yafaray.preview.enable:
                    power *= bpy.data.scenes[0].yafaray.preview.fill_light_power_factor
                    color = bpy.data.scenes[0].yafaray.preview.fill_light_color

            elif name == "Light.001" or name == "Lamp.001":
                pos = (6, -6, -2, 1.0)
                power = 6
                if bpy.data.scenes[0].yafaray.preview.enable:
                    power *= bpy.data.scenes[0].yafaray.preview.fill_light_power_factor
                    color = bpy.data.scenes[0].yafaray.preview.fill_light_color

            elif name == "Light.002" or name == "Lamp.002":
                pos = (-2.9123109, -7.270790733, 4.439187765, 1.0)
                to = (-0.0062182024121284485, 0.6771485209465027, 1.8015732765197754, 1.0)
                power = 5
                if bpy.data.scenes[0].yafaray.preview.enable:
                    power *= bpy.data.scenes[0].yafaray.preview.key_light_power_factor
                    color = bpy.data.scenes[0].yafaray.preview.key_light_color

            elif name == "Light.008" or name == "Lamp.008":
                lightType = "sun"
                power = 0.8
                if bpy.data.scenes[0].yafaray.preview.enable:
                    power *= bpy.data.scenes[0].yafaray.preview.key_light_power_factor
                    color = bpy.data.scenes[0].yafaray.preview.key_light_color

            if bpy.data.scenes[0].yafaray.preview.enable:
                matrix2 = mathutils.Matrix.Rotation(bpy.data.scenes[0].yafaray.preview.light_rot_z, 4, 'Z')
                pos = multiplyMatrix4x4Vector4(matrix2, mathutils.Vector((pos[0], pos[1], pos[2], pos[3])))

        self.logger.print_info("Exporting Light: {0} [{1}]".format(name, lightType))

        if light.create_geometry:  # and not self.lightMat:
            param_map = libyafaray4_bindings.ParamMap()
            param_map_list = libyafaray4_bindings.ParamMapList()
            param_map.set_color("color", color[0], color[1], color[2])  # color for spherelight and area light geometry
            param_map.set_string("type", "light_mat")
            power_sphere = power / light.yaf_sphere_radius
            param_map.set_float("power", power_sphere)

            self.scene_yafaray.create_material(name, param_map, param_map_list)
            self.lightMatName = name
            # param_map.set_bool("light_enabled", light.light_enabled)

        param_map = libyafaray4_bindings.ParamMap()
        if lightType == "point":
            param_map.set_string("type", "pointlight")
            if getattr(light, "use_sphere", False):
                if light.create_geometry:
                    object_name = self.makeSphere(24, 48, pos[0], pos[1], pos[2], light.yaf_sphere_radius,
                                                  self.lightMatName)
                    param_map.set_string("object_name", object_name)
                param_map.set_string("type", "spherelight")
                param_map.set_int("samples", light.yaf_samples)
                param_map.set_float("radius", light.yaf_sphere_radius)
                param_map.set_bool("light_enabled", light.light_enabled)
                param_map.set_bool("cast_shadows", light.cast_shadows)

        elif lightType == "spot":
            if self.is_preview and name == "Light.002":
                angle = 50
            else:
                # Blender reports the angle of the full cone in radians
                # and we need half of the apperture angle in degrees
                angle = degrees(light.spot_size) * 0.5

            param_map.set_string("type", "spotlight")

            param_map.set_float("cone_angle", angle)
            param_map.set_float("blend", light.spot_blend)
            param_map.set_vector("to", to[0], to[1], to[2])
            param_map.set_bool("soft_shadows", light.spot_soft_shadows)
            param_map.set_float("shadowFuzzyness", light.shadow_fuzzyness)
            param_map.set_int("samples", light.yaf_samples)
            param_map.set_bool("light_enabled", light.light_enabled)
            param_map.set_bool("cast_shadows", light.cast_shadows)

        elif lightType == "sun":
            param_map.set_string("type", "sunlight")
            param_map.set_int("samples", light.yaf_samples)
            param_map.set_float("angle", light.angle)
            param_map.set_vector("direction", direct[0], direct[1], direct[2])
            param_map.set_bool("light_enabled", light.light_enabled)
            param_map.set_bool("cast_shadows", light.cast_shadows)

        elif lightType == "directional":
            param_map.set_string("type", "directional")
            param_map.set_vector("direction", direct[0], direct[1], direct[2])
            param_map.set_bool("infinite", light.infinite)
            if not light.infinite:
                param_map.set_float("radius", light.shadow_soft_size)
                param_map.set_vector("from", pos[0], pos[1], pos[2])
            param_map.set_bool("light_enabled", light.light_enabled)
            param_map.set_bool("cast_shadows", light.cast_shadows)

        elif lightType == "ies":
            param_map.set_string("type", "ieslight")
            param_map.set_vector("to", to[0], to[1], to[2])
            ies_file = abspath(light.ies_file)
            if not any(ies_file) and not os.path.exists(ies_file):
                self.logger.printWarning("IES file not found for {0}".format(name))
                return False
            param_map.set_string("file", ies_file)
            param_map.set_int("samples", light.yaf_samples)
            param_map.set_bool("soft_shadows", light.ies_soft_shadows)
            param_map.set_bool("light_enabled", light.light_enabled)
            param_map.set_bool("cast_shadows", light.cast_shadows)

        elif lightType == "area":
            sizeX = light.size
            sizeY = light.size
            if light.shape == 'RECTANGLE':
                sizeY = light.size_y
            matrix = light_object.matrix_world.copy()

            # generate an untransformed rectangle in the XY plane with
            # the light's position as the centerpoint and transform it
            # using its transformation matrix
            point = Vector((-sizeX / 2, -sizeY / 2, 0))
            corner1 = Vector((-sizeX / 2, sizeY / 2, 0))
            corner2 = Vector((sizeX / 2, sizeY / 2, 0))
            corner3 = Vector((sizeX / 2, -sizeY / 2, 0))

            point = matrix * point  # use reverse vector multiply order, API changed with rev. 38674
            corner1 = matrix * corner1  # use reverse vector multiply order, API changed with rev. 38674
            corner2 = matrix * corner2  # use reverse vector multiply order, API changed with rev. 38674
            corner3 = matrix * corner3  # use reverse vector multiply order, API changed with rev. 38674

            param_map = libyafaray4_bindings.ParamMap()
            if light.create_geometry:
                object_name = "AreaLight::" + self.lightMatName
                param_map.set_string("type", "mesh")
                param_map.set_int("num_vertices", 4)
                param_map.set_int("num_faces", 2)
                object_id = self.scene_yafaray.create_object(object_name, param_map)
                material_id = self.scene_yafaray.get_material_id(self.lightMatName)
                yi.add_vertex(object_id, point[0], point[1], point[2])
                yi.add_vertex(object_id, corner1[0], corner1[1], corner1[2])
                yi.add_vertex(object_id, corner2[0], corner2[1], corner2[2])
                yi.add_vertex(object_id, corner3[0], corner3[1], corner3[2])
                yi.add_triangle(object_id, 0, 1, 2, material_id)
                yi.add_triangle(object_id, 0, 2, 3, material_id)
                param_map.clear()
                param_map.set_string("object_name", object_name)

            param_map.set_string("type", "arealight")
            param_map.set_int("samples", light.yaf_samples)
            param_map.set_vector("corner", point[0], point[1], point[2])
            param_map.set_vector("point1", corner1[0], corner1[1], corner1[2])
            param_map.set_vector("point2", corner3[0], corner3[1], corner3[2])
            param_map.set_bool("light_enabled", light.light_enabled)
            param_map.set_bool("cast_shadows", light.cast_shadows)

        if lightType not in {"area", "sun", "directional"}:
            # "from" is not used for area, sunlight and infinite directional light
            param_map.set_vector("from", pos[0], pos[1], pos[2])
        if lightType in {"point", "spot"}:
            if getattr(light, "use_sphere", False) and lightType == "point":
                power = 0.5 * power * power / (light.yaf_sphere_radius * light.yaf_sphere_radius)
            else:
                power = 0.5 * power * power

        param_map.set_color("color", color[0], color[1], color[2])
        param_map.set_float("power", power)
        param_map.set_bool("light_enabled", light.light_enabled)
        param_map.set_bool("cast_shadows", light.cast_shadows)
        param_map.set_bool("with_caustic", light.caustic_photons)
        param_map.set_bool("with_diffuse", light.diffuse_photons)
        param_map.set_bool("photon_only", light.photon_only)
        self.scene_yafaray.create_light(name, param_map)

        return True
