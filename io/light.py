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

import os
from mathutils import Vector
import mathutils
import bpy
from math import degrees, pi, sin, cos
import libyafaray4_bindings
from bpy.path import abspath

def multiplyMatrix4x4Vector4(matrix, vector):
    result = mathutils.Vector((0.0, 0.0, 0.0, 0.0))
    if bpy.app.version >= (2, 80, 0):
        for i in range(4):
            result[i] = vector @ matrix[i]  # use reverse vector multiply order, API changed with rev. 38674
    else:
        for i in range(4):
            result[i] = vector * matrix[i]  # use reverse vector multiply order, API changed with rev. 38674
    return result

class Light:
    def __init__(self, scene, logger, preview):
        self.yaf_scene = scene
        self.yaf_logger = logger
        self.lightMatName = None
        self.preview = preview

    def makeSphere(self, nu, nv, x, y, z, rad, mat):

        # get next free id from interface
        object_name = "SphereLight::" + mat
        yaf_param_map = libyafaray4_bindings.ParamMap()
        yaf_param_map.setString("type", "mesh")
        yaf_param_map.setInt("num_vertices", 2 + (nu - 1) * nv)
        yaf_param_map.setInt("num_faces", 2 * (nu - 1) * nv)
        object_id = self.yaf_scene.createObject(object_name, yaf_param_map)

        self.yaf_scene.addVertex(object_id, x, y, z + rad)
        self.yaf_scene.addVertex(object_id, x, y, z - rad)
        for v in range(0, nv):
            t = v / float(nv)
            sin_v = sin(2.0 * pi * t)
            cos_v = cos(2.0 * pi * t)
            for u in range(1, nu):
                s = u / float(nu)
                sin_u = sin(pi * s)
                cos_u = cos(pi * s)
                self.yaf_scene.addVertex(object_id, x + cos_v * sin_u * rad, y + sin_v * sin_u * rad, z + cos_u * rad)
        material_id = self.yaf_scene.getMaterialId(mat)
        for v in range(0, nv):
            self.yaf_scene.addTriangle(object_id, 0, 2 + v * (nu - 1), 2 + ((v + 1) % nv) * (nu - 1), material_id)
            self.yaf_scene.addTriangle(object_id, 1, ((v + 1) % nv) * (nu - 1) + nu, v * (nu - 1) + nu, material_id)
            for u in range(object_id, 0, nu - 2):
                self.yaf_scene.addTriangle(object_id, 2 + v * (nu - 1) + u, 2 + v * (nu - 1) + u + 1, 2 + ((v + 1) % nv) * (nu - 1) + u, material_id)
                self.yaf_scene.addTriangle(object_id, 2 + v * (nu - 1) + u + 1, 2 + ((v + 1) % nv) * (nu - 1) + u + 1, 2 + ((v + 1) % nv) * (nu - 1) + u, material_id)

        return object_name

    def createLight(self, yi, light_object, matrix=None):

        light = light_object.data
        name = light_object.name

        if matrix is None:
            matrix = light_object.matrix_world.copy()
        # matrix indexing (row, colums) changed in Blender rev.42816, for explanation see also:
        # http://wiki.blender.org/index.php/User:TrumanBlending/Matrix_Indexing
        pos = matrix.col[3]
        direct = matrix.col[2] # msg 'Assignment to reserved built-in symbol: dir' ( change to direct)
        # up = matrix[1]  /* UNUSED */
        to = pos - direct

        lightType = light.lamp_type
        power = light.yaf_energy
        color = light.color

        if self.preview:
            if name == "Light" or name == "Lamp":
                pos = (-6, -4, 8, 1.0)
                power = 5
                if bpy.data.scenes[0].yafaray.preview.enable:
                    power *= bpy.data.scenes[0].yafaray.preview.fillLightPowerFactor
                    color = bpy.data.scenes[0].yafaray.preview.fillLightColor

            elif name == "Light.001" or name == "Lamp.001":
                pos = (6, -6, -2, 1.0)
                power = 6
                if bpy.data.scenes[0].yafaray.preview.enable:
                    power *= bpy.data.scenes[0].yafaray.preview.fillLightPowerFactor
                    color = bpy.data.scenes[0].yafaray.preview.fillLightColor
                    
            elif name == "Light.002" or name == "Lamp.002":
                pos = (-2.9123109, -7.270790733, 4.439187765, 1.0)
                to = (-0.0062182024121284485, 0.6771485209465027, 1.8015732765197754, 1.0)
                power = 5
                if bpy.data.scenes[0].yafaray.preview.enable:
                    power *= bpy.data.scenes[0].yafaray.preview.keyLightPowerFactor
                    color = bpy.data.scenes[0].yafaray.preview.keyLightColor
                    
            elif name == "Light.008" or name == "Lamp.008":
                lightType = "sun"
                power = 0.8
                if bpy.data.scenes[0].yafaray.preview.enable:
                    power *= bpy.data.scenes[0].yafaray.preview.keyLightPowerFactor
                    color = bpy.data.scenes[0].yafaray.preview.keyLightColor
            
            if bpy.data.scenes[0].yafaray.preview.enable:
                matrix2 = mathutils.Matrix.Rotation(bpy.data.scenes[0].yafaray.preview.lightRotZ, 4, 'Z')
                pos = multiplyMatrix4x4Vector4(matrix2, mathutils.Vector((pos[0], pos[1], pos[2], pos[3])))

        self.yaf_logger.printInfo("Exporting Light: {0} [{1}]".format(name, lightType))

        if light.create_geometry:  # and not self.lightMat:
            yaf_param_map = libyafaray4_bindings.ParamMap()
            yaf_param_map_list = libyafaray4_bindings.ParamMapList()
            yaf_param_map.setColor("color", color[0], color[1], color[2])  # color for spherelight and area light geometry
            yaf_param_map.setString("type", "light_mat")
            power_sphere = power / light.yaf_sphere_radius
            yaf_param_map.setFloat("power", power_sphere)
        
            self.yaf_scene.createMaterial(name, yaf_param_map, yaf_param_map_list)
            self.lightMatName = name
            #yaf_param_map.setBool("light_enabled", light.light_enabled)

        yaf_param_map = libyafaray4_bindings.ParamMap()
        if lightType == "point":
            yaf_param_map.setString("type", "pointlight")
            if getattr(light, "use_sphere", False):
                if light.create_geometry:
                    ID = self.makeSphere(24, 48, pos[0], pos[1], pos[2], light.yaf_sphere_radius, self.lightMatName)
                    yaf_param_map.setString("object_name", ID)
                yaf_param_map.setString("type", "spherelight")
                yaf_param_map.setInt("samples", light.yaf_samples)
                yaf_param_map.setFloat("radius", light.yaf_sphere_radius)
                yaf_param_map.setBool("light_enabled", light.light_enabled)
                yaf_param_map.setBool("cast_shadows", light.cast_shadows)

        elif lightType == "spot":
            if self.preview and name == "Light.002":
                angle = 50
            else:
                # Blender reports the angle of the full cone in radians
                # and we need half of the apperture angle in degrees
                angle = degrees(light.spot_size) * 0.5

            yaf_param_map.setString("type", "spotlight")

            yaf_param_map.setFloat("cone_angle", angle)
            yaf_param_map.setFloat("blend", light.spot_blend)
            yaf_param_map.setVector("to", to[0], to[1], to[2])
            yaf_param_map.setBool("soft_shadows", light.spot_soft_shadows)
            yaf_param_map.setFloat("shadowFuzzyness", light.shadow_fuzzyness)
            yaf_param_map.setInt("samples", light.yaf_samples)
            yaf_param_map.setBool("light_enabled", light.light_enabled)
            yaf_param_map.setBool("cast_shadows", light.cast_shadows)

        elif lightType == "sun":
            yaf_param_map.setString("type", "sunlight")
            yaf_param_map.setInt("samples", light.yaf_samples)
            yaf_param_map.setFloat("angle", light.angle)
            yaf_param_map.setVector("direction", direct[0], direct[1], direct[2])
            yaf_param_map.setBool("light_enabled", light.light_enabled)
            yaf_param_map.setBool("cast_shadows", light.cast_shadows)

        elif lightType == "directional":
            yaf_param_map.setString("type", "directional")
            yaf_param_map.setVector("direction", direct[0], direct[1], direct[2])
            yaf_param_map.setBool("infinite", light.infinite)
            if not light.infinite:
                yaf_param_map.setFloat("radius", light.shadow_soft_size)
                yaf_param_map.setVector("from", pos[0], pos[1], pos[2])
            yaf_param_map.setBool("light_enabled", light.light_enabled)
            yaf_param_map.setBool("cast_shadows", light.cast_shadows)

        elif lightType == "ies":
            yaf_param_map.setString("type", "ieslight")
            yaf_param_map.setVector("to", to[0], to[1], to[2])
            ies_file = abspath(light.ies_file)
            if not any(ies_file) and not os.path.exists(ies_file):
                self.yaf_logger.printWarning("IES file not found for {0}".format(name))
                return False
            yaf_param_map.setString("file", ies_file)
            yaf_param_map.setInt("samples", light.yaf_samples)
            yaf_param_map.setBool("soft_shadows", light.ies_soft_shadows)
            yaf_param_map.setBool("light_enabled", light.light_enabled)
            yaf_param_map.setBool("cast_shadows", light.cast_shadows)

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
            
            yaf_param_map = libyafaray4_bindings.ParamMap()
            if light.create_geometry:
                ID = "AreaLight-"+str(yi.getNextFreeId())
                yaf_param_map.setString("type", "mesh")
                yaf_param_map.setInt("num_vertices", 4)
                yaf_param_map.setInt("num_faces", 2)
                self.yaf_scene.createObject(ID)
                yi.setCurrentMaterial(self.lightMatName)
                yi.addVertex(point[0], point[1], point[2])
                yi.addVertex(corner1[0], corner1[1], corner1[2])
                yi.addVertex(corner2[0], corner2[1], corner2[2])
                yi.addVertex(corner3[0], corner3[1], corner3[2])
                yi.addTriangle(0, 1, 2)
                yi.addTriangle(0, 2, 3)
                yi.endObject()
                yaf_param_map.setString("object_name", ID)

            yaf_param_map.setString("type", "arealight")
            yaf_param_map.setInt("samples", light.yaf_samples)
            yaf_param_map.setVector("corner", point[0], point[1], point[2])
            yaf_param_map.setVector("point1", corner1[0], corner1[1], corner1[2])
            yaf_param_map.setVector("point2", corner3[0], corner3[1], corner3[2])
            yaf_param_map.setBool("light_enabled", light.light_enabled)
            yaf_param_map.setBool("cast_shadows", light.cast_shadows)

        if lightType not in {"area", "sun", "directional"}:
            # "from" is not used for area, sunlight and infinite directional light
            yaf_param_map.setVector("from", pos[0], pos[1], pos[2])
        if lightType in {"point", "spot"}:
            if getattr(light, "use_sphere", False) and lightType == "point":
                power = 0.5 * power * power / (light.yaf_sphere_radius * light.yaf_sphere_radius)
            else:
                power = 0.5 * power * power

        yaf_param_map.setColor("color", color[0], color[1], color[2])
        yaf_param_map.setFloat("power", power)
        yaf_param_map.setBool("light_enabled", light.light_enabled)
        yaf_param_map.setBool("cast_shadows", light.cast_shadows)
        yaf_param_map.setBool("with_caustic", light.caustic_photons)
        yaf_param_map.setBool("with_diffuse", light.diffuse_photons)
        yaf_param_map.setBool("photon_only", light.photon_only)
        self.yaf_scene.createLight(name, yaf_param_map)

        return True
