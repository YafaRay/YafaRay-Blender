import bpy
import os
from math import *
from bpy.path import *
import mathutils


class yafLight:
    def __init__(self, interface, preview):
        self.yi = interface
        self.lightMat = None
        self.preview = preview

    def makeSphere(self, nu, nv, x, y, z, rad, mat):

        yi = self.yi

        # get next free id from interface

        ID = yi.getNextFreeID()

        yi.startGeometry()

        if not yi.startTriMesh(ID, 2 + (nu - 1) * nv, 2 * (nu - 1) * nv, False, False):
            yi.printError("Couldn't start trimesh!")

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
            yi.addTriangle(0, 2 + v * (nu - 1), 2 + ((v + 1) % nv) * (nu - 1), mat)
            yi.addTriangle(1, ((v + 1) % nv) * (nu - 1) + nu, v * (nu - 1) + nu, mat)
            for u in range(0, nu - 2):
                yi.addTriangle(2 + v * (nu - 1) + u, 2 + v * (nu - 1) + u + 1, 2 + ((v + 1) % nv) * (nu - 1) + u, mat)
                yi.addTriangle(2 + v * (nu - 1) + u + 1, 2 + ((v + 1) % nv) * (nu - 1) + u + 1, 2 + ((v + 1) % nv) * (nu - 1) + u, mat)

        yi.endTriMesh()
        yi.endGeometry()

        return ID

    def createLight(self, yi, lamp_object, matrix = None):

        lamp = lamp_object.data
        name = lamp_object.name

        if matrix == None:
            matrix = lamp_object.matrix_world
        pos = matrix[3]
        dir = matrix[2]
        up = matrix[1]
        to = pos - dir

        lampType = lamp.lamp_type
        power = lamp.energy
        color = lamp.color

        if self.preview:
            if name == "Lamp":
                pos = (-6, -4, 8, 1.0)
                power = 5
            elif name == "Lamp.001":
                pos = (6, -6, -2, 1.0)
                power = 6
            elif name == "Lamp.002":
                pos = (-2.9123109, -7.270790733, 4.439187765, 1.0)
                to = (-0.0062182024121284485, 0.6771485209465027, 1.8015732765197754, 1.0)
                power = 5
            elif name == "Lamp.008":
                power = 15

        yi.paramsClearAll()

        yi.printInfo("Exporting Lamp: " + str(name) + " [" + str(lampType) + "]")

        if lamp.create_geometry and not self.lightMat:
            self.yi.paramsClearAll()
            self.yi.paramsSetString("type", "light_mat")
            self.lightMat = self.yi.createMaterial("lm")
            self.yi.paramsClearAll()

        if lampType == "point":
            yi.paramsSetString("type", "pointlight")
            power = 0.5 * power * power  # original value

            if lamp.use_sphere:
                radius = lamp.shadow_soft_size
                power /= (radius * radius)  # radius < 1 crash geometry ?

                if lamp.create_geometry:
                    ID = self.makeSphere(24, 48, pos[0], pos[1], pos[2], radius, self.lightMat)
                    yi.paramsSetInt("object", ID)

                yi.paramsSetString("type", "spherelight")
                yi.paramsSetInt("samples", lamp.yaf_samples)
                yi.paramsSetFloat("radius", radius)

        elif lampType == "spot":
            if self.preview and name == "Lamp.002":
                angle = 50
            else:
                # Blender reports the angle of the full cone in radians
                # and we need half of the apperture angle in degrees
                # (spot_size * 180 / pi) / 2
                angle = (lamp.spot_size * 180 / pi) * 0.5

            yi.paramsSetString("type", "spotlight")

            yi.paramsSetFloat("cone_angle", angle)
            yi.paramsSetFloat("blend", lamp.spot_blend)
            yi.paramsSetPoint("to", to[0], to[1], to[2])
            yi.paramsSetBool("soft_shadows", lamp.spot_soft_shadows)
            yi.paramsSetFloat("shadowFuzzyness", lamp.shadow_fuzzyness)
            yi.paramsSetBool("photon_only", lamp.photon_only)
            yi.paramsSetInt("samples", lamp.yaf_samples)
            power = 0.5 * power * power

        elif lampType == "sun":
            yi.paramsSetString("type", "sunlight")
            yi.paramsSetInt("samples", lamp.yaf_samples)
            yi.paramsSetFloat("angle", lamp.angle)
            yi.paramsSetPoint("direction", dir[0], dir[1], dir[2])
            if lamp.directional:
                yi.paramsSetString("type", "directional")
                yi.paramsSetBool("infinite", lamp.infinite)
                yi.paramsSetFloat("radius", lamp.shadow_soft_size)

        elif lampType == "ies":
            # use for IES light
            yi.paramsSetString("type", "ieslight")
            yi.paramsSetPoint("to", to[0], to[1], to[2])
            ies_file = abspath(lamp.ies_file)
            if ies_file != "" and not os.path.exists(ies_file):
                return False
            yi.paramsSetString("file", ies_file)
            yi.paramsSetInt("samples", lamp.yaf_samples)
            yi.paramsSetBool("soft_shadows", lamp.ies_soft_shadows)
            yi.paramsSetFloat("cone_angle", lamp.ies_cone_angle)

        elif lampType == "area":

            sizeX = 1.0
            sizeY = 1.0

            matrix = lamp_object.matrix_world

            # generate an untransformed rectangle in the XY plane with
            # the light's position as the centerpoint and transform it
            # using its transformation matrix

            point = mathutils.Vector((-sizeX / 2, -sizeY / 2, 0))
            corner1 = mathutils.Vector((-sizeX / 2, sizeY / 2, 0))
            corner2 = mathutils.Vector((sizeX / 2, sizeY / 2, 0))
            corner3 = mathutils.Vector((sizeX / 2, -sizeY / 2, 0))
            point = point * matrix
            corner1 = corner1 * matrix
            corner2 = corner2 * matrix
            corner3 = corner3 * matrix

            yi.paramsClearAll()
            if lamp.create_geometry:
                ID = yi.getNextFreeID()
                yi.startGeometry()
                yi.startTriMesh(ID, 4, 2, False, False, 0)

                yi.addVertex(point[0], point[1], point[2])
                yi.addVertex(corner1[0], corner1[1], corner1[2])
                yi.addVertex(corner2[0], corner2[1], corner2[2])
                yi.addVertex(corner3[0], corner3[1], corner3[2])
                yi.addTriangle(0, 1, 2, self.lightMat)
                yi.addTriangle(0, 2, 3, self.lightMat)
                yi.endTriMesh()
                yi.endGeometry()
                yi.paramsSetInt("object", ID)

            yi.paramsSetString("type", "arealight")
            yi.paramsSetInt("samples", lamp.yaf_samples)

            yi.paramsSetPoint("corner", point[0], point[1], point[2])
            yi.paramsSetPoint("point1", corner1[0], corner1[1], corner1[2])
            yi.paramsSetPoint("point2", corner3[0], corner3[1], corner3[2])

        yi.paramsSetPoint("from", pos[0], pos[1], pos[2])
        yi.paramsSetColor("color", color[0], color[1], color[2])
        yi.paramsSetFloat("power", power)
        yi.createLight(name)

        return True
