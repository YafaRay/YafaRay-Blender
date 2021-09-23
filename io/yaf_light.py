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
from bpy.path import abspath

def multiplyMatrix4x4Vector4(matrix, vector):
    result = mathutils.Vector((0.0, 0.0, 0.0, 0.0))
    for i in range(4):
        result[i] = vector * matrix[i]  # use reverse vector multiply order, API changed with rev. 38674

    return result

class yafLight:
    def __init__(self, interface, preview):
        self.yi = interface
        self.lightMatName = None
        self.preview = preview

    def makeSphere(self, nu, nv, x, y, z, rad, mat):
        yi = self.yi
        yi.setCurrentMaterial(mat)

        # get next free id from interface
        ID = "SphereLight-" + str(yi.getNextFreeId())

        yi.startGeometry()
        self.yi.paramsSetString("type", "mesh")
        self.yi.paramsSetInt("num_vertices", 2 + (nu - 1) * nv)
        self.yi.paramsSetInt("num_faces", 2 * (nu - 1) * nv)
        yi.createObject(ID)

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
        yi.endGeometry()

        return ID

    def createLight(self, yi, lamp_object, matrix=None):

        lamp = lamp_object.data
        name = lamp_object.name

        if matrix is None:
            matrix = lamp_object.matrix_world.copy()
        # matrix indexing (row, colums) changed in Blender rev.42816, for explanation see also:
        # http://wiki.blender.org/index.php/User:TrumanBlending/Matrix_Indexing
        pos = matrix.col[3]
        direct = matrix.col[2] # msg 'Assignment to reserved built-in symbol: dir' ( change to direct)
        # up = matrix[1]  /* UNUSED */
        to = pos - direct

        lampType = lamp.lamp_type
        power = lamp.yaf_energy
        color = lamp.color

        if self.preview:
            if name == "Lamp":
                pos = (-6, -4, 8, 1.0)
                power = 5
                if bpy.data.scenes[0].yafaray.preview.enable:
                    power *= bpy.data.scenes[0].yafaray.preview.fillLightPowerFactor
                    color = bpy.data.scenes[0].yafaray.preview.fillLightColor

            elif name == "Lamp.001":
                pos = (6, -6, -2, 1.0)
                power = 6
                if bpy.data.scenes[0].yafaray.preview.enable:
                    power *= bpy.data.scenes[0].yafaray.preview.fillLightPowerFactor
                    color = bpy.data.scenes[0].yafaray.preview.fillLightColor
                    
            elif name == "Lamp.002":
                pos = (-2.9123109, -7.270790733, 4.439187765, 1.0)
                to = (-0.0062182024121284485, 0.6771485209465027, 1.8015732765197754, 1.0)
                power = 5
                if bpy.data.scenes[0].yafaray.preview.enable:
                    power *= bpy.data.scenes[0].yafaray.preview.keyLightPowerFactor
                    color = bpy.data.scenes[0].yafaray.preview.keyLightColor
                    
            elif name == "Lamp.008":
                lampType = "sun"
                power = 0.8
                if bpy.data.scenes[0].yafaray.preview.enable:
                    power *= bpy.data.scenes[0].yafaray.preview.keyLightPowerFactor
                    color = bpy.data.scenes[0].yafaray.preview.keyLightColor
            
            if bpy.data.scenes[0].yafaray.preview.enable:
                matrix2 = mathutils.Matrix.Rotation(bpy.data.scenes[0].yafaray.preview.lightRotZ, 4, 'Z')
                pos = multiplyMatrix4x4Vector4(matrix2, mathutils.Vector((pos[0], pos[1], pos[2], pos[3])))

        yi.paramsClearAll()

        yi.printInfo("Exporting Lamp: {0} [{1}]".format(name, lampType))

        if lamp.create_geometry:  # and not self.lightMat:
            yi.paramsClearAll()
            yi.paramsSetColor("color", color[0], color[1], color[2])  # color for spherelight and area light geometry
            yi.paramsSetString("type", "light_mat")
            power_sphere = power / lamp.yaf_sphere_radius
            yi.paramsSetFloat("power", power_sphere)
        
            self.yi.createMaterial(name)
            self.lightMatName = name
            self.yi.paramsClearAll()
            #yi.paramsSetBool("light_enabled", lamp.light_enabled)

        if lampType == "point":
            yi.paramsSetString("type", "pointlight")
            if getattr(lamp, "use_sphere", False):
                if lamp.create_geometry:
                    ID = self.makeSphere(24, 48, pos[0], pos[1], pos[2], lamp.yaf_sphere_radius, self.lightMatName)
                    yi.paramsSetString("object_name", ID)
                yi.paramsSetString("type", "spherelight")
                yi.paramsSetInt("samples", lamp.yaf_samples)
                yi.paramsSetFloat("radius", lamp.yaf_sphere_radius)
                yi.paramsSetBool("light_enabled", lamp.light_enabled)
                yi.paramsSetBool("cast_shadows", lamp.cast_shadows)

        elif lampType == "spot":
            if self.preview and name == "Lamp.002":
                angle = 50
            else:
                # Blender reports the angle of the full cone in radians
                # and we need half of the apperture angle in degrees
                angle = degrees(lamp.spot_size) * 0.5

            yi.paramsSetString("type", "spotlight")

            yi.paramsSetFloat("cone_angle", angle)
            yi.paramsSetFloat("blend", lamp.spot_blend)
            yi.paramsSetVector("to", to[0], to[1], to[2])
            yi.paramsSetBool("soft_shadows", lamp.spot_soft_shadows)
            yi.paramsSetFloat("shadowFuzzyness", lamp.shadow_fuzzyness)
            yi.paramsSetInt("samples", lamp.yaf_samples)
            yi.paramsSetBool("light_enabled", lamp.light_enabled)
            yi.paramsSetBool("cast_shadows", lamp.cast_shadows)

        elif lampType == "sun":
            yi.paramsSetString("type", "sunlight")
            yi.paramsSetInt("samples", lamp.yaf_samples)
            yi.paramsSetFloat("angle", lamp.angle)
            yi.paramsSetVector("direction", direct[0], direct[1], direct[2])
            yi.paramsSetBool("light_enabled", lamp.light_enabled)
            yi.paramsSetBool("cast_shadows", lamp.cast_shadows)

        elif lampType == "directional":
            yi.paramsSetString("type", "directional")
            yi.paramsSetVector("direction", direct[0], direct[1], direct[2])
            yi.paramsSetBool("infinite", lamp.infinite)
            if not lamp.infinite:
                yi.paramsSetFloat("radius", lamp.shadow_soft_size)
                yi.paramsSetVector("from", pos[0], pos[1], pos[2])
            yi.paramsSetBool("light_enabled", lamp.light_enabled)
            yi.paramsSetBool("cast_shadows", lamp.cast_shadows)

        elif lampType == "ies":
            yi.paramsSetString("type", "ieslight")
            yi.paramsSetVector("to", to[0], to[1], to[2])
            ies_file = abspath(lamp.ies_file)
            if not any(ies_file) and not os.path.exists(ies_file):
                yi.printWarning("IES file not found for {0}".format(name))
                return False
            yi.paramsSetString("file", ies_file)
            yi.paramsSetInt("samples", lamp.yaf_samples)
            yi.paramsSetBool("soft_shadows", lamp.ies_soft_shadows)
            yi.paramsSetBool("light_enabled", lamp.light_enabled)
            yi.paramsSetBool("cast_shadows", lamp.cast_shadows)

        elif lampType == "area":
            sizeX = lamp.size
            sizeY = lamp.size
            if lamp.shape == 'RECTANGLE':
                sizeY = lamp.size_y                       
            matrix = lamp_object.matrix_world.copy()           
            

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
            
            yi.paramsClearAll()
            if lamp.create_geometry:
                ID = "AreaLight-"+str(yi.getNextFreeId())
                yi.startGeometry()
                self.yi.paramsSetString("type", "mesh")
                self.yi.paramsSetInt("num_vertices", 4)
                self.yi.paramsSetInt("num_faces", 2)
                yi.createObject(ID)
                yi.setCurrentMaterial(self.lightMatName)
                yi.addVertex(point[0], point[1], point[2])
                yi.addVertex(corner1[0], corner1[1], corner1[2])
                yi.addVertex(corner2[0], corner2[1], corner2[2])
                yi.addVertex(corner3[0], corner3[1], corner3[2])
                yi.addTriangle(0, 1, 2)
                yi.addTriangle(0, 2, 3)
                yi.endObject()
                yi.endGeometry()
                yi.paramsSetString("object_name", ID)

            yi.paramsSetString("type", "arealight")
            yi.paramsSetInt("samples", lamp.yaf_samples)
            yi.paramsSetVector("corner", point[0], point[1], point[2])
            yi.paramsSetVector("point1", corner1[0], corner1[1], corner1[2])
            yi.paramsSetVector("point2", corner3[0], corner3[1], corner3[2])
            yi.paramsSetBool("light_enabled", lamp.light_enabled)
            yi.paramsSetBool("cast_shadows", lamp.cast_shadows)

        if lampType not in {"sun", "directional"}:
            # "from" is not used for sunlight and infinite directional light
            yi.paramsSetVector("from", pos[0], pos[1], pos[2])
        if lampType in {"point", "spot"}:
            if getattr(lamp, "use_sphere", False) and lampType == "point":
                power = 0.5 * power * power / (lamp.yaf_sphere_radius * lamp.yaf_sphere_radius)
            else:
                power = 0.5 * power * power

        yi.paramsSetColor("color", color[0], color[1], color[2])
        yi.paramsSetFloat("power", power)
        yi.paramsSetBool("light_enabled", lamp.light_enabled)
        yi.paramsSetBool("cast_shadows", lamp.cast_shadows)
        yi.paramsSetBool("with_caustic", lamp.caustic_photons)
        yi.paramsSetBool("with_diffuse", lamp.diffuse_photons)
        yi.paramsSetBool("photon_only", lamp.photon_only)
        yi.createLight(name)

        return True
