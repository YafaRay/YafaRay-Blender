import bpy
from  math import *
import mathutils
#import yafrayinterface

class yafLight:
    def __init__(self, interface):
        self.yi = interface

    def makeSphere(self, nu, nv, x, y, z, rad, mat):
        yi = self.yi

        # get next free id from interface

        ID = yi.getNextFreeID()

        yi.startGeometry();

        if not yi.startTriMesh(ID, 2+(nu-1)*nv, 2*(nu-1)*nv, False, False):
            print("error on starting trimesh!\n")

        yi.addVertex(x, y, z+rad);
        yi.addVertex(x, y, z-rad);
        for v in range(0, nv):
            t = v/float(nv)
            sin_v = sin(2.0*pi*t)
            cos_v = cos(2.0*pi*t)
            for u in range(1, nu):
                s = u/float(nu);
                sin_u = sin(pi*s)
                cos_u = cos(pi*s)
                yi.addVertex(x + cos_v*sin_u*rad, y + sin_v*sin_u*rad, z + cos_u*rad)

        for v in range(0, nv):
            yi.addTriangle( 0, 2+v*(nu-1), 2+((v+1)%nv)*(nu-1), mat );
            yi.addTriangle( 1, ((v+1)%nv)*(nu-1)+nu, v*(nu-1)+nu, mat );
            for u in range(0, nu-2):
                yi.addTriangle( 2+v*(nu-1)+u, 2+v*(nu-1)+u+1, 2+((v+1)%nv)*(nu-1)+u, mat );
                yi.addTriangle( 2+v*(nu-1)+u+1, 2+((v+1)%nv)*(nu-1)+u+1, 2+((v+1)%nv)*(nu-1)+u, mat );

        print("before starting end trimesh ...")
        yi.endTriMesh();
        print("before starting end geometry ...")
        yi.endGeometry();
        print("ID is :" + str(ID+100))
        return ID


    def createLight(self, yi, lamp_object, matrix = None, lamp_mat = None, dupliNum = None):

        lamp = lamp_object.data
        name = lamp_object.name
        #name = "spot"
        if dupliNum != None:
            name += str(dupliNum)

        if matrix == None:
            matrix = lamp_object.matrix_local #this change is at 18.7.10
        pos = matrix[3]
        dir = matrix[2]
        up = matrix[1]
        to = [pos[0] - dir[0], pos[1] - dir[1], pos[2] - dir[2]]

        yi.paramsClearAll()
        #props = obj.properties["YafRay"]
        lampType = lamp.type or lamp_type # for test
        power = lamp.energy
        color = lamp.color

        #lamp = context.lamp
        #scene = context.scene

        yi.paramsClearAll()


        print("INFO: Exporting Lamp:" + str(name) +  " type: " + str(lampType) )
        #print("work started ... ")

        if lampType == "POINT":
            yi.paramsSetString("type", "pointlight")
            power = 0.5 * power * power # original value

            if lamp.use_sphere:
                #yi.paramsClearAll();
                radius = lamp.shadow_soft_size
                power = 0.5*power*power/(radius * radius) # radius < 1 crash geometry ?

                if  lamp.create_geometry == True:
                    ID = self.makeSphere(24, 48, pos[0], pos[1], pos[2], radius, lamp_mat)
                    yi.paramsSetInt("object", ID)

                yi.paramsSetString("type", "spherelight")
                yi.paramsSetInt("samples", lamp.yaf_samples)
                yi.paramsSetFloat("radius", radius)
                #print("complete ")

        elif lampType == "SPOT":
            #light = obj.getData()
            yi.paramsSetString("type", "spotlight")
            #print "spot ", light.getSpotSize()
            yi.paramsSetFloat("cone_angle", (lamp.spot_size * 57.29577))
            yi.paramsSetFloat("blend", lamp.spot_blend)
            yi.paramsSetPoint("to", to[0], to[1], to[2])
            yi.paramsSetBool("soft_shadows", lamp.spot_soft_shadows)
            yi.paramsSetFloat("shadowFuzzyness", lamp.shadow_fuzzyness)
            yi.paramsSetBool("photon_only", lamp.photon_only )
            yi.paramsSetInt("samples", lamp.yaf_samples)
            power = 0.5*power*power

        elif lampType == "SUN":
            yi.paramsSetString("type", "sunlight")
            yi.paramsSetInt("samples", lamp.yaf_samples)
            yi.paramsSetFloat("angle", lamp.angle)
            yi.paramsSetPoint("direction", dir[0], dir[1], dir[2])
            if lamp.directional:
                yi.paramsSetString("type", "directional")
                yi.paramsSetBool("infinite", lamp.infinite)
                yi.paramsSetFloat("radius", lamp.shadow_soft_size)

        #elif lampType == "Directional": # integrate into Sun lamp
            #yi.paramsSetString("type", "directional")
            #yi.paramsSetBool("infinite", lamp.infinite)
            #yi.paramsSetFloat("radius", lamp.shadow_soft_size)
            #yi.paramsSetPoint("direction", dir[0], dir[1], dir[2])

        elif lampType == "HEMI":

            # use for IES light
            yi.paramsSetString("type", "ieslight")
            yi.paramsSetPoint("to", to[0], to[1], to[2])
            import os
            if lamp.ies_file != "" and not os.path.exists(lamp.ies_file):
                return False

            yi.paramsSetString("file", lamp.ies_file)
            yi.paramsSetInt("samples", lamp.yaf_samples)
            yi.paramsSetBool("soft_shadows", lamp.ies_soft_shadows)
            yi.paramsSetFloat("cone_angle", lamp.ies_cone_angle)


        elif lampType == "AREA":
            #yi.paramsSetString("type", "arealight")
            #areaLight = obj.getData() # old
            #sizeX = areaLight.getAreaSizeX()
            #sizeY = areaLight.getAreaSizeY()

            sizeX = lamp.size
            sizeY = lamp.size_y

            matrix = lamp_object.matrix_world.__copy__()
            #lamp_object.transform(matrix)
            #matrix.transpose()

            # generate an untransformed rectangle in the XY plane with
            # the light's position as the centerpoint and transform it
            # using its transformation matrix

            point = mathutils.Vector((-sizeX/2, -sizeY/2, 0))
            corner1 = mathutils.Vector((-sizeX/2, sizeY/2, 0))
            corner2 = mathutils.Vector((sizeX/2, sizeY/2, 0))
            corner3 = mathutils.Vector((sizeX/2, -sizeY/2, 0))
            point = point * matrix
            corner1 = corner1 * matrix
            corner2 = corner2 * matrix
            corner3 = corner3 * matrix

            #print("point: ", point, corner1, corner2, corner3)
            yi.paramsClearAll();
            if lamp.create_geometry  == True:
                ID = yi.getNextFreeID()
                yi.startGeometry();
                yi.startTriMesh(ID, 4, 2, False, False, 0);

                yi.addVertex(point[0], point[1], point[2]);
                yi.addVertex(corner1[0], corner1[1], corner1[2]);
                yi.addVertex(corner2[0], corner2[1], corner2[2]);
                yi.addVertex(corner3[0], corner3[1], corner3[2]);
                yi.addTriangle(0, 1, 2, lamp_mat);
                yi.addTriangle(0, 2, 3, lamp_mat);
                yi.endTriMesh();
                yi.endGeometry();
                yi.paramsSetInt("object", ID);


            yi.paramsSetString("type", "arealight");
            yi.paramsSetInt("samples", lamp.yaf_samples)

            yi.paramsSetPoint("corner", point[0], point[1], point[2]);
            yi.paramsSetPoint("point1", corner1[0], corner1[1], corner1[2]);
            yi.paramsSetPoint("point2", corner3[0], corner3[1], corner3[2]);

        yi.paramsSetPoint("from", pos[0], pos[1], pos[2])
        yi.paramsSetColor("color", color[0], color[1], color[2])
        yi.paramsSetFloat("power", power)


        yi.createLight(name)

        return True
