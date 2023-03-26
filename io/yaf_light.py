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

class yafLight:
    def __init__(self, scene, logger, preview):
        self.yaf_scene = scene
        self.logger = logger
        self.lightMatName = None
        self.preview = preview

    def makeSphere(self, nu, nv, x, y, z, rad, mat):
        
        yi.setCurrentMaterial(mat)

        # get next free id from interface
        ID = "SphereLight-" + str(yi.getNextFreeId())

        param_map.setString("type", "mesh")
        param_map.setInt("num_vertices", 2 + (nu - 1) * nv)
        param_map.setInt("num_faces", 2 * (nu - 1) * nv)
        self.yaf_scene.createObject(ID)

        yi.addVertex(x, y, z + rad)
        yi.addVertex(x, y, z - rad)
        for v in range(0, nv):
            t = v / float(nv)
            sin_v = sin(2.0 * pi * t)
            cos_v = cos(2.0 * pi * t)
            for u in range(1, nu):
                s = u / float(nu)
                sin_u = sin(pi * s)
                cos_u = cos(pi * s)
                yi.addVertex(x + cos_v * sin_u * rad, y + sin_v * sin_u * rad, z + cos_u * rad)

        for v in range(0, nv):
            yi.addTriangle(0, 2 + v * (nu - 1), 2 + ((v + 1) % nv) * (nu - 1))
            yi.addTriangle(1, ((v + 1) % nv) * (nu - 1) + nu, v * (nu - 1) + nu)
            for u in range(0, nu - 2):
                yi.addTriangle(2 + v * (nu - 1) + u, 2 + v * (nu - 1) + u + 1, 2 + ((v + 1) % nv) * (nu - 1) + u)
                yi.addTriangle(2 + v * (nu - 1) + u + 1, 2 + ((v + 1) % nv) * (nu - 1) + u + 1, 2 + ((v + 1) % nv) * (nu - 1) + u)

        yi.endObject()

        return ID

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

        param_map = libyafaray4_bindings.ParamMap()

        self.logger.printInfo("Exporting Light: {0} [{1}]".format(name, lightType))

        if light.create_geometry:  # and not self.lightMat:
            param_map = libyafaray4_bindings.ParamMap()
            param_map.setColor("color", color[0], color[1], color[2])  # color for spherelight and area light geometry
            param_map.setString("type", "light_mat")
            power_sphere = power / light.yaf_sphere_radius
            param_map.setFloat("power", power_sphere)
        
            self.yaf_scene.createMaterial(name)
            self.lightMatName = name
            param_map = libyafaray4_bindings.ParamMap()
            #param_map.setBool("light_enabled", light.light_enabled)

        if lightType == "point":
            param_map.setString("type", "pointlight")
            if getattr(light, "use_sphere", False):
                if light.create_geometry:
                    ID = self.makeSphere(24, 48, pos[0], pos[1], pos[2], light.yaf_sphere_radius, self.lightMatName)
                    param_map.setString("object_name", ID)
                param_map.setString("type", "spherelight")
                param_map.setInt("samples", light.yaf_samples)
                param_map.setFloat("radius", light.yaf_sphere_radius)
                param_map.setBool("light_enabled", light.light_enabled)
                param_map.setBool("cast_shadows", light.cast_shadows)

        elif lightType == "spot":
            if self.preview and name == "Light.002":
                angle = 50
            else:
                # Blender reports the angle of the full cone in radians
                # and we need half of the apperture angle in degrees
                angle = degrees(light.spot_size) * 0.5

            param_map.setString("type", "spotlight")

            param_map.setFloat("cone_angle", angle)
            param_map.setFloat("blend", light.spot_blend)
            param_map.setVector("to", to[0], to[1], to[2])
            param_map.setBool("soft_shadows", light.spot_soft_shadows)
            param_map.setFloat("shadowFuzzyness", light.shadow_fuzzyness)
            param_map.setInt("samples", light.yaf_samples)
            param_map.setBool("light_enabled", light.light_enabled)
            param_map.setBool("cast_shadows", light.cast_shadows)

        elif lightType == "sun":
            param_map.setString("type", "sunlight")
            param_map.setInt("samples", light.yaf_samples)
            param_map.setFloat("angle", light.angle)
            param_map.setVector("direction", direct[0], direct[1], direct[2])
            param_map.setBool("light_enabled", light.light_enabled)
            param_map.setBool("cast_shadows", light.cast_shadows)

        elif lightType == "directional":
            param_map.setString("type", "directional")
            param_map.setVector("direction", direct[0], direct[1], direct[2])
            param_map.setBool("infinite", light.infinite)
            if not light.infinite:
                param_map.setFloat("radius", light.shadow_soft_size)
                param_map.setVector("from", pos[0], pos[1], pos[2])
            param_map.setBool("light_enabled", light.light_enabled)
            param_map.setBool("cast_shadows", light.cast_shadows)

        elif lightType == "ies":
            param_map.setString("type", "ieslight")
            param_map.setVector("to", to[0], to[1], to[2])
            ies_file = abspath(light.ies_file)
            if not any(ies_file) and not os.path.exists(ies_file):
                self.logger.printWarning("IES file not found for {0}".format(name))
                return False
            param_map.setString("file", ies_file)
            param_map.setInt("samples", light.yaf_samples)
            param_map.setBool("soft_shadows", light.ies_soft_shadows)
            param_map.setBool("light_enabled", light.light_enabled)
            param_map.setBool("cast_shadows", light.cast_shadows)

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
                ID = "AreaLight-"+str(yi.getNextFreeId())
                param_map.setString("type", "mesh")
                param_map.setInt("num_vertices", 4)
                param_map.setInt("num_faces", 2)
                self.yaf_scene.createObject(ID)
                yi.setCurrentMaterial(self.lightMatName)
                yi.addVertex(point[0], point[1], point[2])
                yi.addVertex(corner1[0], corner1[1], corner1[2])
                yi.addVertex(corner2[0], corner2[1], corner2[2])
                yi.addVertex(corner3[0], corner3[1], corner3[2])
                yi.addTriangle(0, 1, 2)
                yi.addTriangle(0, 2, 3)
                yi.endObject()
                param_map.setString("object_name", ID)

            param_map.setString("type", "arealight")
            param_map.setInt("samples", light.yaf_samples)
            param_map.setVector("corner", point[0], point[1], point[2])
            param_map.setVector("point1", corner1[0], corner1[1], corner1[2])
            param_map.setVector("point2", corner3[0], corner3[1], corner3[2])
            param_map.setBool("light_enabled", light.light_enabled)
            param_map.setBool("cast_shadows", light.cast_shadows)

        if lightType not in {"area", "sun", "directional"}:
            # "from" is not used for area, sunlight and infinite directional light
            param_map.setVector("from", pos[0], pos[1], pos[2])
        if lightType in {"point", "spot"}:
            if getattr(light, "use_sphere", False) and lightType == "point":
                power = 0.5 * power * power / (light.yaf_sphere_radius * light.yaf_sphere_radius)
            else:
                power = 0.5 * power * power

        param_map.setColor("color", color[0], color[1], color[2])
        param_map.setFloat("power", power)
        param_map.setBool("light_enabled", light.light_enabled)
        param_map.setBool("cast_shadows", light.cast_shadows)
        param_map.setBool("with_caustic", light.caustic_photons)
        param_map.setBool("with_diffuse", light.diffuse_photons)
        param_map.setBool("photon_only", light.photon_only)
        self.yaf_scene.createLight(name, param_map)

        return True
